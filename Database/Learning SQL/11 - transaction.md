[TOC]

# transaction

independent sql statements might be good for ad hoc reporting or data maintenance scripts, but application logic will frequently include multiple sql statements that need to execute together as a logical unit of work. we will show what's necessary for such multi-sql statements concurrent to execute.

## multi-user database

database more often allows multiple user to query and modify data concurrently. if only read-access its still manageable, however if it involves modifying / adding data the might become a mess

### lock(ing)

lock is required for such situation to control the simultaneous use of data resources. lock are put in place to ensure modification executes in sequentially. there exists two locking strategy

- only one write lock is distributed for modifying data and multiple read lock can be obtained, no read lock can be obtained until write lock is released -> we will be receiving state of database
- only one write lock is distributed for modifying data, no read lock is required, instead database server guarantees consistent view of data from time query begins till query finish, also known as *versioning* -> we will be receiving a mirror copy

first approach can lead to long wait time given the high read and write traffic, the second approach can be problematic if there is time-consuming queries on going. mssql goes for the first approach, oracle uses the second approach, mysql give the option to database admin based on the preference of database engine.

### lock granularities

lock can be applied to different levels, tables, page, and rows.

> page is a segment of memory generally in the range of 2kb to 16kb (of a table)

the different levels affects the bookkeeping load, eg. table level means less bookkeeping but might also causes unacceptable wait times as we have more users. granularity depends on preference (setting or engine). locks might be escalated from row to table under certain circumstances.

## what is a transaction?

if

- we have 100% uptime
- users always allow programs to finish executing
- application always completed without encountering errors

lock is good enough. but its not in reality, we need transaction to ensure concurrency. its a device for grouping together multiple sql statements such that either all or non of the statements succeed (atomicity). one example would be to xfer money from account A to account B, it should look something like remove account A then update account B, if something fails after the first deduction then the money will just be gone. this is something that we would like to be prevented, thus transaction. a transaction means to issue all sql statements and ensure all of them succeed then issue another commit command, if something happens it will issue a rollback command which is to inform the server to undo all changes made since transaction begins.

```sql
START TRANSACTION
UPDATE -- ...
IF condition THEN
	UPDATE -- ...
	IF updated THEN
	COMMIT
    ELSE
        ROLLBACK
    END IF
ELSE
	ROLLBACK
END IF
```

regardless of commit or rollback all acquired resources (locks) will be returned during execution will be released when the transaction completes. if both statements completed successfully but server shut down before commit or rollback can be executed, the transaction will be rolled back when the server comes back online. if the failure happens during commit then database server must reapply the changes from transaction when the server is restarted (a property also known as durability)

## starting a transaction

database server handles transaction creation in one of two ways

- an active transaction is always associated with a database session. no explicit statement required, when current transaction ends, the server automatically starts a new transaction for current session
- requires explicit transaction begin statement, individual sql statements are automatically committed independently of one another.

the first approach is life saving especially in situation where we accidentally deleted the huge amount of data. for servers using second approach will be default to auto-commit mode if no explicit transaction statement.

> a tip is to set auto commit mode to false for each login

## ending a transaction

once we are utilizing transaction we will need to explicitly end our transaction to make changes, by either commit or rollback. besides commit or rollback there are a few situation which can cause transaction to be ended

- server shut down
- a schema statement is issued
- another start transaction command is issued
- server prematurely ends transaction because server detects dead lock and decides that the transaction is culprit

2 arises because changing schema cant be roll back thus is will commit previous transaction. 4 occurs when two different transaction are waiting for the resources that the other transaction currently holds, eg transaction A updated table A and waiting for write lock on table B, while transaction B updated table B and waiting for write lock on table A, they will wait for one another forever. when such situation is detected, one of the transaction is chosen to be rolled back for the other to proceed. the terminated transaction can be restarted and will succeed without encountering another deadlock situation. situation 2 will not notify user but situation 4 will with such message

> deadlock found ... try restarting transaction

its reasonable to practice transaction retry that has been rolled back due to deadlock protection. if deadlock is common problem then it might be a good practice to standardize the order of execution / data resource access

## transaction save points

sometime we might want to only rollback to portion of our work. this can be achieved by setting savepoints. all savepoints must be given a name to allow multiple savepoints in a single transaction.

```sql
SAVEPOINT my_savepoint

ROLLBACK TO SAVEPOINT my_savepoint

-- a complete example
START TRANSACTION
UPDATE product
SET date_retired = CURRENT_TIMESTAMP()
WHERE product_cd = 'XYZ'
SAVEPOINT before_close_account

UPDATE account
SET status = 'CLOSED', close_date = CURRENT_TIMESTAMP(), last_activity_date = CURRENT_TIMESTAMP()
WHERE product_cd = 'XYZ'

ROLLBACK TO SAVEPOINT before_close_accounts
COMMIT
```

the net effect of this transaction is that the product is retired but no account is closed.

 a few pointers on savepoints

- despite the name, nothing is saved when we create the savepoint, we must eventually commit if we want the transaction to be permanent
- if rollback is issued without a named savepoint, all savepoints within the transaction will be ignored and the entire transaction will be undone.

## on database engine

different database engine provide different low level database functionality, eg locking granularity, table partitioning, recovery capabilities and etc. mysql is kind enough to allow different engine for different tables. its generally recommended to use InnoDB or Falcon for tables that take part in transaction where both uses row-level locking and versioning to provide highest level of concurrency across different storage engines. we can specify storage engine when we are creating a table or change the existing engine the table is using. using `show table` we can see what engine is utilized

```sql
ALTER TABLE transaction ENGINE = 'INNODB'
```


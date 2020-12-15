[TOC]

# indexes

## wikipedia definition and quora 

a database index is a data structure that improves the speed of data retrieval operation on a database table. we search the interested information without searching the entire table row by row. it can be created using one or more columns of the table, providing the basis for both rapid random lookups and efficient access of ordered records.

primary key is predefined when we are creating the table, indexing is done when we would like to search efficiently later on by create a temporary "primary key" and only loading these primary key column to memory for searching.

index can be null but primary key can't be null

___

## practice

mostly index is created on column specified in the where clause of a query as the database retrieves and filters data from the tables based on those columns.

creating demo table

```sql
CREATE TABLE tablemane ( 
    name VARCHAR(20) NOT NULL, 
    age INT, 
    pan_no VARCHAR(20), 
    phone_no VARCHAR(20) 
);
```



running demo table

```sql
SHOW INDEX FROM tablename
EXPLAIN SELECT * FROM tablename WHERE name = 'sth';
-- for unindexed table we can see the 'row' column shows how many row is searched
```

creating primary key to speed up by making

- phone_no as primary key
- assumption there exists no two duplicated phone number or no two user can exists with same phone number

Side topic on primary key, what if we don't create primary key ourself?
InnoDB implicitly creates one for us (by design its required), once the user create a primary key later on the auto created one is replaced

to check InnoDB default primary key

```sql
SHOW EXTENDED INDEX FROM tablename;
```

we should see some composite index on DB_ROW_ID , DB_TRX_ID, DB_ROLL_PTR, more on these later on.

### differences between key & index

```sql
ALTER TABLE tablename ADD PRIMARY KEY (phone_no);
SHOW INDEXES FROM index_demo;
```

___

[database indexing](https://www.freecodecamp.org/news/database-indexing-at-a-glance-bb50809d48bd/)
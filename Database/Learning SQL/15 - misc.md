[TOC]

# misc

## combination insert / update statements

upsert. if we are to create a table that capture information on which bank branches is visited by which customer we can do as follow

```sql
CREATE TABLE branch_usage
	(
    	branch_id SMALLINT UNSIGNED NOT NULL,
        cust_id INTEGER UNSIGNED NOT NULL,
        last_visited_on DATETIME,
        CONSTRAINT pk_branch_usage PRIMARY KEY (branch_id, cust_id)
    )
```

primary key constraint for branch and customer id to prevent addition of existing pair. if customer 1 visits branch 5 the first time we can insert no problem but then if customer 1 visits branch 5 the second time we cant insert but to update. to upsert we can

```sql
INSERT INTO branch_usage (branch_id, cust_id, last_visited_on)
VALUES (1, 5, CURRENT_TIMESTAMP())
ON DUPLICATED KEY UPDATE last_visited_on = CURRENT_TIMESTAMP()
```

## ordered updates and deletes

```sql
UPDATE account
SET avail_balance = avail_balance + 100
WHERE product_cd IN ('CHK', 'SAV', 'MM')
ORDER BY open_date ASC
LIMIT 10
```

## multitable updates and deletes

we could do multi-table updates and deletes by swapping the usual select query to `update` or `delete`. if we are using innodb then its not possible thus we need to fall back to multiple single-table statements in proper order such that foreign key are not violated (this is also the same reason why innodb doesn't allow multitable update / delete)
[TOC]

# subqueries

subquery is a query contained within another SQL statemen

- it is always enclosed within parenthesis
- its usually executed prior to the containing statement

like a normal query it can contains any return eg. single row with single column and etc. the return type determines how it may be used and which operators the containing statement may use to interact with the returns. subquery will be discarded when the main query has finish execution.

if we are confused on what the subquery is trying to achieve we can just run the subquery itself.

if the subquery returns a single row with single column, its allowed to use with one of the expression in an equality condition.

## subquery types

we can categorize the types with the return rows / columns, and other factors eg. self contained, referenced and etc.

### non correlated subqueries

its may be executed alone and does not reference anything from the containing statement. most subquery will be in this form unless we are writing an `update` or `delete` statement, which will frequently use correlated subqueries. if the return is single row and single column its known as a `scalar subquery` and can appear on either side of a condition using the usual operators ( <, >, =, and etc.) 

> to test the where 3 < (subquery) from xuesql.com

if the subquery returns more than one row and we are using it with a equality condition, it will error out.

### multiple-row, single-column subqueries

if our subquery is expected to return multiple rows, although we could not use equality condition, there are a few workarounds.

- the `in` and `not in` operators
  - we can check if the value can be found within set of values, repeated values in the subquery is ignored, to address this we could just add a simple `distinct` to the subquery. this approach will return null values row

```sql
SELECT emp_id, fname, lname, title
FROM employee
WHERE emp_id IN (
    SELECT superior_emp_id
    FROM employee
)
-- =================================
SELECT emp_id, fname, lname, title
FROM employee
WHERE emp_id NOT IN (
    SELECT superior_emp_id
    FROM employee
    WHERE superior_emp_id IS NOT NULL 
    -- take note of the filter condition
    -- this is to ensure null values do not appear in the table
)
```

- the `all` operator

  > The ALL operator returns true if all of the subquery values meet the condition
  
  
  
  - all operator allows us to compare between a single value and every value in a set, by using one of the comparison operators with `all` operator

```sql
SELECT emp_id, fname, lname, title
FROM employee
WHERE emp_id <> ALL(
    SELECT superior_emp_id
    FROM employee
    WHERE superior_emp_id IS NOT NULL
)
```

> when using NOT IN or <> ALL we must be careful to ensure the set of values does not contains NULL, the server equates value on left to each member of the set and any attempt to equate a value expression to NULL yields UNKNOWN, thus return an empty set

- the `any` operator

  > The ANY operator returns true if any of the subquery values meet the condition

  

  - using any is similar to all, but as soon as a single comparison is favorable it stops evaluation

### multicolumn subqueries

```sql
SELECT account_id, product_cd, cust_id
FROM account
WHERE (open_branch_id, open_emp_id) IN
	(
    	SELECT b.branch_id, e.emp_id
        FROM branch b INNER JOIN employee e
        	ON b.branch_id = e.assigned_branch_id
        WHERE b.name = 'Woburn Branch'
        	AND (e.title = 'Teller' or e.title = 'Head Teller')
    )
```

things to note, the parenthesis columns order must be the exact same as the return subqueries order

## correlated subqueries

a correlated subquery is not executed before the main query, instead its executed once for each candidate row (rows that might be included in the final results)

```sql
SELECT c.cust_id, c.cust_type_cd, c.city
FROM customer c
WHERE 2 = (
    SELECT COUNT(*)
    FROM account a
    WHERE a.cust_id = c.cust_id
)
```

the c.cust_id is what makes the subquery correlated, the containing query must supply values for c.cust_id for the subquery to execute. **the containing query retrieves all rows from the customer table and executes the subquery once for  each customer passing in the appropriate customer ID for each execution**. if the subquery returns the value 2, the the filter condition is met and the row is added to the result set.

another example

```sql
SELECT c.cust_id, c.cust_type_cd, c.city
FROM customer c
WHERE (
    SELECT SUM(a.available_balance)
    FROM account a
    WHERE a.cust_id = c.cust_id
) BETWEEN 5000 AND 10000
```

the correlated subquery is executed 13 times, once for each customer row and the execution returns the total account balance for the given customer

## the exists operator

exists operator is often used to identify if relation exists without regard for the quantity

```sql
SELECT a.accound_id
FROM account a
WHERE EXISTS (
    SELECT 1
    FROM transaction t
    WHERE t.account_id = a.account_id
    	AND t.txn_date = '2008-01-01'
)
```

we may also use `not exists` to check subqueries that returns no row

## data manipulation using correlation subqueries

```sql
UPDATE account a
SET a.last_activity_date = (
    SELECT MAX(t.txn_date)
    FROM transaction t
    WHERE t.accound_id = a.account_id
) WHERE EXISTS (
    SELECT 1
    FROM transaction t
    WHERE t.account_id = a.account_id
)
```

its easy for us to forget to cater to account with no transaction. this section is to demonstrate how we can bulk update the database with correlation subqueries and its not only limited to `select` statements.

> take note not all database allows aliasing on delete staments

## when to use subqueries

### subqueries as data sources

```sql
SELECT d.dept_id, d.name, e_cnt.how_many num_employees
FROM department d INNER JOIN
	(
        SELECT dept_id, COUNT(*) how_many
        FROM employee
        GROUP BY dept_id
    ) e_cnt
    ON d.dept_id = e_cnt.dept_id
```

to take note subqueries in `from` clause must be noncorrelated since its executed first. above shows us how we can go beyond the set of available tables and create new view of data we desire and join the result with existing tables

### data fabrication

```sql
SELECT groups.name, COUNT(*) num_customers
FROM 
(
    SELECT SUM(a.available_balance), cust_balance
    FROM account a INNER JOIN product p
        ON a.product_cd = p.product_cd
    WHERE p.product_type_cd = 'ACCOUNT'
    GROUP BY a.cust_id
) cust_rollup
INNER JOIN
(
    SELECT 'SMALL FRY' name, 0 low_limit, 4999.99 high_limit
    UNION ALL
    SELECT 'AVERAGE JOES' name, 5000 low_limit, 9999.99 high_limit
    UNION ALL
    SELECT 'HEAVY HITTERS' name, 10000 low_limit, 999999.99 high_limit
) groups
ON cust_rollup.cust_balance BETWEEN groups.low_limit and groups.high_limit
GROUP BY groups.name
```

advantages of using subqueries is such that we need not build permanent table to hold these information which will soon littered by these tables. also these tables is prone to cease due to activities eg. missing backup, server upgrades, server downtime due to space allocation and etc.

### task oriented subqueries

sometimes we could break down flat queries into subqueries which might helps in terms of efficiency (in the example below its due to less column used for grouping, take note of the grouping portion)

```sql
-- flat
SELECT p.name product, b.name branch,
	CONCAT(e.fname, ' ', e.lname) name,
	SUM(a.avail_balance) tot_deposits
FROM account a INNER JOIN employeee 
	ON a.open_emp_id = e.emp_id
	INNER JOIN branch b
	ON a.open_branch_id = b.branch_id
	INNER JOIN product p
	ON a.product_cd = p.product_cd
WHERE p.product_type_cd = 'ACCOUNT'
GROUP BY p.name, b.name, e.fname, e.lname
ORDER BY 1, 2
-- subquery
SELECT p.name product, b.name branch,
	CONCAT(e.fname, ' ', e.lname) name,
	account_groups.tot_deposits
FROM (
    SELECT product_cd, open_branch_id branch_id,
    	open_emp_id emp_id,
    	SUM(avail_balance) tot_deposits
    FROM account
    GROUP BY product_cd, open_branch_id, open_emp_id
) account_groups
INNER JOIN employee e ON e.emp_id = account_groups.emp_id
INNER JOIN branch b ON b.branch_id = account_groups.branch_id
INNER JOIN product p ON p.product_cd = account_groups.product_cd
WHERE p.product_type_cd = 'ACCOUNT'
```

### subqueries as filter conditions

its both applicable to `having` and `where` clause

### subqueries as expression generators

```sql
-- should return same result with the query above but different flavour
SELECT
    (
    	SELECT p.name FROM product p WHERE p.product_cd = a.product_cd AND p.product_type_cd = 'ACCOUNT'
    ) product,
    (
    	SELECT b.name FROM branch b WHERE b.branch_id = a.open_branch_id
    ) branch,
    (
    	SELECT CONCAT(e.fname, ' ', e.lname FROM employee e WHERE e.emp_id = a.open_emp_id
    ) name,
    SUM(a.avail_balance) tot_deposits
FROM account a
GROUP BY a.product_cd, a.open_branch_id, a.open_emp_id
ORDER BY 1, 2
```

the return is 14 rows where the above query is 11 rows. the discrepancy is due to there exists three product names are null. this arises due to previous queries has a filter condition to check if product_type_cd is 'ACCOUNT'

```sql
SELECT all_prod.product, all_prod.branch, all_prod.name, all_prod.tot_deposits
FROM (
	-- previous query
) all_prod
WHERE all_prod.name IS NOT NULL
ORDER BY 1, 2
```

more examples, non correlated scalar subqueries to generate values for an `insert` statement. we are supposed to lookup key values for all data such that we can populate foreign key column in the account table.

```sql
INSERT INTO account
(
    account_id, product_id, cust_id, open_date, last_activity_date,
    status, open_branch_id, open_emp_id, avail_balance, pending_balance
) VALUES
(
    NULL,
    (SELECT product_cde FROM product WHERE name = 'SAVINGS ACCOUNT'),
    (SELECT cust_id FROM customer WHERE fed_id = '555-55-5555'),
    '2008-09-25', '2008-09-25', 'ACTIVE',
    (SELECT branch_id FROM branch WHERE name = 'Quincy Branch'),
    (SELECT emp_id FROM employee WHERE lname = 'Portman' AND fname = 'Frank'),
    0, 0
)
```

problem with the approach above is if we use subqueries to generate data for columns that allow `null` values, our `insert` statement will succeed even if one of your subqueries fails to return a value. the other approach we could take is to execute four queries to retrieve the primary key values and place those values into the insert statement.
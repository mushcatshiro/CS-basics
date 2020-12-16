[TOC]

# views

views is a good approach to expose to public internal data, keeping implementation details private and minimize impact to users. view is a **mechanism to query data**, unlike tables it does not involve storage (no physical storage is required). we can create one by assigning a name to `select` statement and store the query for public use.

```sql
CREATE VIEW custimer_vw
	(
    	cust_id,
        fed_id,
        cust_type_cd,
        address,
        city,
        state,
        zipcode
    )
AS
SELECT cust_id,
	CONCAT('ends in ', substr(fed_id, 8, 4)) fed_id,
	cust_type_cd,
	address,
	city,
	state,
	postal_code
FROM customer
```

when we execute the statement above it stores the definition for future use. no query will be execute, no data is retrieved or stored. we can query against view as such

```sql
SELECT cust_id,
	fed_id
FROM customer_vw
-- its not what actually being executed instead its
SELECT cust_id,
	CONCAT('ends in ', substr(fed_id, 8, 4)) fed_id
FROM customer
```

## why views

### data security

to mask sensitive information. we can implement constraints both in rows (by `where` clause) can columns. 

### data aggregation

often we want to get aggregated data and it abstracts the need of writing the query from scratch. we can create a table and modify the view definition to retrieve data from the new table.

```sql
CREATE TABLE customer_total
AS 
SELECT * FROM customer_totals_vw
```

all queries that uses customer_totals_vw will pull data from this new table customer_total

### hiding complexity

```sql
CREATE VIEW branch_activity_vw
	(
    	branch_name,
        city,
        state,
        num_emp,
        num_active_acc,
        tot_transaction
    )
AS
SELECT br.name, br.city, br.state,
	(SELECT COUNT(*) FROM emplopyee emp WHERE emp.assigned_branch_id = br.branch_id) num_emp,
	(SELECT COUNT(*) FROM account acnt WHERE acnt.status = 'ACTIVE' AND acnt_open_branch_id = br.branch_id) num_active_acc,
	(SELECT COUNT(*) FROM transaction txn WHERE txn.execution_branch_id = br.branch_id) tot_transaction
FROM branch br
```

the subqueries will not be executed if the respective view columns are not selected, is could improve some performance.

### joining partitioned data

some table might be partitioned based on time eg. every 6 month to split into a table itself. we could write a view to query all historical data.

### updatable views

view are for viewing purpose, it would be bizarre if we want to allow user to modify the table by allowing them to interact with the table itself. thus updatable views where there exists some restrictions but its doable. eg for mysql

- no aggregate function are used
- the view does not employ `group by` or `having` clauses
- no subquery exists in the `select` or `from` clause and any subqueries in the `where` clause does not refer to tables in the `from` clause
- the view doesn't utilize `union`, `union all` and `distinct`
- the `from` clause  includes at least one table or updatable view
- the `from` clause uses only inner joins if there is more than one table or view

```sql
UPDATE customer_vw
SET city = 'woodburn'
WHERE city = 'woburn'
-- but not
SET city = 'woburn' AND fed_id = '99999999'
WHERE city = 'woodburn'
-- insert for this view is not possible due to agg function
```

### updating complex views

```sql
CREATE VIEW busuness_customer_vw
	(
    	cust_id,
        fed_id,
        address,
        city,
        state,
        zipcode,
        postal_code,
        business_name,
        state_id,
        incorp_date
    )
AS
SELECT cst.cust_id, cst.fed_id, cst.address, cst.city, cst.state, cst.postal_code,
	bsn.name, bsn.state_id, bsn.incorp_date
FROM customer cst INENR JOIN business bsn
	ON cst.cust_id = bsn.cust_id
WHERE cust_type_cd = 'B'
```

we are allowed to modify tables involved in this complex query, but only one table at a time (same for update and insert)
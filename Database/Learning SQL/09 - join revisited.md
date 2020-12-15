[TOC]

# join revisited

## outer joins

in previous chapters we have been considering join conditions that will succeed. here we will look into joins that might fail to find matches for all the rows in the tables. lets say we have 10 customers which 4 of them are business customers. when we are joining customers' table to to business table we might encounter problem where only 4 rows is shown. if we wanted to show all customers in the join we can do as follows

````sql
SELECT a.account_id, a.cust_id, b.name
FROM a account a LEFT OUTER JOIN business b
	WHERE a.cust_id = b.cust_id
/*
account id | cust id | name
1          | 1       | null
...
9          | 9       | business name
*/
````

> outer join includes all the row from one table and includes data from the second table only if matching rows are found

we specified left outer join in the example thus we expected all rows from account tables and matching business table rows. for this example if we join to individual table then we are expected to see 6 non-null rows

## left versus right joins

its a matter of preference, both side works

## three-way outer joins

we can do multi-table outer joins. its technically not a cascading effect. it sticks to the main table in the `from` clause.

```sql
SELECT a.account_id, a.product_cd,
	CONCAT(i.fname, ' ', i.lname) person_name
	b.name business_name
FROM account a LEFT OUTER JOIN individual i
	ON a.cust_id = i.cust_id
	LEFT OUTER JOIN business b
	ON a.cust_id = b.cust_id
-- we are expected a table with 10 rows which col[2] have 6 non null rows, and col[3] have 4 non null rows
```

although there isn't any restrictions (?) to the number of tables we can outer join but if that is ever a concern we could just work with subqueries instead

```sql
-- textbook example
SELECT account_ind.account_id, account_id.product_cd,
	account_ind.person_name, b.name business_name
FROM 
	(SELECT a.account_id, a.product_cd, a.cust_id, CONCAT(i.fname, ' ', i.lname) person_name FROM account a LEFT OUTER JOIN individual i  ON a.cust_id = i.cust_id) account_ind 
	LEFT OUTER JOIN business b
	ON accound_ind.cust_id = b.cust_id
-- my proposal
SELECT a.account_id, a.product_cd,
	(SELECT CONCAT(i.fname, ' ', i.lname) FROM individual i WHERE i.cust_id = a.cust_id) person_name,
	(SELECT b.name FROM business b WHERE b.cust_id = a.cust_id) business_name
FROM account a
```

## self outer joins

cartesian join revisited. in previous chapter we fabricated a table from scratch such that we can categorize customers in to 3 category depending on their available balance. if we wanted to fabricate a much larger table with hundreds of rows the query can become ugly quickly. below is an example

```sql
SELECT DATE_ADD('2008-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) dt
FROM 
	(SELECT 0 num UNION ALL
     SELECT 1 num UNION ALL
     -- ...
    ) ones
    CROSS JOIN (
    	SELECT 0 num UNION ALL
        -- ...
    ) tens
    CROSS JOIN (
    	SELECT 0 num UNION ALL
        -- ...
    ) hundreds
WHERE DATE_ADD('2008-01-01', INTERVAL (ones.num + tens.num + hundreds.num) DAY) < '2009-01-01'
-- line above is to filter dates exceed year 2008
ORDER BY 1
```

if we were asked to check transaction per day in 2008 we could do as follows (query above is called as a function below to simplify)

```sql
SELECT days.dt, COUNT(t.tnx_id),
FROM transaction t 
	RIGHT OUTER JOIN days
GROUP BY days.dt
ORDER by 1
```

## natural joins

natural join is basically giving the database server to determine what join condition to use, its strongly advised to avoid this join be explicit in your queries

```sql
SELECT a.account_id, a.cust_id, c.cust_type_cd, c.fed_id
FROM account a NATURAL JOIN customer c
```

one of the biggest pitfall is if we are joining two tables where the foreign key is not having same name if will default to cross join.
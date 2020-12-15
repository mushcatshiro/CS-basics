[TOC]

# Querying multiple tables

databases tables are usually normalized thus the need of quering multiple tables and combine them - joining the tables. here we first discuss the most common join - inner join and subsequently revisit for more joins.

## cartesian product

$$
A \times B = \{(a, b) | a \in A, b \in B \}
$$

```sql
SELECT e.fname, e.lname, d.name
FROM employee e JOIN department d
```

here we use a simple / plain JOIN. the result might not be what we expected, every employee name is assigned to all existed department name eg. shiro - operations, shiro - loans, shiro - administration, which wasnt the the case when shiro can only have one department.

this is due to the lack of specification on how the joining should be done, the database server thus generated the result with cartesian product, which is every permutation of two tables (n employees x m departments = nm result rows). this is also known as a cross join (with less application), if we wish to use it

```sql
-- ...
	CROSS JOIN table_x x
```



## inner joins

with the addition of *on* subclause we can yield the desired results.

```sql
SELECT e.fname, e.lname, d.name
FROM employee e JOIN department d
ON e.dept_id = d.dept_id
```

inner joins will skip / exclude those where if a value exists for the dept_id column in one table but not the other. inner join is the default if not specified, its best if we specify it.

if the names of the column are **exactly** the same we can use *using* subclause instead of *on*.

```sql
SELECT e.fname, e.lname, d.name
FROM employee e JOIN department.id USING (dept_id)
```

## ansi join syntax

all major database (oracle, mssql, mysql etc) adopted the SQL92 join syntax, but also an older join syntax as shown,

```sql
SELECT e.fname, e.lname, d.name
FROM employee e, branch b
WHERE e.dept_id = d.dept_id
	AND e.start_date < '2007-02-02'
	AND e.assigned_branch_id = b.branch_id
```

the use of *WHERE* is used instead of *on* or *using* subclause is used.

advantages of ANSI join

- query is easier to understand, since join condition and filter conditions are separated by two (sub)clause (on and where)
- the join conditions for each pair of tables are contained in their own *on* clause making it less likely that part of a join will be mistakenly omitted

```sql
SELECT e.fname, e.lname, d.name
FROM employee e INNER JOIN department d
	ON e.dept_id = d.dept_id
	INNER JOIN branch b
	on e.assigned_branch_id = b.branch_id
```

- queries that use SQL92 join syntax are portable across database servers, but the old syntax implementation is slightly different across different servers

## joining three or more tables

joining more tables is similar to what have been shown above, the order in FROM clause doesn't matter. remember SQL is nonprocedural, the order doesn't matter, the actual order is determined by the database engine whichever is more efficient. there exists methods to force certain behavior by using *STRAIGHT_JOIN* or *ORDERED* or *LEADING* optimizer hint if you think a certain order actually improves the efficiency.

joining more tables is like rolling a snowball, it pick up more and more column as subsequent tables are joined.

## using subqueries as tables

```sql
SELECT e.fname, e.lname, d.name
FROM employee e INNER JOIN (SELECT * FROM department WHERE name = 'woodburn branch') as d
```

## using same table twice

we might find sometimes we need to join the same table more than once eg. there are foreign keys to the branch table from both the account table and the employee table, if we would like to include both in the query result we can include the branch table twice in *FROM* cause join to employee and account each once.

```sql
SELECT a.account_id, e.emp_id, b_a.name open_branch, b_e.name emp_branch
FROM account a INNER JOIN branch b_a
	ON a.open_branch_id = b_a.branch_id
	INNER JOIN employee e
	ON a.open_emp_id = e.emp_id
	INNER JOIN branch b_e
	ON e.assigned_branch_id = b_e.branch_id
WHERE a.product_cd = 'CHK'
```

by assigning different aliases to the branch table instance, the server is able to identify the instance we are refering to.

## self-joins

we could join a table to itself within the same query

```sql
SELECT e.fname, e.lname, e_mgr.fname mgr_fname, e_mgr.lname mgr_lname
FROM employee e INNER JOIN employee e_mgr
	ON e.supervisor_id = e_mgr.emp_id
```

when we are using a table multiple times (self or joined table), aliasing is **required**

## Equi-joins vs Non-Equi-Joins

we have been discussing equi-joins thus far, which refers to values from the two tables must match  for the join to succeed.

```sql
--...
	ON something = something_else
```

while majority of the queries are equi-joins, we could do non-equi-joins as follows,

```sql
SELECT e.emp_id, e.fname, e.lname
FROM employee e INNER JOIN product P
	ON e.start_date >= p.date_offered
	AND e.start_date <= p.date_retired
WHERE p.name = 'no-fee-checking'
```

this type of joining have no foreign key relationships, the intend is to retrieve range

### self-non-equi-join

```sql
SELECT e1.fname, e1.lname, 'VS' vs, e2.fname, e2.lname
FROM employee e1 INNER JOIN employee e2
	ON e1.emp_id != e2.emp_id
WHERE e1.title = 'Teller'
	AND e2.title = 'Teller'
```

the join above have on flaw, we will have duplicated entries eg shiro vs haku and haku vs shiro, to resolve that we could do as follows,

```sql
SELECT e1.fname, e1.lname, 'VS' vs, e2.fname, e2.lname
FROM employee e1 INNER JOIN employee e2
	ON e1.emp_id < e2.emp_id -- or >
WHERE e1.title = 'Teller'
	AND e2.title = 'Teller'
```

## join conditions vs filter conditions

join condition and filter condition can share the same clauses due to SQL flexibility, eg

```sql
-- example 1
SELECT a.account_id, a.product_cd, c.fed_id
FROM account aINNER JOIN customer c
	ON a.cust_id = c.cust_id
WHERE c.cust_type_cd = 'B'
-- example 2
SELECT a.account_id, a.product_cd, c.fed_id
FROM account aINNER JOIN customer c
	ON a.cust_id = c.cust_id
	AND c.cust_type_cd = 'B'
-- example 3
SELECT a.account_id, a.product_cd, c.fed_id
FROM account aINNER JOIN customer c
WHERE a.cust_id = c.cust_id
	AND c.cust_type_cd = 'B'
```

all query above yield same result set, thus its best to select the most readable format for maintenance (example 1 is more desired, *ON* subclause for joining and *WHERE* clause for filtering)
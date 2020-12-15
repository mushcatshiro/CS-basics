[TOC]

# working with sets

relational databases are essentially about sets.

## set theory primer

$$
a \cup b \\
a \cap b \\
a \setminus b \\
$$

## set theory in practise

rule of thumb to follow when we are performing set operations on two table

- both table must have same number of columns
- data type of each column **must** be able to be converted from one to another or be the same

a compound query example

```sql
SELECT 1 num, 'abc' str
UNION
SELECT 9 num, 'xyz' str
```

## set operators

set operators are provided in SQL to perform set operation with additional flavour where one that includes duplicates and another that removes duplicates (not necessarily all)

### union operator

> union and union all

both allow to combine multiple datasets, but *UNION* sorts the combined set and remove duplicates whereas *UNION ALL* does not. *UNION all* resulted query total row will always be the sum of the combined tables (even for repeated query) and is simplest for server to handle.

### intersect operator

intersect operator doesn't exists in mysql <= 6.0, do check before using it. if there is no overlapping then the result query will be an empty set. similar to *UNION*, intersect has *INTERSECT* and *INTERSECT ALL*

### except operator

except operator, similar to intersect operator doesn't exists in all database servers and in Oracle db its called *MINUS* instead. the result query will be the **First** table minus any overlap with the second table. *EXCEPT* removes all occurence of duplicate data from A (including any duplicated entries in A itself), *EXCEPT ALL* only removed one occurences of duplicated data from A and every occurences in B.

## set operation rules

### sorting compound query results

to sort the compound query result, we can add an *ORDER BY* clause **after** the last query and specify the the column name from the **first** query.

````sql
SELECT emp_id, assigned_branch_id
FROM employee
WHERE title = 'Teller'
UNION
SELECT open_emp_id, open_branch_id
FROM account
WHERE product_cd = 'SAV'
ORDER BY emp_id
````

### set operation precedence

in general compound queries that contains three or more queries are evaluated from top to bottom with the following caveats

- ANSI SQL specification calls for the *INTERSECT* operator to have precedence over other set operators
- you may dictate the order in which queries are combined by enclosing multiple queries in parenthesis

above are the reasons that mysql does not yet implement *INTERSECT* operator or allow parenthesis in compound queries

```sql
(SELECT * FROM A 
 UNION ALL 
 SELECT * FROM B)
INTERSECT
(SELECT * FROM C
 UNION
 SELECT * FROM D)
```

the precedence should be A u B, C u D then q1 n q2
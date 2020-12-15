[TOC]

# conditional logic

we can utilize conditional logic with `case` expression. an example from previous table that shows name of individual and business.

```sql
SELECT c.cust_id, c.fed_id
	CASE 
		WHEN c.cust_type_cd = 'I'
			THEN CONCAT(i.fname, ' ', i.lname)
		WHEN c.cust_type_cd = 'B'
			THEN b.name
		ELSE 'Unknown'
	END name
FROM customer c LEFT OUTER JOIN individual i
	ON c.cust_id = i.cust_id
	LEFT OUTER JOIN business b
	ON c.cust_id = b.cust_id
```

case expression are designed to mimic the if then else statement found in most programming languages (eg oracle decode(), mysql if()) and design to facilitate if then else logic but with two advantages over built-in funcitons

- case is part of sql standard (SQL92 release) and have been implemented in many database
- case expression are build into sql grammar and can be included in `select`, `update`, `delete` statements

## search case expressions

```
CASE
	WHEN C1 THEN E1
	WHEN C2 THEN E2
	ELSE E3
END
```

one thing to note E1 - EN needs to be in same type else will error out. the expression returned can be any type, including subqueries. below is an example where 

- we don't use outer joins and
- we use subqueries as return expression

```sql
SELECT c.cust_id, c.fed_id
	CASE
		WHEN c.cust_cd_type = 'I'
			THEN (SELECT CONCAT(i.fname, ' ', i.lname) FROM individual i WHERE i.cust_id = c.cust_id)
		WHEN c.cust_cd_type = 'B'
			THEN (SELECT b.name FROM business b WHERE b.cust_id = c.cust_id)
		ELSE 'Unknown'
	END name
FROM customer c
```

this approach is much flexible and only query whatever data needed, should be more efficient than the multi-joining approach above

## simple case expressions

its something similar to search case expression but less flexible

```
CASE V0
	WHEN V1 THEN E1
END
```

V0 represents a value (columns), and check against V1 and returns E1. the rigidity rises when we wanted to do more than just simple comparison and matching.

## case expression examples

### result set transformations

to transform col[0] into row[0] and so on

```sql
SELECT YEAR(open_date), COUNT(*) how_many
FROM account
WHERE open_date between '1999-12-31' and '2006-01-01'
GROUP BY YEAR(open_date)
-- xform!
SELECT
	SUM(SELECT CASE WHEN YEAR(open_date) = '2000' THEN 1 ELSE 0) year_2000,
	SUM(SELECT CASE WHEN YEAR(open_date) = '2001' THEN 1 ELSE 0) year_2001,
	SUM(SELECT CASE WHEN YEAR(open_date) = '2002' THEN 1 ELSE 0) year_2002,
	SUM(SELECT CASE WHEN YEAR(open_date) = '2003' THEN 1 ELSE 0) year_2003,
	SUM(SELECT CASE WHEN YEAR(open_date) = '2004' THEN 1 ELSE 0) year_2004,
	SUM(SELECT CASE WHEN YEAR(open_date) = '2005' THEN 1 ELSE 0) year_2005
FROM account
WHERE open_date between '1999-12-31' and '2006-01-01'
```

> note the transformation above could be easily achieved with PIVOT clause

### selective aggregation

```sql
SELECT CONCAT('Alert! Account #', a.account_id, 'has incorrect balance')
FROM account a
WHERE (a.avail_balance, a.balance) <>
	(
    	SELECT
        	SUM(CASE 
                	WHEN t.funds_avail_date > CURRENT_TIMESTAMP() 
                		THEN 0
              		WHEN t.txn_type_cd = 'DBT'
               			THEN t.amount * -1
               		ELSE t.amount
               	END),
        	SUM(CASE
               		WHEN t.txn_type_cd = 'DBT'
               			THEN t.amount * -1
               		ELSE t.amount
        		END)
        FROM transaction t
        WHERE t.accound_id = a.account_id
    )
```

### check for existence

checking existence is also something we might be interested to, and we only need to acknowledge the existence but not the actual number.

```sql
SELECT c.cust_id, c.fed_id, c.cust_type_cd,
	CASE
		WHEN EXISTS(SELECT 1 FROM account a WHERE a.cust_id = c.cust_id AND a.prod_cd = 'CHK') THEN 'Y'
		ELSE 'N'
	END has_cheking,
	CASE
		WHEN EXISTS(SELECT 1 FROM account a WHERE a.cust_id = c.cust_id AND a.prod_cd = 'SAV') THEN 'Y'
		ELSE 'N'
	END has_savings
FROM customer c
-- another example
SELECT c.cust_id, c.fed_id, c.cust_type_cd,
	CASE (SELECT COUNT(*) FROM account a WHERE a.cust_id = c.cust_id)
		WHEN 0 THEN '0'
		WHEN 1 THEN '1'
		WHEN 2 THEN '2'
		ELSE '3+'
	END num_accounts
FROM customer c
```

## divide by zero error

depending on database server it could throw error if denominator is detected as 0 or return null. we could use case expression to check on this.

```sql
SELECT a.cust_id, a.prod_cd, a.avail_balance /
	CASE
		WHEN prod_tots.tot_balance = 0 THEN 1
		ELSE prod_tots.tot_balance
	END percent_of_total,
FROM account a INNER JOIN
	(
		SELECT a.prod_cd, SUM(a.avail_balance) tot_balance FROM a.account GROUP BY a.prod_cd
    ) prod_tots
    ON a.prod_cd  = prod_tots.prod_cd
    -- i think its weird for one to check the denominator in such way
    -- instead i propose to check if the calculation result is null / devise by zero
```

## conditional updates

sometimes we need to decide what values to set for certain columns to. eg for each transaction we need to modify avail_balance, pending_balance and last_activity_date columns in the account table

```sql
UPDATE account
	SET last_activity_date = CURRENT_TIMESTAMP(),
	    pending_balance = pending_balance + (
        	SELECT t.amount *
            	CASE t.txn_type_cd = 'DBT' THEN -1 ELSE 1 END
        ),
        avail_balance = avail_balance + (
        	SELECT
            	CASE
            		WHEN t.funds_avail_date > CURRENT_TIMESTAMP() THEN 0
            		ELSE t.amount *
            			CASE t.txn_type_cd WHEN 'DBT' THEN -1 ELSE 1 END
            	END
            FROM transaction t
            WHERE t.txn_id = 999
        )
WHERE account.account_id = (
	SELECT t.account_id FROM transaction t WHERE t.txn_id = 999
)
```

## handling null values

null is a total valid value to store in database given we find fit. a simple way to ensure null value is also being retrieved we can do as follow

```sql
SELECT emp_id, lname, fname,
	CASE
		WHEN title IS NULL THEN 'UNK'
		ELSE title
	END title
FROM employees
```


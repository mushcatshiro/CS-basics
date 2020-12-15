[TOC]

# Grouping and aggregates

data is stored at lowest granularity, grouping allows us to deal with these data at a higher granularity.

```sql
SELECT open_emp_id, COUNT(*) AS how_many
FROM account
GROUP BY open_emp_id
```

count with asterisk essentially tells db server to count everything in the group. knowing group by clause runs **after** where clause thus any further filtering is required to use the **having** clause.

## implicit and explicit groups

if we only retrieving aggregates functions in select clause we can have implicit groups as follow,

```sql
SELECT MAX(avail_balance),
       MIN(avail_balance),
       COUNT(*) num_account
FROM account
WHERE product_cd = 'CHK'
```

however the following is not permissible when we try to extent the query to execute query for all available product type.

```sql
SELECT MAX(avail_balance),
       MIN(avail_balance),
       COUNT(*) num_account,
       product_cd
FROM account
-- require the following explicit grouping statement
GROUP BY product_id
```

## count and count distinct

```sql
SELECT COUNT(open_emp_id)
FROM account
-- will return row count

SELECT COUNT(DISTINCT open_emp_id)
FROM account
-- will return dictinct user count
```

## expressions

we can have expressions within these aggergate functions eg.

```sql
SELECT MAX(pending_balance - avail_balance)
max_uncleared
FROM account
```

## NULL

null are handled such that all aggregate function **ignores** null row except count(COL_NAME)

## generating groups

single column grouping is shown above

### multicolumn grouping

```sql
SELECT product_cd,
       open_branch_id,
       SUM(avail_balance) tot_balance,
FROM account
GROUP BY product_cd,
         open_branch_id
```

abive is an example of multicolumn grouping. we can see the additional column appears in both select and group by clause. we are expected to see each column group total multiplicated rows.

### via expressions

```sql
SELECT EXTRACT(YEAR FROM start_date) year,
       COUNT(*) how_namy
FROM employee
GROUP BY EXTRACT(YEAR FROM start_date)
```

execution order...

### generating rollups

rollups are similar to group summary and we could do rollups within query as follow

```sql
SELECT product_cd,
       open_branch_id,
       SUM(avail_balance) tot_balance,
FROM account
GROUP BY product_cd,
         open_branch_id WITH ROLLUP
```

there exists another useful function `with cube` which summaries all possible combination.

## filtering

having is used to fapply filter condition after groups have been generated

```sql
SELECT product_cd,
       SUM(avail_balance) prod_palance
FROM account
WHERE status = 'active'
GROUP BY product_cd
HAVING SUM(avail_balance) >= 10000
```

we can include aggregate function in having clause that do not appear in the select clause as demonstrated

```sql
SELECT product_cd,
       SUM(avail_balance) prod_palance
FROM account
WHERE status = 'active'
GROUP BY product_cd
HAVING MIN(avail_balance) >= 1000
       AND MAX(avail_balance) <= 10000
```

these min and max aggregate function are applied to each group checking if within group A there exists avail_balance out of the boundary and excludes the entire group.
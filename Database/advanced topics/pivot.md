[TOC]

# Pivot and Unpivot

> for mssql

```mssql
SELECT NON_PIVOT_COL,
	FIRST_PIVOTED_COL AS COL1,
FROM
	TABLE_ as TABLE_ALIAS
PIVOT
	(
    	AGG_FUNC(AGG_COL)
        FOR COL_THAT_CONTAINS_VALUES_THAT_WILL_BECOME_COL_NAME
        IN (PIVOTED_COL_LIST)
    ) AS PIVOT_TABLE_ALIAS
```

example_1

| PRODUCT | DAY_OF_WEEK | PROFIT |
| ------- | ----------- | ------ |
| ball    | MON         | 100    |
| ball    | TUE         | 120    |
| ball    | WED         | 90     |
| pen     | MON         | 20     |
| pen     | TUE         | 50     |

```mssql
SELECT
	PRODUCT,
	'MON',
	'TUE',
	'WED',
	'THU',
	'FRI',
	'SAT',
	'SUN'
	-- or equivalent *
FROM example_1
PIVOT
	(
    	SUM(PROFIT)
        FOR DAY_OF_WEEK
        IN (SELECT DAY_OF_WEEK FROM example_1)
    )
```

> postgresql


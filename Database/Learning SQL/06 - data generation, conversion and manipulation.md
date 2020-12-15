[TOC]

# data generation, conversion and manipulation

differnent database server provides different out of box functionality.

## working with string data

1. char - different db server allows differnent length, but generally it holds fixed length, blank paddeled strings
2. varchar - holds variable-length strings
3. text / clob - holds very large variable-length strings (or documents)

### string generation

if the length of string exceeds the maximum column length, server will throw an exception by default. but we can configure it to truncate instead. 

````sql
-- for mysql we can check out sql_mode and set to ansi to enable auto truncate
SELECT @@session.sql_mode
SET sql_mode = 'ansi'

-- with truncate turned on by default we can check any truncation by the folowwing line after updating
SHOW WARNINGS
````

### escape characters

we could either do the double single qoute or some db servers allow to use backslash for escaping. another thing to note is whenever we select data from database and pass to the next handler / software remember to handle all these string escaping related issue.

### special characters

eg. german or french, we could use build in function `char()` to insert. also the character presented might be different based on the db server setting for charater set.

## working with numerical data

all common arithmetic operation are readily available.

### controlling precision

operation eg. ceiling, flooring, rounding

### handling signed data

there exists a function which return 0, 1, -1 based on the sign

## working with temporal data

one of the more complex out of the three.

### generation temporal data

4 methods to generate

1. copy from existing date, datetime, time column
2. executing a built-in function
3. building a string representation of temporal data to be evaluated by the server

> on 3, db server will have its own set of formatting eg. mysql STR_TO_DATE('2020-11-28 21:00:00', '%Y-%m-%d %H:%i:%s')

4. for current date / time there exists built in function for those

### temporal function that returns date

```sql
SELECT DATE_ADD(CURRENT_DATE(), INTERVAL 5 DAY)
```

### temporal function that returns numbers

```sql
SELECT DATEDIFF('date1', 'date2')
-- note its date1 - date 2
```


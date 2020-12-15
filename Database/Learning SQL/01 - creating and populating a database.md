[TOC]

# creating and populating a database

## data types

### character

fixed length or variable-length strings. fixed length strings are right padded with spaces and consumes same number of bytes.

```sql
char(20)
varchar(20)
```

for larger text documents, emails, XMLs use text types (mediumtext or longtext)

character sets

```sql
SHOW CHARACTER SET;
```

latin based languages eg english is sufficient small enough to store each character in a single byte. other languages eg japanese or chinese contains large numbers of characters thus requiring multiple bytes storage for each character. 

```sql
varchar(20) character set utf8;
-- or
create database dbname character set utf8;
```

### text data

to store data that exceeds 64KB size limit. 

- data will be truncated if the data loaded exceeds the text type limit.
- trailing spaces will not be removed when data is loaded
- sorting and grouping text columns only first 1024 bytes are used, although it can be increased
- different database server for text types

### numerical data

- boolean 0 or 1
- system generated primary key
- positive integers
- high precision data

in MySQL we can specify a numeric data to be signed or unsigned. floats that exceeds precision will be rounded.

### temporal data

date, time and datetime.

timestamp

## after table creation

```sql
>> Query OK, 0 rows affected
>> DESC tablename;
```

## NULL

indicates absence of value

- not applicable
- unknown
- empty set

## populating and modifying tables

### inserting data

generating numeric key data, we usually leaves this to database itself with AUTO_INCREMENT. when we manually insert data the auto increment column can be left as NULL.

- as long as our temporal data provided matches the format, database engine will convert the string to the correct format.

### updating data

```sql
>> Query OK, 1 row affected.
>> Rows Matched: 1 Changes: 1 Warnings: 0
```

### delete data

## when good statements go bad

### non unique primary key

if there isn't any other constrains we can insert records and bypassing the auto increment restrictions. but if there is primary key constrains it will prevent duplicate key values

### nonexistent foreign key

when we try to insert a nonexistent foreign key to a table, database will also prevent this from happening. this constrain exists in InnoDB database engine.

### column value violations

eg. ENUM columns that allows M or F, if we insert something else it will also error out.

### invalid data conversions

```sql
UPDATE tablename
SET birth_date = str_to_date('DEC-12-1995', '%b-%d-%Y')
WHERE person_id = 1
```


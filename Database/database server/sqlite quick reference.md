[TOC]

# quick reference

## sqlite all tables

```sql
SELECT name 
FROM sqlite_master 
WHERE type ='table' AND name NOT LIKE 'sqlite_%';
```

## sqlite table's columns

```sql
SELECT sql 
FROM sqlite_master 
WHERE name = 'albums';
```

## importing from flat files to database

````bash
>> .mode csv # or tsv
>> .import FILENAME TABLENAME
>> .schema # check the previous import SQL
````
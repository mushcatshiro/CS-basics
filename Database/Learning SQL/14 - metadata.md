[TOC]

# metadata

database stores information about all database objects that were created to store this data. we will be discussing how and where this information is stored, how we can access it and utilize it. a few metadata as follow

- table name
- storage engine
- `NOT NULL` constrain

and etc.
these data is known as the data dictionary or system catalog. it needs to be stored persistently and be able to retrieve easily in order to verify and execute SQL statements. also it ensures modification can only go through proper mechanism. there exists standards for exchange of metadata but each database server uses a different mechanism to publish metadata.

## information_schema

all objects available within information_schema database are views. unlike describe utility, views within information_schema can be queried thus used programmatically.

```sql
SELECT table_name, table_type
FROM information_schema.tables -- views, columns, statistics, table_constraints and more
WHERE table_schema = 'bank'
ORDER BY 1 -- ordinal_position
-- it would be beneficial if we explicitly type in USE your_database before checking metadata in GUI
```

we can query all sorts of information eg. view list, view definition, column information 

> ordinal position include merely as a means to retrieve the columns in the order in which they were added to the table

## working with metadata

### schema generation scripts

we can query into the metadata such that we can create a duplicated table in full sql.

### deployment verification

lets say we would like to make changes to database eg. add column and etc. we could write a sql query to check current existing row count for each table / columns and run it before and after we implement the change to ensure the migration is successful.

### dynamic sql generation

its a bit tedious thus skip. 

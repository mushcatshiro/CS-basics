[TOC]

# Query Primer

## query mechanics

once all access requirements are met, query is handled to the query optimizer, whose job is to determine the most efficient way to execute the query. it will look the order in which to join the tables named in *from* clause and available indexes and picks an execution plan.(more in High Performance MySQL, O'Reilly - generate indexes, analyze execution plans, influence optimizer via query hints, server startup parameters and more)

## query clauses

- select
- from 
- where
- group by
- having 
- order by

## select

usually executed the last, reason being we need to know all the possible columns that could be included in the final result set before we can determine what to include in the final result set.

> select clause determines all possible columns should be included in the query result set

we could add in customization to our select statement eg adding in new column, expressions, build-in functions (truncate etc.)

### column alias

we can assign our own labels to columns in our result set. it can be explicit or implicit,

```sql
>> SELECT asdf as status -- or
>> SELECT asdf status
-- both works
```

some customization (not an exhaustive list),

```sql
>> SELECT DISTINCT name
```

## from

> from clause defines the tables used by a query, along with the means of linking the tables together

- permanent tables (created using schema statements)
- temporary tables (in subqueries)
- virtual tables (created using *create view* statement)

### short introduction to subqueries and views

**subqueries** are surrounded by parenthesis, and can be found in various parts in the query statement

**views** is a query stored in data dictionary. it looks and acts like a table but there is no data associated with a view, database only store the definition of a view. when we query against a view, the query is merged with the view definition to create a final query to be executed.

- security: restrict user from directly accessing to a table
- simplicity: such that user can care less on complex joins / relations
- consistency: same as above

## where

> where clause is the filtering mechanism for unwanted rows from your query set

filters could be complexed conditions, using *or*, *and*, *not* to link up.

when we are using *or* -- only one of the conditions need to evaluate to true and it will be returned; 

when we are using *and* -- all conditions must be evaluate to true.

parenthesis can be added if we want to separate out the filtering logics.

## group by and having

in short group is to aggregate data and having functions like where, these two clauses are more advanced topic to be discussed in later chapter

```sql
-- departments with 2 or more employees
SELECT d.name, COUNT(e.emp_id)
FROM Departments d INNER JOIN Employee e
    ON d.Id = e.department_id
GROUP BY d.ID
HAVING COUNT(e.emp_id) > 2
```

## order by

> order by clause is the sorting mechanism for the result set using expressions or raw data from column(s)

we can have multiple columns such that its ordered within groups. sorting default is ascending. order by is usually companioned with limit clause.

> limit clause is applied after all filtering, grouping, and ordering have occurred. it will never change the outcome of select statement other than restricting number of records.

### limit clause second parameter

```sql
select open_emp_id, count(*) how_many
from account
group by open_emp_id
order by how_many, open_emp_id
limit 2, 1;
```

the first designates at which record to begin adding records to the final set, eg. in the example above its the 3rd record (starts from 0), and second parameter specified how many record to include, thus we are getting the 3rd highest count employee id with the query above.

### ranking queries

order by + limit are called ranking queries. this opened up queries for top and bottom query to answer business questions.

### sorting via expressions

its possible to add expressions to the column that is supposed to be ordered

````sql
>> order by RIGHT(column, 3)
````

### sorting via numeric placeholders

this might is not common as it uses the column's position instead of column name, which is less expressive

___

## execution order

the execution order is ususally as listed below

1. FROM / JOIN - this allows us to search and locate our data, temporary table might be generated for subsequent oprations
2. WHERE - to filter out data we are not interested in. since its executed before select thus we can't work with aliases here
3. GROUP BY - if there are rows that is not able to be groupped it will also be truncated from the result set
4. HAVING - next layer of filtering on groupped data, still not able to use aliases
5. SELECT - select the columns that we specified
6. DISTINCT - remove duplicated row in specified columns
7. ORDER BY - only executed once data is finalized, post SELECT thus aliases works here
8. LIMIT / OFFSET
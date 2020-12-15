[TOC]

# filtering

where clause is separated by and or or operators. multiple operators logic was stated in [previous chapter](.\02 - query primer.md). parentheses also was mentioned, its good to have parenthesis for multiple conditions with more than 2 logic operators.

### the not operator

```sql
>> AND NOT(conditions)
```

not operator is not always the best for readability, use it sparingly

## building conditions

filtering condition could be a wide range of data type including subquery, expressions and we can have arithmetic operators, comparison operators as the operators

### condition type 1: equality

```sql
>> column = 'something'
```

### condition type2: inequality

```sql
>> WHERE column <> 'something'
```

### condition type3: range conditions

```sql
>> WHERE date_ > 'some date' or date_ <= 'some date'
>> WHERE date_ between 'some EARLY date' and 'some LATE date'
```

using between we should always specify the lower limit of the range first because if we do the other way round it would be interpret as such

```sql
>> WHERE date_ between 'some LATE date' and 'some EARLY date'
-- is interpreted as
>> WHERE date_ >= 'some LATE date' and date_ <= 'some LATE date'
```

its possible to do string ranges, it works based on the string character set order

### condition type4: membership

instead of using multiple 'or' we can do as follows,

```sql
>> WHERE column in ('abc', 'bca', 'cba')
```

membership can be combined with subqueries or *NOT IN* to fulfill more business needs

### condition type5: matching

wildcards,

```sql
-- use _ for exactly one character
-- and use % for any number of characters including 0
```

or regex,

```sql
>> WHERE column REGEXP '^[FG]' -- different servers have different func call
```

## Null

null is a complicated type, where its used when data is not applicable, value yet to be known and value undefined. one must take note an expression can be null but **never** equivalent to null. to test expression if its null,

```sql
>> WHERE column IS NULL
```

side topic since null is not check against equivalency thus if we do

```sql
>> WHERE column != '1' -- null will be ignored and not appear in the query result
-- logic null != '1' but null is not checked against thus is ignored
```

its good to always assume there is null when we do filtering, unless we know exactly the schema
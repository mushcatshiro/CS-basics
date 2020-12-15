# Leetcode Sql

objective

- solve all 108 questions and try to learn by actually writing
- write a comprehensive conclusion on methodology and understanding
- combined with book Learning SQL
- stucked with free questions at the moment...

_________

#### Q175 combine two tables

Write a SQL query for a report that provides the following information for each person in the Person table, *regardless if there is an address for each of those people*:

```sql
select Person.FirstName,
       Person.LastName,
       Address.City,
       Address.State
from Person, Address where Person.PersonId = Address.PersonId
-- runtime 532ms

-- or 

select Person.FirstName,
       Person.LastName,
       Address.City,
       Address.State
from Person left join Address on Person.PersonId = Address.PersonId

-- runtime 673ms
```

> not sure whats the lesson learnt here, the runtime seems to be not accurate
but i suspect with and without the Person. perfix will impact search speed

#### Q176 second highest salary

```sql
select Max(Salary) as SecondHighestSalary
from Employee
where Salary < (select Max(Salary) from Employee)

-- or

select Salary as SecondHighestSalary
from Employee
order by Salary
limit 1, 1

```

> second method is less preferable as its more rigid

##### Q177 nth highest salary

*If there is no nth highest salary, then the query should return null*

```sql
CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
    SET N = N - 1;
    RETURN (
        # Write your MySQL query statement below.
        ifnull((select distinct Salary
        from Employee
        order by Salary DESC
        limit 1
        offset N), NULL)
    );
END
```

> why select distinct? without distinct what will happen? refer to question

#### Q178 Rank Scores

```
given
+----+-------+
| Id | Score |
+----+-------+
| 1  | 3.50  |
| 2  | 3.65  |
| 3  | 4.00  |
| 4  | 3.85  |
| 5  | 4.00  |
| 6  | 3.65  |
+----+-------+

return
+-------+------+
| Score | Rank |
+-------+------+
| 4.00  | 1    |
| 4.00  | 1    |
| 3.85  | 2    |
| 3.65  | 3    |
| 3.65  | 3    |
| 3.50  | 4    |
+-------+------+
```

```sql
SELECT
    S1.Score,
    (SELECT COUNT(DISTINCT Score) FROM Scores AS S2 WHERE S2.Score >= S1.Score) as "Rank"
FROM Scores AS S1
ORDER BY Score DESC

```

> no clue where to start but its an good question to understand the execution order (select is probably one of the last to be executed)

#### Q180 Consecutive Numbers

Write a SQL query to find all numbers that appear at least three times consecutively.

```
+----+-----+
| Id | Num |
+----+-----+
| 1  |  1  |
| 2  |  1  |
| 3  |  1  |
| 4  |  2  |
| 5  |  1  |
| 6  |  2  |
| 7  |  2  |
+----+-----+
```

```sql
-- interpret wrongly the question, instead this solves count > 3
select L1.Num
from (select Count(Num) as C1, Num from Logs group by Num) as L1
where L1.C1 >=3

-- correct answer
SELECT *
FROM
    Logs l1,
    Logs l2,
    Logs l3
WHERE
    l1.Id = l2.Id - 1
    AND l2.Id = l3.Id - 1
    AND l1.Num = l2.Num
    AND l2.Num = l3.Num
```

#### Q181 Employees Earning More Than Their Managers

```sql
select
    E.Name as 'Employee'
    # E.Salary,
    # M.Name,
    # M.Salary
from Employee E inner join Employee M 
	on E.ManagerId = M.Id
where E.Salary > M.Salary
```

> concept of self join (not a join method ie inner outer left and right)

#### Q182 Duplicate Emails

Write a SQL query to find all duplicate emails in a table named Person	

```sql
select t.Email
from (select count(Email) as cnt, Email from Person group by Email) as t
where t.cnt > 1

-- or

Select Email
From Person
GROUP BY Email
having count(Email) > 1
```

> remembering there is this 'having' statement

#### Q183 Customers who never order

```
+----+-------+
| Id | Name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+

+----+------------+
| Id | CustomerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+

+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+
```

```sql
select 
    Name as 'Customers'
from Customers
where Id not in (select CustomerId from Orders)
```

> not in. nothing much maybe reminding myself the important of naming collisions with table name and resolving with string ''

#### Q184 Department Highest Salary

```sql
SELECT d.Name "Department", e.Name "Employee", e.Salary
FROM Employee e JOIN Department d
  ON e.DepartmentId = d.Id
WHERE
    (d.Id , e.Salary) IN
    (SELECT DepartmentId, MAX(Salary)
     FROM Employee
     GROUP BY DepartmentId)
```

#### Q185 Department Top Three Salaries ??

```sql
SELECT d.Name AS 'Department', e1.Name AS 'Employee', e1.Salary
FROM Employee e1 JOIN Department d
	ON e1.DepartmentId = d.Id
WHERE 3 > 
	(SELECT COUNT(DISTINCT e2.Salary)
     FROM Employee e2
     WHERE e2.Salary > e1.Salary
     AND e1.DepartmentId = e2.DepartmentId)
 -- or
SELECT d.Name AS Department, e.Name AS Employee, e.Salary
FROM Employee e JOIN Department d
	ON e.DepartmentId = d.Id
WHERE (SELECT COUNT(DISTINCT Salary)
       FROM Employee
       WHERE Salary > e.Salary
       AND DepartmentId = d.Id) < 3
```

#### Q196 Delete Duplicate Emails

Write a SQL query to delete all duplicate email entries in a table named Person, keeping only unique emails based on its *smallest Id*

```sql
delete from Person where Id not in (select t.Id from (select min(Id) as Id from Person group by Email) as t)

-- or

# find duplicated -> keep smallest

delete from Person where Id not in 
    (select t.Id from
        (select min(P.Id) as Id
         from Person P
         where Email in 
            (select Email 
             from Person 
             group by Email
             having count(Email) > 1 )
        group by P.Email) as t)

-- 2nd attempt

delete from Person where Id not in 
    (select t.Id from
        (select min(P.Id) as Id
         from Person P
         where Email in 
            (select count(Email) as cnt, Email
             from Person 
             group by Email) # here is where i am refering to aggregate function wont work if we wanted to include the Id
        group by P.Email) as t)

```

> approach 1 is much easier since we wanted to keep the smallest, so we find the smallest of every email then not in  
for approach 2 is much complicated (still not working, and dont think it will work because aggregate function dont work in favour)  
*also why having exist is basically due to aggregate function will always run after where clause and before having clause*  
another thing to take note is if we are using insert delete or update we can never directly refer to the table thats why the *nested select*

#### Q197 Rising Temperature

find all dates' Ids with higher temperature compared to its previous (yesterday's) dates.

```sql
select w1.Id # today
from Weather w1, Weather W2
where w1.Temperature > w2.Temperature # today is hotter than yesterday
    and TO_DAYS(w1.RecordDate) - TO_DAYS(w2.RecordDate) = 1 # today is always 1 day bigger than yesterday
```

> not to confuse today and yesterday

#### Q262 Trips and Users

The Trips table holds all taxi trips. Each trip has a unique Id, while Client_Id and Driver_Id are both foreign keys to the Users_Id at the Users table. Status is an ENUM type of (‘completed’, ‘cancelled_by_driver’, ‘cancelled_by_client’). The Users table holds all users. Each user has an unique Users_Id, and Role is an ENUM type of (‘client’, ‘driver’, ‘partner’).

Write a SQL query to find the cancellation rate of requests made by unbanned users (both client and driver must be unbanned) between **Oct 1, 2013** and **Oct 3, 2013**. The cancellation rate is computed by dividing the number of canceled (by client or driver) requests made by unbanned users by the total number of requests made by unbanned users.

For the above tables, your SQL query should return the following rows with the cancellation rate being rounded to *two* decimal places.

```sql
SELECT Request_at "Day", ROUND(count(IF(status = 'cancelled_by_client' or status ='cancelled_by_driver',1,NULL))/ count(*),2) "Cancellation Rate"
FROM Trips
WHERE Client_Id IN (SELECT Users_Id
    FROM Users
    WHERE Banned = 'No'
    AND Role = 'client')
AND Driver_Id IN (SELECT Users_Id
    FROM Users
    WHERE Banned = 'No'
    AND Role = 'driver')
AND Request_at BETWEEN '2013-10-01' AND '2013-10-03'
GROUP BY Request_at
```

#### Q595 big countries

satisfy two different conditions

```sql
select name, population, area
from World
where area > 3000000 or population > 25000000
```

> nothign much

#### Q596 classes with more than 5 students

```sql
select class
from courses
group by class
having count(distinct student) >= 5
```

> nothing much, not to repeat same mistake

#### Q601 Human Traffic of Stadium

Write an SQL query to display the records with three or more rows with **consecutive** id, and the number of people is greater than or equal to 100 for each.

```sql
SELECT DISTINCT S1.*
FROM stadium S1
JOIN stadium S2
JOIN stadium S3
	ON ((S1.id = S2.id - 1 AND S1.id = S3.id -2)
	OR (S3.id = S1.id - 1 AND S3.id = S2.id -2)
	OR (S3.id = S2.id - 1 AND S3.id = S1.id -2))
WHERE S1.people >= 100
	AND S2.people >= 100
	AND S3.people >= 100
ORDER BY S1.id;
```

#### Q620 not boring movies

```sql
select id, movie, description, rating
from cinema
where id%2 != 0
    and description not in ('boring')
order by rating desc
```

> nothing much

#### Q624 Exchange Seats

to change seat for adjecent students, if odd skip the last student

```sql
SELECT
    (CASE
        WHEN MOD(id, 2) != 0 AND counts != id THEN id + 1
        WHEN MOD(id, 2) != 0 AND counts = id THEN id
        ELSE id - 1
    END) AS id,
    student
FROM
    seat,
    (SELECT
        COUNT(*) AS counts
    FROM
        seat) AS seat_counts
ORDER BY id ASC;
```

#### Q627 swap sex

Given a table salary, such as the one below, that has m=male and f=female values. Swap all f and m values (i.e., change all f values to m and vice versa) with a **single update statement** and no intermediate temp table.

Note that you must write a single update statement, **DO NOT** write any select statement for this problem.

```sql
update salary set sex = (case when sex = 'm' then 'f' when sex = 'f' then 'm' END)
```

> use of case
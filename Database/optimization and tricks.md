[TOC]

#  optimzation and tricks

1. if a column is nullable, instead of leaving it as null make it 0 or some other default value to prevent full scan
2. choose the best data type, eg. bytes required (int or bigint, signed or unsigned)
3. timestamp instead of datetime
4. enum instead of string
5. keep string len low
6. use int for IP address?
7. replace single column index to multi column index
8. use join instead of subquery
9. simplify update or delete
10. always shift calculation towards the equation right side eg. WHERE age = 10 + 1, if WHERE age + 1 = 10 => full scan
11. IN instead of OR
12. avoid checking non-equality or NOT IN in WHERE clause
13. BETWEEN instead of IN
14. 
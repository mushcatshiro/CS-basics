[TOC]

# using java library

or java api.

arraylist example

```java
ArrayList<String> myList = new ArrayList<String>();
String a = new String("cat");
myList.add(a);
String b = new String("dog");
myList.add(b);
int size = myList.size();
Object o = myList.get(1);
myList.remove(1);
boolean isIn = myList.contains(b);
```

advantages over plain array,

- not required to predetermine size
- not required to assign to specific location eg. myList[1]
- parameterized with <>

## short circuit methods

&& and || are lazy evaluated, thus if first condition is evaluated and return favorable result it will stop evaluating the next. it could raise some issues when the reference variable is not assigned. to force evaluation we could use & and |, but they are typically used for manipulating bits.

## java library

every class in java library belongs to a package eg. javax.swing or java.util. package provides name scoping to prevent collisions. more on library later. only those under java.lang doesnt require import. the import isn't something like include in C, it wont bloat up the code and make it slower.
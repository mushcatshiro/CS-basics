[TOC]

# numbers matter

math class in java doesn't have any instance variable value, its methods are private access and static thus we don't and can't create an instance of math with `new` but just reference it.

## regular and static methods

`static` allows class to be run without the need of having the class. static basically refers to behavior is independent of instance variable.

```java
public class Duck{
    private int size;
    public static void main(String[] args){
        System.out.println("size of duck" + size);  // will not compile cant reference non static variable from static content
        System.out.println("size of duck" + getSize());  // same applies for non static methods
    }
    public void setSize(int s){
        size = s;
    }
    public int getSize(){
        return size
    }
}

// however the opposite works ie non-static method can access a static vatiable
```

we can prevent users from instantiating a non-abstract class by marking the constructor `private`. however this does not means that a class with one or multiple static method should never be instantiated. PSVM is static but still doesn't stop us from instantiating it for testing.

## static variable

```java
public class Duck{
   private static int duckCount = 0;  // static and will not reset, all instances share single copy of static variables
   public Duck(){
       duckCount++;
   }
}

// contrasting with the following
class Duck{
    int duckCount = 0;
    public Duck(){
        duckCount++;
    }
}
```

static variables are shared. static variables are initialized when a class is loaded (JVM decides when) and gets default value if not explicitly initialized. its initialized before any object of that class is created and before any static method of the class runs.

## final

static final variables are constants. to initialize a static final variable,

```java
class Foo {
    final static int x;
    static {
        x = 42;
    }
}

// or

public class Foo {
    public static final int FOO_x = 42;
}
```

final variable means you can't change its value, final method means you can't override the method, and final class means you can't extend the class.

## wrapping a primitive

before java 5.0 we can have `ArrayList<Integer>` so requires wrapping and unwrapping which is not something we will be using so ... skip!

## static imports

nope. not for you. skip!

```java
// to save some typing we can import class and use it as such
import static java.lang.System.out;
import static java.lang.Math.*;

class WithStatic {
    public static void main(String[] args) {
        out.println(“sqrt “ + sqrt(2.0));
    }
}
```

there are some occasions where if we need to have a lot of prints or using math sqrt then we can do the static imports to cut down the mundane typing else should avoid.

___

Java Reflection API

java.util.Date is only good for timestamp of now, the rest use java.utils.Calendar (for date manipulation)

```java
Calendar c = Calendar.getInstance();
long day = c.getTimeInMillis();
day += 1000 * 60 * 60;
c.add(c.Date, 35);
System.out.println(c.getTime())
```




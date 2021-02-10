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
```

static variable

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



___

Java Reflection API


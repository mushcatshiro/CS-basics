[TOC]

# classes and objects

object oriented programming. inheritance is able to win over procedural in the sense that if we have lots of similar but unique objects, we could inherit from a root object and overrides the methods whenever we see fits.

- instance variables: what an object is supposed to know
- methods: what an object is supposed to do

a class is not an object is a blueprint for an object, it informs jvm on how to create a copy of that object (w/ or w/o different instance variables)

```java
class Cat {
    int size;
    String breed;
    String name;
    void meow() {
        System.out.println("meow");
    }
}
// main as the entry point, thus act as a test most of the time
// the rest of the time is to launch your java application
class CatTestDriver {
    public static void main (String[] args) {
        Cat c = new Cat();
        c.name = "shiro";
        c.meow()
    }
}
```

OO expects objects to talk to another object, not to dwell in the main function.

## on GC

each java object created goes into the heap, or more precisely garbage-collectible heap. jvm will manage these memory allocated by identifying objects that can never be used again and run when we are running low on memory (more on this later).

## on JAR

jar or java archive is when we have large file structure to deliver by generating a .jar file and include a manifest that defines which class in that jar holds the main method that should be run

## on OO

we can extend a program without touching previously tested code
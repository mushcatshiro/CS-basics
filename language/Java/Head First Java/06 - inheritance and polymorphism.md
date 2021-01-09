[TOC]

# inheritance and polymorphism

some inheritance

```java
public class animal {
    String picture; // url
    String food;
    boolean hunger;
    int boundaries;
    String location;
    
    void makeNoise() {}
    void eat() {}
    void sleep() {}
    void roam() {}
}

public class Lion extends animal {
    public void roam() {
        super.roam(); // calls the inherited version
        // do your lion roam
        // so it becomes run roam from animal
        // and continue stuff under it
    }
}
```

a superclass is a class that is inherited by other class or subclass. or in java we extends the subclass with superclass. instance variable are not overridden. we can give the inherited instance variable any value it choose.

jvm start walk up the inheritance chain, and execute whichever lowest available.

we extend something that passes IS-A test (one way relationship), instance variable is something that passes HAS-A test.

## access levels

private - default - protected - public

access levels control who see what. public members are inherited, private arent. more on default and protected later.

##  polymorphism

```java
animal myLion = new Lion();
// an example
animal[] animals = new animal[2];
animals[0] = new Lion();
animals[1] = new Tiger();
for (int i : animals.length) {
    animals[i].roam();
}
// another example
class vet {
    public void giveShot(animal a){
        // do stuff to animal
        a.makeNoise();
    }
}
```

in short its future compatibility.

## engineering note on inheritance

- usually its wide but not deep (2 or less levels), some exceptions eg GUIs
- we can extend almost all class, except inner class or final class or have private constructors
  - class can be public and non-public but not private
- final class is to ensure methods will always work
- we could make a method final
- methods are supposed to share the same template, eg same args and same return types else its an overload not override
- methods in subclasses should not be less accessible

## methods overloading

its having two methods with same name but different arguments list. there is no polymorphism in overloaded methods. we can have different return types but it cant be the only difference and it can have different access levels.

```java
// a legal overloading
public class Overloads {
    String uniqueID;
    public int addNums(int a, int b) {
        return a + b;
    }
    public double addNums(double a, double b) {
        return a + b;
    }
    public void setUniqueID(String theID) {
        // lots of validation code, and then:
        uniqueID = theID;
    }
    public void setUniqueID(int ssNumber) {
        String numString = “” + ssNumber;
        setUniqueID(numString);
    }
}
```


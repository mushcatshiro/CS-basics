[TOC]

# life and death of an object

stack and heap. heap is where object are created, and stack is where method invocations and local variables live.

instance variables are declared in a class but not in method. they lives in the object they belong to.

local variables are declared in a methods including method parameters. they live only as long as the method is on the stack.

methods are stacked. 

```java
public void a{
    go();
}
public void go{
    gogo();
}
public void gogo{
    // sth
}
```

sequence of events will be a - go - gogo - pop gogo from stack - pop go from stack pop a from stack.

objects will always be on the heap, variables that references to the object only stores the reference not the actual object itself.

what about objects with instance variable which is also an object? instance variable will allocate memory for every primitive types and reference to object.

## object creation

1. declare a reference variable
2. create an object
3. link the object and reference

```java
Duck myDuck; // 1
new Duck(); // 2, we are calling the duck constructor not the method duck
Duck myDuck = new Duck() // 3
```

if the duck constructor does not exists, JVM will do it for you

```java
public duck(){} // no return type?
```

```java
public class Duck{
    public Duck(){
        System.out.println("quack"); // equivalence to python init
    }
}

public class useDuck{
    public static void main (String[] args){
        Duck d = new Duck(); // "quack"
    }
}
```

a constructor runs before the object can be assigned to a reference thus there is no return type and thats how we differentiate between method and constructor. constructors are not inherited, but will be called when we instantiated one. JVM will only sub in the default constructor if it dont find one. if we would like to have arg and no arg constructor, we need to create both ourselves. also to ensure constructor is overloaded properly, they must have different argument list. constructors doesnt have be to public.

with that said, when we `new` some object all instance variable (including those up in the inheritance tree) will be created in a single heap. thus all constructor in the superclasses will run.

```java
// invoking superclass constructor
public class Duck extends Animal{
    int size;
    public Duck(int newSize){
        super(); // to invoke superclass constructor, basically Animal()
        size = newSize;
    }
}
```

super is called implicitly if not specified. super must always be the first statement to be called, if not when we `new` a object it will error out. `super` accepts arguments, which benefits situation that a superclass constructors requires one. to invoke an overloaded constructor from another, we can use `this` which refers to the current object. `this` can only use within a constructor and mutually exclusive with `super`.

```java
class Mini extends Car{
    Color color;
    public Mini(){
        this(Color.red);
    }
    public Mini(Color c){
        super("Mini");
        color = c;
        // more init
    }
    public Mini(int size){
        this(Color.Red);
        super(size);
        // doesnt work
    }
}
```

## life span of an object

it depends on the references referring to it. it will be kept alive as long as there is references referring to it. a reference variable is either a local variable or an instance variable. a local variable (stack) lives within the method that declared that variable and an instance variable (heap) lives as long as the object does. if a reference variable goes out of the scope but still alive, the object it refers to is still alive on heap. the trick is to know when its GC eligible when we are done with them, else we will see out of memory death.

___

## six usage of `this` keyword

```java
// refer to current class instance variable
class Student{
    int no;
    String name;
    Student(int no, String name){
        this.no=no;
        this.name=name;
	}
}
// to invoke current class method
class A{
    void m(){System.out.println("hello m");}
    void n(){
        System.out.println("hello n");
        //m();//same as this.m()
        this.m();
    }
}
// to invoket current class constructor
class A{
    A(){System.out.println("hello a");}
    A(int x){
        this();
        System.out.println(x);
    }
}
// argument in the method
class S2{
  void m(S2 obj){
  	System.out.println("method is invoked");
  }
  void p(){
  	m(this);
  }
  public static void main(String args[]){
      S2 s1 = new S2();
      s1.p();
  }
}
// argument in constructor call
class B{
  A4 obj;
  B(A4 obj){
    this.obj=obj;
  }
  void display(){
  	System.out.println(obj.data);//using data member of A4 class
  }
}

class A4{
  int data=10;
  A4(){
   	B b=new B(this);
   	b.display();
  }
  public static void main(String args[]){
  	A4 a=new A4();
  }
}
// return current class instance
class A{
    A getA(){
    return this;
	}
}
```


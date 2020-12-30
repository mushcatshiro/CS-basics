[TOC]

# variables

variables are more than just primitive data types. we could have objects as variables - object reference (for type safety).

> in case someone wonders, 1bit, byte (8bit), short (16bit), int (32bit), long(64bit), float(32bit), double(64bits)

we can downsample / lose precision our values, with warning.

## object reference

there is no object variables, its reference. it holds bits that represent a way to access that object (*like* a pointer, that only jvm knows whats inside the reference variable).

these reference is an indicator of the eligibility of GC.

> in fact, arrays are objects too together with other data structures. also it could hold object reference too.

```java
// declare Dog array variable
Dog[] pets;
// create Dog array variable
pets = new Dog[7];
// assign Dog object to elements of the array
pets[0] = new Dog;
```


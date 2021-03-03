[TOC]

# risky behavior

handling runtime errors.

```java
import javax.sound.midi.*;

public class MusicTest {
    public void play {
        try {
            Sequencer sequencer = MidiSystem.getSequencer();
            System.out.println("successfully got a sequencer");
        } catch (MidiUnavailableException ex) {
            System.out.println("gg manz");
        }
    }
    public static void main(String[] args) {
        MusicTest mt = new MusicTest();
        mt.play();
    }
}
```

is it necessary to know what error will be thrown in order to catch the runtime exception? no we can catch `Exception` as it the superclass of specific exceptions.

```java
// full loop
public void takeRisk() throws BadException {
    if (abandonedAllHope) {
        throw new BadException;
    }
}

public void run() {
    try {
        anObject.takeRisk();
    } catch (BadException ex) {
        System.out.println("gg manz");
        ex.printStackTrace;
    } finally {
        System.out.println("save anyway");
    }
}

// throwing multiple exceptions
public void takeRisk() throws BadException, FatalException {
    if (abandonedSomeHope) {
        throw new BadException;
    }
    if (abandonedAllHope) {
        throw new FatalException;
    }
}
// similar to catching single exception, we could just have multiple catch statements
```

exceptions are polymorphic, we could declare throwing a higher level / superclass exceptions and specify which to throw in the code and catch this superclass exception. we should order the catch block from specific exception to the more general exception. siblings can be in any order.

## ducking

if we are calling a risky method, compiler needs us to acknowledge it. but we can duck it by declaring that we are throwing exception even though we are not the one throwing but the one calling the method that might throw one.

```java
public class Washer {
    Laundry laundry = new Laundry();
    public void foo() throws ClothingException {
        laundry.doLaundry();
    }
    public static void main (String[] args) throws ClothingException {
        // if main doesnt throws exception it will not compile
        Washer a = new Washer();
        a.foo();
    }
}
```

how this works is basically when a method throws an exception the method is popped off the stack and exception is thrown to the next method down the stack - which is the caller. but if the caller is a ducker, it also pops off the stack immediately. this happens recursively until there is nothing left and JVM shuts down.

whoever calls something that throws exception need to catch or duck it.
[TOC]

# Make a connection

networking with sockets and multithreading. IP and TCP port number.

## client side

```java
import java.io.*;
import java.net.*; // for socket class
public class DailyAdviceClient {
    public void go() {
        try {
            Socket s = new Socket("127.0.0.1", 4242);
            InputStreamReader streamReader = new InputStreamReader(s.getInputStream());
            BufferedReader reader = new BufferedReader(streamReader);
            String advice = reader.readLine();
            System.out.println("Today you should: " + advice);
            reader.close();
        } catch(IOException ex) {
            ex.printStackTrace();
        }
    }
    public static void main(String[] args) {
        DailyAdviceClient client = new DailyAdviceClient();
        client.go();
    }
}
```

## server side

to accept / wait for client requests and broadcast. to example shown is single threaded.

```java
import java.io.*;
import java.net.*;
public class DailyAdviceServer {
    String[] adviceList = {"quit", "you will be rich", "nothing is worst that that", "you are worthy"};
    public void go() {
        try {
            ServerSocket serverSock = new ServerSocket(4242);

            while(true) {
                Socket sock = serverSock.accept();

                PrintWriter writer = new PrintWriter(sock.getOutputStream());
                String advice = getAdvice();
                writer.println(advice);
                writer.close();
                System.out.println(advice);
            }
        } catch(IOException ex) {
            ex.printStackTrace();
        }
    } // close go
    private String getAdvice() {
        int random = (int) (Math.random() * adviceList.length);
        return adviceList[random];
    }

    public static void main(String[] args) {
        DailyAdviceServer server = new DailyAdviceServer();
        server.go();
    }
}
```

## threading

```java
Thread t = new Thread();
t.start();
```

with this two lines of code we create a new Thread object (virtual thread) and launch a separate thread of execution with its own call stack and immediately dies as we are missing out the thread job. multithreading creates the illusion of handling multiple things at once by going back and forth between thread and call stacks.

### to launch a new thread

runnable is like a job and thread is like a worker. runnable holds the method that goes on the bottom of the new thread's stack: run(), this run function is the main entry point of the job.

### example

```java
public class MyRunnable implements Runnable {
    public void run() {
        go();
    }
    public void go() {
        doMore();
    }
    public void doMore() {
        System.out.println("top o’ the stack");
    }
}
class ThreadTestDrive {
    public static void main (String[] args) {
        Runnable threadJob = new MyRunnable();
        Thread myThread = new Thread(threadJob);
        myThread .start();
        System.out.println("back in main");
    }
```

once a thread becomes runnable, it can have 3 states, runnable, running and blocked. typically a thread moves back and forth between runnable and running as JVM thread scheduler selects which thread to run. thread scheduler can also move a running thread into a blocked state for a number of reasons including a thread might be executing code to read from a socket input stream but there is no data to read or a thread is waiting for a synchronous response.

## thread scheduler

there is no guarantee of the scheduler's scheduling and there is no api to control over it thus **never base our program's correctness on the scheduler working in a particular way**. same code same machine might yield different results. this does not conflict with the write once run everywhere motto, as the programmer must implement the code such that the result must be the same regardless of the scheduler's behavior. make the thread to `sleep` is a good way of guarantee it does not run for the specified duration.

the code block above might produce the following results,

```bash
>> java ThreadTestDrive
>> "back in main"
>> "top o’ the stack"
# or
>> java ThreadTestDrive
>> "top o’ the stack"
>> "back in main"
# run a couple times and observe the results
```

this is due to the scheduler's different scheduling, between the main stack or the runnable stack. it could go back and forth for each block (function eg. run, go , doMore etc) or multiple block.

### what happens when the thread finishes?

once thread run method has completed, we can't restart it anymore. the Thread class will no longer be a thread (v-thread) and will stay on the heap until GC. this is different from the idea of creating a thread pool, as we also don't restart threads from the pool.

### on sleep

to make threads take turn, we can put them to sleep periodically by calling the static sleep method which duration is in milliseconds.

```java
Thread.sleep(2 * 1000);
```

sleep method throws InterruptedException thus,

```java
try{
    Thread.sleep(2 * 1000);
} catch (InterruptedException ex) {
    ex.printStackTrace();
} // this is probably one of the useless code that dev have no choice to follow
```

with sleep we make the program **more** predictable not predictable.

### more threads and thread names

```java
public class RunThreads implements Runnable {
    public static void main(String[] args) {
        RunThreads runner = new RunThreads();
        Thread alpha = new Thread(runner);
        Thread beta = new Thread(runner);
        alpha.setName("Alpha thread");
        beta.setName("Beta thread");
        alpha.start();
        beta.start();
    }
    public void run() {
        for (int i = 0; i < 25; i++) {
            String threadName = Thread.currentThread().getName();
            System.out.println(threadName + " is running");
        }
    }
}
```

## threading issues - concurrency

concurrency issues introduce race conditions where multiple threads have access to single object's data.

```java
class BankAccount {
    private int balance = 100;

    public int getBalance() {
        return balance;
    }
    public void withdraw(int amount) {
        balance = balance - amount;
    }
}
public class RyanAndMonicaJob implements Runnable {
    private BankAccount account = new BankAccount();
    public static void main (String [] args) {
        RyanAndMonicaJob theJob = new RyanAndMonicaJob();
        Thread one = new Thread(theJob);
        Thread two = new Thread(theJob);
        one.setName("Ryan");
        two.setName("Monica");
        one.start();
        two.start();
    }
    private void makeWithdrawal(int amount) {
        if (account.getBalance() >= amount) {
            System.out.println(Thread.currentThread().getName() + " is about to withdraw");
            try {
                System.out.println(Thread.currentThread().getName() + " is going to sleep");
                Thread.sleep(500);
            } catch(InterruptedException ex) {ex.printStackTrace(); }
            System.out.println(Thread.currentThread().getName() + " woke up.");
            account.withdraw(amount);
            System.out.println(Thread.currentThread().getName() + " completes the withdrawl");
        }
        else {
            System.out.println("Sorry, not enough for " + Thread.currentThread().getName());
        }
    }
    public void run() {
        for (int x = 0; x < 10; x++) {
            makeWithdrawl(10);
            if (account.getBalance() < 0) {
                System.out.println("Overdrawn!");
            }
        }
    }
}
```

### introducing lock

lock ensures atomic transaction with keyword `synchronized`. what we are locking here essentially is the object itself not the method. if an object have two synchronized methods it means that you can't have two threads entering any of the synchronized methods.

```java
// modification needed
private synchronized void makeWithdrawal(int amount){}
```

### synchronized everything?

its not a good idea to synchronize everything, as it comes with a price and even worse deadlock problem. we can synchronize at a finer granularity.

```java
public void go() {
    doStuff();
    synchronized(this) {
        criticalStuff();
        moreCriticalStuff();
    }
}
```

### deadlock problem

a deadlock problem is where two threads holds the key of the subsequent key the other threads needs. if multithreading is a thing in our project read "Java Threads" by Scott Oaks and Henry Wong for design tips on avoiding deadlock

### static variable state

if we have 3 objects, JVM will create 4 keys 3 for each object and 1 for the class itself. thus if we synchronize a static method, JVM locks the class itself.
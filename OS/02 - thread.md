[TOC]

# Thread

basic unit of CPU utilization / programmed instruction that can be managed independently by scheduler. it has a set of program counter, stack, registers and thread ID, thus for multithreading in a single process say N threads, we will have N program counter, stack and so on. however there are stuffs that are shared within the same process including code, data, and opened files.

threading is useful for non-blocking tasks. take flask as an example (flask / python might not implement as such), for every request coming in a thread is created such that the app instance will handle the request and can still listen for new requests.

## 1. benefits

- responsiveness - non-blocking
- resource sharing - in single address space multiple tasks can be performed simultaneously (flask example)
- economy - multithreading overhead is lower compared to say, multiprocessing
- scalability - in multiprocessor architecture systems, multi-threaded application can split amongst available processors

## 2. thread of threads

### 2.1 Kernel Threads

each process consist of at least one kernel thread, if multiple threads exists within the same process they share memory and file resources (stack, registers, program counter and thread-local storage). kernel threads are preemtively multitasked if OS process schedule is also. they are relatively cheap to create, destroy and execute context switching. kernel can assign one thread to each logical core and can be swapped if it get blocked, however its slower than to swap out user threads

### 2.2 User Threads

sometimes implemented in userspace. kernel is unaware of them thus is scheduled and managed in userspace. no interaction with kernel during context switch thus is extremely efficient and is achieved by locally saving CPU registers used by the user thread to be executed. as the scheduling occurs in userspace, the scheduling policy can be more easily tailored to the requirements of the program's workload. using blocking system call can be problematic, and its blocking until the call returns by the kernel, thus starves other threads in the same process from executing. this is mitigated by implementing an interface that blocks the calling thread than the entire process.

## 3. types of parallelism

in practice its always hybrid

1. data parallelism: divides data amongst multiple threads (cores), and perform the same task on each subset of the data, similar to mapreduce.
2. task parallelism: divides different task to be performed among the different threads (cores) and performs them simultaneously.

## 4. multithreading models

there are two types of threads in modern system - user threads and kernel threads. user threads are supported above the kernel without kernel support and these are threads that programmers would put into their programs. kernel threads are supported within the kernel of the OS itself. modern OS supports kernel level threads, allowing kernel to perform multiple simultaneous tasks and / or to service multiple kernel system calls simultaneously. in theory we could map user threads to kernel threads using the following strategy.

### 4.1 Many(user)-To-One Model

thread management is handled by thread library in user space which is efficient (context switching is fast). however if a blocking system call is made, then **entire process** is blocked. because a single kernel thread can operates only on single CPU, it cannot utilize multiprocessing on multiple CPU.

### 4.2 One-To-One Model

overcomes blocking system calls and splits processes across multiple CPUs at the cost of overhead managing OTO model. most implementation limits on how many threads can be created.

### 4.3 Many-To-Many model

multiplexes any number of user treads onto an equal or smaller number of kernel threads, combining the best of both worlds. no restrictions on the number of threads created, no blocking system calls and multiple CPUs can be utilized. individual processes may be allocated to variable number of kernel threads depending on the number of CPU present and other factors.

## 5. Thread Safety

only applicable to multi-threaded code. a thread-safe code manipulates shared data structures such that all threads behave properly and fulfill their design spec without unintended interaction or when used by multiple threads regardless of how threads are executed, no additional coordination from the calling code. given single process multithreading threads shares same address space, establishing thread safety is done by synchronization (in short threads joined up or handshake at certain point to reach an agreement or commit to certain sequence of action).

### 5.1 strategy to avoid race condition and achieve thread safety

first strategy: avoiding sharing states

1. re-entrancy: code up such that all state are stored on local stack and non-local states is accessed through atomic operations. also it must be able to partially executed then resumed by **any** thread and yield same result. note re-entrancy itself is not thread-safety and thread-safety does not imply re-entrancy. 
2. thread-local storage: variable are localized and each thread has its own copy. these value are preserved across subroutine and other code boundaries, even its executed by another thread
3. immutable objects: state of object cannot be changed after construction. read-only data is shared, mutable operation can be implemented in such a way that new objects are created instead of modifying existing ones.

second strategy: synchronization-related and shared state is required

1. Mutex: access to shared data is serialized using mechanism to ensure only one thread read or write the data at any time. having side effects including deadlocks, livelocks and resource starvation
2. atomic operations: shared data is accessed by using atomic operations which cannot be interrupted by other threads. it forms basis of many thread locking mechanism and are used to implement mutex primitives.

### 5.2 thread safety levels

there could be scenario where concurrent reads are guaranteed to be thread-safety but concurrent writes are not..

- Thread safe - guaranteed to be free of race conditions when accessed by multiple threads simultaneously (single object)
- conditionally safe - different threads can access different object simultaneously, and access to shared data is protected from race conditions
- not thread safe - data structures should not be accessed simultaneously by different threads

### 5.3 deadlocks

a state where each member of a group waits for another member (including itself) to do some action (usually to release locks for process synchronization) and if no mechanism is implemented to detect / address deadlock the state will be lasted indefinitely.

#### 5.3.1 required condition to form deadlocks

"Coffman conditions"

1. mutual exclusion: there exists at least one resource held in non-sharable mode
2. resource holding: a process / thread is holding at least one resource and requesting for additional resource which is also being held up
3. no preemption: resource releasing can only be voluntarily
4. circular wait:

#### 5.3.2 handling deadlocks

- ignoring deadlocks - application of ostrich algorithm, is used when time intervals between occurrences of deadlocks are large and data loss incurred every time is tolerable. it can be safely done if deadlocks are formally proven to never occur or cost of prevention / detection is too high eg RTIC framework or if some deadlock happens every 10 years its easier to just reboot.
- detection - deadlocks are allowed and the system will examine if deadlock exists and handle accordingly
  - process termination - rollback and restart one or more process, this approach is certain and fast but overhead might be high as we rollback computations (if all are restarted). thus a workaround is to restart one process at a time until its resolved, still the overhead is high as we need to check deadlock state for every restart until resolved. enhancement eg age of process and priority could help to alleviate some of the overhead.
  - resource preemption - resources allocated to various processes may be successively preempted and allocated to other process until deadlock is broken.
- prevention - preventing one of the four Coffman conditions
  - removing mutex such that no process have exclusive access to resource, proven impossible for resources that cant be spooled (allow caching?). however for spooled resource deadlock can still occur. algorithm avoid mutex are call non-blocking synchronization algorithms
  - resource holding may be removed by requiring processes to request all the resource needed before starting. its difficult to know in advance resource needed and its inefficient. another approach is process can only request for resource if they have none, which might also be impractical because resource might be allocated and remain unused for long period of time. also process requiring popular resource may have to wait indefinitely, as resource may always be allocated to other processes causing resource starvation
  - no preemption might also be difficult or impossible as process has to have a resource for a certain amount of time (non-deterministic) else processing outcome might not be consistent. inability to enforce preemption may interfere with priority algorithm, preempt lock out resource generally implies rollback and significant overhead. algorithms that allow preemption including lock-free, wait-free algorithms and optimistic concurrency control.
- circular wait avoidance is achieved by disabling interrupts during critical sections and using hierarchy to determine partial ordering of resources. if no hierarchy exists, memory address of resource can be used to determine ordering and resources are requested in the increasing order of enumeration. Dijkstra's solution can also be used.

### 5.4 race condition

a condition where the system substantive behavior is dependent on the sequence or timing of other **uncontrollable** events, or in the case of threads (processes) its the sequence or timing of threads (processes). its difficult to reproduce as the result is non-deterministic.

## 6. Linux Thread

linux does not distinguish between processes and threads instead its referred to "tasks". a `fork()` syscall completely duplicates a task, and `clone()` allows for varying degrees of sharing between parent and child tasks controlled by flags. linux implements `task_struct` thus if no flag is specified the **resources** pointed to by the structure are copied, if flags are set, only the **pointers** to the resources are copied, hence resource sharing. (deep copy vs shallow copy)

## 7. Threading in python 3

## 8. reference materials

- https://web.mit.edu/6.005/www/fa14/classes/18-thread-safety/
- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/4_Threads.html
- https://docs.python.org/3/library/threading.html#

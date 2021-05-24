[TOC]

# Thread

basic unit of CPU utilization / programmed instruction that can be managed independently by scheduler. it has a set of program counter, stack, registers and thread ID, thus for multithreading in a single process say N threads, we will have N program counter, stack and so on. however there are stuffs that are shared within the same process including code, data, and opened files.

threading is useful for non-blocking tasks. take flask as an example (flask / python might not implement as such), for every request coming in a thread is created such that the app instance will handle the request and can still listen for new requests.

## benefits

- responsiveness - non-blocking
- resource sharing - in single address space multiple tasks can be performed simultaneously (flask example)
- economy - multithreading overhead is lower compared to say, multiprocessing
- scalability - in multiprocessor architecture systems, multi-threaded application can split amongst available processors

## Thread Safety

only applicable to multi-threaded code. a thread-safe code manipulates shared data structures such that all threads behave properly and fulfill their design spec without unintended interaction or when used by multiple threads regardless of how threads are executed, no additional coordination from the calling code. given single process multithreading threads shares same address space, establishing thread safety is done by synchronization (in short threads joined up or handshake at certain point to reach an agreement or commit to certain sequence of action).

### strategy for achieving thread safety (java)

1. confinement
2. immutability
3. thread safe data type

### thread safety levels

there could be scenarion where concurrent reads are guaranteed to be thread-safety but concurrent writes are not..

- Thread safe - guaranteed to be free of race conditions when accessed by multiple threads simultaneously (single object)
- conditionally safe - different threads can access different object simultaneously, and access to shared data is protected from race conditions
- not thread safe - data structures should not be accessed simultaneously by different threads

### deadlocks

a state where each member of a group waits for another member (including itself) to do some action (usually to release locks for process synchronization) and if no mechanism is implemented to detect / address deadlock the state will be lasted indefinitely.

#### required condition to form deadlocks

"coffman conditions"

1. mutual exclusion: there exists at least one resource held in non-sharable mode
2. resource holding: a process / thread is holding at least one resource and requesting for additional resource which is also being held up
3. no preemption: resource releasing can only be voluntarily
4. circular wait:

#### handling deadlocks

- ignoring deadlocks - application of ostrich algorithm, is used when time intervals between occurences of deadlocks are large and data loss incurred everytime is tolerable. it can be safely done if deadlocks are formally proven to never occur or cost of prevention / detection is too high eg RTIC framework or if some deadlock happens every 10 years its easier to just reboot.
- detection - deadlocks are allowed and the system will examine if deadlock exists and handle accordingly
  - process termination - rollback and restart one or more process, this approach is certain and fast but overhead might be high as we rollback computations (if all are restarted). thus a workaround is to restart one process at a time until its resolved, still the overhead is high as we need to check deadlock state for every restart until resolved. enhancement eg age of process and priority could help to alleviate some of the overhead.
  - resource preemption - resources allocated to various processes may be successively preempted and allocated to other process until deadlock is broken.
- prevention - preventing one of the four coffman conditions
  - removing mutex such that no process have exclusive access to resource, proven impossible for resources that cant be spooled (allow caching?). however for spooled resource deadlock can still occur. algorithm avoid mutex are call non-blocking synchronization algorithms
  - resource holding may be removed by requiring processes to request all the resource needed before starting. its difficult to know in advance resource needed and its inefficient. another approach is process can only request for resource if they have none, which might also be impractical

### race condition

## Threading in python 3

## reference materials

- https://web.mit.edu/6.005/www/fa14/classes/18-thread-safety/
- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/4_Threads.html
- https://docs.python.org/3/library/threading.html#

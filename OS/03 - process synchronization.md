[TOC]

# process synchronization

## 1. the critical-section problem

in the producer-consumer problem we sees an example of a critical section problem where in a number of cooperating processes, each of them has a critical section of code with the following conditions and terminologies,

- only one process in the group can be allowed to execute in their critical section at any one time. if one process is executing the critical section, other process need to wait until the first process has completed their critical section
- the code preceding the critical section which control access to the critical section is termed entry section, which acts like a carefully controlled locking door
- the code following the critical section is termed exit section, it generally releases the lock on someone else's door or broadcasts that they are no longer in the critical section
- the rest of the code which is not the critical, exit nor entry section is termed remainder section

thus a solution to the critical section problem must satisfy the following three conditions,

1. Mutex
2. Progress
3. Bounded Waiting

## 2. references

- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/5_Synchronization.html
[TOC]

# process synchronization

## 1. the critical-section problem

in the producer-consumer problem we sees an example of a critical section problem where in a number of cooperating processes, each of them has a critical section of code with the following conditions and terminologies,

- only one process in the group can be allowed to execute in their critical section at any one time. if one process is executing the critical section, other process need to wait until the first process has completed their critical section
- the code preceding the critical section which control access to the critical section is termed entry section, which acts like a carefully controlled locking door
- the code following the critical section is termed exit section, it generally releases the lock on someone else's door or broadcasts that they are no longer in the critical section
- the rest of the code which is not the critical, exit nor entry section is termed remainder section

thus a solution to the critical section problem must satisfy the following three conditions,

1. Mutex - only one process at a time can be executed in their critical section
2. Progress - if no process is currently executing their critical section, and one or more processes wants to execute their critical section, then only the processes not in their remainder section can participate in the decision, and the decision cannot be postponed indefinitely (processes cannot be blocked forever waiting to get their critical sections)
3. Bounded Waiting - there exists a limit as to how many other processes can get into their critical sections after a process requests entry into their critical section and before access is granted. (process request entro to their critical section will get a turn eventually and there is a limit as to how many other processes gets to go first)

we can only assume processes proceed at non-zero speed, but we cant assume about the relative speed of one process versus another. kernel process is also subjected to race conditions, which is an undesired behavior when updating commonly shared kernel data structure such as open file tables or virtual memory management, and it can be in one of two forms,

- non-preemtive kernels do not allow processes to be interrupted in kernel mode, which eliminates race conditions, but requires kernel mode operation to complete quickly, and can be problematic for real time systems as timing is not guaranteed
- preemtive kernels allow for real-time operations, but must be carefully written to avoid race conditions, especially tricky for SMP systems in which multiple kernel processes may be running simultaneously on different processors.

### 1.1 Peterson's solution

its not guaranteed to work on modern hardware due to the vagaries of load and store operations, but illustrated important concepts. the solution is based on two processes, P0 and P1, which alternated between their critical sections and remainder section. the solution requires two **shared** data items,

- int turn - to indicates whose turn is to enter the critical section, eg if turn == 1 the P1 is allowed
- boolean flag[2] - indicates when a processes wants to enter the critical section, eg when P1 wants to enter their critical section, it sets flag[1] to true

```pseudocode
do {
    flag[i] = TRUE;
    turn = j;
    while (flag[j] && turn == j) {
    	/* do nothing
    	   note flag[] is guaranteed, 
    	   its who gets to assign turn
    	   then the other process can execute their critical section;
    	   also do note that as long as flag or turn is evaluated false
    	   then process can proceed to critical section
    	*/
    }; 
    	/* critical section */
    flag[i] = FALSE;
    	/* ramainder section */
} while (TRUE);
```

proof of solution

- mutex - if one process is executing their critical section when other wishes to do so, the second process will become blocked by the flag of the first process. if both process attempts to enter at the same time, the last process to execute `turn = j` gets blocked.
- progress - each process can only be blocked while if the other process wants to use critical section (`flag[j] == TRUE`) and it is the other process's turn to use the critical section (`turn == j`). only both conditions are tru then the other process is allowed to enter the critical section, and upon exiting critical section `flag[j]` is set to false, releasing process `i`. the shared variable assures that only one process at a time can be blocked and the flag variable allows one process to release the other when exiting their critical section.
- bounded waiting - as each process enters their entry section, they set the turn variable to be the other processes turn. since no process ever sets it back to their own turn, this ensures that each process will have to let the other process go first at most one time before it becomes their turn again.

### 1.2 peterson's solution modern hardware limitation

modern hardware will try to improve system performance, processors and compilers by reordering read and write operations that have no dependencies. for single threaded application the reordering is immaterial as far as the program is concerned, however on multithreaded application with shared data the reordering of instructions may render inconsistent or unexpected results.

this may leads to P1 setting `turn = 2` then P2 sets `flag[2] = True` and `turn = 1` and proceeds to execute P2; if the reorder happens where now if P1 sets `flag[1] = True` both P1 and P2 will have their critical section executed simultaneously.

## 2. hardware synchronization

to generalize peterson's solution, each process when entering their critical section must set some **lock** to prevent other processes from entering their critical section simultaneously, and must release the lock when exiting their critical section to allow other processes to proceed. it must be possible to attain the lock only when no other processes has already set a lock. specifics implementation can be complicated and may include hardware solutions.

a simple solution to the critical section problem is to prevent a process from being interrupted while in their critical section which is the approach taken by non-preemtive kernels. this does not work well in multiprocessor environments, due to difficulties in disabling and re-enabling interrupts on all processors. there is also a question as to how this approach affects timing if the clock interrupt is disabled.

another approach is for hardware to provide certain *atomic* operations. these operations are guaranteed to operate as a single instruction without interruption. one of such operation is "Test and Set", which simultaneously sets a boolean lock variable and returns its previous value,

```pseudocode
boolean TestAndSet (boolean *target){
	boolean rv = *target;
	*target = TRUE;
	return rv
}
do {
	while (TestAndSetLock(&lock)) {
		/* do nothing
		*/
	}
	/* critical section */
	lock = FALSE;
	/* remainder section */
} while (TRUE);
/* we initialize lock as false */
```

or another variation,

```pseudocode
int CompareAndSwap(int *value, int expected, int newValue){
	int temp = *value;
	if (*value == expected){
		*value = newValue;
	}
	return temp;
}
do {
	while(CompareAndSwap(&lock, 0, 1) != 0){
		/* do nothing
		*/
	}
	/* critical section */
	lock = 0;
	/* remainder section */
} while (TRUE);
/* we initialize lock as 0 */
```

both examples satisfies mutual exclusion requirements but not guaranteed bounded waiting and order of the processes entering. its possible for a process to wait forever as theoretically its possible for a fast process to release lock and reacquire the lock before the slow process get a chance. a variation that satisfy this requirement is as shown below by using two shared data structures `boolean lock` and `boolean waiting[N]` where N is the number of processes in contention for critical sections,

```pseudocode
do {
	waiting[i] = TRUE;
	key = TRUE;
	while (waiting[i] && key){
		key = TestAndSet(&lock);
	}
	waiting[i] = FALSE;
	/* critical section */
	j = (i + 1) % n;
	while ((j != i) && !waiting[j]){
		j = (j + 1) % n;
	}
	if (j == i){
		lock = FALSE;
	} else {
		waiting[j] = FALSE;
	}
	/* remainder section */
} while (TRUE);
/* waiting array are initialized to false, and lock is initialized to 0 */
```

the key feature of the above algorithm is that the process blocks on the `AND` of the critical section being locked and that this process is in waiting state. when exiting a critical section, the exiting process does not just unlock the critical section and let the other process have a free-for-all trying to get in. rather it looks in an orderly progression (starting with the next process on the list) for a process that has been waiting, and if it finds one, then it releases that particular process from its waiting state without unlocking the critical the critical section, thereby allowing a specific process into the critical section while continuing to block others.

## 3. mutex locks

the hardware solution presented above are often difficult for ordinary programmers to access, particularly on multi-processor machine. therefore most system offers software API equivalent called mutex locks. one acquires a lock prior entering critical section and release it when exiting (both atomic)

```pseudocode
do{
	acquireLock();
	/* critical section */
	releaseLock();
	/* remainder section */
} while (TRUE);

acquireLock() {
	while (!available);
	/* busy wait */
	available = false;
}

releaseLock(){
	available = true;
}
```

as shown above is a busy loop used to block processes in acquire phase, and is referred to as spinlocks. spinlocks are wasteful of CPU cycles, especially for single-cpu single-threaded machines as its blocking until scheduler kicks the spinning process off the CPU. however it also doesn't incur overhead of context switch, thus is best for multi-threaded machines when it is expected that the lock is released after a short time.

## 4. semaphores

a more robust alternative to simple mutexes is to use semaphores, which are integer variables for which only two atomic operations are defined, the wait and signal operations shown below.

```pseudocode
wait(s){
	while s <= 0;
	/* no-op */
	s--;
}
signal(s){
	s++;
}
```

not that not only must the variable-changing steps (`s++` and `s--`) be indivisible, it is also necessary that for the wait operation when the test process false that there be no interruptions before `s` gets decremented, it is okay however for the busy loop to be interrupted when the test is true, which prevents the system from hanging forever.

### 4.1 using semaphore

#### 4.1.1 binary semaphores

takes 0 or 1 to solve the critical section problem above, and can be used as mutexes on system that do not provide separate mutex mechanism

```pseudocode
/* semaphore as mutex */
do {
	wait(mutex);
	/* critical section */
	signal(mutex);
	/* remainder section */
} while (TRUE);
```

#### 4.1.2 counting semaphores

can take on any integer and are used to count the number of remaining of some limited resource. the counter is initialized to the number of such resource available in the system and whenever the counting semaphore is greater than zero, then a process can enter a critical section and used one of the resources. when the counter gets to zero or negative depending on implementation, the the process blocks until another process frees up a resources and increments the counting semaphore with a signal call. if we want to ensure P1 executes S1 before P2 executes S2, we can do as such,

````pseudocode
/* in P1 */
S1;
signal(synch);
/* in P2 */
wait(synch);
S2;
/* initialize synch to zero, P2 will be block on the wait until after P1 executes signal */
````

#### 4.2 implementing semaphore

the semaphore implementation above still uses a busy loop in the wait call. an alternative is to block a process when it is forced to wait for an available semaphore, and swap it out of the CPU. in this implementation each semaphore needs to maintain a list of processes that are blocked waiting for it, such that one of the processes can be woken up and swap back into the CPU immediately or whether it needs to hang out in the ready queue for a while (determined by scheduler), and the implementation is as follow,

```c
/* semaphore structure */
typedef struct {
    int value;
    struct process *list;
} semaphore;

wait(semaphore *s){
    s -> value--;
    if (s -> value < 0){
        add_this_process_to_s -> list;
        block();
    }
}

signal(semaphore *s){
    s -> value++;
    if (s -> value <= 0){
        remove_a_process_P_from_s -> list;
        wakeup(p)
    }
}
```

this implementation the value of semaphore can actually be negative, which is the magnitude is the number of process waiting for that semaphore. this is a result of decrementing the counter before checking its value. the key of success of semaphores is that the wait and signal operation are atomic, no other process can execute a wait or signal operation on the **same semaphore** at the same time (its still possible to work with other semaphore) on single processors this can be implemented by disabling interrupts during the execution of wait and signal, multiprocessor system have to use more complex methods, including spinlocking.

#### 4.3 deadlocks and starvation

one important problem arises when using semaphores to block process waiting for a limited resource is the problem of deadlocks, which occurs when multiple processes are blocked, each waiting for a resource that can only be freed by one of the other blocked process. 

another problem is starvation in which one or more processes gets blocked forever, and never gets a change to take their turn in the critical section. if we did not specify the algorithms for adding processes to the waiting queue in the semaphore in the `wait()` call, or selecting one to be removed from the queue in the `signal()` call. if FIFO queue is chosen, then every process will eventually get their turn, but if a LIFO queue is implemented then first process to start could starve.

#### 4.4 priority inversion

a challenging scheduling problem arises when a high-priority process gets block waiting for a resource that is currently held by a low-priority process. if the low priority process gets preempted by one or more medium-priority process, then the high priority process is essentially made to wait for the medium priority process to finish before the low priority process can release the needed resource, causing priority inversion. and if there are enough medium priority processes, then the high priority process may be forced to wait for a very long time. one solution is to use priority-inheritance protocol where low-priority process holding a resource for which a high-priority process is waiting will temporarily inherit the high priority from the waiting process. this prevents medium-priority process from preempting the low priority process until it releases the resource, blocking the priority inversion problem.

## 5. classic problems of synchronization

classic problems are used to test virtually every new proposed synchronization algorithms

### 5.1 the bounded-buffer problem

the generalization of producer-consumer problem wherein access is controlled to a shared group of buffers of a limited size. in this solution, two counting semaphores "full" and "empty" keep track of the current number of full and empty buffers respectively (initialized to 0 and N respectively). the binary semaphore mutex controls access to the critical section (initialized to 1). the producer and consumer are nearly identical - one can think the producer as producing full buffers and consumer producing empty buffers,

```pseudocode
/* producer */
do {
	/* produce an item in nextp */
	wait(empty);
	wait(mutex);
	/* add nextp to buffer */
	signal(mutex);
	signal(full);
} while(TRUE);
/* consumer */
do {
	wait(full);
	wait(mutex);
	/* remove an item from buffer to nextc */
	signal(mutex);
	signal(empty);
	/* consume the item in nextc */
} while(TRUE);
```

### 5.2 the readers-writers problem

in the readers-writers problem there are some processes (termed readers) who only read shared and never change it; and there are other processes (termed writers) who may change the data in addition to or instead of reading it. there is no limit to how many readers can access the data simultaneously, but when a writer accesses the data, it needs exclusive access.

there are several variations to the reader-writers problem mostly centered around relative priorities of readers versus writers.

- the first readers-writers problem give priority to readers. if a reader wants to access the data, and there is not already a writer accessing it, the access is granted to the reader. however this could lead to starvation of the writers, as there could always be more readers coming along to access the data. writers are forced to wait until data is available, if it accompanied with a steady stream of readers, the readers will have the priority over writers
- the second readers-writers problem give priority to writers. when a writer wants to access to the data it jumps to the head of the queue - all waiting readers are blocked, and the writer gets access to the data as soon as it becomes available. on the opposite a steady stream of writers starves the readers.

## 6. monitors

## 7. examples

## 8. references

- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/5_Synchronization.html
[TOC]

# 1. process

is an instance of a program executed by one or more threads. it contains program code and its activity. a computer program contains a collection of instructions, and a process is the execution of those instruction after its being loaded from disk to memory. its possible to open up multiple instance of the same program and more often results in more than one process being executed.

multitasking is a method to allow multiple processes to share processors (CPU) and other system resources. each core executes a single task at a time. however multitasking allows each processor to switch context (preemption). a common form of multitasking is provided by CPU's time-sharing (method to interleacing the execution of user's / kernel processes and threads.

a computer system process consists of

- an image of the executable machine code associated with a program
- memory that includes executable code, process-specific data (stack), heap to hold intermediate computation data generated
- os descriptors of resources allocated to current process
- security attributes eg owner and permissions
- processor state eg registers and physical memory address

the OS holds most of the information about active processes in data structure called process control blocks. any subset of the resources may be associated with each process's threads in OS that supports threads or child processes. processes are isolated to reduce the likeliness of interfering each other and causing system failures. inter-process communication is possible.

## 1.1 time-sharing

## 1.2 process control blocks

stores process specific information

- process state
- process ID
- CPU registers and program counter
- CPU-scheduling information - eg priority infomation and pointers to scheduling queue
- memory management information
- accouting information
- IO status information

## 1.3 more on process memory

- executable code ia read from non-volatile storage when the program is launched
- data section stores global and static variables, allocated and initeialized prior to executing main
- the heap used for dynamic memory allocation to manage `new`, `malloc`, `free` and etc
- the stack is used for local variables, function return values and is reserved when they are declared; its freed up when variables go out of scope
- stack and heap starts from opposite ends within the process's free space, thus stack overflow or insufficient memory error

when processes is swapped out and later restored, additional information eg program counter and value of registers are required to be stored to allow restoring process.

## 1.4 process states

- new - process being created
- ready - process has all resources needed to run but CPU is not currently executing it's instruction
- running - the CPU is executing process's instruction
- waiting - process not running as it is waiting for some resource to become available or some event to happen
- terminated - process is completed

## 2. Process scheduling

main objective of process scheduling system is to keep CPU busy at all times and delever acceptable response time for all programs. its achieved by implementing suitable policies for swapping in and out CPU.

### 2.1 Scheduling queues

there are at least three of queues, job queue to store all processes, ready queue for processes in ready state and device queue is for processes waiting for a device's availability or device to deliver data. its possible for each device to have its own queue and other ques to be created.

### 2.2 preemptive scheduling

preemption is the act of temporarily interrupting an executing task with intention of running it later. the interruption is done by external scheduler with no assistance or cooperation from the task. its considered highly secured for each interruption and resuming also such change is known as context switching.

#### 2.2.1 kernel preemption

if not permitted to run to completion, it would tend to produce race condition resulting in deadlock. there is a tradeoff between removing preemptive behavior while processing and system responsiveness. also user mode and kernel mode determines privilege level within the system, and might be used to differentiate if a task is preemptable.

#### 2.2.2 preemptive multitasking

there exists cooperative multitasking where process or task must be explicitly programmed to yield (give up current running thread and add to queue) when they are not needed. its the scheduler determines what to execute next therefore all processes will get **some** amount of CPU time at any given time. this approach allows computer system to deal with important external events. at any specific time, processes are grouped into two category which either IO bound or CPU bound and its the IO bound tasks is blocked and allow to reprioritize other processes to utilize CPU.

#### 2.2.3 Time Slice

the length of time for which a process is allowed to run in preemptive multitasking system. the scheduler is run once every time slice to choose what's next to run. balance between system performance and process responsiveness is critical as scheduler might be consuming too much processing time or processes will take longer to respond. interruption allows OS kernel to switch between processes when the time slice expires allow processor time to be shared between tasks and giving the illusion that these tasks are in parallel.

### 2.3 scheduler

the method where work is assigned to resources to complete work, it could be virtual computation elements (threads, processes) to hardware resources (processors, network links). with scheduler its possible to multitask with single core CPU. a scheduler might have multiple conflicting goals: maximize throughput,minimize wait time, minimize latency, maximize fairness. we determine process scheduler by the frequency of the decisions.

#### 2.3.1 long-term scheduling

decides which processes to be admitted to the ready queue (main memory). it dictates what process to run on a system and the degree of concurrency to be supported at any given time. its the best interest to mix between IO bound and CPU bound processes else either the ready or waiting queue will be always empty. large scale system might deploy special scheduling software to prevent blocking due to waiting, eg batch processing mapreduce.

#### 2.3.2 medium-term scheduling

temporarily removes processes from main memory and ready queue to place them in secondary memory (hdd) or vice versa, or swapping in and out. usually it chooses process that are inactive for some time, having low priority, having page faulting frequently or process which takes up large amount of memory. in modern system medium-tier scheduler might actually perform the role of long-term scheduler, by treating binaries as "swapped-out processes" upon execution.

#### 2.3.3 short-term scheduling

decides which of the ready, in-memory processes to be executed by swapping process out of CPU after a clock interrupt, IO interrupt, OS syscall or other form of signal for every time slice.

#### 2.3.4 preemtive scheduler

on every time slice, it invokes an interrupt handler that runs in kernel mode and implement the scheduling function.

### 2.4 context switching

whenever in interupt arrives, CPU must do a state-save of the current process then switch to kernel mode to handle interupt and then do a state-restore. similarly for context switch, every time slice expires a new process is loaded from the ready queue. the states are information within process control blocks which are used for saving and restoring states.

### 2.5 Dispatcher

gives control of the CPU to the processes selected by short-term scheduler in kernel mode

- context switching where dispatcher saves the state (context) of process or thread and loads the initial or previous state of a new process
- switching to user mode
- jump to proper location in the program to restart / resume at the saved state

### 2.6 cooperative scheduling

context switch is never initiated until processes voluntarily yield control periodically or idling or logically blocked. thus a cooperative scheduler's role is reduced down to starting processes and letting them return control voluntarily. it widely used in embedded systems and also `await` languages with single-threaded event-loop in their runtime eg. JS and Python (?) it could potentially cause problem where a single process consumes all CPU time for itself, be it performing extensive computation or busy waiting, which hangs the system. we could alleviate this by using a watchdog timer.

### 2.7 scheduling algorithms

- FIFO
- Priority scheduling
- shortest remaining time first
- fixed priority preemptive scheduling
- round-robin scheduling
- multilevel queue scheduling
- work-conserving scheduling
- manual scheduling

## reference materials

- https://www.cs.uic.edu/~jbell/CourseNotes/OperatingSystems/3_Processes.html
- 

[TOC]

# Thread

basic unit of CPU utilization / programmed instruction that can be managed independently by scheduler. it has a set of program counter, stack, registers and thread ID, thus for multithreading in a single process say N threads, we will have N program counter, stack and so on. however there are stuffs that are shared within the same process including code, data, and opened files.

threading is useful for non-blocking tasks. take flask as an example (flask / python might not implement as such), for every request coming in a thread is created such that the app instance will handle the request and can still listen for new requests.

## benefits

- responsiveness - non-blocking
- resource sharing - in single address space multiple tasks can be performed simultaneously (flask example)
- economy - multithreading overhead is lower compared to say, multiprocessing
- scalability - in multiprocessor architecture systems, multi-threaded application can split amongst available processors


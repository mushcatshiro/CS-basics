[TOC]

# Asynchronous Python for the Complete Beginner

async is a style of doing concurrent programming (doing many things at once). in native python, we achieve that by, 

- creating multiple processes (multi-core concurrency) which the OS handles all the multi-tasking work
- creating multiple threads (with GIL limitation), which also relies on OS to handle the multi-tasking work
- async, no OS, one process one thread, sooooo what's the trick?

analogy - synchronous chess game and asynchronous chess game, both in a 1 vs 24 setting where the 1 takes 5 seconds for every move and the 24 takes 55 seconds to make their move. the prior will take 12 hours and the latter will take 1 hour if math is done correctly. in short its optimizing the 1's waiting time, which in CS context it is the CPU, we want it to wait the least amount of time.

## suspend and resume

- async function need to be able to suspend and resume
- when it enters a waiting period, it will only resume when the wait is over
- four ways to implement such behavior
  - callback functions
  - generator functions `yield`
  - async await
  - greenlets (greenlet package)

## scheduling (cooperative multitasking)

async frameworks need a scheduler, or event loop to decide which function gets the CPU next. essentially it keep track of all running tasks, whenever a function is suspended it returns control to the loop and the event loop finds another function to start or resume.

below shows multiple examples,

### sync

```python
import time

def sync_func():
    print('hello')
    time.sleep(3)
    print('world')

if __name__ == '__main__':
    sync_func()
```

### async with yield

```python
import asyncio
loop = asyncio.get_event_loop()

@asyncio.coroutine
def async_func_with_yield():
    print('hello')
    yield from asyncio.sleep(3)
    print('world')


if __name__ == '__main__':
    loop.run_until_complete(hello())
```

### async with await

```python
import asyncio
loop = asyncio.get_event_loop()

@asyncio
async def async_func_with_await():
    print('hello')
    await asyncio.sleep(3)
    print('world')


if __name__ == '__main__':
    loop.run_until_complete(hello())
```

### gevent / evenlet

```python
from gevent import sleep  # or from evenlet import sleep

def async_func():
    print('hello')
    time.sleep(3)
    print('world')

if __name__ == '__main__':
    async_func()
```

## pitfalls

due to the nature of having single thread, intensive CPU tasks must routinely release the CPU to avoid starvation. one of the approach is to sleep it periodically, and another would be to ask the loop to return control back as soon as possible with `await asyncio.sleep(0)`.

### python standard library

some library in python are designed to be blocking including,

- socket.*
- select.*
- subprocess.*
- os.waitpid
- threading.*
- multiprocessing.*
- time.sleep

thus check the async framework for the equivalent of these for a non-blocking alternative. alternatively, gevent and greenlet can monkeypatch to make it async compatible.

> asyncio is designed in mind for people to write and think asynchronously, unlike gevent and greenlet that still holds up to synchronous programming

|                          | Process       | Threads           | Async            |
| ------------------------ | ------------- | ----------------- | ---------------- |
| optimize waiting periods | y (preemtive) | y (preemtive)     | y (cooperative)  |
| use all CPU cores        | y             | n                 | n                |
| Scalability              | low (tens)    | medium (hundreds) | high (thousands) |
| Use blocking std lib     | y             | y                 | n                |
| GIL interference         | n             | some              | n                |

## reference

[link](https://www.youtube.com/watch?v=iG6fr81xHKA&ab_channel=PyCon2017)
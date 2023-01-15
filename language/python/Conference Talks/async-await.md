# Async... oh, wait (introduction to Async/Await)

```python
import asyncio

async def hello():
    print("hello")
    await asyncio.sleep(1)
    print("goodbye")

async def main():
    await hello()
    await hello()

asyncio.run(main())
```

despite the two `awaits` it is still ran sequentially. to really get two `hello`
and sleep for 1 second before the two `goodbye` we need to wrap it as such,

```python
... await asyncio.gather(hello(), hello())
```

if instead of using `asyncio.sleep` by using `time.sleep(1)`, sequentially
execution is presented. and if we `await` `time.sleep` we will get an error
something like `Type error: object NoneType cant be used in 'await' expression`.

## the basics

functions

```python
print("hello")
# hello
print(print(print))
# None
# 2nd print will print the print fn
# the outest print will print the result of the 2nd print
```

generators

```python
def generate_even_0(start, end):
    # will get slow as the range gets bigger
    numbers = []
    for i in range(start, end):
        if i%2 == 0:
            numbers.append(i)
    return numbers
            

def generate_even_1(start, end):
    # will not print the numbers by running print(generate_even_1(1, 100))
    # using next(generator_obj) or while True to print StopIteration Exception
    # is raised
    for i in range(start, end):
        if i%2 == 0:
            yield i


def loop(generators: List):
    # to handle situation where multiple generator object with differnt length
    while True:
        if not generators:
            return 0
        for i, g in enumerate(generators):
            try:
                print(next(g))
            except StopException:
                del generators[i]
```

## back to the hello example

```python
import time

def asleep(seconds):
    start = time.time()
    while time.time() - start < 2:
        yield

def hello():
    print("hello")
    ## solution 1
    # yield
    ## solution 2
    # start = time.time()
    # while time.time() - start < 2:
    #     yield
    ## solution 3
    # yield asleep(2)
    ## solution 4
    # yield from asleep(2)
    time.sleep(1)
    print("goodbye")


def loop(generators: List):
    while True:
        if not generators:
            return 0
        for i, g in enumerate(generators):
            try:
                print(next(g))
            except StopException:
                del generators[i]
```

it runs sequentially and hist the error `TypeError: 'NoneType' object is not an iterator`
by adding a `yield` before `time.sleep` it now runs without error and behaves
as expected, two `hello`s, sleep and two `goodbye`s. however with only a tiny
difference, there is a sleep for 2 seconds between the `goodbye`s. by changing
to solution 2, it fixes the problem. solution 3 prints everything in rapid
succession wihout sleeping, because the `yield` in `hello()` yields a generator
instead. by using `yield from` it works again.


```python
import asyncio

async def main():
    await asyncio.gather(hello(), hello())

asyncio.run(main())
```

it still works as solution 4. how to extrapolate to any packages? is it needed
to re-implement everything? yes.

```python
import time
import threading

def hello():
    print("hello")
    sleep(1)
    print("goodbye")

def main():
    thread_1 = threading.Thread(target=hello)
    thread_2 = threading.Thread(target=hello)
    thread_1.start()
    thread_2.start()
```

using threads somehow appears to solve the problem however, threads have no way
to know where exactly to `sleep`. thread switching may happen anywhere in the
`hello` function. with python's GIL limitation, no two threads can run at the
same time. threads might be more suitable for network requests which requests
are made almost at the same time.

## Threads, Multiprocessing and Asyncio

```python
import threading
import multiprocessing
import asyncio
import time

def hello()
    time.sleep(3)

def snap(f):
    return f()

async def ahello():
    await asyncio.sleep(3)

def t_main():
    threads = [threading.Thread(target=hello) for _ in range(4000)]
    start = time.time()
    for thread in threads:
        thread.start()
    for threads in threads:
        thread.join()
    print(time.time()-start)

def m_main()
    with multiprocessing.Pool() as pool:
        start = time.time()
        pool.map(snap, [hello for _ in range(4000)])
    print(time.time()-start)

async def a_main():
    tasks = [ahello() for _ in range(4000)]:
    start = time.time()
    await asyncio.gather(*tasks)
    print(time.time()-start)
```

> note excluding processes creation time

for `a_main` it finishes in ~3 seconds; `t_main` finishes after 4.3 seconds,
which takes a little longer due to the thread creation process (memcp); `m_main`
is a little different from threads variant, it start 4000 python instances. it
took quite some time. why miltiprocessing in python if it is comparable to
threads? by replacing the `hello` function to,

### http request

```python
# run 200 not 4000
import requests
import aiohttp

def hello():
    with requests.Session() as s:
        s.get("https://google.com")

async def a_hello():
    async with aiohttp.ClientSession() as s:
        await s.get("https://google.com")
```

> note run the code above at your own risk, ddos on google will have its
> consequences

`a_main` finishes under 1 second; `t_main` runs in 5 seconds; `m_main` finishes
in 4 seconds.

### is prime

```python
# run 5 not 4000
def is_prime(n):
    for i in range(number-1, 0, -1):
        if number % i == 0:
            return True
    return False

async def ahello():
    await asyncio.sleep(1)
    is_prime(16769823)

def hello():
    time.sleep(1)
    is_prime(16769823)
```

`ahello` takes 6 seconds, the sleep happen simultaneously and a blocking function
which runs sequentially. `hello` with `t_main()` also takes more or less similar
duration. `hello` with `m_main` results in 3 seconds, including the creation of
processes.

### mixing http request and isPrime

```python
async def ahello():
    is_prime(16769823)
    async with aiohttp.ClientSession() as s:
        results = await asyncio.gather(
            *[s.get("https://google.com") for _ in range(10)]
        )
        print([(await r.text())[:20] for r in results])
    is_prime(16769823)

def hello():
    is_prime(16769823)
    with requests.Session() as s:
        results = [
            s.get("https://google.com") for _ in range(10)
        ]
        print([(r.text())[:20] for r in results])
    is_prime(16769823)
```

`ahello` takes 13 seconds, `hello` with threads takes 13 seconds, `hello` with
multiprocessing takes 5 seconds (with 10 processors). however what if the
requests increases to 100?

## conclusion

`asyncio` is great for heavy IO operations but not great for cpu bound task.
cpu bound task is great for multiprocessing. to further improve performance by
combining `asyncio` with multiprocessing,

```python
def is_prime(n):
    for i in range(number-1, 0, -1):
        if number % i == 0:
            return True
    return False

async def ahello():
    is_prime(16769823)
    async with aiohttp.ClientSession() as s:
        results = await asyncio.gather(
            *[s.get("https://google.com") for _ in range(10)]
        )
        print([(await r.text())[:20] for r in results])
    is_prime(16769823)

def _main(coroutine):
    asyncio.run(coroutine())


async def main():
    start = time.time()
    with multiprocessing.Pool(5) as pool:
        for _ in pool.map(_main, [ahello for _ in range(5)]):
            pass
    print(time.time() - start)
```

this results in 4.5 seconds.

### cats

```python
class SyncCat:
    def exists(self):
        self._eat()
        self._have_free_time()
    
    def _eat(self):
        print("eat")
    
    def _have_free_time(self):
        print("have free time")
        self._sleep()
    
    def _sleep(self):
        print("sleeping")
        time.sleep(2)
        print("wake")

class AsyncCat(SyncCat):
    async def exists(self):
        self._eat()
        await self._have_free_time()
    
    async def _have_free_time(self):
        print("have free time")
        await self._sleep()
    
    async def _sleep(self):
        print("sleeping")
        await asyncio.sleep(2)
        print("wake")

cats = [AsyncCat() for _ in range(5)]

async def main(cats):
    await asyncio.gather(*[cat.exists() for cat in cats])

asyncio.run(main(cats))
```

the example above assume the code is easy and can be modified easily. in cases
where the `_have_free_time` is much complicated? i.e. more code, compiled C and
etc. the workaround would be introducing threads with a limitation for IO bound
tasks improvements. it is also a cheap hack for laziness.

```python
class AsyncCat(SyncCat):
    async def exists(self):
        self._eat()
        loop = asyncio.get_event_loop()
        # `None` here is a threadpool executor
        await loop.run_in_executor(None, self._have_free_time)
    
    def _have_free_time(self):
        # inherited code without modification
        ...
    
    def _sleep(self)
        # inherited code without modification
        ...
    
    def _eat(self):
        # inherited code without modification
        ...

async def main():
    cats = [AsyncCat() for _ in range(5)]
    await asyncio.gather(*(cat.exists() for cat in cats))

asyncio.run(main())
```

basically learn everything and use the appropriate tool for the appropriate
situation.

## reference and further readings

- [link](https://www.youtube.com/watch?v=VTl9WNP7GCU&ab_channel=CodingTech)
- John Reese "what is coroutine anyway?"
- John Reese "thinking outside of the GIL"
- Raymond Hettinger "thinking about concurrency"
- Yury Selivanov "asyncio in python 3.7 and 3.8"
- Andrew Svetlov "asyncio pitfals"
- Lukasz Langa "asyncio and music"
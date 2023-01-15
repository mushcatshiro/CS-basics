# Thinking Outside the GIL with AsyncIO and Multiprocessing

## What's GIL?

- global interpreter lock
- one VM thread at a time
- no concurrent memory access
- I/O wait releases lock

to achieve high performance on modern python service. the service is a stateful monitoring service that gathers ~100M data points, process and aggregate anomalies to store and alarm users, requires to be able to add new features easily, to be deployed easily and have few dependencies.

starts out with single binary per server, app in three phases, gather all data, process and aggregate results. using thread pool to control I/O concurrency. does not scale well as data get larger to read everything in-memory, but underutilizing CPU due to GIL limitation.

## what can be done?

1. moving to py3 (~45% memory saving and ~20% runtime reduction)
2. sharding and scales with the number of workers but trading off with complicated deployments and communication overhead
3. multiprocessing which scales with CPU cores (builtin IPC) but still one task per process, how python copy-on-write/ref count works (memory duplication) and I/O heavy is generally not benefitting from multiprocessing compared to other alternatives
4. AsyncIO is faster than threads with massive I/O concurrency however still limited by GIL and coroutines can timeout before started executing as queue gets too long

```python
async def fetch_url(url):
    return await aiohttp.request("GET", url)  # executed when it is awaited

async def fetch_multi(url1, url2):
    future1 = fetch(url1)  # not executed a future object is returned
    future2 = fetch(url2)
    a, b = await asyncio.gather(future1, future2)
    return a, b
```

> to use multiprocessing + asyncio

```python
async def run_loop(inp):
    pass

def bootstrap(inp):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_loop(inp))

def main():
    p = multiprocessing.Process(
        target=bootstrap,
        args=(inp,)
    )
    p.start()
```

### further optimizations and considerations

- multiple work queues
- combine tasks into batches
- use spawned processes

- minimize pickling
- prechunk work items
- aggregate results in the child
- use map/reduce

## Reference

[youtube video link](https://www.youtube.com/watch?v=0kXaLh8Fz3k&ab_channel=PyCon2018)
[aiomultiprocess](https://github.com/omnilib/aiomultiprocess)
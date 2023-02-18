import os

import redis
from rq import Worker, Queue, Connection


if __name__ == "__main__":
    name = os.environ.get("CLIENTNAME")
    redis_connection = redis.from_url("redis://redis:6379/0")
    with Connection(redis_connection):
        queue = Queue()
        Worker(queue, name=f"worker{name}").work()
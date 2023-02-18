import os

# import redis
from redis import Redis
from rq import Worker, Queue, Connection, use_connection


if __name__ == "__main__":
    name = os.environ.get("CLIENTNAME")
    # redis_connection = redis.from_url("redis://redis:6379/0")
    with Connection(Redis(host="redis", port=6379, db=0)):
        queue = Queue()
        Worker(queue, name=f"worker{name}").work()

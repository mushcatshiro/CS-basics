from flask import Flask, request, jsonify, g
from rq import Queue, push_connection
import redis
from bichar import bichar

app = Flask(__name__)


def get_redis_connection():
    redis_connection = getattr(g, '_redis_connection', None)
    if redis_connection is None:
        redis_url = "redis://redis:6379/0"
        redis_connection = g._redis_connection = redis.from_url(redis_url)
    return redis_connection

@app.before_request
def push_rq_connection():
    push_connection(get_redis_connection())

@app.route("/add", methods=["POST"])
def add():
    args = request.json
    q = Queue()
    q.enqueue(bichar, args["target"])
    return jsonify({"response": "task added!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0")
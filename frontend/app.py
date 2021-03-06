from myworker import workerfunc
from flask import Flask
from redis import Redis
from rq import Queue

app = Flask(__name__)
redis = Redis(host="redis", port=6379)
q = Queue(connection=redis)


@app.route('/')
def hello():
    redis.incr('hits')
    hits = redis.get('hits')
    q.enqueue(workerfunc, hits)
    return 'Hello duckface! I have been seen %s times.' % hits


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

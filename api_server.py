from flask import Flask, request
import redis
import json

app = Flask(__name__)

def connect_to_redis():
    r = redis.Redis(host='redis-17437.c284.us-east1-2.gce.cloud.redislabs.com', port=17437, db=0, password='gT9vj4LvMCmCah0TNYk4eaU5lWK9deXj')
    return r

@app.route('/submit', methods=['POST'])
def submit_job():
    r = connect_to_redis()
    code_to_run = request.json.get("code")
    if code_to_run:
        r.rpush('job_queue', code_to_run)
        return json.dumps({"status": "submitted"}), 200
    else:
        return json.dumps({"status": "error", "message": "No code provided"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import redis
import subprocess
import time
import socket
import json

def connect_to_redis():
    r = redis.Redis(host='redis-17437.c284.us-east1-2.gce.cloud.redislabs.com', port=17437, db=0, password='gT9vj4LvMCmCah0TNYk4eaU5lWK9deXj')
    return r

def execute_job(job):
    try:
        result = subprocess.check_output(job, shell=True)
    except Exception as e:
        result = str(e)
    return result

def register_node(r, node_info):
    r.hset("nodes", socket.gethostname(), json.dumps(node_info))

def send_heartbeat(r):
    r.hset("heartbeat", socket.gethostname(), int(time.time()))

def main():
    r = connect_to_redis()
    node_info = {
        "cpu": "x86_64",  # Placeholder, replace with real CPU info
        "memory": "16GB"  # Placeholder, replace with real memory info
    }

    register_node(r, node_info)

    while True:
        send_heartbeat(r)
        _, code_to_run = r.blpop("job_queue")
        result = execute_job(code_to_run)
        print(f"Task executed: {code_to_run}")
        r.rpush("result_queue", result)
        time.sleep(1)  # 1-second sleep to simulate work, remove in production

if __name__ == '__main__':
    main()

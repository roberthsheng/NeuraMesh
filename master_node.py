import redis
import json
import time

def connect_to_redis():
    r = redis.Redis(host='redis-17437.c284.us-east1-2.gce.cloud.redislabs.com', port=17437, db=0, password='gT9vj4LvMCmCah0TNYk4eaU5lWK9deXj')
    return r

def get_registered_nodes(r):
    return {k.decode(): json.loads(v.decode()) for k, v in r.hgetall("nodes").items()}

def check_heartbeats(r):
    heartbeats = {k.decode(): int(v.decode()) for k, v in r.hgetall("heartbeat").items()}
    for node, last_beat in heartbeats.items():
        if time.time() - last_beat > 5:
            print(f"Node {node} is down.")

def collect_results(r):
    return [res.decode() for res in r.lrange("result_queue", 0, -1)]

def main():
    r = connect_to_redis()
    while True:
        registered_nodes = get_registered_nodes(r)
        print(f"Registered nodes: {registered_nodes}")

        check_heartbeats(r)

        results = collect_results(r)
        print(f"Aggregated Results: {results}")
        time.sleep(2)

if __name__ == '__main__':
    main()

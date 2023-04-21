import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
# pubsub.subscribe('crime', 'politics')
pubsub.subscribe('robbery')

for message in pubsub.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])
        print(data)
        # print(f"Received message on topic {message['channel']} with key {message['data']}: {data['message']}")
        # r.lrem(message['channel'], 1, message['data'])
import redis
import json
import requests

r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
# pubsub.subscribe('crime', 'politics')
pubsub.subscribe('robbery')
endpoint_url = "http://127.0.0.1:9000//ner"

def query_ner_model(news_text):
    payload_json = {
            'text': news_text['content']
        }

    response = requests.post(endpoint_url, headers={'Content-Type':'application/json'}, json=payload_json)
    locations = print(response.json())
    return locations

for message in pubsub.listen():
    if message['type'] == 'message':
        # dict containing 3 keys: link, published, content
        news_dict = json.loads(message['data'])
        news_text = news_dict['content']
        
        locations = query_ner_model(news_text)
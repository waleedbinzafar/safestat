from ParseFeed import *
import yaml
from yaml import Loader
import json

if __name__=="__main__":
    f = open("sources.yml", 'r')
    conf = yaml.load(f,Loader=Loader)
    sources = conf['sources']

    redis_queue = redis.Redis(host='localhost', port=6379, db=0)
    # read the topics from the yaml file; these are news tags
    topics = [topic for topic in sources]

    for topic in topics:
        # Looping over all topics/tags, get the different RSS sources from yaml 
        topic_sources = sources[topic]

        # create the feed parser object for each RSS feed
        topic_feeds = [ParseFeed(topic_sources[source], source, watchword=topic) for source in topic_sources]
        
        for feed in topic_feeds:
            # get new events for each RSS feed
            new_events = feed.fetch_feed()
            if len(new_events)>0:
                for event in new_events:
                    # publish new events to the message queue
                    redis_queue.publish(topic, json.dumps(event))
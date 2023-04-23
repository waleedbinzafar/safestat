import redis
import feedparser
import re

class ParseFeed:
    def __init__(self, url, source='', watchword='rape'):
        self.url = url
        self.source = source
        self.cache = RedisCache()
        self.watchword = watchword
    
    def fetch_feed(self):
        # fetch and parse the RSS feed using feedparser
        feed = feedparser.parse(self.url)
        self.new_events = []
        for entry in feed.entries:
            match = re.search(self.watchword, entry["content"][0]["value"], re.IGNORECASE)
            if match:
                self.add_event(entry)

        return self.new_events
                
    def add_event(self, entry):
        # check redis cache
        if not self.cache.check_cache(entry.link):
            self.cache.add_to_cache(entry.link, entry.published)
            self.new_events.append({"link": entry.link, "published": entry.published, "content":entry.content[0]["value"], "tag":self.watchword})
            print(entry.link)
        else:
            print("Already exists:", entry.link)
        
    def __str__(self):
        return self.source+" parser"

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0, expiry=10):
        self.redis = redis.Redis(host=host, port=port, db=db)
        self.expiry = expiry

    def check_cache(self, key):
        # check if key exists in the Redis cache
        return self.redis.exists(key)

    def add_to_cache(self, key, val='added'):
        # add key to the Redis cache with a 24-hour expiry time
        self.redis.set(key, val, ex=self.expiry)
        print("Added to cache")
        
    def delete_from_cache(self, key):
        self.redis.delete(key)
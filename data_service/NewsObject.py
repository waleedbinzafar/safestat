import requests

class NewsObject:
    def __init__(self, news_dict, ner_model_url, db=None) -> None:
        self.link = news_dict['link']
        self.published = news_dict['published']
        self.news_text = news_dict['content']
        self.ner_model = ner_model_url
        self.paras = self.news_text.split('\n')
        self.tag = news_dict['tag']
        self.db = db

    def query_ner_model(self):
        for para in self.paras:
            payload_json = {
                    'text': para
                }

            response = requests.post(self.ner_model, headers={'Content-Type':'application/json'}, json=payload_json)
            self.locs = response.json()
            if len(self.locs)==1 and self.locs[0]=="":
                self.locs=[]
            if len(self.locs)>0:
                break

    def store_to_db(self):
        # Only store if there is a valid DB object
        if self.db:
            # Insert if tag not in DB
            if not self.db.entity_exists('tag', self.tag):
                self.db.insert_tag(self.tag)

            # insert if locs not in DB
            for loc in self.locs:
                if not self.db.entity_exists('loc', loc):
                    self.db.insert_loc(loc)

            if len(self.locs)>0:
                # insert if crime not in DB and if there's a valid location
                if not self.db.entity_exists('crime', self.link):
                    text = self.paras[0]
                    if len(text)>200:
                        text = text[:200]
                    self.db.insert_crime(self.link, self.published, self.tag, text)

                    for loc in self.locs:
                        self.db.insert_loc_crime(self.link, loc)

                    print("Crime written to DB")
        else:
            print('No DB attached')
import redis
import json
from NewsObject import NewsObject
from db_utils import SafeStatDB

r = redis.Redis(host='localhost', port=6379, db=0)
pubsub = r.pubsub()
# pubsub.subscribe('crime', 'politics')
pubsub.subscribe('robbery', 'rape', 'terrorist')
endpoint_url = "http://127.0.0.1:9000//ner"
news_dict = {'link': 'https://tribune.com.pk/story/2410325/gold-shop-safe-cracker-held', 'published': 'Thu, 06 Apr 23 19:52:46 +0500', 'content': 'The mastermind of a robbery at a jewellery shop in the Feroza area five months back has been found jailed in another case in Chakwal.\n\nAccording to the police, the suspect, Baba Allah Ditta, had been a resident of Sahiwal and Faisalabad and was wanted in cases registered in several police stations. Eight robbers armed with modern weapons had stolen a safe during a robbery at the jewellery shop in Madni Bazaar in Feroza early in the morning on November 1 last year. It was reported that there was a big quantity of gold, silver, cash, cheque books and other documents worth about Rs15 million in the safe. \n\nThe robbers also kidnapped a hotel owner going for Fajr prayers in the local mosque, Hafiz Abu Bakr. However, they released him from their vehicle after snatching his mobile phone.\n\nAn official said that the police had later arrested a gang member, Nadeem Shahzad, from Faisalabad, who made revelations during interrogation about crimes committed across the country. On the basis of his statement, the Pakka Laran police arrested 65-year-old Allah Ditta, the suspected gang leader, and obtained his remand from Chakwal.\n\nA police official said the the suspected gang leader had made revelations regarding robberies across the country and he was considered an expert in breaking open iron safes in goldsmith shops in Punjab, Sindh, Khyber-Pakhtunkhwa and Azad Kashmir.\n\nPublished in The Express Tribune, April 7th, 2023.'}
safestatdb = SafeStatDB()
for message in pubsub.listen():
    if message['type'] == 'message':
        # dict containing 3 keys: link, published, content
        news = NewsObject(json.loads(message['data']), endpoint_url, safestatdb)
        news.query_ner_model()
        news.store_to_db()
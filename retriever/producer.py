from kafka import KafkaProducer
import json

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
             bootstrap_servers=['localhost:9092'],
             value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce(self, data):
            for item in data:
                if item["Antisemitic"]:
                    topic_name = 'raw_tweets_antisemitic'
                else:
                    topic_name = 'raw_tweets_not_antisemitic'
                item["_id"] = str(item["_id"])
                item["CreateDate"] = item["CreateDate"].isoformat()
                self.producer.send(topic_name,item)
            self.producer.flush()
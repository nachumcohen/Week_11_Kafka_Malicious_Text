from kafka import KafkaProducer
import json

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
             bootstrap_servers=['kafka:9093'],
             value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce(self, tweet):
        if tweet["Antisemitic"]:
            topic_name = 'enriched_preprocessed_tweets_antisemitic'
        else:
            topic_name = 'enriched_preprocessed_tweets_not_antisemitic'
        self.producer.send(topic_name,tweet)
        self.producer.flush()
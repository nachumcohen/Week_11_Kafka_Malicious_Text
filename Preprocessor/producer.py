from kafka import KafkaProducer
import json


class Producer:

    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers="localhost:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def push_preprocessed_tweets_antisemitic(self,msg):

        self.producer.send("preprocessed_tweets_antisemitic", value=msg)
        self.producer.flush()


    def push_preprocessed_not_tweets_antisemitic(self,msg):

        self.producer.send("preprocessed_tweets_not_antisemitic", value=msg)
        self.producer.flush()
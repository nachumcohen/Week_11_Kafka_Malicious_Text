from kafka import KafkaProducer
import json

class Producer:

    def __init__(self):

        self.producer = KafkaProducer(
            bootstrap_servers="kafka:9093",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def push_preprocessed_tweets_antisemitic(self, msg):

        # Send processed antisemitic tweet to the 'preprocessed_tweets_antisemitic' topic
        self.producer.send("preprocessed_tweets_antisemitic", value=msg)
        self.producer.flush()  # Ensure message is actually sent

    def push_preprocessed_not_tweets_antisemitic(self, msg):

        # Send processed non-antisemitic tweet to the 'preprocessed_tweets_not_antisemitic' topic
        self.producer.send("preprocessed_tweets_not_antisemitic", value=msg)
        self.producer.flush()  # Ensure message is actually sent

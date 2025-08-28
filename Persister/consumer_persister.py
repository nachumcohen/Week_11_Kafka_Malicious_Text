import threading
from pymongo import MongoClient
from kafka import KafkaConsumer
import json

# Connect to local MongoDB instance and select the database
client = MongoClient("mongodb://localhost:27017/")
db = client["tweets_db"]


class TweetPersister:

    def persist_tweet(self, name_topic, collection_name: str):

        # Consume messages from a Kafka topic and insert them into a MongoDB collection
        consumer = KafkaConsumer(
            name_topic,
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id=f"topic_{name_topic}",
            enable_auto_commit=True
        )

        for message in consumer:
            msg = message.value
            interesting_collection = db[collection_name]

            # Insert each message into MongoDB, ignore errors [duplicates]
            try:
                interesting_collection.insert_one(msg)
            except Exception as e:
                print(e)
                pass

    def consume_tweets_antisemitic(self):

        #Consumer for antisemitic tweets
        self.persist_tweet("enriched_preprocessed_tweets_antisemitic", "tweets_antisemitic")

    def consume_not_tweets_antisemitic(self):

        # Consumer for non-antisemitic tweets
        self.persist_tweet("enriched_preprocessed_tweets_not_antisemitic", "tweets_not_antisemitic")

    def start_consumers(self):

        # Start two separate threads to consume both topics concurrently

        t1 = threading.Thread(target=self.consume_tweets_antisemitic)
        t2 = threading.Thread(target=self.consume_not_tweets_antisemitic)

        t1.start()
        t2.start()

        t1.join()
        t2.join()

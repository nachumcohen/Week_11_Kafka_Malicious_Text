import threading
from kafka import KafkaConsumer
import json
from clean.cleaner import Cleaner
from producer import Producer


class TweetConsumer:

    def __init__(self):
        self.producer = Producer()

    def process_tweets(self ,topic_name, push_method):
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id=f"group_{topic_name}",
            enable_auto_commit=True
        )
        clean_text = Cleaner()
        for message in consumer:
            msg = message.value
            msg["clean_text"] = clean_text.get_clean_text(msg["text"])
            print(msg)
            push_method(msg)


    def push_antisemitic(self, msg):
        self.producer.push_preprocessed_tweets_antisemitic(msg)

    def push_not_antisemitic(self, msg):
        self.producer.push_preprocessed_not_tweets_antisemitic(msg)

    def start_consumers(self):
        t1 = threading.Thread(target=self.process_tweets, args=("raw_tweets_antisemitic", self.push_antisemitic))
        t2 = threading.Thread(target=self.process_tweets, args=("raw_tweets_not_antisemitic", self.push_not_antisemitic))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

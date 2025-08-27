import threading
from kafka import KafkaConsumer
import json
from clean.cleaner import Cleaner
from producer import Producer


class TweetConsumer:
    def __init__(self):
        self.producer = Producer()

    @staticmethod
    def process_tweets(topic_name, push_method):
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers="localhost:9092",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id=f"group_{topic_name}",
            enable_auto_commit=True
        )

        for message in consumer:
            msg = message.value
            clean_text = Cleaner(msg["text"])
            clean_text.remove_punctuation()
            clean_text.remove_special_marks()
            clean_text.remove_whitespace()
            clean_text.remove_stopwords()
            clean_text.text_to_lower()
            clean_text.lemma_words()

            msg["clean_text"] = clean_text.return_self_text()
            push_method(msg)
            print(msg)


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


T = TweetProcessor()
T.start_consumers()
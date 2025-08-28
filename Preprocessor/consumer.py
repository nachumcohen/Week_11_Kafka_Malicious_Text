import threading
from kafka import KafkaConsumer
import json
from clean.cleaner import Cleaner
from producer import Producer


class TweetConsumer:

    def __init__(self):

        # Initialize a Producer instance for pushing processed tweets
        self.producer = Producer()

    def process_tweets(self, topic_name, push_method):

        # Consume messages from a Kafka topic, clean the text, and push processed message.
        consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers="kafka:9093",
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
            group_id=f"group_{topic_name}",
            enable_auto_commit=True
        )

        clean_text = Cleaner()  # Cleaner instance to process tweet text

        for message in consumer:
            msg = message.value
            # Clean the text and add a new key 'clean_text'
            msg["clean_text"] = clean_text.get_clean_text(msg["text"])
            print(msg)
            # Push the processed message using the specified method
            push_method(msg)

    def push_antisemitic(self, msg):

        # Send processed antisemitic tweet to the Producer
        self.producer.push_preprocessed_tweets_antisemitic(msg)

    def push_not_antisemitic(self, msg):

        # Send processed non-antisemitic tweet to the Producer
        self.producer.push_preprocessed_not_tweets_antisemitic(msg)

    def start_consumers(self):

        # Start two threads to consume and process both antisemitic and non-antisemitic tweets concurrently
        t1 = threading.Thread(target=self.process_tweets, args=("raw_tweets_antisemitic", self.push_antisemitic))
        t2 = threading.Thread(target=self.process_tweets, args=("raw_tweets_not_antisemitic", self.push_not_antisemitic))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

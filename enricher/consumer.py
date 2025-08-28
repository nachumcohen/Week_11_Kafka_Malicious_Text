from kafka import KafkaConsumer
import json

class Consumer:
    def __init__(self):
        self.antisemitic_consumer = KafkaConsumer('preprocessed_tweets_antisemitic',
                                 group_id='my_consumer_group',
                                 bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='earliest', # Start consuming from the beginning
                                 enable_auto_commit=True,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 consumer_timeout_ms = 5000)

        self.not_antisemitic_consumer = KafkaConsumer('preprocessed_tweets_not_antisemitic',
                                 group_id='my_consumer_group_2',
                                 bootstrap_servers=['localhost:9092'],
                                 auto_offset_reset='earliest', # Start consuming from the beginning
                                 enable_auto_commit=True,
                                 value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                                 consumer_timeout_ms = 5000)


    def stop_consumers(self):
        self.antisemitic_consumer.close()
        self.not_antisemitic_consumer.close()


    def _consume(self, consumer):
        print("Starting consumer...")
        for message in consumer:
            yield message.value



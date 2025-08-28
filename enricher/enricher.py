from consumer import Consumer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import os
from config import blacklist_path
import re
from datetime import datetime
from dateutil import parser
from clean.cleaner import Cleaner
from producer import Producer

class Enricher:
    def __init__(self):
        self.consumer = Consumer()
        self.init_nltk()
        self.producer = Producer()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.consumer.stop_consumers()

    def init_nltk(self):
        nltk_dir = "/tmp/nltk_data"
        os.makedirs(nltk_dir, exist_ok=True)
        nltk.data.path.append(nltk_dir)
        nltk.download('vader_lexicon', download_dir=nltk_dir, quiet=True)  # download vader_lexicon for nltk lib

    def _classified_emotion(self, tweet):
        emotion = SentimentIntensityAnalyzer().polarity_scores(tweet)
        score = emotion["compound"]
        if score < -0.5:
            return 'negative'
        elif score < 0.5:
            return 'neutral'
        return 'positive'


    def assign_emotion(self, data_item):
        score = self._classified_emotion(data_item["text"])
        data_item["sentiment"] = score


    def _load_blacklist(self):
        black_list = []
        black_list_cleaner = Cleaner()
        with open(blacklist_path, "r") as file:
            for line in file:
                line = black_list_cleaner.get_clean_text(line)
                print(line)
                black_list.append(line)
        return black_list

    def _detected_weapons(self, tweet, black_list):
        for weapon in black_list:
            if weapon in tweet:
                return weapon
        return ""

    def _detect_dates(self, text):
        reg = r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})|(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))|(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})"
        match = re.search(reg, text)
        relevant_timestamp = ""
        if match:
            dt_object = parser.parse(match.group(0))
            relevant_timestamp = dt_object.strftime("%Y-%m-%d")
        return relevant_timestamp


    def enrich(self):
        blacklist = self._load_blacklist()
        while True:
            anti_semi_tweets = self.consumer._consume(self.consumer.antisemitic_consumer)
            semi_tweets = self.consumer._consume(self.consumer.not_antisemitic_consumer)
            for tweet in anti_semi_tweets:
                self.assign_emotion(tweet)
                tweet["weapons_detected"] = self._detected_weapons(tweet["clean_text"], blacklist)
                tweet["relevant_timestamp"] = self._detect_dates(tweet["text"])
                self.producer.produce(tweet)
                print(tweet)

            for tweet in semi_tweets:
                self.assign_emotion(tweet)
                tweet["weapons_detected"] = self._detected_weapons("clean_text", blacklist)
                tweet["relevant_timestamp"] = self._detect_dates(tweet["text"])
                self.producer.produce(tweet)
                print(tweet)


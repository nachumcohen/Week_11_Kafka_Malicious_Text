# Week_11_Kafka_Malicious_Text

This repository implements a Kafka-based pipeline for processing malicious texts (tweets) with multiple services for retrieval, preprocessing, enrichment, storage, and data retrieval.

## Project Structure

### 1. retriever
- Purpose: Scheduled data retrieval from MongoDB Atlas.
- Functionality: Fetches tweets every minute and publishes them to Kafka topics:
  - raw_tweets_antisemitic
  - raw_tweets_not_antisemitic
- Files: Contains classes for connecting to the cloud DB and sending data to Kafka.

### 2. preprocessor
- Purpose: Consumes raw tweets from Kafka, cleans text, and republishes processed data.
- Processing includes:
  - Remove punctuation and special characters
  - Remove extra whitespace
  - Remove stop words
  - Convert text to lowercase
  - Lemmatization
- Output topics:
  - preprocessed_tweets_antisemitic
  - preprocessed_tweets_not_antisemitic

### 3. enricher/
- Purpose: Adds additional features to preprocessed tweets.
- Processing includes:
  - Sentiment analysis (positive / negative / neutral)
  - Detecting weapons based on a blacklist
  - Extracting latest timestamp from text content
- Output topics:
  - enriched_preprocessed_tweets_antisemitic
  - enriched_preprocessed_tweets_not_antisemitic

### 4. persister/
- Purpose: Stores enriched tweets into local MongoDB.
- Collections:
  - tweets_antisemitic
  - tweets_not_antisemitic
- Functionality: Listens to enriched Kafka topics and saves the data.

### 5. dataretrieval/
- Purpose: Provides a FastAPI service to retrieve stored tweets.
- Endpoints:
  - /tweets_antisemitic → returns all antisemitic tweets
  - /tweets_not_antisemitic → returns all non-antisemitic tweets

### 6. clean/
- Purpose: Text cleaning utilities.
- Contains: Class for performing all text preprocessing steps (punctuation removal, lemmatization, stop word removal, etc.)

### 7. producer.py
- Purpose: Wrapper class to send messages to Kafka topics from services.

## Notes
- Each service has its own Dockerfile for containerization.
- Commands for building, running locally, and pushing Docker images should be documented separately.
- Kafka is used as the messaging backbone to decouple services.
- MongoDB Atlas is used for cloud storage in Retriever, and local MongoDB is used for Persister and DataRetrieval.


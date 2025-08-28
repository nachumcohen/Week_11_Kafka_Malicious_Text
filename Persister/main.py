from Persister.consumer_persister import TweetPersister


def main():
    tweetPersister = TweetPersister()
    tweetPersister.start_consumers()

if __name__ == "__main__":
    main()
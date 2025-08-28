from consumer import TweetConsumer


def main():
    consumer = TweetConsumer()
    consumer.start_consumers()


if __name__ == "__main__":
    main()
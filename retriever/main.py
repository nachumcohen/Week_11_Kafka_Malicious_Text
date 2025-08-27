from mongo_dal import Dal
from producer import Producer
import time


dal = Dal()
producer = Producer()


def main():
    print("prrr")
    while True:
        data = dal.get_data()
        if len(data) == 0:
            print("no data to retrieve")
            time.sleep(10)
            continue
        producer.produce(data)


if __name__ == "__main__":
    main()


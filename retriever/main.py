from mongo_dal import Dal
import time


dal = Dal()
def main():
    while True:
        data = dal.get_data()
        if len(data) == 0:
            print("no data to retrieve")
            time.sleep(10)
            continue



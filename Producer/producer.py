from flask import Flask, request
from threading import Thread
import requests
import random
import threading
from contextlib import suppress
from time import sleep

Items_ids = []

app = Flask(__name__)
@app.route('/producer', methods = ['GET', 'POST'])
def producer():
    data = request.get_json()
    if(data['item_id'] in Items_ids):
            Items_ids.remove(data['item_id'])
            print(f'Item with id: {data["item_id"]} is received from {data["sender"]} !\n')
    else:
           print(f'Wrong item with id: {data["item_id"]} is received from {data["sender"]}!\n')
    return {'status_code': 200}


def send_data():
    with suppress(Exception):
        while True:
            random_id = random.randint(1, 1000)
            Items_ids.append(random_id)
            sender = "Producer"
            payload = dict({'item_id': random_id, 'received_from': sender})
            print(f"{sender} sent item with id: {random_id}")
            requests.post('http://localhost:8081/aggregator', json = payload)
           

def start_threads():
    Thread1 = threading.Timer(1.0, send_data)
    Thread1.start()
    Thread2 = threading.Timer(1.0, send_data)
    Thread2.start()
    Thread3 = threading.Timer(1.0, send_data)
    Thread3.start()
    Thread4 = threading.Timer(1.0, send_data)
    Thread4.start()
    Thread5 = threading.Timer(1.0, send_data)
    Thread5.start()
    Thread6 = threading.Timer(1.0, send_data)
    Thread6.start()
   
if __name__ == "__main__":
    producer_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 8080, debug = False, use_reloader = False), daemon= True)
    producer_thread.start()
    
    while True:
        RefreshThreads = threading.Thread(target= start_threads)
        RefreshThreads.start()
        sleep(3)



   

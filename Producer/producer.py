from flask import Flask, request
from threading import Thread
import requests
import random
from time import sleep
import time

threads = []

app = Flask(__name__)
@app.route('/producer', methods = ['GET', 'POST'])
def producer():
    data = request.get_json()
    print(f'Item with id: {data["item_id"]} is received from consumers!\n')
    return {'isSuccess': True}

def send_data():
    try:
        data = random.randint(1, 1000)
        payload = dict({'item_id': data})
        time.sleep(2)
        print(f"Item with id: {data} is sent to the consumers!")
        requests.post('http://localhost:8081/aggregator_producer', json = payload, timeout = 0.0000000001)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
     pass

def run_producer():
    producer_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 8080, debug = False, use_reloader = False), daemon = True)
    threads.append(producer_thread)
    sleep(2)
    thread_random = 20
    for _ in range(thread_random):
        client_thread = Thread(target = send_data)
        threads.append(client_thread)

    for thread in threads:
        thread.start()
        sleep(2)

    for thread in threads:
        thread.join()
   
run_producer()
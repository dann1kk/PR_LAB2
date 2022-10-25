from flask import Flask, request
from threading import Thread
import requests
import queue
import random 
from time import sleep


app = Flask(__name__)

threads = []

items_queue = queue.Queue()
items_queue.join()

@app.route('/consumer', methods = ['GET', 'POST'])
def producer_aggregator():
    data = request.get_json()
    print(f'Item with id: {data["item_id"]} is received!\n')
    sleep(2)
    items_queue.put(data)
    return {'isSuccess': True}

def send_order():
    try:
        order = items_queue.get()
        items_queue.task_done()
        payload = dict({'item_id': order['item_id']})
        print(f'Item with id: {order["item_id"]} is sent to producers!\n')
        requests.post('http://localhost:8081/aggregator_consumer', json = payload, timeout = 0.0000000001)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        pass
    
def run_consumer():
    consumer_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 8082, debug = False, use_reloader = False), daemon = True)
    threads.append(consumer_thread)
    sleep(3)
    thread_random = random.randint(5, 30)
    for _ in range(thread_random):
        thread = Thread(target = send_order)
        threads.append(thread)

    for thread in threads:
        thread.start()
        sleep(2)

    for thread in threads:
        thread.join()

    
run_consumer()
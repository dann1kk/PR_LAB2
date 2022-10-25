from flask import Flask, request
from threading import Thread
import requests
import random
from time import sleep
import queue

threads = []

producer_queue = queue.Queue()
consumer_queue = queue.Queue()
producer_queue.join()
consumer_queue.join()


app = Flask(__name__)

@app.route('/aggregator_producer', methods = ['GET', 'POST'])
def aggregator_producer():
    data = request.get_json()
    print(f'Order nr.{data["item_id"]} is received from producers!\n')
    sleep(2)
    producer_queue.put(data)
    return {'isSuccess': True}

@app.route('/aggregator_consumer', methods = ['GET', 'POST'])
def aggregator_consumer():
    data = request.get_json()
    print(f'Item with id:{data["item_id"]} is received from consumers!\n')
    sleep(2)
    consumer_queue.put(data)
    return {'isSuccess': True}

def send_consumer():
    try:
        order = producer_queue.get()
        producer_queue.task_done()
        payload = dict({'item_id': order['item_id']})
        print(f'Order nr.{order["item_id"]} is sent to consumers!\n')
        requests.post('http://localhost:8082/consumer', json = payload, timeout = 0.0000000001)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        pass
    
def send_producer():
    try:
        order = consumer_queue.get()
        consumer_queue.task_done()
        payload = dict({'item_id': order['item_id']})
        print(f'Item with id: {order["item_id"]} is sent to producers!')
        requests.post('http://localhost:8080/producer', json = payload, timeout = 0.0000000001)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        pass
    
def run_aggregator():
    producer_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 8081, debug = False, use_reloader = False), daemon = True)
    threads.append(producer_thread)
    sleep(3)
    thread_random = 20
    for _ in range(thread_random):
        consumers_thread = Thread(target = send_consumer)
        threads.append(consumers_thread)
    for _ in range(thread_random):
        producers_thread = Thread(target = send_producer)
        threads.append(producers_thread)

    for thread in threads:
        thread.start()
        sleep(2)

    for thread in threads:
        thread.join()

run_aggregator()
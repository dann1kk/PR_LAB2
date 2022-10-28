from time import sleep
from flask import Flask, request
from threading import Thread
import requests
import queue
import threading
from contextlib import suppress

app = Flask(__name__)

items_queue = queue.Queue()
items_queue.join()

@app.route('/consumer', methods = ['GET', 'POST'])
def consumer():
    data = request.get_json()
    print(f'Item with id: {data["item_id"]} is received from {data["sender"]}!\n')
    items_queue.put(data)
    return {'status_code': 200}

def send_data():
    with suppress(Exception):
     while True:
        order = items_queue.get()
        items_queue.task_done()
        payload = dict({'item_id': order['item_id'], 'received_from': 'Consumer'})
        print(f'Item with id: {order["item_id"]} is sent to Producer!\n')
        requests.post('http://localhost:8081/aggregator', json = payload, timeout = 0.0000000001)
    

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
    consumer_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 8082, debug = False, use_reloader = False), daemon = True)
    consumer_thread.start()
    
    while True:
        RefreshThreads = threading.Thread(target= start_threads)
        RefreshThreads.start()
        sleep(3)
    

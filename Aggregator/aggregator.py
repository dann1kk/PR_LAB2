from threading import Thread
import queue
from time import sleep
from flask import Flask, request
import requests
import threading

consumer_queue = queue.Queue()
consumer_queue.join()
producer_queue = queue.Queue()
producer_queue.join()

app = Flask(__name__)
@app.route('/aggregator', methods = ['GET', 'POST'])
def aggregator():
    data = request.get_json()
    print(f'Item with id:{data["item_id"]} is received from {data["received_from"]}!\n')
    if (data['received_from'] == "Producer"):
        producer_queue.put(data)
    else:
        consumer_queue.put(data)
    return {'status_code': 200}

def send_data():
    try:
        item_producer = producer_queue.get()
        producer_queue.task_done()
        payload = dict({'item_id': item_producer['item_id'], 'sender': item_producer['received_from']})
        requests.post('http://localhost:8082/consumer', json = payload)
    except (queue.Empty, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            pass
    try:
        item_consumer = consumer_queue.get()
        consumer_queue.task_done()
        payload = dict({'item_id': item_consumer['item_id'], 'sender': item_consumer['received_from']})
        requests.post('http://localhost:8080/producer', json = payload)
    except (queue.Empty, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            pass

def start_threads():
    Thread1 = threading.Timer(3.0, send_data)
    Thread1.start()
    Thread2 = threading.Timer(3.0, send_data)
    Thread2.start()
    Thread3 = threading.Timer(3.0, send_data)
    Thread3.start()
    Thread4 = threading.Timer(3.0, send_data)
    Thread4.start()
    Thread5 = threading.Timer(3.0, send_data)
    Thread5.start()
    Thread6 = threading.Timer(3.0, send_data)
    Thread6.start()

if __name__ == "__main__":
    aggregator_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 8081, debug = False, use_reloader = False), daemon = True)
    aggregator_thread.start()

    while True:
        RefreshThreads = threading.Thread(target= start_threads)
        RefreshThreads.start()
        sleep(3)


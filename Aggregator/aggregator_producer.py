from resources import *

@app.route('/aggregator_producer', methods = ['GET', 'POST'])
def aggregator_producer():
    data = request.get_json()
    print(f'Item with id:{data["item_id"]} is received from producers!\n')
    sleep(3)
    producer_queue.put(data)
    return {'isSuccess': True}

def send_consumer():
    try:
        order = producer_queue.get()
        producer_queue.task_done()
        payload = dict({'item_id': order['item_id']})
        print(f'Item with id: {order["item_id"]} is sent to consumers!\n')
        requests.post('http://localhost:8082/consumer', json = payload, timeout = 0.0000000001)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        pass

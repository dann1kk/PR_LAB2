from resources import *

@app.route('/aggregator_consumer', methods = ['GET', 'POST'])
def aggregator_consumer():
    data = request.get_json()
    print(f'Item with id:{data["item_id"]} is received from consumers!\n')
    sleep(3)
    consumer_queue.put(data)
    return {'isSuccess': True}

def send_producer():
    try:
        order = consumer_queue.get()
        consumer_queue.task_done()
        payload = dict({'item_id': order['item_id']})
        print(f'Item with id: {order["item_id"]} is sent to producers!')
        requests.post('http://localhost:8080/producer', json = payload, timeout = 0.0000000001)
    except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        pass
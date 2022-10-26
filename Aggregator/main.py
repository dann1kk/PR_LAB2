from threading import Thread
from time import sleep
from aggregator_producer import *
from aggregator_consumer import *

threads = []
thread_random = 20

def main():
    producer_thread = Thread(target = lambda: app.run(host = '0.0.0.0', port = 8081, debug = False, use_reloader = False), daemon = True)
    threads.append(producer_thread)
    for _ in range(thread_random):
        consumers_thread = Thread(target = send_consumer)
        threads.append(consumers_thread)
    for _ in range(thread_random):
        producers_thread = Thread(target = send_producer)
        threads.append(producers_thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        sleep(1)

main()
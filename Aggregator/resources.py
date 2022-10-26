from flask import Flask, request
from threading import Thread
import queue
import requests 
from time import sleep

app = Flask(__name__)

consumer_queue = queue.Queue()
consumer_queue.join()
producer_queue = queue.Queue()
producer_queue.join()
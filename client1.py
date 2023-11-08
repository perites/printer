import threading
import requests
import time

URL = "http://127.0.0.1:5000/"


def show_message(message):
    if isinstance(message, dict):
        print(f'{message["sender"]} : {message["message"]} at {message["time"]}')
    else:
        print(message)


def send_message():
    while True:
        message = input()
        message = {"time": time.ctime(), "sender": "client1", "message": message}
        requests.post(URL, json=message)


def fetch_messages():
    last_message = ""
    while True:

        message = requests.get(URL)
        message = message.json()
        if message and message != last_message:
            show_message(message)
            last_message = message

        time.sleep(1)


send_message_thread = threading.Thread(target=send_message)
fetch_messages_thread = threading.Thread(target=fetch_messages, daemon=True)
send_message_thread.start()
fetch_messages_thread.start()

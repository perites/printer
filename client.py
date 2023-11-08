import threading
import requests
import time

URL = "http://127.0.0.1:5000/"


def show_message(message):
    if isinstance(message, dict):
        print(f'\n{message["sender"]} to {message["message_to"]}: {message["message"]} at {message["time"]}')
    else:
        print(message)


def send_message(name):
    while True:
        message_to = input("message to :")
        message = input("message : ")
        message = {"time": time.ctime(), "sender": name, "message": message, "message_to": message_to}
        requests.post(URL, json=message)


def fetch_messages(name):
    while True:
        headers = {"message-to": name}
        message = requests.get(URL, headers=headers)
        if message and (message := message.json()) != "nnm":
            show_message(message)
        time.sleep(1)


name = input("your name : ")
send_message_thread = threading.Thread(target=send_message, args=(name,))
fetch_messages_thread = threading.Thread(target=fetch_messages, args=(name,))
send_message_thread.start()
fetch_messages_thread.start()

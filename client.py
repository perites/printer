import threading
import requests
import time

URL = "http://127.0.0.1:5000/"


class ClientMessagesContoller():
    def __init__(self, name):
        self.client_name = name

    def show_message(self, message):
        if isinstance(message, dict):
            print(f'\n{message["message_from"]} to {message["message_to"]}: {message["message"]} at {message["time"]}')
        else:
            print(message)

    def send_message(self):
        while True:
            message_to = input("message to: ")
            message = input("message: ")
            message = {"time": time.ctime(), "message_from": self.client_name, "message": message, "message_to": message_to}
            requests.post(URL, json=message)

    def fetch_messages(self):
        headers = {"message-to": self.client_name}
        while True:
            message = requests.get(URL, headers=headers)
            if (message := message.json()) != "nnm":
                self.show_message(message)
            time.sleep(1)

    def start_chatting(self):
        send_message_thread = threading.Thread(target=self.send_message)
        fetch_messages_thread = threading.Thread(target=self.fetch_messages)
        send_message_thread.start()
        fetch_messages_thread.start()


mc = ClientMessagesContoller(input("your name: "))
mc.start_chatting()

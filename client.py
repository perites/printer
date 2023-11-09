import threading
import requests
import time

URL = "https://chat-test-k49y.onrender.com"
URL = "http://127.0.0.1:5000/"


class ClientMessagesContoller():
    def __init__(self, name):
        self.client_name = name
        self.commads = ["help", "omembers", "chat"]
        self.chat = False

    def show_message(self, message):
        if isinstance(message, dict):
            if message["system"]:
                print(f'\n{message["message_from"]} to {message["message_to"]}:{message["message"]} at {message["time"]}')
                return

            print(f'\n{message["message_from"]} to {message["message_to"]}:{message["message"]} at {message["time"]}')
            message = {"time": time.ctime(), "message_from": self.client_name, "message": f"have read your message:  {message['message']}", "message_to": message['message_from'], "system": True}
            requests.post(URL, json=message)
        else:
            print("\n" + message)

    def send_message(self):
        message_to = input("chat with:")
        while self.chat:
            message = input("message:")
            match message:
                case "exit":
                    self.chat = False
                    return
                case "":
                    print("message cant be empty")
                case _:
                    message = {"time": time.ctime(), "message_from": self.client_name, "message": message, "message_to": message_to, "system": False}
                    requests.post(URL, json=message)

    def fetch_messages(self):
        headers = {"message-to": self.client_name}
        while self.chat:
            message = requests.get(URL, headers=headers)
            if (message := message.json()):
                self.show_message(message)
            time.sleep(1)

    def start_chatting(self):
        send_message_thread = threading.Thread(target=self.send_message)
        fetch_messages_thread = threading.Thread(target=self.fetch_messages)
        send_message_thread.start()
        fetch_messages_thread.start()

    def terminal(self):
        while not self.chat:
            user_input = input("command:")
            match user_input:
                case "help":
                    print(self.commads)

                case "omembers":
                    answer = requests.get(URL + "/omembers").json()
                    print(f"Currently online {len(answer)} members:\n{answer}")

                case "chat":
                    self.chat = True
                    self.start_chatting()

                case _:
                    print("wrong command")


mc = ClientMessagesContoller(input("your name:"))
while True:
    mc.terminal()

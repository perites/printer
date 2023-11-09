import threading
import requests
import time

URL = "https://chat-test-k49y.onrender.com"
# URL = "http://127.0.0.1:5000/"


class ClientMessagesContoller():
    def __init__(self, name):
        self.client_name = name
        self.commads = ["help", "omembers", "chat", "exit (while in chat)"]
        self.chat = False

    def show_message(self, message):
        if isinstance(message, dict):
            if message["system"]:
                print(f'\n{message["message_from"]} to {message["message_to"]}:{message["message"]} at {message["time"]}')
                return

            print(f'\n{message["message_from"]} to {message["message_to"]}:{message["message"]} at {message["time"]}')
            message = {"time": time.ctime(), "message_from": self.client_name, "message": f" have read your message:  {message['message']}", "message_to": message['message_from'], "system": True}
            requests.post(URL, json=message)
        else:
            print("\n" + message)

    def send_message(self):
        message_to = input("chat with:")
        while self.chat:
            message = input("message:")
            if message == "exit":
                self.chat = False
            elif message == "" or "ㅤ" in message:
                print("message cant be empty")
            else:
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


def validate_name():
    while True:
        name = input("your name:")

        if " " in name or "ㅤ" in name or name == "":
            print("name cant be empty")

        else:
            answer = requests.get(URL + "/omembers").json()
            if name in answer:
                print("name already taken")
            else:
                return name


mc = ClientMessagesContoller(validate_name())
while True:
    mc.terminal()

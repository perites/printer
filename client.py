import threading
import requests
import time
from dataclasses import dataclass, asdict
URL = "https://chat-test-k49y.onrender.com"
# URL = "http://127.0.0.1:5000/"


@dataclass
class Message():
    message: str
    message_from: str
    message_to: str
    system_message: bool = False
    time: str = time.ctime()

    def __str__(self):
        return f"\n{self.message_from} to {self.message_to}: {self.message} at {self.time}"


class ClientMessagesContoller():
    def __init__(self):
        self.user_name = self.validate_name()
        self.commads = ["help", "omembers", "chat", "exit (while in chat)"]
        self.chat = False

        fetch_messages_thread = threading.Thread(target=self.fetch_messages)
        fetch_messages_thread.start()

    def terminal(self):
        while not self.chat:
            user_input = input("command: ")
            match user_input:
                case "help":
                    print(self.commads)

                case "omembers":
                    answer = self.get_online_members()
                    print(f"Currently online {len(answer)} members:\n{answer}")

                case "chat":
                    self.chat = True
                    self.start_chatting()

                case _:
                    print("wrong command")

    def start_chatting(self):
        get_user_message_thread = threading.Thread(target=self.get_user_message)
        get_user_message_thread.start()

    def get_user_message(self):
        message_to = input("chat with: ")
        while self.chat:
            message = input("message: ")
            if message == "exit":
                self.chat = False
            elif message == "" or "ㅤ" in message:
                print("message cant be empty")
            else:
                message = asdict(Message(message_from=self.user_name, message_to=message_to, message=message))
                self.send_message(message)

    def fetch_messages(self):
        headers = {"message-to": self.user_name}
        while True:
            message = requests.get(URL, headers=headers)
            if (message := message.json()):
                self.show_message(message)
            time.sleep(1)

    def show_message(self, message):
        if not isinstance(message, dict):
            print("\n" + message)
            return

        message = Message(**message)
        print(message)

        if message.system_message:
            return
        message = asdict(Message(message_from=self.user_name, message_to=message.message_from, message=f"message seen: '{message.message}'", system_message=True))
        self.send_message(message)

    def send_message(self, message):
        requests.post(URL, json=message)

    def get_online_members(self):
        return requests.get(URL + "/omembers").json()

    def validate_name(self):
        while True:
            name = input("your name: ")
            print(name)
            print(self.get_online_members())
            if " " in name or "ㅤ" in name or name == "":
                print("name cant be empty")
            elif name in self.get_online_members():
                print("name already taken")
            else:
                return name


mc = ClientMessagesContoller()
while True:
    mc.terminal()

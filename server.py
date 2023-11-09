from flask import Flask, request, jsonify
import time
import threading
app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7a0a1003456342385cb9e30b6b'


class ServerMessagesController():
    def __init__(self):
        self.all_messages = []
        self.members_online = {}

    def store_message(self, message):
        self.all_messages.append(message)

    def find_message(self, message_to):
        for message in self.all_messages:
            if message["message_to"] == message_to:
                self.all_messages.remove(message)
                return message

    def members_online_update(self):
        while True:
            items_to_remove = []

            members_online_copy = self.members_online.copy()
            for user, last_o in members_online_copy.items():
                if time.time() - last_o > 10:
                    items_to_remove.append(user)
            for user in items_to_remove:
                del self.members_online[user]


mc = ServerMessagesController()
members_online_update_thread = threading.Thread(target=mc.members_online_update)
members_online_update_thread.start()


@ app.route("/", methods=["POST"])
def get_messages():
    message = request.json
    mc.store_message(message)

    return "", 200


@ app.route("/", methods=["GET"])
def give_messages():
    message_to = request.headers.get("message-to")
    mc.members_online[message_to] = time.time()
    return jsonify(mc.find_message(message_to))


@ app.route("/omembers", methods=["GET"])
def online_members():
    return jsonify(list(mc.members_online.keys()))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

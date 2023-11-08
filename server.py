from flask import Flask, request, jsonify
app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7a0a1003456342385cb9e30b6b'


class ServerMessagesController():
    def __init__(self):
        self.all_messages = []

    def store_message(self, message):
        self.all_messages.append(message)

    def find_message(self, message_to):
        for message in self.all_messages:
            if message["message_to"] == message_to:
                self.all_messages.remove(message)
                return message

        return "nnm"


mc = ServerMessagesController()


@app.route("/", methods=["POST"])
def get_messages():
    message = request.json
    mc.store_message(message)

    return "", 200


@app.route("/", methods=["GET"])
def give_messages():
    message_to = request.headers.get("message-to")

    return jsonify(mc.find_message(message_to))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

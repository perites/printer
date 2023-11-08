from flask import Flask, request, jsonify
app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7a0a1003456342385cb9e30b6b'

MESSAGES = []


def store_message(message):
    global MESSAGES
    MESSAGES.append(message)


def find_message(message_to):
    global MESSAGES
    for message in MESSAGES:
        if message["message_to"] == message_to:
            MESSAGES.remove(message)
            return message

    return "nnm"


@app.route("/", methods=["POST"])
def get_messages():
    message = request.json
    store_message(message)

    return "", 200


@app.route("/", methods=["GET"])
def give_messages():
    message_to = request.headers.get("message-to")

    return jsonify(find_message(message_to))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

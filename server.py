from flask import Flask, request, jsonify
import time
app = Flask(__name__)
app.config["SECRET_KEY"] = 'c42e8d7a0a1003456342385cb9e30b6b'

MESSAGE = ""


@app.route("/", methods=["POST"])
def get_messages():
    message = request.json
    global MESSAGE
    MESSAGE = message
    return jsonify(message)


@app.route("/", methods=["GET"])
def give_messages():
    global MESSAGE
    message = MESSAGE
    return jsonify(message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

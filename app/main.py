# app/main.py
from flask import Flask, jsonify

app = Flask(__name__)


# This is a simple endpoint that says "I'm alive"
@app.route("/health")
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route("/")
def home():
    return jsonify({"message": "Hello from my app!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

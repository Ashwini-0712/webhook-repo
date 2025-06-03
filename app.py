from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from db import collection
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = request.headers.get('X-GitHub-Event')

    payload = {}
    timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")

    if event == "push":
        payload = {
            "event_type": "push",
            "author": data["pusher"]["name"],
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": timestamp
        }

    elif event == "pull_request":
        action = data["action"]
        if action in ["opened", "reopened"]:
            payload = {
                "event_type": "pull_request",
                "author": data["pull_request"]["user"]["login"],
                "from_branch": data["pull_request"]["head"]["ref"],
                "to_branch": data["pull_request"]["base"]["ref"],
                "timestamp": timestamp
            }

    if payload:
        collection.insert_one(payload)

    return jsonify({"status": "received"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("_id", -1).limit(10))
    for e in events:
        e["_id"] = str(e["_id"])
    return jsonify(events)

if __name__ == '__main__':
    app.run(port=5000)

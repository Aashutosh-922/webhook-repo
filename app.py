from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import pytz

app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["github_events"]
collection = db["events"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def github_webhook():
    payload = request.json
    event_type = request.headers.get("X-GitHub-Event")

    try:
        if event_type == "push":
            author = payload["pusher"]["name"]
            to_branch = payload["ref"].split("/")[-1]
            commit_id = payload["head_commit"]["id"]

            data = {
                "request_id": commit_id,
                "author": author,
                "action": "PUSH",
                "from_branch": None,
                "to_branch": to_branch,
                "timestamp": utc_now()
            }

            collection.insert_one(data)

        elif event_type == "pull_request":
            pr = payload["pull_request"]
            author = pr["user"]["login"]
            from_branch = pr["head"]["ref"]
            to_branch = pr["base"]["ref"]
            pr_id = str(pr["id"])

            # Check if merged
            if pr.get("merged"):
                action = "MERGE"
            else:
                action = "PULL_REQUEST"

            data = {
                "request_id": pr_id,
                "author": author,
                "action": action,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": utc_now()
            }

            collection.insert_one(data)

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route("/events", methods=["GET"])
def get_events():
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(20))
    return jsonify(events)


def utc_now():
    return datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")


if __name__ == "__main__":
    app.run(debug=True, port=5000)

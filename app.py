from flask import Flask, render_template, request
import time
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            with open("tokennum.txt") as f:
                tokens = [line.strip() for line in f if line.strip()]

            with open("convo.txt") as f:
                convo_id = f.read().strip()

            with open("gaali.txt") as f:
                messages = [line.strip() for line in f if line.strip()]

            with open("time.txt") as f:
                delay = int(f.read().strip())

            for token in tokens:
                for msg in messages:
                    url = f"https://graph.facebook.com/v19.0/{convo_id}/messages"
                    data = {
                        "messaging_type": "MESSAGE_TAG",
                        "tag": "ACCOUNT_UPDATE",
                        "recipient": {"id": convo_id},
                        "message": {"text": msg},
                        "access_token": token
                    }
                    res = requests.post(url, json=data)
                    print(f"Sent: {msg} | Status: {res.status_code}")
                    time.sleep(delay)

            return "Messages sent successfully!"

        except Exception as e:
            return f"Error: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run()

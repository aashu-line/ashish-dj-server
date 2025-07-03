import time
import threading
import requests
import os
from flask import Flask, request, render_template_string

OWNER_UPI = "ap6273776-1@okaxis"
OWNER_PASSWORD = "S9NK1_DJ_S3RV3R"

app = Flask(__name__)

HTML_PAGE = '''
<!doctype html>
<title>Ashish Sanki DJ Server</title>
<h1 style="color: red;">🔥 WELCOME TO SANKI DJ ASHISH BOT 🔥</h1>
<p>Made by Ashish Pal | UPI: {{upi}}</p>
<form method="post">
    Password: <input name="password"><br><br>
    <input type="submit" value="Start Server">
</form>
<pre>{{output}}</pre>
'''

def send_messages():
    try:
        with open("convo.txt", "r") as f:
            convo_id = f.read().strip()
        with open("gaali.txt", "r") as f:
            messages = f.readlines()
        with open("tokennum.txt", "r") as f:
            tokens = f.readlines()
        with open("time.txt", "r") as f:
            delay = int(f.read().strip())
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    i = 0
    while True:
        try:
            token = tokens[i % len(tokens)].strip()
            message = messages[i % len(messages)].strip()
            url = f"https://graph.facebook.com/v17.0/t_{convo_id}"
            payload = {
                "access_token": token,
                "message": message
            }
            r = requests.post(url, json=payload)
            if r.status_code == 200:
                print(f"[✓] Sent: {message}")
            else:
                print(f"[×] Failed: {message} → {r.text}")
            time.sleep(delay)
            i += 1
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(5)

@app.route('/', methods=['GET', 'POST'])
def home():
    output = ""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == OWNER_PASSWORD:
            t = threading.Thread(target=send_messages)
            t.start()
            output = "✅ Bot started successfully!"
        else:
            output = f"❌ Invalid password. Please pay ₹500 to use.\nContact Owner UPI: {OWNER_UPI}"
    return render_template_string(HTML_PAGE, output=output, upi=OWNER_UPI)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

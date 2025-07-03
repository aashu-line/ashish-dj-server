from flask import Flask, request, render_template, redirect
import os
import requests
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OWNER_UPI = "ap6273776-1@okaxis"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upi = request.form.get('upi')
        convo_id = request.form.get('convo_id')

        if upi != OWNER_UPI:
            return f"<h3>❌ Access Denied! Pay ₹500 UPI: {OWNER_UPI} to unlock.</h3>"

        # Save uploaded files
        for key in ['tokennum', 'gaali', 'time', 'hatersname']:
            file = request.files.get(key)
            if file:
                file.save(os.path.join(UPLOAD_FOLDER, key + '.txt'))

        with open(os.path.join(UPLOAD_FOLDER, 'convo.txt'), 'w') as f:
            f.write(convo_id)

        # Start sending gaalis
        send_gaali()

        return "<h3>✅ Gaalis sent successfully from Ashish Sanki DJ Server!</h3>"

    return render_template('index.html')

def send_gaali():
    try:
        with open('uploads/tokennum.txt') as f:
            tokens = [t.strip() for t in f.readlines()]

        with open('uploads/gaali.txt') as f:
            messages = [m.strip() for m in f.readlines()]

        with open('uploads/convo.txt') as f:
            convo_id = f.read().strip()

        with open('uploads/time.txt') as f:
            delay = int(f.read().strip())

        with open('uploads/hatersname.txt') as f:
            hater = f.read().strip()

        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        for i, msg in enumerate(messages):
            token = tokens[i % len(tokens)]
            full_msg = f"{hater} {msg}"
            url = f"https://graph.facebook.com/v17.0/t_{convo_id}"
            data = {'access_token': token, 'message': full_msg}
            res = requests.post(url, json=data, headers=headers)
            print(f"[{i+1}] Sent: {full_msg} - Status: {res.status_code}")
            time.sleep(delay)

    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    app.run(debug=True)

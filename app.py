import os
import threading
import time
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from run import start_miner 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_2026_szaby')
# 30 napig megjegyzi a bejelentkezést, ha bepipálod!
app.permanent_session_lifetime = timedelta(days=30)

mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(mongo_url)
db = client['twitch_miner_web']
twitch_data_collection = db['twitch_data']

ADMIN_USER = os.getenv('WEB_USERNAME', 'szaby')
ADMIN_PASS = os.getenv('WEB_PASSWORD', '2003')

TWITCH_USERNAME = os.getenv('TWITCH_USERNAME', '0szaby0')
TWITCH_AUTH_TOKEN = os.getenv('TWITCH_AUTH_TOKEN', '')

@app.route('/')
def home():
    if 'username' in session:
        accounts = list(twitch_data_collection.find({}))
        processed_accounts = []
        for acc in accounts:
            acc['_id'] = str(acc['_id'])
            history = acc.get('history', [0])
            current_points = history[-1] if history else 0
            
            acc['chart_data'] = history[-40:] if len(history) > 0 else [0]
            acc['current_points'] = current_points
            acc['formatted_points'] = f"{current_points:,}".replace(',', ' ')
            acc['diff'] = history[-1] - history[-2] if len(history) >= 2 else 0
            acc['is_online'] = acc.get('is_online', False)
            processed_accounts.append(acc)
        
        processed_accounts.sort(key=lambda x: (x.get('is_online', False), x.get('current_points', 0)), reverse=True)
        
        return render_template(
            'dashboard.html', 
            username=session['username'], 
            accounts=processed_accounts,
            twitch_name=TWITCH_USERNAME,
            twitch_token=TWITCH_AUTH_TOKEN
        )
    return redirect(url_for('login'))

@app.route('/api/data')
def api_data():
    if 'username' not in session:
        return jsonify({"error": "Nincs bejelentkezve"}), 401
    accounts = list(twitch_data_collection.find({}))
    processed_accounts = []
    for acc in accounts:
        history = acc.get('history', [0])
        current_points = history[-1] if history else 0
        processed_accounts.append({
            "channel_name": acc['channel_name'],
            "current_points": current_points,
            "formatted_points": f"{current_points:,}".replace(',', ' '),
            "diff": history[-1] - history[-2] if len(history) >= 2 else 0,
            "is_online": acc.get('is_online', False),
            "chart_data": history[-40:] if len(history) > 0 else [0]
        })
    return jsonify(processed_accounts)

@app.route('/api/log_error', methods=['POST'])
def log_error():
    data = request.json
    error_msg = data.get('error', 'Ismeretlen hiba')
    channel = data.get('channel', 'Ismeretlen csatorna')
    print(f"\n{'='*50}\n!!! FRONTEND CHAT HIBA ({channel}) !!!\nHIBA OKA: {error_msg}\n{'='*50}\n")
    return jsonify({"status": "ok"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session.clear()
            if request.form.get('remember'):
                session.permanent = True  # Beállítja a 30 napos megjegyzést
            session['username'] = ADMIN_USER
            return redirect(url_for('home'))
        else:
            error = "Hibás felhasználónév vagy jelszó!"
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    start_miner()

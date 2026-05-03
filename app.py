import os
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
from run import start_miner 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_2026_szaby')

mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(mongo_url)
db = client['twitch_miner_web']
twitch_data_collection = db['twitch_data']

ADMIN_USER = os.getenv('WEB_USERNAME', 'szaby')
ADMIN_PASS = os.getenv('WEB_PASSWORD', '2003')

# --- Ezek kellenek az Automata Chathoz ---
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
            
            # Grafikon adatok
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == ADMIN_USER and request.form.get('password') == ADMIN_PASS:
            session['username'] = ADMIN_USER
            return redirect(url_for('home'))
    return render_template('login.html')

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

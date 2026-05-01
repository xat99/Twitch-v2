import os
import threading
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
from run import start_miner 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_2024')

# MongoDB csatlakozás
mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(mongo_url)
db = client['twitch_miner_web']
twitch_data_collection = db['twitch_data']
config_collection = db['config']

ADMIN_USER = os.getenv('WEB_USERNAME', 'szaby')
ADMIN_PASS = os.getenv('WEB_PASSWORD', '2003')

@app.route('/')
def home():
    if 'username' in session:
        accounts = list(twitch_data_collection.find({}))
        tokens = config_collection.find_one({"type": "twitch_tokens"}) or {}
        
        for acc in accounts:
            acc['_id'] = str(acc['_id'])
            history = acc.get('history', [0])
            acc['current_points'] = history[-1]
            acc['diff'] = history[-1] - history[-2] if len(history) >= 2 else 0
        
        # SORREND: A legtöbb pontszámú legyen legfelül
        accounts.sort(key=lambda x: x['current_points'], reverse=True)
        
        return render_template('dashboard.html', username=session['username'], accounts=accounts, tokens=tokens)
    return redirect(url_for('login'))

@app.route('/save_tokens', methods=['POST'])
def save_tokens():
    if 'username' in session:
        auth_token = request.form.get('auth_token')
        unique_id = request.form.get('unique_id')
        
        config_collection.update_one(
            {"type": "twitch_tokens"},
            {"$set": {"auth_token": auth_token, "unique_id": unique_id}},
            upsert=True
        )
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            session['username'] = ADMIN_USER
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    # A weboldal a háttérben indul, hogy ne akadályozza a botot
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    # Elindítjuk a bányászt a fő szálon
    start_miner()

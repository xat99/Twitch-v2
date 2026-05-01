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

# MongoDB Atlas kapcsolat
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
        
        processed_accounts = []
        for acc in accounts:
            acc['_id'] = str(acc['_id'])
            
            # Kinyerjük az adatbázisból az utolsó mentett pontszámot
            history = acc.get('history', [0])
            current_points = history[-1] if history else 0
            diff = history[-1] - history[-2] if len(history) >= 2 else 0
            
            # --- A LÉNYEG: Minden néven átadjuk a HTML-nek, hogy biztosan megtalálja! ---
            acc['current_points'] = current_points
            acc['channel_points'] = current_points  # <-- Ezt a nevet kereste a weboldalad!
            acc['balance'] = current_points
            acc['diff'] = diff
            
            # Bónusz: Egy szépen formázott verzió (pl. 825 560), amit használhatsz a HTML-ben
            acc['formatted_points'] = f"{current_points:,}".replace(',', ' ')
            
            processed_accounts.append(acc)
        
        # SORREND: A legtöbb ponttal rendelkező streamer (pl. Picury) lesz legfelül
        processed_accounts.sort(key=lambda x: x.get('current_points', 0), reverse=True)
        
        return render_template('dashboard.html', username=session['username'], accounts=processed_accounts, tokens=tokens)
    return redirect(url_for('login'))

@app.route('/save_tokens', methods=['POST'])
def save_tokens():
    if 'username' in session:
        auth_token = request.form.get('auth_token')
        unique_id = request.form.get('unique_id')
        config_collection.update_one(
            {"type": "twitch_tokens"},
            {"$set": {"auth_token": auth_token, "unique_id": unique_id, "updated_at": time.time()}},
            upsert=True
        )
    return redirect(url_for('home'))

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
    
    print("Log: Weboldal elindítva, bányász indítása...")
    start_miner()

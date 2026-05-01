import os
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
from run import start_miner 

# Környezeti változók (.env fájl) betöltése
load_dotenv()

app = Flask(__name__)
# A session titkosításához szükséges kulcs (Render környezeti változóból vagy alapértelmezett)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_2026_szaby')

# --- MONGODB ATLAS KAPCSOLAT ---
mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(mongo_url)
db = client['twitch_miner_web']
twitch_data_collection = db['twitch_data']
config_collection = db['config']

# --- WEB ADMIN BEJELENTKEZÉSI ADATOK ---
ADMIN_USER = os.getenv('WEB_USERNAME', 'szaby')
ADMIN_PASS = os.getenv('WEB_PASSWORD', '2003')

# --- TWITCH ADATOK AZ AUTOMATA CHATHEZ (tmi.js) ---
TWITCH_USERNAME = os.getenv('TWITCH_USERNAME', '0szaby0')
# Fontos: A token formátuma ideális esetben 'oauth:xxxxxxxx'
TWITCH_AUTH_TOKEN = os.getenv('TWITCH_AUTH_TOKEN', '')

@app.route('/')
def home():
    # Csak akkor engedjük be, ha bejelentkezett a weboldalra
    if 'username' in session:
        # Lekérjük az összes streamer adatát az adatbázisból
        accounts = list(twitch_data_collection.find({}))
        
        processed_accounts = []
        for acc in accounts:
            # MongoDB belső ID-t szöveggé alakítjuk a HTML miatt
            acc['_id'] = str(acc['_id'])
            
            # Legutolsó pontszám kinyerése a history listából
            history = acc.get('history', [0])
            current_points = history[-1] if history else 0
            
            # Pontok formázása (825000 -> 825 000)
            acc['current_points'] = current_points
            acc['formatted_points'] = f"{current_points:,}".replace(',', ' ')
            
            # Különbség számítása az utolsó frissítés óta
            acc['diff'] = history[-1] - history[-2] if len(history) >= 2 else 0
            
            # Élő státusz (ezt a run.py frissíti 1 percenként)
            acc['is_online'] = acc.get('is_online', False)
            
            processed_accounts.append(acc)
        
        # RENDEZÉS:
        # 1. Aki LIVE, az kerül legfelülre
        # 2. Utána a legtöbb ponttal rendelkező csatornák következnek
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
        # Belépési adatok ellenőrzése a Renderen megadott ENV-ek alapján
        user = request.form.get('username')
        pw = request.form.get('password')
        
        if user == ADMIN_USER and pw == ADMIN_PASS:
            session['username'] = ADMIN_USER
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Hibás felhasználónév vagy jelszó!")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Ez a rész felel az indításért
if __name__ == '__main__':
    # Render.com dinamikus port kezelése
    port = int(os.environ.get("PORT", 5000))
    
    # A Flask weboldalt egy külön háttérszálon indítjuk el, 
    # hogy ne blokkolja le a bányász programot.
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    
    print("Log: Weboldal sikeresen elindítva a háttérben.")
    print("Log: Bányász motor (run.py) indítása...")
    
    # Meghívjuk a run.py-ban lévő fő függvényt
    start_miner()

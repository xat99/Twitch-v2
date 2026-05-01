import os
import threading
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
from run import start_miner 

# Környezeti változók betöltése
load_dotenv()

app = Flask(__name__)
# Titkos kulcs a session kezeléséhez
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_2026_szaby')

# MongoDB Atlas kapcsolat beállítása
mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(mongo_url)
db = client['twitch_miner_web']
twitch_data_collection = db['twitch_data']
config_collection = db['config']

# Admin belépési adatok a .env fájlból (vagy alapértelmezett)
ADMIN_USER = os.getenv('WEB_USERNAME', 'szaby')
ADMIN_PASS = os.getenv('WEB_PASSWORD', '2003')

@app.route('/')
def home():
    """Főoldal - Dashboard megjelenítése"""
    if 'username' in session:
        # Lekérjük az összes streamer adatát az adatbázisból
        accounts = list(twitch_data_collection.find({}))
        # Lekérjük a manuálisan mentett tokeneket is (ha vannak)
        tokens = config_collection.find_one({"type": "twitch_tokens"}) or {}
        
        processed_accounts = []
        for acc in accounts:
            acc['_id'] = str(acc['_id'])
            # Megnézzük a pontszám előzményeket
            history = acc.get('history', [0])
            # Az aktuális pont az utolsó elem a listában
            current_points = history[-1] if history else 0
            
            # Kiszámoljuk a változást (diff) az előző mentéshez képest
            diff = 0
            if len(history) >= 2:
                diff = history[-1] - history[-2]
            
            acc['current_points'] = current_points
            acc['diff'] = diff
            processed_accounts.append(acc)
        
        # SORREND: A legtöbb pontszámú streamer kerül legfelülre (Csökkenő sorrend)
        processed_accounts.sort(key=lambda x: x.get('current_points', 0), reverse=True)
        
        return render_template('dashboard.html', 
                               username=session['username'], 
                               accounts=processed_accounts, 
                               tokens=tokens)
    
    return redirect(url_for('login'))

@app.route('/save_tokens', methods=['POST'])
def save_tokens():
    """Tokenek mentése a Dashboard felületről"""
    if 'username' in session:
        auth_token = request.form.get('auth_token')
        unique_id = request.form.get('unique_id')
        
        # Elmentjük az adatbázisba, hogy a run.py innen olvassa ki indításkor
        config_collection.update_one(
            {"type": "twitch_tokens"},
            {"$set": {
                "auth_token": auth_token, 
                "unique_id": unique_id,
                "updated_at": os.times()[4] # Időbélyeg
            }},
            upsert=True
        )
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Bejelentkezési oldal kezelése"""
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        
        if user == ADMIN_USER and pw == ADMIN_PASS:
            session['username'] = user
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Hibás felhasználónév vagy jelszó!")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Kijelentkezés"""
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Render.com-hoz szükséges port beállítás
    port = int(os.environ.get("PORT", 5000))
    
    # Elindítjuk a Flask weboldalt egy külön szálon (háttérben)
    flask_thread = threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False)
    )
    flask_thread.daemon = True
    flask_thread.start()
    
    # Elindítjuk a fő bányász programot a run.py-ból
    print("Log: Weboldal elindítva, bányász indítása...")
    start_miner()

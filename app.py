import os
import threading
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv

# Importáljuk a start_miner függvényt a run.py-ból
from run import start_miner 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

# MongoDB csatlakozás beállítása
mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(mongo_url)
db = client['twitch_miner_web']
users_collection = db['users']
twitch_data_collection = db['twitch_data']

# Admin beállítása (szaby / 2003)
ADMIN_USER = os.getenv('WEB_USERNAME', 'szaby')
ADMIN_PASS = os.getenv('WEB_PASSWORD', '2003')
users_collection.update_one({'username': ADMIN_USER}, {'$set': {'password': ADMIN_PASS}}, upsert=True)

@app.route('/')
def home():
    if 'username' in session:
        accounts = list(twitch_data_collection.find({}))
        for acc in accounts:
            history = acc.get('history', [0])
            acc['current_points'] = history[-1]
            acc['diff'] = history[-1] - history[-2] if len(history) >= 2 else 0
        return render_template('dashboard.html', username=session['username'], accounts=accounts)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            session['username'] = ADMIN_USER
            return redirect(url_for('home'))
        error = "Hibás felhasználónév vagy jelszó!"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # 1. Elindítjuk a bányászt a háttérben (külön szálon)
    # Így a bot fut, de a program megy tovább a weboldalhoz
    miner_thread = threading.Thread(target=start_miner, daemon=True)
    miner_thread.start()

    # 2. Elindítjuk a Flask weboldalt (ez nyitja meg a portot a Rendernek)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

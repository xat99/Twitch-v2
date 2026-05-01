import os
import threading
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
from run import start_miner 

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key_2024')

mongo_url = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/')
client = MongoClient(mongo_url)
db = client['twitch_miner_web']
twitch_data_collection = db['twitch_data']

ADMIN_USER = os.getenv('WEB_USERNAME', 'szaby')
ADMIN_PASS = os.getenv('WEB_PASSWORD', '2003')

@app.route('/')
def home():
    if 'username' in session:
        # Lekérjük az összes adatot
        accounts = list(twitch_data_collection.find({}))
        for acc in accounts:
            acc['_id'] = str(acc['_id'])
            history = acc.get('history', [0])
            acc['current_points'] = history[-1]
            # Kiszámoljuk a változást (diff)
            acc['diff'] = history[-1] - history[-2] if len(history) >= 2 else 0
        
        # SORREND: A legtöbb pontszámú legyen elől (csökkenő sorrend)
        accounts.sort(key=lambda x: x['current_points'], reverse=True)
        
        return render_template('dashboard.html', username=session['username'], accounts=accounts)
    return redirect(url_for('login'))

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
    # A weboldal a háttérben indul
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=port, use_reloader=False))
    flask_thread.daemon = True
    flask_thread.start()
    # A bányász a fő szálon
    start_miner()

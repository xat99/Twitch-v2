import os
from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

client = MongoClient(os.getenv('MONGO_URI', 'mongodb://mongodb:27017/'))
db = client['twitch_miner_web']
users_collection = db['users']
twitch_data_collection = db['twitch_data']

ADMIN_USER = os.getenv('WEB_USERNAME', 'szaby')
ADMIN_PASS = os.getenv('WEB_PASSWORD', '2003')

users_collection.update_one(
    {'username': ADMIN_USER},
    {'$set': {'password': ADMIN_PASS}},
    upsert=True
)

@app.route('/', methods=['GET'])
def home():
    if 'username' in session:
        accounts = []
        all_channels_data = list(twitch_data_collection.find({}))
        
        for data in all_channels_data:
            history = data.get('history', [0])
            current_points = history[-1] if history else 0
            
            if len(history) >= 2:
                diff = history[-1] - history[-2]
            else:
                diff = 0

            accounts.append({
                "channel_name": data.get("channel_name", "Ismeretlen"),
                "current_points": current_points,
                "history": history,
                "diff": diff
            })
            
        return render_template('dashboard.html', username=session['username'], accounts=accounts)
    
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            error = 'Helytelen felhasználónév vagy jelszó!'
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Kiolvassuk a Render által kért portot, de ha nincs, maradunk az 5000-nél
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

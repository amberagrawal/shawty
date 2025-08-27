import os
import string
import random
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from pymongo import MongoClient
from urllib.parse import urlparse
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import bcrypt
from bson.objectid import ObjectId

app = Flask(__name__)

# --- CONFIGURATION ---
# Use environment variables for sensitive data
# For local development, you can set these in your terminal or use a .env file
# For deployment, you will set these in your hosting service's dashboard
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'a-default-fallback-secret-key-for-dev')
CONNECTION_STRING = os.environ.get('MONGO_URI')

# --- Database Connection ---
if not CONNECTION_STRING:
    raise ValueError("No MONGO_URI set for the database connection")

client = MongoClient(CONNECTION_STRING)
db = client['mydatabase']
urls_collection = db['urls']
users_collection = db['users']

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirect to /login if user is not authenticated

class User(UserMixin):
    def __init__(self, username):
        self.username = username
        user_data = users_collection.find_one({"username": username})
        self.id = str(user_data["_id"]) if user_data else None

    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({"_id": user_id})
        if user_data:
            return User(user_data["username"])
        return None

@login_manager.user_loader
def load_user(user_id):
    # In MongoDB, _id is an ObjectId, so we need to convert it
    from bson.objectid import ObjectId
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data['username'])
    return None

# --- Authentication Routes ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if users_collection.find_one({'username': username}):
            flash('Username already exists.', 'danger')
            return redirect(url_for('signup'))
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users_collection.insert_one({'username': username, 'password': hashed_password})
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user_data = users_collection.find_one({'username': username})
        
        if user_data and bcrypt.checkpw(password.encode('utf-8'), user_data['password']):
            user = User(username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- Main Application Routes ---
@app.route('/')
def index():
    return render_template('index.html')

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    if urls_collection.find_one({"short_code": short_code}):
        return generate_short_code()
    return short_code

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('url')
    custom_slug = data.get('custom_slug')

    if not long_url or not urlparse(long_url).scheme:
        return jsonify({'error': 'Invalid URL provided'}), 400

    owner = current_user.username if current_user.is_authenticated else None

    if custom_slug:
        if not owner:
            return jsonify({'error': 'You must be signed in to use a custom name.'}), 403
        if urls_collection.find_one({"short_code": custom_slug}):
            return jsonify({'error': 'That custom name is already taken.'}), 409
        short_code = custom_slug
    else:
        short_code = generate_short_code()

    urls_collection.insert_one({
        "long_url": long_url,
        "short_code": short_code,
        "owner": owner
    })
    
    return jsonify({'short_url': request.host_url + short_code})

@app.route('/<short_code>')
def redirect_to_url(short_code):
    url_entry = urls_collection.find_one({"short_code": short_code})
    if url_entry:
        return redirect(url_entry['long_url'])
    else:
        return "URL not found", 404

# --- API Route for History ---
@app.route('/api/history')
@login_required
def get_history():
    history_data = urls_collection.find({"owner": current_user.username})
    history_list = [
        {"short_code": item["short_code"], "long_url": item["long_url"]}
        for item in history_data
    ]
    return jsonify(history_list)

# --- API Route for Deleting a Link ---
@app.route('/api/delete/<short_code>', methods=['DELETE'])
@login_required
def delete_url(short_code):
    # Find the URL to ensure it belongs to the current user before deleting
    url_to_delete = urls_collection.find_one({"short_code": short_code, "owner": current_user.username})
    
    if not url_to_delete:
        # If the URL doesn't exist or doesn't belong to the user, return an error
        return jsonify({'error': 'URL not found or you do not have permission to delete it.'}), 404
        
    # If the check passes, delete the URL
    urls_collection.delete_one({"_id": url_to_delete["_id"]})
    
    return jsonify({'message': 'URL deleted successfully.'}), 200

if __name__ == '__main__':
    app.run(debug=True)

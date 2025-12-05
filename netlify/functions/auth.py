"""
Netlify Function - Authentication API
"""
import json
import hashlib
import hmac
import os
import time
from urllib.parse import parse_qs

# Simple user storage
USERS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'users.json')
SECRET_KEY = "your-secret-key-prescient-2024"

def ensure_data_dir():
    data_dir = os.path.dirname(USERS_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def load_users():
    ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        default_users = {
            "eiz": {
                "username": "eiz",
                "email": "eiz@prescient.com",
                "password": hash_password("iris"),
                "is_active": True
            }
        }
        save_users(default_users)
        return default_users
    
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    ensure_data_dir()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    salt = b'prescient-salt-2024'
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

def verify_password(plain_password, hashed_password):
    return hash_password(plain_password) == hashed_password

def create_token(username):
    payload = f"{username}:{int(time.time())}"
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{signature}"

def handler(event, context):
    # Handle CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    try:
        data = json.loads(event['body'])
        path = event['path']
        
        if '/login' in path or '/token' in path:
            return handle_login(data)
        elif '/register' in path:
            return handle_register(data)
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({"detail": "Endpoint not found"})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({"detail": str(e)})
        }

def handle_login(data):
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({"detail": "Username and password required"})
        }
    
    users = load_users()
    user = users.get(username)
    
    if not user or not verify_password(password, user['password']):
        return {
            'statusCode': 401,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({"detail": "Username atau password salah"})
        }
    
    token = create_token(username)
    
    response = {
        "access_token": token,
        "token_type": "bearer",
        "username": username
    }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(response)
    }

def handle_register(data):
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    
    if not email or not username or not password:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({"detail": "Email, username, and password required"})
        }
    
    users = load_users()
    
    if username in users:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({"detail": "Username sudah digunakan"})
        }
    
    for user in users.values():
        if user['email'] == email:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({"detail": "Email sudah terdaftar"})
            }
    
    users[username] = {
        "username": username,
        "email": email,
        "password": hash_password(password),
        "is_active": True
    }
    
    save_users(users)
    
    response = {
        "success": True,
        "message": f"Akun berhasil dibuat untuk {username}!",
        "user": {"email": email, "username": username}
    }
    
    return {
        'statusCode': 201,
        'headers': {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(response)
    }

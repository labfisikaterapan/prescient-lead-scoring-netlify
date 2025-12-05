"""
Vercel Serverless Function - Authentication API
Endpoints: /api/auth/login, /api/auth/register
"""

from http.server import BaseHTTPRequestHandler
import json
import hashlib
import hmac
import os
import time
from urllib.parse import urlparse, parse_qs

# Simple user storage (JSON file)
USERS_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')
SECRET_KEY = "your-secret-key-prescient-2024"  # Change in production

def ensure_data_dir():
    """Ensure data directory exists"""
    data_dir = os.path.dirname(USERS_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def load_users():
    """Load users from JSON file"""
    ensure_data_dir()
    if not os.path.exists(USERS_FILE):
        # Create with default users
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
    """Save users to JSON file"""
    ensure_data_dir()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Hash password using PBKDF2-HMAC-SHA256"""
    salt = b'prescient-salt-2024'  # Static salt for simplicity
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000).hex()

def verify_password(plain_password, hashed_password):
    """Verify password"""
    return hash_password(plain_password) == hashed_password

def create_token(username):
    """Create simple JWT-like token"""
    payload = f"{username}:{int(time.time())}"
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}:{signature}"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests for login/register"""
        path = urlparse(self.path).path
        
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            if path == '/api/auth/login' or path == '/auth/token':
                self.handle_login(data)
            elif path == '/api/auth/register':
                self.handle_register(data)
            else:
                self.send_error_response(404, "Endpoint not found")
                
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def handle_login(self, data):
        """Handle login request"""
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            self.send_error_response(400, "Username and password required")
            return
        
        users = load_users()
        user = users.get(username)
        
        if not user or not verify_password(password, user['password']):
            self.send_error_response(401, "Username atau password salah")
            return
        
        # Create token
        token = create_token(username)
        
        response = {
            "access_token": token,
            "token_type": "bearer",
            "username": username
        }
        
        self.send_success_response(response)
    
    def handle_register(self, data):
        """Handle registration request"""
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        
        if not email or not username or not password:
            self.send_error_response(400, "Email, username, and password required")
            return
        
        users = load_users()
        
        # Check if username exists
        if username in users:
            self.send_error_response(400, "Username sudah digunakan")
            return
        
        # Check if email exists
        for user in users.values():
            if user['email'] == email:
                self.send_error_response(400, "Email sudah terdaftar")
                return
        
        # Create new user
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
            "user": {
                "email": email,
                "username": username
            }
        }
        
        self.send_success_response(response, 201)
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_success_response(self, data, code=200):
        """Send success response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error = {"detail": message}
        self.wfile.write(json.dumps(error).encode('utf-8'))

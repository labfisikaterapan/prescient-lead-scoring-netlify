# ============================================================
# PRESCIENT AUTHENTICATION SETUP GUIDE
# ============================================================

## 📋 OVERVIEW
Backend autentikasi lengkap untuk Prescient dengan:
- ✅ User Registration (Email + Username + Password)
- ✅ Login dengan JWT Token
- ✅ Forgot Password dengan Email Reset Link
- ✅ SQLite Database dengan SQLAlchemy
- ✅ Password Hashing (bcrypt)
- ✅ SMTP Gmail Integration

## 🚀 QUICK START

### 1. Install Dependencies
```bash
pip install sqlalchemy python-jose[cryptography] passlib[bcrypt] python-multipart pydantic[email]
```

### 2. Configure Gmail SMTP (PENTING!)

#### Step-by-step:
1. **Enable 2-Step Verification** di akun Gmail Anda:
   - Buka: https://myaccount.google.com/security
   - Aktifkan "2-Step Verification"

2. **Create App Password**:
   - Buka: https://myaccount.google.com/apppasswords
   - Select "Mail" dan "Other (Custom name)"
   - Name: "Prescient"
   - Copy 16-character password yang muncul

3. **Update auth.py**:
   ```python
   # Line 26-27 di auth.py
   EMAIL_USER = "your-email@gmail.com"      # Ganti dengan email Anda
   EMAIL_PASSWORD = "xxxx xxxx xxxx xxxx"   # Paste App Password (16 karakter)
   ```

### 3. Start Server
```bash
python main.py
```

Server akan berjalan di: http://localhost:8000

## 📡 API ENDPOINTS

### 1. Register User
**POST** `/auth/register`

**Request Body:**
```json
{
  "email": "user@gmail.com",
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Akun berhasil dibuat untuk johndoe!",
  "user": {
    "id": 1,
    "email": "user@gmail.com",
    "username": "johndoe"
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@gmail.com","username":"testuser","password":"pass123"}'
```

---

### 2. Login (Get Token)
**POST** `/auth/token`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepass123"
}
```

**Response (Success):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123"}'
```

---

### 3. Forgot Password
**POST** `/auth/forgot-password`

**Request Body:**
```json
{
  "email": "user@gmail.com"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Instruksi reset password telah dikirim ke email Anda.",
  "debug_token": "eyJhbGc..."  // REMOVE IN PRODUCTION
}
```

**Email yang dikirim:**
- Subject: "Prescient - Reset Password Request"
- Berisi: Link reset password dengan token JWT
- Link format: `http://localhost:8000/reset-password?token=...`
- Token expires dalam 1 jam

**cURL Example:**
```bash
curl -X POST http://localhost:8000/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"test@gmail.com"}'
```

---

## 🔐 SECURITY FEATURES

### Password Hashing
- Algorithm: **bcrypt** (industry standard)
- Salt rounds: Auto-generated per password
- Plain passwords NEVER disimpan di database

### JWT Tokens
- Algorithm: **HS256**
- Secret Key: `prescient-secret-key-change-this-in-production-2024`
  - ⚠️ **GANTI SECRET KEY DI PRODUCTION!**
- Token expiry: 24 jam (login), 1 jam (reset password)

### Database
- Engine: **SQLite** (file: `prescient.db`)
- ORM: **SQLAlchemy**
- Schema:
  ```sql
  CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
  );
  ```

---

## 🌐 FRONTEND INTEGRATION

### JavaScript Fetch Examples

#### 1. Register Form Integration
```javascript
// Update register-form submit handler
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('reg-email').value;
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    
    const btn = e.target.querySelector('button');
    btn.innerText = 'Mendaftar...';
    btn.disabled = true;
    
    try {
        const response = await fetch('http://localhost:8000/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(`✅ ${data.message}`);
            // Redirect to login
            registerView.classList.add('hidden');
            loginView.classList.remove('hidden');
        } else {
            alert(`❌ Error: ${data.detail}`);
        }
    } catch (error) {
        alert('❌ Gagal menghubungi server: ' + error.message);
    } finally {
        btn.innerText = 'Daftar Akun';
        btn.disabled = false;
    }
});
```

#### 2. Login Form Integration
```javascript
// Update login-form submit handler
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    try {
        const response = await fetch('http://localhost:8000/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Save token
            localStorage.setItem('access_token', data.access_token);
            
            // Redirect to dashboard
            authContainer.classList.add('hidden');
            dashboardContainer.classList.remove('hidden');
            initDashboard();
        } else {
            const err = document.getElementById('login-error');
            err.classList.remove('hidden');
            setTimeout(() => err.classList.add('hidden'), 3000);
        }
    } catch (error) {
        alert('❌ Gagal login: ' + error.message);
    }
});
```

#### 3. Forgot Password Form Integration
```javascript
// Update forgot-form submit handler
document.getElementById('forgot-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = e.target.querySelector('input[type="email"]').value;
    const btn = e.target.querySelector('button');
    
    btn.innerText = 'Mengirim...';
    btn.disabled = true;
    
    try {
        const response = await fetch('http://localhost:8000/auth/forgot-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(`✅ ${data.message}\n\nPesan telah dikirim ke: ${email}`);
            // Back to login
            forgotView.classList.add('hidden');
            loginView.classList.remove('hidden');
        } else {
            alert(`❌ Error: ${data.detail}`);
        }
    } catch (error) {
        alert('❌ Gagal mengirim email: ' + error.message);
    } finally {
        btn.innerText = 'Kirim Instruksi';
        btn.disabled = false;
    }
});
```

---

## 📧 EMAIL TEMPLATE

Email yang dikirim menggunakan HTML template dengan:
- 🎨 Dark theme matching Prescient branding
- 🔗 Clickable reset button
- ⏰ Token expiry warning (1 jam)
- 🔐 Security notice

Preview email: Lihat kode di `auth.py` line 124-163

---

## 🧪 TESTING

### Test dengan cURL

```bash
# 1. Register user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@gmail.com","username":"testuser","password":"test123"}'

# 2. Login
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test123"}'

# 3. Forgot password
curl -X POST http://localhost:8000/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email":"test@gmail.com"}'
```

### Test dengan Browser
1. Buka: http://localhost:8000/docs
2. Ekspansi endpoint yang ingin ditest
3. Click "Try it out"
4. Masukkan data
5. Click "Execute"

---

## ⚠️ PRODUCTION CHECKLIST

Sebelum deploy ke production:

- [ ] Ganti `SECRET_KEY` di `auth.py` dengan random string 32+ karakter
- [ ] Set `EMAIL_USER` dan `EMAIL_PASSWORD` dari environment variables
- [ ] Ganti SQLite dengan PostgreSQL/MySQL untuk production
- [ ] Remove `debug_token` dari forgot-password response
- [ ] Enable HTTPS untuk API endpoint
- [ ] Set proper CORS origins (jangan `*`)
- [ ] Implement rate limiting untuk prevent spam
- [ ] Add email verification untuk registration
- [ ] Implement password reset confirmation page

---

## 🐛 TROUBLESHOOTING

### Error: "SMTPAuthenticationError"
**Solusi:**
- Pastikan 2-Step Verification aktif di Gmail
- Gunakan App Password, bukan password Gmail biasa
- Cek EMAIL_USER dan EMAIL_PASSWORD sudah benar

### Error: "Email already registered"
**Solusi:**
- Email sudah pernah digunakan
- Gunakan email lain atau login dengan akun existing

### Error: "Database locked"
**Solusi:**
- Tutup semua koneksi database
- Restart server
- Jika persist, hapus `prescient.db` dan restart (data hilang!)

### Email tidak terkirim
**Solusi:**
- Cek koneksi internet
- Cek SMTP credentials di `auth.py`
- Cek email di folder Spam
- Enable "Less secure app access" di Gmail (jika perlu)

---

## 📁 FILE STRUCTURE

```
prescient-app/
├── main.py                  # Main FastAPI app (updated)
├── database.py              # Database models & config
├── auth.py                  # Auth utilities (JWT, hashing, email)
├── auth_routes.py           # Auth endpoints (register, login, forgot)
├── requirements_auth.txt    # Authentication dependencies
├── prescient.db             # SQLite database (auto-created)
└── static/
    └── index.html          # Frontend (to be updated)
```

---

## 🎯 NEXT STEPS

1. **Install dependencies:** `pip install -r requirements_auth.txt`
2. **Configure Gmail:** Update EMAIL_USER & EMAIL_PASSWORD di `auth.py`
3. **Test endpoints:** Gunakan cURL atau Postman
4. **Update frontend:** Integrate JavaScript fetch code ke `index.html`
5. **Test email:** Kirim forgot password request

---

## 📞 SUPPORT

Issues? Contact:
- GitHub: Rivaldy-25-Lval
- Project: Prescient - Predictive Lead Scoring

---

**Last Updated:** December 4, 2025
**Version:** 1.0.0

# 🚀 DEPLOYMENT GUIDE - Prescient AI

## ✅ Step 1: Push ke GitHub

### A. Buat Repository di GitHub (MANUAL)
1. Buka https://github.com/new
2. Repository name: `Prescient-AI`
3. Description: `AI-Powered Lead Scoring System`
4. **Public** atau **Private** (pilih sesuai kebutuhan)
5. ❌ **JANGAN** centang "Add README" (sudah ada)
6. Klik **Create repository**

### B. Push dari Local
```bash
cd "C:\Users\mriva\OneDrive\Desktop\Website AI\Capstone web\prescient-app"

# Sudah dijalankan:
git init
git add .
git commit -m "Initial commit: Prescient AI - Lead Scoring System"
git branch -M main
git remote add origin https://github.com/Rivaldy-25-Lval/Prescient-AI.git

# Jalankan ini setelah repository dibuat di GitHub:
git push -u origin main
```

## 🌐 Step 2: Deploy Online

### Option 1: Render.com (RECOMMENDED - FREE)

#### A. Prepare Files

**1. Create `render.yaml`** (sudah dibuat otomatis):
```yaml
services:
  - type: web
    name: prescient-ai
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.16
```

**2. Pastikan `requirements.txt` lengkap**

#### B. Deploy Steps
1. Buka https://render.com (sign up gratis)
2. Klik **New** → **Web Service**
3. Connect GitHub repository: `Rivaldy-25-Lval/Prescient-AI`
4. Settings:
   - **Name**: `prescient-ai`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`
5. Klik **Create Web Service**
6. Tunggu ~5 menit untuk build
7. URL: `https://prescient-ai.onrender.com`

### Option 2: Railway.app (FREE dengan GitHub Student Pack)

1. Buka https://railway.app
2. Sign in dengan GitHub
3. **New Project** → **Deploy from GitHub repo**
4. Pilih `Prescient-AI`
5. Railway auto-detect Python dan deploy
6. Domain otomatis: `prescient-ai.up.railway.app`

### Option 3: Heroku (Paid setelah trial)

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Create app
heroku create prescient-ai

# Add buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open
heroku open
```

### Option 4: PythonAnywhere (FREE dengan limit)

1. Buka https://www.pythonanywhere.com
2. Sign up gratis
3. Upload files atau clone dari GitHub
4. Setup web app dengan WSGI
5. Domain: `yourusername.pythonanywhere.com`

## 📝 Files untuk Deployment

### `render.yaml` (Render-specific)
```yaml
services:
  - type: web
    name: prescient-ai
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
```

### `Procfile` (Heroku-specific)
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### `runtime.txt` (Optional - specify Python version)
```
python-3.9.16
```

## ⚙️ Environment Variables (Production)

Set di deployment platform:
```
SECRET_KEY=your-secret-key-here-generate-random
DATABASE_URL=postgresql://...  # jika pakai PostgreSQL
ALLOWED_HOSTS=prescient-ai.onrender.com
```

## 🎯 Post-Deployment

1. **Test URL**: `https://your-app.onrender.com`
2. **Login**: `eiz` / `iris`
3. **Check API**: `https://your-app.onrender.com/docs`

## 📊 Monitoring

- **Render**: Dashboard → Logs
- **Railway**: Project → Deployments → Logs
- **Heroku**: `heroku logs --tail`

## 🔒 Security Checklist

- [ ] Change default credentials
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS (otomatis di Render/Railway)
- [ ] Limit CORS origins di production
- [ ] Add rate limiting

## 📞 Support

Jika ada masalah:
1. Check logs di deployment platform
2. Verify `requirements.txt` complete
3. Test local: `uvicorn main:app --reload`
4. Check GitHub Actions (jika pakai CI/CD)

---

## 🎉 QUICK DEPLOY CHECKLIST

- [x] Git init & commit
- [ ] Create GitHub repository
- [ ] Push to GitHub
- [ ] Choose deployment platform
- [ ] Deploy & test
- [ ] Share URL! 🚀

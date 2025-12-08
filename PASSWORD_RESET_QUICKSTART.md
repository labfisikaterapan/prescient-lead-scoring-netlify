# 🚀 Quick Start - Password Reset Setup

## ⚡ 3 Langkah Setup (5 Menit)

### 1️⃣ Buat Gmail App Password
1. Buka https://myaccount.google.com/security
2. Aktifkan **2-Step Verification**
3. Cari **"App passwords"** → Generate baru
4. App name: `Prescient` → Generate
5. **Copy 16-digit password** (contoh: `abcd efgh ijkl mnop`)

### 2️⃣ Set Environment Variables di Netlify
1. Login https://app.netlify.com
2. Pilih site → **Site settings** → **Environment variables**
3. Add 3 variables:
   ```
   EMAIL_USER = yourapp@gmail.com
   EMAIL_PASS = abcd efgh ijkl mnop
   JWT_SECRET = prescient-secret-key-2024-change-this
   ```
4. **Save** semua

### 3️⃣ Redeploy
1. Tab **Deploys** → **Trigger deploy** → **Deploy site**
2. Tunggu 1-2 menit
3. ✅ **Selesai!**

---

## 🧪 Test Fitur

1. Buka site Anda
2. Klik **"Lupa Password"**
3. Input email: `lab.fisikaterapan@untirta.ac.id`
4. Klik **"Kirim Instruksi"**
5. Cek inbox email → Klik link reset
6. Buat password baru
7. Login dengan password baru ✅

---

## 📖 Full Documentation

Lihat **ENV_VARIABLES_SETUP.md** untuk:
- Troubleshooting lengkap
- Security best practices
- Email template preview
- Function logs debugging

---

## 🔧 Local Development

```bash
# Install dependencies
npm install

# Run locally (with Netlify Dev)
netlify dev
```

Buka: http://localhost:8888

**Note:** Untuk test email local, set env variables di terminal:
```bash
$env:EMAIL_USER="your@gmail.com"
$env:EMAIL_PASS="your-app-password"
$env:JWT_SECRET="local-secret"
netlify dev
```

---

**Need Help?** Check ENV_VARIABLES_SETUP.md atau Netlify Function Logs!

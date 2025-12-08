# 🔐 SECURE PASSWORD RESET - Environment Variables Setup

## 📋 Environment Variables yang Diperlukan

Untuk mengaktifkan fitur "Lupa Password" dengan email, Anda perlu mengatur **3 Environment Variables** di Netlify Dashboard:

### 1. EMAIL_USER
- **Nilai:** Alamat Gmail Anda (contoh: `yourapp@gmail.com`)
- **Fungsi:** Pengirim email reset password

### 2. EMAIL_PASS
- **Nilai:** Gmail App Password (BUKAN password Gmail biasa!)
- **Fungsi:** Autentikasi SMTP untuk mengirim email
- **⚠️ PENTING:** Ini adalah App Password khusus, bukan password login Gmail Anda

### 3. JWT_SECRET
- **Nilai:** String rahasia untuk signing token (contoh: `prescient-super-secret-key-2024`)
- **Fungsi:** Mengamankan reset token agar tidak bisa dipalsukan
- **Tips:** Gunakan string random yang panjang (minimal 32 karakter)

### 4. SITE_URL (Optional)
- **Nilai:** URL produksi Anda (contoh: `https://prescient-lead-scoring.netlify.app`)
- **Fungsi:** Base URL untuk link reset password
- **Note:** Jika tidak diatur, akan otomatis terdeteksi

---

## 🔧 Cara Setting di Netlify Dashboard

### Step 1: Buat Gmail App Password

1. **Buka Gmail** Anda
2. **Klik foto profil** (kanan atas) → **Manage your Google Account**
3. **Pilih "Security"** di menu kiri
4. **Aktifkan 2-Step Verification** (jika belum)
5. **Cari "App passwords"** di search bar
6. **Klik "App passwords"**
7. **Generate password baru:**
   - App name: `Prescient Lead Scoring`
   - Device: `Other`
8. **Copy 16-digit password** yang muncul (contoh: `abcd efgh ijkl mnop`)
9. **Simpan** password ini dengan aman!

### Step 2: Set Environment Variables di Netlify

1. **Login ke Netlify** (https://app.netlify.com)
2. **Pilih site** Anda: `prescient-lead-scoring-netlify`
3. **Klik "Site settings"** (tab paling kanan)
4. **Scroll ke "Environment variables"** di menu kiri
5. **Klik "Add a variable"**
6. **Tambahkan 3 variables:**

   ```
   Key: EMAIL_USER
   Value: yourapp@gmail.com
   Scopes: Same value for all deploy contexts
   ```

   ```
   Key: EMAIL_PASS
   Value: abcd efgh ijkl mnop (16-digit App Password dari Gmail)
   Scopes: Same value for all deploy contexts
   ```

   ```
   Key: JWT_SECRET
   Value: prescient-super-secret-key-change-this-to-random-string-2024
   Scopes: Same value for all deploy contexts
   ```

7. **Klik "Save"** untuk setiap variable
8. **Redeploy site** agar environment variables aktif:
   - Klik tab "Deploys"
   - Klik "Trigger deploy" → "Deploy site"

---

## ✅ Cara Test Fitur Reset Password

### Test 1: Request Reset Email

1. **Buka aplikasi** Anda di browser
2. **Klik "Lupa Password"** di halaman login
3. **Masukkan email** yang terdaftar (contoh: `lab.fisikaterapan@untirta.ac.id`)
4. **Klik "Kirim Instruksi"**
5. **Periksa inbox email** Anda
6. **Buka email** dengan subject "🔐 Reset Password - Prescient Lead Scoring"

### Test 2: Reset Password

1. **Klik tombol "Reset Password Sekarang"** di email
2. **Atau copy link** dan paste ke browser
3. **Masukkan password baru** (minimal 5 karakter)
4. **Konfirmasi password**
5. **Klik "Reset Password"**
6. **Login dengan password baru** di halaman utama

---

## 🐛 Troubleshooting

### Problem: Email tidak terkirim

**Solusi 1: Periksa Environment Variables**
- Pastikan `EMAIL_USER` dan `EMAIL_PASS` sudah benar
- Pastikan tidak ada spasi di awal/akhir value
- Redeploy site setelah menambah variables

**Solusi 2: Periksa Gmail App Password**
- Pastikan menggunakan App Password, bukan password Gmail biasa
- Generate ulang App Password jika perlu
- Pastikan 2-Step Verification aktif

**Solusi 3: Periksa Function Logs**
- Buka Netlify Dashboard → Site → Functions → Logs
- Cari error message dari `send-reset` function
- Periksa console.log untuk debugging

### Problem: Token expired

**Penyebab:** Link reset password berlaku 1 jam
**Solusi:** Request ulang reset password dari halaman login

### Problem: Token tidak valid

**Penyebab:** JWT_SECRET berbeda atau token rusak
**Solusi:** 
- Pastikan JWT_SECRET tidak berubah
- Request ulang reset password

---

## 🔒 Security Best Practices

### ✅ DO:
- Gunakan Gmail App Password (bukan password asli)
- Gunakan JWT_SECRET yang panjang dan random
- Simpan Environment Variables di Netlify (jangan di code)
- Gunakan HTTPS untuk produksi
- Set token expiry (default: 1 jam)

### ❌ DON'T:
- Jangan commit password/secret ke Git
- Jangan share Environment Variables
- Jangan gunakan JWT_SECRET yang mudah ditebak
- Jangan expose token di response (production)

---

## 📁 File Structure

```
prescient-app/
├── netlify/
│   └── functions/
│       ├── send-reset.js          # Send reset email
│       └── reset-password.js      # Verify token & update password
├── static/
│   ├── index.html                 # Main app (updated forgot handler)
│   └── reset-password.html        # Reset password page (NEW)
├── data/
│   └── users.json                 # User database (localStorage simulation)
├── package.json                   # Dependencies
├── netlify.toml                   # Netlify config
└── ENV_VARIABLES_SETUP.md         # This file
```

---

## 🚀 Deploy Commands

### Install Dependencies
```bash
npm install
```

### Test Locally
```bash
netlify dev
```
Buka: http://localhost:8888

### Deploy to Production
```bash
# Option 1: Git push (auto-deploy)
git add .
git commit -m "Add secure password reset with email"
git push

# Option 2: Manual deploy
netlify deploy --prod
```

---

## 📧 Email Template Preview

Email yang dikirim akan terlihat seperti ini:

```
Subject: 🔐 Reset Password - Prescient Lead Scoring

Halo, [USERNAME]!

Kami menerima permintaan untuk mereset password akun Anda di Prescient Lead Scoring.

[Reset Password Sekarang] (Button)

Atau copy link berikut:
https://your-site.netlify.app/reset-password.html?token=eyJhbGc...

⚠️ Link ini hanya berlaku selama 1 jam.

Email ini dikirim secara otomatis oleh sistem.
© 2025 Lab Fisika Terapan - Untirta
```

---

## 📞 Support

Jika mengalami masalah, periksa:

1. **Function Logs** di Netlify Dashboard
2. **Browser Console** (F12) untuk error frontend
3. **Email Spam Folder** jika email tidak masuk inbox
4. **Environment Variables** apakah sudah benar

---

**Happy Coding! 🎉**

*Generated for Prescient Lead Scoring Application*
*Lab Fisika Terapan - Universitas Sultan Ageng Tirtayasa*

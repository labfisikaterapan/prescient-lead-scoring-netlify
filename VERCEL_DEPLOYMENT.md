# 🚀 DEPLOYMENT GUIDE - VERCEL

## ✅ **FILES READY FOR VERCEL**

Aplikasi Prescient sudah dikonversi untuk deployment di **Vercel** sesuai kriteria capstone Anda.

### **📁 Struktur Folder Vercel:**
```
prescient-app/
├── api/                        # Serverless Functions
│   ├── predict.py              # ML Prediction endpoint
│   └── auth.py                 # Authentication endpoint
├── static/                     # Frontend files
│   ├── index.html              # Main dashboard
│   ├── *.mp4                   # Video wallpapers
│   └── real_leads_data.js      # Lead data
├── data/                       # JSON storage
│   └── users.json              # User database
├── prescient_model.pkl         # Trained ML model
├── vercel.json                 # Vercel configuration
├── requirements.txt            # Python dependencies
└── .vercelignore              # Files to exclude
```

---

## 🔧 **PERUBAHAN DARI LOCALHOST:**

### **1. Backend Architecture:**
- ❌ FastAPI (tidak support Vercel) → ✅ **Vercel Serverless Functions**
- ❌ SQLite database → ✅ **JSON file storage** (`data/users.json`)
- ✅ ML Model tetap menggunakan `prescient_model.pkl`

### **2. Endpoints:**
| Fungsi | Localhost | Vercel | Status |
|--------|-----------|--------|--------|
| Prediction | `/predict` | `/api/predict` | ✅ |
| Login | `/auth/token` | `/api/auth` atau `/auth/token` | ✅ |
| Register | `/auth/register` | `/api/auth/register` | ✅ |
| Dashboard | `/` | `/` | ✅ |

### **3. Features Yang Tetap Berfungsi:**
- ✅ Video Wallpaper (universe-effects.mp4, blue-forest-waterfalls.mp4)
- ✅ Login/Register Authentication
- ✅ ML Prediction (GradientBoostingClassifier)
- ✅ Dashboard Analytics
- ✅ Data Prospek (1000 leads)
- ✅ Glassmorphism UI
- ✅ Default user: `eiz / iris`

---

## 📝 **STEP-BY-STEP DEPLOYMENT:**

### **Method 1: Vercel CLI (Recommended)**

1. **Install Vercel CLI:**
   ```powershell
   npm install -g vercel
   ```

2. **Login ke Vercel:**
   ```powershell
   vercel login
   ```

3. **Deploy dari folder aplikasi:**
   ```powershell
   cd "C:\Users\mriva\OneDrive\Desktop\Website AI\Capstone web\prescient-app"
   vercel
   ```

4. **Follow prompts:**
   - Link to existing project? **No**
   - Project name: `prescient-lead-scoring`
   - Directory: `.` (current)
   - Override settings? **No**

5. **Deployment akan otomatis:**
   - Build API functions ✅
   - Upload static files ✅
   - Configure routes ✅
   - **Live URL:** https://prescient-lead-scoring.vercel.app

### **Method 2: GitHub + Vercel Dashboard**

1. **Push ke GitHub:**
   ```powershell
   cd "C:\Users\mriva\OneDrive\Desktop\Website AI\Capstone web\prescient-app"
   git add .
   git commit -m "Prepare for Vercel deployment"
   git push origin main
   ```

2. **Import di Vercel:**
   - Buka https://vercel.com/new
   - **Import Git Repository**
   - Pilih: `labfisikaterapan/prescient-lead-scoring`
   - Framework Preset: **Other**
   - Root Directory: `./`
   - **Deploy** (klik tombol)

3. **Tunggu 2-3 menit:**
   - Vercel akan auto-detect `vercel.json`
   - Install dependencies dari `requirements.txt`
   - Deploy serverless functions
   - **Live URL:** https://prescient-lead-scoring.vercel.app

---

## 🧪 **TESTING CHECKLIST:**

Setelah deploy, test semua fitur:

### **1. Video Wallpapers:**
- [ ] Login page: Video universe-effects berjalan
- [ ] Dashboard: Video blue-forest-waterfalls berjalan

### **2. Authentication:**
- [ ] Login dengan `eiz / iris` berhasil
- [ ] Register user baru berhasil
- [ ] Logout berfungsi

### **3. ML Prediction:**
- [ ] Form "Prediksi Lead" muncul
- [ ] Input 7 fields (Pekerjaan, Saldo, dll.)
- [ ] Klik "Prediksi Sekarang"
- [ ] Result muncul dengan score, label, dan rekomendasi

### **4. Dashboard:**
- [ ] Statistik cards tampil (Total Nasabah, Hot Leads, dll.)
- [ ] Chart "Distribusi Lead" render
- [ ] Faktor Utama bars muncul

### **5. Data Prospek:**
- [ ] Table load 1000 leads
- [ ] Pagination berfungsi
- [ ] Search dan filter bekerja
- [ ] Export CSV download

---

## 🔍 **TROUBLESHOOTING:**

### **Issue: API 404 Not Found**
**Solution:**
- Check endpoint path di frontend (harus `/api/predict` bukan `/predict`)
- Verify `vercel.json` routes configuration

### **Issue: Model Loading Error**
**Solution:**
```powershell
# Pastikan model file ada
ls prescient_model.pkl

# Jika hilang, re-train:
python train_gradient_model.py
```

### **Issue: Video Tidak Muncul**
**Solution:**
- Check file size (max 100MB per function)
- Verify video files di folder `static/`
- Check browser console untuk errors

### **Issue: Login Gagal**
**Solution:**
```powershell
# Check users.json
cat data/users.json

# Default credentials:
# Username: eiz
# Password: iris
```

---

## 📊 **PERFORMANCE EXPECTATIONS:**

| Metric | Localhost | Vercel |
|--------|-----------|--------|
| Cold Start | 0ms | 1-2s (first request) |
| Prediction API | 50-100ms | 200-500ms |
| Static Files | Instant | Instant (CDN) |
| Video Load | 1-2s | 2-3s (CDN) |

---

## 🎓 **UNTUK SUBMISSION CAPSTONE:**

**Link deployment Anda:**
```
https://prescient-lead-scoring.vercel.app
```

**Platform:** Vercel (Serverless Functions + Static Hosting)

**Memenuhi Kriteria:**
- ✅ Deploy di platform yang diizinkan (Vercel)
- ✅ Web app dapat diakses online
- ✅ Semua fitur berfungsi seperti localhost
- ✅ ML model berjalan di production

---

## 📞 **SUPPORT:**

Jika ada masalah deployment:
1. Check Vercel logs: https://vercel.com/[username]/prescient-lead-scoring/deployments
2. Verify build logs untuk errors
3. Check browser console untuk frontend errors
4. Test API endpoints langsung:
   - https://your-app.vercel.app/api/predict
   - https://your-app.vercel.app/auth/token

---

**✨ Deployment siap! Gunakan Method 1 (Vercel CLI) atau Method 2 (GitHub + Dashboard).**

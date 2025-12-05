# 🚀 Quick Start Guide

## Langkah 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Langkah 2: Verifikasi Model

Model `prescient_model.pkl` sudah tersedia. Jika ingin training ulang:

```bash
python train_model.py
```

## Langkah 3: Jalankan Server

```bash
python main.py
```

Server akan running di: **http://localhost:8000**

## Langkah 4: Akses Dashboard

- Buka `static/index.html` di browser
- Atau gunakan Live Server di VS Code

## Langkah 5: Test API

Buka Swagger UI: **http://localhost:8000/docs**

---

## Testing Prediksi

### Contoh Request (Hot Lead):
```json
{
  "age": 45,
  "job": "management",
  "marital": "married",
  "education": "tertiary",
  "default": "no",
  "balance": 5000.0,
  "housing": "yes",
  "loan": "no",
  "contact": "cellular",
  "day": 20,
  "month": "may",
  "duration": 450,
  "campaign": 1,
  "pdays": -1,
  "previous": 0,
  "poutcome": "success"
}
```

### Contoh Request (Cold Lead):
```json
{
  "age": 25,
  "job": "student",
  "marital": "single",
  "education": "secondary",
  "default": "no",
  "balance": 50.0,
  "housing": "no",
  "loan": "no",
  "contact": "unknown",
  "day": 5,
  "month": "may",
  "duration": 30,
  "campaign": 5,
  "pdays": -1,
  "previous": 0,
  "poutcome": "failure"
}
```

---

## Troubleshooting

### Port 8000 sudah digunakan?
Ubah port di `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### CORS Error?
Pastikan server running dan CORS middleware enabled.

### Model error?
Re-run training: `python train_model.py`

---

**Selamat! Sistem Prescient siap digunakan! 🎉**

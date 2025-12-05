# Quick Test Guide - API Integration

## ✅ Server Status
Server is running on: **http://127.0.0.1:8000**

---

## 🧪 Testing Steps

### 1. Open the Application
Navigate to: **http://127.0.0.1:8000/**

### 2. Login
- Username: `eiz`
- Password: `iris`

### 3. What to Expect

#### Initial Load:
- You'll see "Loading predictions..." in the table briefly
- After 1-2 seconds, real prediction scores will appear

#### Prediction Scores:
- 🟢 **Green (Hot Lead)**: Score > 80% - High conversion probability
- 🟡 **Yellow (Warm Lead)**: Score 50-80% - Medium conversion probability  
- 🔴 **Red (Cold Lead)**: Score < 50% - Low conversion probability

#### Stats Dashboard:
- **Total Leads**: Shows 150 immediately
- **Hot Leads**: Shows "Loading..." then updates after ~3 seconds

---

## 🔍 Verification Checklist

✅ **Visual Checks:**
1. Scores are displayed as percentages (e.g., "85%", "42%", "91%")
2. Colors match score ranges (green/yellow/red)
3. No "NaN" or "undefined" values in the table
4. Pagination works correctly (10 leads per page)

✅ **Console Checks (F12):**
1. Open Browser DevTools (F12)
2. Go to "Console" tab
3. Look for successful API calls: `POST http://127.0.0.1:8000/predict 200`
4. No red error messages

✅ **Network Checks (F12):**
1. Go to "Network" tab in DevTools
2. Filter by "Fetch/XHR"
3. You should see multiple `/predict` requests
4. Each should return Status: 200 OK
5. Response body should contain: `prediction_score`, `label`, `recommendation`

---

## 🎯 Sample API Call (For Manual Testing)

You can test the API directly using PowerShell:

```powershell
$body = @{
    age = 35
    job = "management"
    marital = "married"
    education = "tertiary"
    default = "no"
    balance = 1500
    housing = "yes"
    loan = "no"
    contact = "cellular"
    day = 15
    month = "may"
    duration = 300
    campaign = 2
    pdays = -1
    previous = 0
    poutcome = "unknown"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" -Method POST -Body $body -ContentType "application/json"
$response | ConvertTo-Json
```

**Expected Output:**
```json
{
  "prediction_score": 0.8542,
  "label": "Hot Lead",
  "probability_percentage": "85.42%",
  "recommendation": "PRIORITAS TINGGI: Segera hubungi nasabah ini! Potensi konversi sangat tinggi."
}
```

---

## 🐛 Troubleshooting

### Issue: Scores show "Loading..." forever
**Fix:** 
- Check browser console for errors
- Verify server is running: `Get-NetTCPConnection -LocalPort 8000`
- Check CORS settings in `main.py`

### Issue: All scores are 50% / "Unknown"
**Fix:**
- API calls are failing
- Check if model file exists: `prescient_model.pkl`
- Review server terminal for errors

### Issue: "Connection Refused" errors
**Fix:**
- Server might have stopped
- Restart server: `python main.py`
- Check firewall settings

---

## 📊 Performance Expectations

- **Page Load Time**: 1-3 seconds (includes 10 API calls)
- **Pagination Switch**: 1-2 seconds per page
- **Total Leads**: 150 (15 pages × 10 leads)
- **API Response Time**: ~100-200ms per prediction

---

## 🎉 Success Indicators

1. ✅ Scores are displayed as percentages
2. ✅ Colors correctly represent Hot/Warm/Cold leads
3. ✅ Stats update after initial load
4. ✅ No console errors
5. ✅ Smooth pagination between pages
6. ✅ Realistic score distribution (not all random)

---

**Last Updated**: November 2024  
**Server Status**: ✅ Running on port 8000

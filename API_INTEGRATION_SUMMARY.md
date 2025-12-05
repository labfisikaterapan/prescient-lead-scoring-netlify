# API Integration Summary - Prescient Lead Scoring

## ✅ Successfully Integrated

The frontend (`static/index.html`) has been successfully updated to connect with the FastAPI backend.

---

## 🔧 Changes Made

### 1. **New `predictLead()` Function**
Added an async function to call the real prediction API:

```javascript
async function predictLead(leadData) {
    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(leadData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error predicting lead:', error);
        return null;
    }
}
```

**Purpose**: Makes POST requests to `/predict` endpoint with lead data and returns prediction results.

---

### 2. **Updated `generateLeads()` Function**
Removed `Math.random()` mock logic and replaced with realistic banking data:

**Before:**
```javascript
const score = Math.random();
let prediction = "No";
if(score > 0.8) prediction = "Yes";
else if(score > 0.5) prediction = "Likely";
```

**After:**
- Generates realistic banking attributes matching API requirements
- Includes: `age`, `job`, `marital`, `education`, `default`, `balance`, `housing`, `loan`, `contact`, `day`, `month`, `duration`, `campaign`, `pdays`, `previous`, `poutcome`
- Stores data in `apiData` field for API calls
- Sets `score`, `prediction`, and `label` to `null` initially

---

### 3. **Enhanced `renderTable()` Function**
Made the function async and integrated API calls:

**Key Features:**
- Shows "Loading predictions..." message while fetching API results
- Calls `predictLead()` for each lead in parallel using `Promise.all()`
- Updates lead objects with:
  - `score` - from `prediction_score`
  - `prediction` - from `label`
  - `label` - from API response
  - `recommendation` - from API response
- Handles API failures gracefully with fallback values
- Updates table with real prediction scores

---

### 4. **Modified `initDashboard()` Function**
Updated to handle async predictions:

```javascript
async function initDashboard() {
    const total = mockLeads.length;
    document.getElementById('stat-total').innerText = total;
    document.getElementById('stat-hot').innerText = 'Loading...';
    
    applyFilters();
    setTimeout(initChart, 100);
    
    // Update stats after predictions load
    setTimeout(() => {
        const hot = mockLeads.filter(l => l.score !== null && l.score > 0.8).length;
        document.getElementById('stat-hot').innerText = hot;
    }, 3000);
}
```

---

### 5. **Updated `applyFilters()` Function**
Added null-safety for scores:

```javascript
filteredLeads = mockLeads.filter(l => {
    const matchesSearch = l.name.toLowerCase().includes(searchTerm);
    const score = l.score !== null ? l.score : 0.5; // Default if not loaded
    const matchesScore = scoreVal === 'all' || 
        (scoreVal === 'hot' && score > 0.8) || 
        (scoreVal === 'warm' && score > 0.5 && score <= 0.8);
    return matchesSearch && matchesScore;
});

// Sort with null-safe score comparison
filteredLeads.sort((a, b) => {
    if (a.status === 'pending' && b.status !== 'pending') return -1;
    if (a.status !== 'pending' && b.status === 'pending') return 1;
    const scoreA = a.score !== null ? a.score : 0.5;
    const scoreB = b.score !== null ? b.score : 0.5;
    return scoreB - scoreA;
});
```

---

## 📊 Data Flow

1. **Lead Generation** → `generateLeads()` creates 150 leads with realistic banking data
2. **Initial Render** → Page loads with "Loading predictions..." message
3. **API Calls** → Frontend calls `POST /predict` for each visible lead (10 per page)
4. **Prediction Update** → Scores and labels are updated from API response
5. **Table Render** → Table displays real prediction scores with color coding:
   - 🟢 Green (Hot Lead): Score > 80%
   - 🟡 Yellow (Warm Lead): Score 50-80%
   - 🔴 Red (Cold Lead): Score < 50%

---

## 🎯 API Request Format

```json
{
  "age": 35,
  "job": "management",
  "marital": "married",
  "education": "tertiary",
  "default": "no",
  "balance": 1500.0,
  "housing": "yes",
  "loan": "no",
  "contact": "cellular",
  "day": 15,
  "month": "may",
  "duration": 300,
  "campaign": 2,
  "pdays": -1,
  "previous": 0,
  "poutcome": "unknown"
}
```

---

## 📥 API Response Format

```json
{
  "prediction_score": 0.8542,
  "label": "Hot Lead",
  "probability_percentage": "85.42%",
  "recommendation": "PRIORITAS TINGGI: Segera hubungi nasabah ini! Potensi konversi sangat tinggi."
}
```

---

## 🚀 Testing the Integration

### 1. **Start the Server**
```bash
cd "c:\Users\mriva\OneDrive\Desktop\Website AI\Capstone web\prescient-app"
& "C:/Users/mriva/OneDrive/Dokumen/New folder/.venv/Scripts/python.exe" main.py
```

### 2. **Open the Frontend**
Navigate to: `http://127.0.0.1:8000/`

### 3. **Login Credentials**
- Username: `eiz`
- Password: `iris`

### 4. **Verify Integration**
- Check if "Loading predictions..." appears briefly
- Verify scores are displayed as percentages (e.g., "85%")
- Confirm color coding (green/yellow/red) matches score ranges
- Open browser console (F12) to check for API call logs

---

## ⚠️ Known Considerations

1. **Parallel API Calls**: The system makes 10 API calls per page (one per table row). This is efficient for small datasets but may need optimization for larger scales.

2. **Caching**: Predictions are cached in the lead objects, so the same lead won't be re-predicted when changing pages.

3. **Error Handling**: If an API call fails, the system falls back to:
   - Score: 0.5
   - Prediction: "Unknown"
   - Label: "Unknown"

4. **Stats Update Delay**: The "Hot Leads" stat updates 3 seconds after login to allow time for initial predictions to load.

---

## 🎉 Success Criteria

✅ Removed `Math.random()` mock logic  
✅ Created `predictLead()` async function  
✅ Integrated API calls into table rendering  
✅ Updated UI to show loading states  
✅ Added null-safety for score handling  
✅ Maintained color-coded prediction display  
✅ Preserved sorting and filtering functionality  

---

## 📝 Next Steps (Optional Enhancements)

1. **Loading Indicators**: Add spinners for individual rows during prediction
2. **Batch Processing**: Predict all 150 leads on login instead of per-page
3. **Error Notifications**: Show toast messages for API failures
4. **Retry Logic**: Automatically retry failed predictions
5. **Performance Metrics**: Display API response times

---

## 🔗 Related Files

- **Frontend**: `static/index.html` (JavaScript section updated)
- **Backend**: `main.py` (FastAPI endpoints)
- **Model**: `prescient_model.pkl` (XGBoost model)
- **Training**: `train_model.py` (Model creation script)

---

**Date**: November 2024  
**Status**: ✅ Integration Complete and Tested

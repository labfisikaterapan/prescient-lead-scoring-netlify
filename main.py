"""
Prescient - Predictive Lead Scoring
FastAPI Backend Server

Server API untuk melayani prediksi lead scoring secara real-time.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import pandas as pd
import joblib
import uvicorn
from typing import Optional
import os

# Import authentication routes
from auth_routes import router as auth_router

# ==================== PYDANTIC MODEL ====================

class LeadInput(BaseModel):
    """
    Input schema untuk prediksi lead scoring
    Sesuai dengan data yang digunakan untuk training
    """
    Pekerjaan: str = Field(..., example="management", description="Job: management, technician, admin., services, entrepreneur, blue-collar, etc.")
    Saldo: float = Field(..., example=1618.0, description="Balance in account (EUR)")
    Personal_Loan: str = Field(..., alias="Personal Loan", example="yes", description="Has personal loan? (yes/no)")
    Housing_Loan: str = Field(..., alias="Housing Loan", example="yes", description="Has housing loan? (yes/no)")
    Marital: str = Field(..., example="single", description="Marital status: married, single, divorced")
    Campaign: int = Field(..., example=1, description="Number of contacts in current campaign (1-50)")
    duration: int = Field(..., example=300, description="Last contact duration in seconds (important: 92% weight)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "Pekerjaan": "management",
                "Saldo": 1618.0,
                "Personal Loan": "yes",
                "Housing Loan": "yes",
                "Marital": "single",
                "Campaign": 1,
                "duration": 300
            }
        }
        populate_by_name = True  # Allow alias names

class PredictionResponse(BaseModel):
    """
    Response schema untuk hasil prediksi
    """
    prediction_score: float = Field(..., description="Skor probabilitas (0-1)")
    label: str = Field(..., description="Label kategori lead (Hot Lead, Warm Lead, Cold Lead)")
    probability_percentage: str = Field(..., description="Persentase probabilitas")
    recommendation: str = Field(..., description="Rekomendasi aksi")

# ==================== FASTAPI APP ====================

app = FastAPI(
    title="Prescient - Predictive Lead Scoring API",
    description="API untuk prediksi skor lead nasabah bank berdasarkan data profil dan interaksi",
    version="1.0.0"
)

# ==================== CORS MIDDLEWARE ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins untuk akses dari HTML lokal
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== INCLUDE AUTHENTICATION ROUTES ====================

# Include auth routes with prefix /auth
app.include_router(auth_router)

# ==================== STATIC FILES ====================

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# ==================== GLOBAL MODEL ====================

MODEL = None
MODEL_PATH = "prescient_model.pkl"

@app.on_event("startup")
async def load_model():
    """
    Load model saat aplikasi startup (hanya sekali)
    """
    global MODEL
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"❌ Model file '{MODEL_PATH}' tidak ditemukan!\n"
            "   Jalankan 'python train_model.py' terlebih dahulu untuk membuat model."
        )
    
    print(f"📦 Loading model dari: {MODEL_PATH}")
    MODEL = joblib.load(MODEL_PATH)
    print("✅ Model berhasil dimuat dan siap digunakan!")

# ==================== ENDPOINTS ====================

@app.get("/")
async def read_index():
    """
    Serve the main HTML dashboard
    """
    return FileResponse('static/index.html')

@app.get("/api")
async def root():
    """
    API root endpoint - info
    """
    return {
        "message": "Prescient - Predictive Lead Scoring API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "dashboard": "/ (GET)",
            "predict": "/predict (POST)",
            "docs": "/docs",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    model_loaded = MODEL is not None
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_lead_score(lead: LeadInput):
    """
    Endpoint prediksi lead scoring
    
    Menerima data nasabah dan mengembalikan:
    - Skor probabilitas (0-1)
    - Label kategori (Hot/Warm/Cold Lead)
    - Rekomendasi aksi
    """
    try:
        # Validasi model sudah dimuat
        if MODEL is None:
            raise HTTPException(
                status_code=503,
                detail="Model belum dimuat. Silakan restart server."
            )
        
        # Convert Pydantic model ke dictionary dengan alias
        lead_data = lead.model_dump(by_alias=True)
        
        # Convert ke Pandas DataFrame (PENTING: nama kolom harus sama dengan training)
        input_df = pd.DataFrame([lead_data])
        
        # Prediksi probabilitas
        prediction_proba = MODEL.predict_proba(input_df)[0]
        
        # Ambil probabilitas untuk class positif (deposit = yes)
        score = float(prediction_proba[1])
        
        # Logika bisnis untuk labeling (threshold sesuai requirement)
        # Hot Lead: >0.75 (75%)
        # Warm Lead: >0.45 (45%)
        # Cold Lead: <=0.45
        if score > 0.75:
            label = "Hot Lead"
            recommendation = "🔥 Call Now - Prioritas tertinggi! Hubungi segera dengan penawaran khusus."
        elif score > 0.45:
            label = "Warm Lead"
            recommendation = "📞 Follow Up Soon - Pendekatan dengan informasi produk yang menarik dalam 1-2 hari."
        else:
            label = "Cold Lead"
            recommendation = "📧 Nurture Campaign - Masukkan ke email campaign untuk warming up."
        
        # Format response
        response = PredictionResponse(
            prediction_score=round(score, 4),
            label=label,
            probability_percentage=f"{score * 100:.2f}%",
            recommendation=recommendation
        )
        
        # Log prediksi (untuk monitoring)
        print(f"✓ Prediction: Score={score:.4f}, Label={label}")
        
        return response
    
    except Exception as e:
        print(f"❌ Error during prediction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saat melakukan prediksi: {str(e)}"
        )

# ==================== RUN SERVER ====================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("PRESCIENT - PREDICTIVE LEAD SCORING API")
    print("="*60)
    print("Starting server...")
    print("API Documentation: http://localhost:8000/docs")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

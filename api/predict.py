"""
Vercel Serverless Function - ML Prediction API
Endpoint: /api/predict
"""

from http.server import BaseHTTPRequestHandler
import json
import pandas as pd
import joblib
import os
from urllib.parse import parse_qs

# Load model once (cached by Vercel)
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'prescient_model.pkl')
MODEL = None

def load_model():
    global MODEL
    if MODEL is None:
        MODEL = joblib.load(MODEL_PATH)
    return MODEL

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST request for prediction"""
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            lead_data = json.loads(post_data.decode('utf-8'))
            
            # Load model
            model = load_model()
            
            # Validate required fields
            required_fields = ['Pekerjaan', 'Saldo', 'Personal Loan', 'Housing Loan', 'Marital', 'Campaign', 'duration']
            for field in required_fields:
                if field not in lead_data:
                    self.send_error_response(400, f"Missing field: {field}")
                    return
            
            # Convert to DataFrame
            input_df = pd.DataFrame([lead_data])
            
            # Predict
            prediction_proba = model.predict_proba(input_df)[0]
            score = float(prediction_proba[1])
            
            # Determine label
            if score > 0.75:
                label = "Hot Lead"
                recommendation = "🔥 Call Now - Prioritas tertinggi! Hubungi segera dengan penawaran khusus."
            elif score > 0.45:
                label = "Warm Lead"
                recommendation = "📞 Follow Up Soon - Pendekatan dengan informasi produk yang menarik dalam 1-2 hari."
            else:
                label = "Cold Lead"
                recommendation = "📧 Nurture Campaign - Masukkan ke email campaign untuk warming up."
            
            # Create response
            response = {
                "prediction_score": round(score, 4),
                "label": label,
                "probability_percentage": f"{score * 100:.2f}%",
                "recommendation": recommendation
            }
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_error_response(500, str(e))
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_error_response(self, code, message):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error = {"detail": message}
        self.wfile.write(json.dumps(error).encode('utf-8'))

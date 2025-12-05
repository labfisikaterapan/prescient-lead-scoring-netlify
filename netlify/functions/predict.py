"""
Netlify Function - ML Prediction API
"""
import json
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pandas as pd
import joblib

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'prescient_model.pkl')
MODEL = None

def load_model():
    global MODEL
    if MODEL is None:
        MODEL = joblib.load(MODEL_PATH)
    return MODEL

def handler(event, context):
    # Handle CORS preflight
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    try:
        # Parse request body
        lead_data = json.loads(event['body'])
        
        # Load model
        model = load_model()
        
        # Validate required fields
        required_fields = ['Pekerjaan', 'Saldo', 'Personal Loan', 'Housing Loan', 'Marital', 'Campaign', 'duration']
        for field in required_fields:
            if field not in lead_data:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    },
                    'body': json.dumps({"detail": f"Missing field: {field}"})
                }
        
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
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"detail": str(e)})
        }

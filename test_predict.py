"""
Test script untuk predict endpoint
"""
import requests
import json

# Test data
test_cases = [
    {
        "name": "High Potential Lead (Hot)",
        "data": {
            "Pekerjaan": "management",
            "Saldo": 15000.0,
            "Personal Loan": "no",
            "Housing Loan": "yes",
            "Marital": "married",
            "Campaign": 1,
            "duration": 450
        }
    },
    {
        "name": "Medium Potential Lead (Warm)",
        "data": {
            "Pekerjaan": "technician",
            "Saldo": 3000.0,
            "Personal Loan": "yes",
            "Housing Loan": "no",
            "Marital": "single",
            "Campaign": 2,
            "duration": 200
        }
    },
    {
        "name": "Low Potential Lead (Cold)",
        "data": {
            "Pekerjaan": "services",
            "Saldo": 500.0,
            "Personal Loan": "yes",
            "Housing Loan": "yes",
            "Marital": "divorced",
            "Campaign": 5,
            "duration": 50
        }
    }
]

print("\n" + "="*70)
print("PRESCIENT - PREDICT ENDPOINT TEST")
print("="*70 + "\n")

url = "http://127.0.0.1:8000/predict"

for test in test_cases:
    print(f"\n🧪 Testing: {test['name']}")
    print(f"   Input: {json.dumps(test['data'], indent=6)}")
    
    try:
        response = requests.post(url, json=test['data'])
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n   ✅ Success!")
            print(f"   📊 Score: {result['prediction_score']}")
            print(f"   🏷️  Label: {result['label']}")
            print(f"   📈 Probability: {result['probability_percentage']}")
            print(f"   💡 Recommendation: {result['recommendation']}")
        else:
            print(f"\n   ❌ Error {response.status_code}: {response.text}")
    
    except requests.exceptions.ConnectionError:
        print(f"\n   ❌ Connection Error - Make sure server is running!")
        break
    except Exception as e:
        print(f"\n   ❌ Error: {str(e)}")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70 + "\n")

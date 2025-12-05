"""Simple integration test for Prescient"""
import requests

base = 'http://localhost:8000'

print('Testing Prescient Integration')
print('=' * 50)

# Test 1: Health check
print('\n1. Health Check...')
r = requests.get(f'{base}/health')
print(f'   Status: {r.status_code}')
if r.status_code == 200:
    print(f'   Response: {r.json()}')

# Test 2: Auth Health
print('\n2. Auth Health Check...')
try:
    r = requests.get(f'{base}/auth/health')
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        print(f'   Response: {r.json()}')
except Exception as e:
    print(f'   Error: {e}')

# Test 3: Register
print('\n3. Register User...')
try:
    r = requests.post(f'{base}/auth/register', json={
        'email': 'demo@test.com',
        'username': 'demouser',
        'password': 'demo123'
    })
    print(f'   Status: {r.status_code}')
    if r.status_code in [200, 201]:
        print(f'   SUCCESS: {r.json()}')
    elif r.status_code == 400:
        print('   User already exists (OK)')
    else:
        print(f'   Response: {r.json()}')
except Exception as e:
    print(f'   Error: {e}')

# Test 4: Login
print('\n4. Login User...')
try:
    r = requests.post(f'{base}/auth/token', json={
        'username': 'demouser',
        'password': 'demo123'
    })
    print(f'   Status: {r.status_code}')
    if r.status_code == 200:
        data = r.json()
        print(f'   Token received: {data["access_token"][:30]}...')
    else:
        print(f'   Response: {r.json()}')
except Exception as e:
    print(f'   Error: {e}')

# Test 5: Dashboard
print('\n5. Dashboard Access...')
r = requests.get(f'{base}/')
print(f'   Status: {r.status_code}')
print(f'   Size: {len(r.content)} bytes')

# Test 6: Prediction
print('\n6. ML Prediction...')
r = requests.post(f'{base}/predict', json={
    "age": 35, "job": "management", "marital": "married",
    "education": "tertiary", "default": "no", "balance": 1500,
    "housing": "yes", "loan": "no", "contact": "cellular",
    "day": 15, "month": "may", "duration": 300, "campaign": 2,
    "pdays": -1, "previous": 0, "poutcome": "unknown"
})
print(f'   Status: {r.status_code}')
if r.status_code == 200:
    data = r.json()
    print(f'   Score: {data["prediction_score"]}')
    print(f'   Label: {data["label"]}')

print('\n' + '=' * 50)
print('INTEGRATION TEST COMPLETE')
print('=' * 50)

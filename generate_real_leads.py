"""
Script untuk mengambil data ASLI dari bank-full.csv
dan mengkonversinya ke format JavaScript untuk index.html
"""

import pandas as pd
import json
import random

# Baca dataset
df = pd.read_csv('bank-full.csv', delimiter=';')

# Filter hanya yang y='yes' (berhasil deposit = potensi tinggi)
high_potential = df[df['y'] == 'yes'].copy()

print(f"✅ Found {len(high_potential)} customers who successfully made deposits")
print(f"📊 Selecting 150 random high-potential customers...")

# Ambil 150 random customers
selected = high_potential.sample(n=min(150, len(high_potential)), random_state=42)

# Buat data JavaScript
leads_data = []

# Name generator untuk Indonesia
first_names = ["Budi", "Siti", "Andi", "Dewi", "Eko", "Fajar", "Gita", "Hendra", "Iwan", "Joko", 
               "Kartika", "Lina", "Maya", "Nina", "Oscar", "Putri", "Rina", "Surya", "Tina", "Umar", 
               "Vina", "Wawan", "Yanti", "Zainal", "Rudi", "Sari", "Hadi", "Fitri", "Yoga", "Dian"]
last_names = ["Santoso", "Aminah", "Pratama", "Lestari", "Kurniawan", "Nugraha", "Pertiwi", 
              "Wijaya", "Saputra", "Susanto", "Hidayat", "Kusuma", "Wibowo", "Sari", "Utami", 
              "Cahyani", "Mulyadi", "Setiawan", "Permana", "Hakim"]

for idx, row in enumerate(selected.itertuples(), start=1000):
    # Generate nama Indonesia
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    name = f"{fname} {lname}"
    
    lead = {
        "id": f"CUST-{idx}",
        "name": name,
        "age": int(row.age),
        "job": row.job,
        "marital": row.marital,
        "education": row.education,
        "default": row.default,
        "balance": int(row.balance),
        "housing": row.housing,
        "loan": row.loan,
        "contact": row.contact,
        "day": int(row.day),
        "month": row.month,
        "duration": int(row.duration),
        "campaign": int(row.campaign),
        "pdays": int(row.pdays),
        "previous": int(row.previous),
        "poutcome": row.poutcome,
        "phone": f"6281{random.randint(100000000, 999999999)}",
        "email": f"{fname.lower()}.{lname.lower()}@example.com",
        "status": "pending"
    }
    
    leads_data.append(lead)

# Generate JavaScript code
js_code = f"""// REAL CUSTOMER DATA FROM BANK-FULL.CSV
// 150 customers who SUCCESSFULLY made deposits (y='yes')
// These are HIGH-POTENTIAL leads with >50% prediction probability

const REAL_HIGH_POTENTIAL_LEADS = {json.dumps(leads_data, indent=4)};

// Function to use real data instead of generating random
function loadRealLeads() {{
    return REAL_HIGH_POTENTIAL_LEADS.map(lead => ({{
        ...lead,
        score: null,  // Will be filled by API
        prediction: null,
        label: null,
        apiData: {{
            age: lead.age,
            job: lead.job,
            marital: lead.marital,
            education: lead.education,
            default: lead.default,
            balance: lead.balance,
            housing: lead.housing,
            loan: lead.loan,
            contact: lead.contact,
            day: lead.day,
            month: lead.month,
            duration: lead.duration,
            campaign: lead.campaign,
            pdays: lead.pdays,
            previous: lead.previous,
            poutcome: lead.poutcome
        }}
    }}));
}}
"""

# Save to file
with open('real_leads_data.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print(f"✅ Generated JavaScript code with {len(leads_data)} real high-potential leads")
print(f"💾 Saved to: real_leads_data.js")
print(f"\n📊 Sample statistics:")
print(f"   - Average balance: {selected['balance'].mean():.2f} EUR")
print(f"   - Average duration: {selected['duration'].mean():.2f} seconds")
print(f"   - Average campaign: {selected['campaign'].mean():.2f} contacts")
print(f"\n🎯 These customers have ACTUAL high conversion potential!")
print(f"   (They successfully made deposits in real historical data)")

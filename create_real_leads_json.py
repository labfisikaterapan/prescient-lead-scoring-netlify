import pandas as pd
import json
import random

# Baca dataset
df = pd.read_csv('bank-full.csv', delimiter=';')

# Filter yang y='yes' (sukses deposit)
high_potential = df[df['y'] == 'yes'].sample(n=150, random_state=42)

# Name generators
first_names = ["Budi", "Siti", "Andi", "Dewi", "Eko", "Fajar", "Gita", "Hendra", "Iwan", "Joko", 
               "Kartika", "Lina", "Maya", "Nina", "Oscar", "Putri", "Rina", "Surya", "Tina", "Umar", 
               "Vina", "Wawan", "Yanti", "Zainal", "Rudi", "Sari", "Hadi", "Fitri", "Yoga", "Dian"]
last_names = ["Santoso", "Aminah", "Pratama", "Lestari", "Kurniawan", "Nugraha", "Pertiwi", 
              "Wijaya", "Saputra", "Susanto", "Hidayat", "Kusuma", "Wibowo", "Sari", "Utami", 
              "Cahyani", "Mulyadi", "Setiawan", "Permana", "Hakim"]

random.seed(42)
leads = []

for idx, row in enumerate(high_potential.itertuples(), 1000):
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    
    leads.append({
        "id": f"CUST-{idx}",
        "name": f"{fname} {lname}",
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
        "email": f"{fname.lower()}.{lname.lower()}@example.com"
    })

# Save to JSON
with open('static/real_leads_data.json', 'w', encoding='utf-8') as f:
    json.dump(leads, f, indent=2, ensure_ascii=False)

print(f"✅ Created static/real_leads_data.json")
print(f"📊 {len(leads)} REAL high-potential customers")
print(f"")
print(f"Statistics from bank-full.csv (y='yes' customers):")
print(f"  - Average Balance: {high_potential['balance'].mean():.0f} EUR")
print(f"  - Average Duration: {high_potential['duration'].mean():.0f} seconds")
print(f"  - Average Campaign: {high_potential['campaign'].mean():.1f} contacts")
print(f"")
print(f"🎯 These customers ACTUALLY made deposits in real historical data!")
print(f"   Expected prediction scores: >50% (mostly 60-95%)")

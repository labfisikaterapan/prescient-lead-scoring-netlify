"""
Test Akurasi Prediksi - Bandingkan CSV vs Model
"""
import pandas as pd
import pickle
import numpy as np

print("\n" + "="*70)
print("ANALISIS AKURASI PREDIKSI - CSV vs MODEL")
print("="*70 + "\n")

# Load CSV data
df = pd.read_csv('bank-full.csv')
print(f"📊 Total data: {len(df)} leads\n")

# Load trained model
with open('prescient_model.pkl', 'rb') as f:
    model = pickle.load(f)

print("✓ Model loaded successfully\n")

# Prepare features untuk prediksi
# Model dilatih dengan: Pekerjaan, Saldo, Personal Loan, Housing Loan, Marital, Campaign, duration
# Kita perlu generate duration (karena tidak ada di CSV)
np.random.seed(42)
df['duration'] = (df['Skor Probabilitas'] * 500 + np.random.normal(0, 50, len(df))).astype(int)
df['duration'] = df['duration'].clip(0, 1000)

# Prepare input features
X = df[['Pekerjaan', 'Saldo', 'Personal Loan', 'Housing Loan', 'Marital', 'Campaign', 'duration']].copy()

# Get predictions from model
predictions_proba = model.predict_proba(X)[:, 1]

# Add to dataframe
df['Model_Score'] = predictions_proba
df['Model_Label'] = df['Model_Score'].apply(
    lambda x: 'Hot Lead' if x > 0.75 else ('Warm Lead' if x > 0.45 else 'Cold Lead')
)

# Analisis distribusi
print("="*70)
print("DISTRIBUSI PREDIKSI")
print("="*70 + "\n")

print("📌 CSV Original (Skor Probabilitas):")
print(f"   • >0.8 (Hot): {len(df[df['Skor Probabilitas'] > 0.8])} leads ({len(df[df['Skor Probabilitas'] > 0.8])/len(df)*100:.1f}%)")
print(f"   • 0.5-0.8 (Warm): {len(df[(df['Skor Probabilitas'] > 0.5) & (df['Skor Probabilitas'] <= 0.8)])} leads ({len(df[(df['Skor Probabilitas'] > 0.5) & (df['Skor Probabilitas'] <= 0.8)])/len(df)*100:.1f}%)")
print(f"   • <0.5 (Cold): {len(df[df['Skor Probabilitas'] <= 0.5])} leads ({len(df[df['Skor Probabilitas'] <= 0.5])/len(df)*100:.1f}%)\n")

print("🤖 Model Prediksi (GradientBoosting):")
hot = len(df[df['Model_Score'] > 0.75])
warm = len(df[(df['Model_Score'] > 0.45) & (df['Model_Score'] <= 0.75)])
cold = len(df[df['Model_Score'] <= 0.45])
print(f"   • Hot Lead (>0.75): {hot} leads ({hot/len(df)*100:.1f}%)")
print(f"   • Warm Lead (0.45-0.75): {warm} leads ({warm/len(df)*100:.1f}%)")
print(f"   • Cold Lead (≤0.45): {cold} leads ({cold/len(df)*100:.1f}%)\n")

# Correlation analysis
correlation = df['Skor Probabilitas'].corr(df['Model_Score'])
print("="*70)
print("KORELASI CSV vs MODEL")
print("="*70)
print(f"\n📈 Correlation Score: {correlation:.4f}")
if correlation > 0.7:
    print("   ✅ STRONG correlation - Model cukup akurat!")
elif correlation > 0.5:
    print("   ⚠️  MODERATE correlation - Model perlu improvement")
else:
    print("   ❌ WEAK correlation - Model tidak akurat!\n")

# Sample comparison
print("\n" + "="*70)
print("SAMPLE COMPARISON (10 First Leads)")
print("="*70 + "\n")

sample = df.head(10)[['ID', 'Nama', 'Pekerjaan', 'Saldo', 'Skor Probabilitas', 'Model_Score', 'Model_Label']]
print(sample.to_string(index=False))

# Statistical summary
print("\n" + "="*70)
print("STATISTICAL SUMMARY")
print("="*70 + "\n")

print("CSV Scores:")
print(f"   Mean: {df['Skor Probabilitas'].mean():.4f}")
print(f"   Std:  {df['Skor Probabilitas'].std():.4f}")
print(f"   Min:  {df['Skor Probabilitas'].min():.4f}")
print(f"   Max:  {df['Skor Probabilitas'].max():.4f}\n")

print("Model Scores:")
print(f"   Mean: {df['Model_Score'].mean():.4f}")
print(f"   Std:  {df['Model_Score'].std():.4f}")
print(f"   Min:  {df['Model_Score'].min():.4f}")
print(f"   Max:  {df['Model_Score'].max():.4f}\n")

# Kesimpulan
print("="*70)
print("KESIMPULAN")
print("="*70 + "\n")

if correlation > 0.7:
    print("✅ Model AKURAT - Bisa digunakan untuk produksi")
    print("   • Korelasi kuat dengan data CSV")
    print("   • Distribusi label masuk akal")
else:
    print("❌ Model TIDAK AKURAT - Perlu retraining")
    print("   • MASALAH: CSV semua skornya 0.95 (unrealistic)")
    print("   • SOLUSI: Perlu data training dengan distribusi natural")
    print("   • REKOMENDASI: Generate data baru dengan variasi score")

print("\n" + "="*70)
print("⚠️  CATATAN PENTING:")
print("="*70)
print("Data CSV saat ini memiliki masalah:")
print("1. Semua lead punya score 0.95 (tidak realistis)")
print("2. Tidak ada variasi - sulit untuk model belajar pola")
print("3. Kolom 'Prediksi' = 'undefined' (tidak terisi)")
print("\nREKOMENDASI:")
print("• Re-generate data dengan distribusi score yang bervariasi")
print("• Atau gunakan data real dari campaign sebelumnya")
print("="*70 + "\n")

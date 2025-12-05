"""
Prescient - Predictive Lead Scoring
Train Model Script

Script ini melatih model machine learning untuk memprediksi kemungkinan
nasabah bank akan melakukan deposito berdasarkan data historis.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import joblib
import warnings
warnings.filterwarnings('ignore')

# Import model - prioritas XGBoost, fallback ke RandomForest
try:
    from xgboost import XGBClassifier
    USE_XGBOOST = True
    print("✓ XGBoost tersedia - akan menggunakan XGBoost Classifier")
except ImportError:
    from sklearn.ensemble import RandomForestClassifier
    USE_XGBOOST = False
    print("⚠ XGBoost tidak tersedia - menggunakan RandomForest Classifier")

def load_data(filepath):
    """
    Load dataset bank dengan delimiter semicolon
    """
    print(f"\n📂 Loading data dari: {filepath}")
    df = pd.read_csv(filepath, delimiter=';')
    print(f"✓ Data berhasil dimuat: {df.shape[0]} rows, {df.shape[1]} columns")
    return df

def preprocess_data(df):
    """
    Preprocessing data: pisahkan features dan target
    """
    print("\n🔧 Preprocessing data...")
    
    # Pisahkan features (X) dan target (y)
    X = df.drop('y', axis=1)
    y = df['y'].map({'no': 0, 'yes': 1})  # Convert ke binary
    
    print(f"✓ Features shape: {X.shape}")
    print(f"✓ Target distribution:\n{y.value_counts()}")
    print(f"✓ Class imbalance ratio: {y.value_counts()[0]/y.value_counts()[1]:.2f}:1")
    
    return X, y

def create_preprocessing_pipeline():
    """
    Membuat pipeline preprocessing dengan ColumnTransformer
    """
    # Definisi kolom kategorikal dan numerik
    categorical_features = ['job', 'marital', 'education', 'default', 
                          'housing', 'loan', 'contact', 'month', 'poutcome']
    numerical_features = ['age', 'balance', 'day', 'duration', 
                         'campaign', 'pdays', 'previous']
    
    print(f"\n🔄 Membuat preprocessing pipeline...")
    print(f"   Categorical features: {len(categorical_features)}")
    print(f"   Numerical features: {len(numerical_features)}")
    
    # ColumnTransformer untuk preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), 
             categorical_features)
        ],
        remainder='passthrough'
    )
    
    return preprocessor

def create_model_pipeline(preprocessor):
    """
    Membuat pipeline lengkap: preprocessor + model
    """
    print("\n🤖 Membuat model pipeline...")
    
    if USE_XGBOOST:
        # XGBoost dengan handling imbalance
        model = XGBClassifier(
            n_estimators=200,
            max_depth=10,
            learning_rate=0.1,
            scale_pos_weight=4.5,  # Untuk handling imbalance (ratio ~4.5:1)
            random_state=42,
            n_jobs=-1,
            eval_metric='logloss'
        )
        print("   Model: XGBoost Classifier")
        print("   - n_estimators: 200")
        print("   - max_depth: 10")
        print("   - scale_pos_weight: 4.5 (handling imbalance)")
    else:
        # RandomForest dengan class_weight balanced
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            class_weight='balanced',  # Handling imbalance
            random_state=42,
            n_jobs=-1
        )
        print("   Model: RandomForest Classifier")
        print("   - n_estimators: 200")
        print("   - max_depth: 10")
        print("   - class_weight: balanced (handling imbalance)")
    
    # Pipeline lengkap
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])
    
    return pipeline

def train_and_evaluate(pipeline, X_train, X_test, y_train, y_test):
    """
    Train model dan evaluasi performance
    """
    print("\n🎯 Training model...")
    pipeline.fit(X_train, y_train)
    print("✓ Training selesai!")
    
    # Prediksi
    print("\n📊 Evaluating model...")
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    
    # Classification Report
    print("\n" + "="*60)
    print("CLASSIFICATION REPORT")
    print("="*60)
    print(classification_report(y_test, y_pred, 
                                target_names=['No Deposit', 'Deposit'],
                                digits=4))
    
    # Confusion Matrix
    print("="*60)
    print("CONFUSION MATRIX")
    print("="*60)
    cm = confusion_matrix(y_test, y_pred)
    print(f"True Negatives:  {cm[0][0]:>6}")
    print(f"False Positives: {cm[0][1]:>6}")
    print(f"False Negatives: {cm[1][0]:>6}")
    print(f"True Positives:  {cm[1][1]:>6}")
    
    # ROC-AUC Score
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    print("\n" + "="*60)
    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print("="*60)
    
    return pipeline

def save_model(pipeline, filepath='prescient_model.pkl'):
    """
    Simpan model pipeline ke file
    """
    print(f"\n💾 Menyimpan model ke: {filepath}")
    joblib.dump(pipeline, filepath)
    print(f"✓ Model berhasil disimpan!")
    
    # Cek ukuran file
    import os
    file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
    print(f"   File size: {file_size:.2f} MB")

def main():
    """
    Main training pipeline
    """
    print("\n" + "="*60)
    print("PRESCIENT - PREDICTIVE LEAD SCORING")
    print("Model Training Script")
    print("="*60)
    
    # 1. Load data
    df = load_data('bank-full.csv')
    
    # 2. Preprocess
    X, y = preprocess_data(df)
    
    # 3. Split data
    print("\n✂️  Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Train set: {X_train.shape[0]} samples")
    print(f"   Test set:  {X_test.shape[0]} samples")
    
    # 4. Create preprocessing pipeline
    preprocessor = create_preprocessing_pipeline()
    
    # 5. Create model pipeline
    pipeline = create_model_pipeline(preprocessor)
    
    # 6. Train and evaluate
    trained_pipeline = train_and_evaluate(pipeline, X_train, X_test, y_train, y_test)
    
    # 7. Save model
    save_model(trained_pipeline)
    
    print("\n" + "="*60)
    print("✅ TRAINING SELESAI!")
    print("="*60)
    print("Model siap digunakan untuk prediksi.")
    print("Jalankan 'python main.py' untuk start API server.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()

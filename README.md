# Prescient AI - Predictive Lead Scoring System

🤖 **AI-Powered Lead Scoring for Banking Campaign Optimization**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

Prescient AI adalah sistem machine learning yang membantu bank mengidentifikasi prospek dengan probabilitas tertinggi untuk melakukan deposit. Sistem ini menggunakan **GradientBoostingClassifier** untuk memprediksi conversion probability berdasarkan data profil dan interaksi nasabah.

### ✨ Key Features

- 🎯 **AI Prediction Engine** - GradientBoosting model dengan akurasi 61.6%
- 📊 **Real-time Dashboard** - Visualisasi lead scoring dan analytics
- 🔥 **Lead Prioritization** - Otomatis kategorisasi Hot/Warm/Cold leads
- 🔐 **Secure Authentication** - JWT token dengan PBKDF2-HMAC-SHA256
- 📱 **Responsive Design** - Glassmorphism UI dengan live video backgrounds
- 🚀 **REST API** - FastAPI backend untuk prediksi real-time

## 🎯 Model Performance

- **Algorithm**: GradientBoostingClassifier
- **Cross-Validation Score**: 61.6% (±4.45%)
- **Key Features**: Duration (92%), Balance (78%), Job (65%)

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Rivaldy-25-Lval/Prescient-AI.git
cd Prescient-AI

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8000
```

### Demo Credentials
- **Username**: `eiz`
- **Password**: `iris`

## 📊 Lead Scoring Logic

| Score | Label | Action |
|-------|-------|--------|
| >75% | 🔥 Hot Lead | Call Now |
| 45-75% | ⚡ Warm Lead | Follow up 1-2 days |
| <45% | ❄️ Cold Lead | Nurture campaign |

## 👥 Team

**A25-CS100 • Capstone Project**
- M. Rivaldy Pratama - ML Engineer (M318D5Y1369)
- Eidelwise Prily S. - ML Engineer (M318D5X0520)
- (R004D5Y1293) - (Muhammad Ihsanul Fikri)- (React & Back-End with AI) 
- (R322D5Y1228) - (Muhammad Aulia Irsyad)- (React & Back-End with AI) 
- (R172D5X0997) - (Lilis Karlina Sipahutar)- (React & Back-End with AI) 




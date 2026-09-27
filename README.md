# AI Mental Wellness System Using Indian Psychology (Manas AI)

An academic mini-project synthesizing **Indian Knowledge Systems (IKS)**, data science, and transparent machine learning to provide self-reflection insights and healthy lifestyle guidance.

> **IMPORTANT DISCLAIMER**: This system is strictly an academic mental-wellness assessment project, **NOT a medical diagnostic system**. The system does not diagnose depression, anxiety disorders, psychiatric illness, or any medical condition.

---

## 🏛️ System Architecture

The project enforces a strict, modular separation of concerns:

```
c:/Manas AI/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI REST endpoints
│   │   ├── iks/          # Indian Psychology & Triguna models
│   │   ├── ml/           # Scikit-learn Random Forest model & trainer
│   │   ├── models/       # Database & ORM models
│   │   ├── schemas/      # Pydantic validation schemas
│   │   ├── services/     # Business logic & scoring services
│   │   ├── config.py     # Configuration and CORS settings
│   │   └── main.py       # FastAPI application entrypoint
│   ├── tests/            # Automated test suite
│   ├── requirements.txt  # Python dependencies
│   └── run.py            # Development server runner
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable UI components (Navbar, Disclaimers)
│   │   ├── data/         # Static datasets & definitions
│   │   ├── pages/        # Application views (LandingPage, Assessment, Report)
│   │   ├── services/     # API integration client
│   │   ├── App.jsx       # Root application layout
│   │   └── index.css     # Tailwind styling & typography
│   ├── package.json
│   └── vite.config.js
├── data/                 # Datasets & reference norms
├── README.md
└── .gitignore
```

---

## 🚀 Quickstart Guide

### Prerequisites
- **Python**: 3.10+ (with virtual environment support)
- **Node.js**: 18+ (with npm)

### 1. Backend Setup & Startup
```powershell
# In project root:
backend\venv\Scripts\python backend\run.py
```
- API Health Check: `http://127.0.0.1:8000/api/health`
- Interactive API Docs: `http://127.0.0.1:8000/docs`

### 2. Frontend Setup & Startup
```powershell
# In a second terminal:
cd frontend
npm run dev
```
- Web Application: `http://localhost:5173`

### 3. Run Automated Tests
```powershell
backend\venv\Scripts\pytest backend/tests
```

---

## 📚 Implementation Stages

- **Stage 1 (Current)**: Project Foundation, Modular Directory Structure, FastAPI Setup, CORS & React Communication, Clean Minimal Landing Page.
- **Stage 2**: Assessment Data Models, Questionnaire Design & Scoring Engine.
- **Stage 3**: Machine Learning Model (Random Forest Classification & Feature Importance).
- **Stage 4**: IKS Interpretation & Recommendation Engine (*Triguna*, *Chitta*, *Dinacharya*).
- **Stage 5**: Visual Report Dashboard & Explainable Presentation.
- **Stage 6**: End-to-End Integration, Testing & Academic Presentation.
# Manas-AI

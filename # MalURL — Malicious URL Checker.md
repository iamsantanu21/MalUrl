# MalURL — Malicious URL Checker

Short description
A small FastAPI server plus a Chrome extension that predicts whether a URL is safe, phishing, defacement, or malware using features extracted from the URL.

Prerequisites
- Python 3.8+
- Chrome (for loading the extension)
- A trained model file named `lgb_model.pkl` placed in the repo root (same dir as `server.py`).

Install & run (recommended)
1. Create and activate a venv:
   - macOS / Linux:
     ```sh
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   - Windows:
     ```ps
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```

2. Install packages:
   ```sh
   pip install fastapi uvicorn pandas joblib scikit-learn lightgbm
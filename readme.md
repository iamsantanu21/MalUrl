# MalURL — Malicious URL Checker

A FastAPI server + Chrome extension that predicts whether a URL is SAFE, PHISHING, DEFACEMENT, or MALWARE using URL-derived features and a LightGBM model.

## Quick overview
- server.py — FastAPI server and endpoints
- features.py — feature extractor used by the server
- lgb_model.pkl — trained LightGBM model (required)
- label_encoder.pkl — label encoder (required)
- feature_columns.json, feature_meta.json — feature definitions
- extension/ — Chrome extension files (manifest.json, popup.html, popup.js)
- malicious_phish.csv, malicious-tfidf.ipynb — data & notebook

## Prerequisites
- Python 3.8+
- Chrome (for loading the extension)
- Place `lgb_model.pkl` and `label_encoder.pkl` in the repository root (same folder as `server.py`).

## Setup (macOS / Linux)
1. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```
If you don't have requirements.txt, run:
```bash
pip install fastapi uvicorn pandas joblib scikit-learn lightgbm python-multipart
```

## Start the API server
From the repository root:
```bash
uvicorn server:app --host 127.0.0.1 --port 8010 --reload
```
Server base URL: http://127.0.0.1:8010

## API endpoints
- GET /ping — health check
- POST /debug_features — body: {"url":"https://example.com"} — returns extracted features
- POST /predict — body: {"url":"https://example.com"} — returns predicted label and probabilities

Example predict request:
```bash
curl -X POST http://127.0.0.1:8010/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

## Load Chrome extension locally
1. Open chrome://extensions
2. Enable "Developer mode"
3. Click "Load unpacked" and select the `extension/` folder
4. Open the popup and click "Check" (popup.js calls the API URL configured inside it — update if needed)

## CORS
If the extension or other frontend is blocked by CORS, add FastAPI CORS middleware in server.py:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # prefer restricting to your front-end origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Helpful files to add (suggested)
requirements.txt:
```text
fastapi
uvicorn
pandas
joblib
scikit-learn
lightgbm
python-multipart
```

start.sh:
```bash
#!/usr/bin/env bash
source .venv/bin/activate
uvicorn server:app --host 127.0.0.1 --port 8010 --reload
```
Make executable:
```bash
chmod +x start.sh
```

## Push to GitHub (quick)
1. Create a repo on GitHub.
2. From repo root:
```bash
git branch -M main
git remote add origin git@github.com:YOUR_USER/YOUR_REPO.git
git push -u origin main
```
If you get "Permission denied (publickey)", add your SSH key to GitHub or use HTTPS:
```bash
git remote set-url origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

SSH key quick steps (macOS):
```bash
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/id_ed25519
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
pbcopy < ~/.ssh/id_ed25519.pub
# paste into GitHub: Settings → SSH and GPG keys
ssh -T git@github.com
```

## Troubleshooting
- model file not found: ensure `lgb_model.pkl` and `label_encoder.pkl` are in the repo root.
- feature mismatch: use /debug_features to inspect produced feature keys/order and compare with feature_columns.json.
- zsh: don't paste shell comment lines starting with `#` as executable commands.

## Security & license
- Do not expose the API publicly without authentication and rate limiting.
- Add a LICENSE file (e.g., MIT) and any dataset attributions.

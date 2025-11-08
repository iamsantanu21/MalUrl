# server.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os, json, joblib, pandas as pd

# ⬇️ import YOUR feature builder from features.py
# features.py must define: def main(url: str) -> list | dict
from features import main as build_from_notebook

HERE = os.path.dirname(os.path.abspath(__file__))

# load artifacts
model = joblib.load(os.path.join(HERE, "lgb_model.pkl"))
with open(os.path.join(HERE, "feature_columns.json")) as f:
    FEATURE_COLS = json.load(f)

app = FastAPI()

class Req(BaseModel):
    url: str

def extract_features(url: str) -> pd.DataFrame:
    feats = build_from_notebook(url)

    # if dict: align to training columns and fill missing with 0
    if isinstance(feats, dict):
        row = {c: feats.get(c, 0) for c in FEATURE_COLS}
        return pd.DataFrame([row])[FEATURE_COLS]

    # else treat as list/array
    feats = list(feats)
    exp, got = len(FEATURE_COLS), len(feats)
    if got != exp:
        raise ValueError(f"Feature length mismatch: expected {exp}, got {got}")
    return pd.DataFrame([feats], columns=FEATURE_COLS)



@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.post("/debug_features")
def debug_features(req: Req):
    try:
        X = extract_features(req.url)
        return {"columns": FEATURE_COLS, "values": X.iloc[0].tolist()}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/predict")
def predict(req: Req):
    try:
        X = extract_features(req.url)
        pred = int(model.predict(X)[0])
        # Typical LabelEncoder order (alphabetical):
        # benign=0, defacement=1, malware=2, phishing=3
        label_map = {0: "SAFE", 1: "DEFACEMENT", 2: "MALWARE", 3: "PHISHING"}
        return {"url": req.url, "prediction": label_map.get(pred, pred)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

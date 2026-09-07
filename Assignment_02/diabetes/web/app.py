"""
Web Application Server — Giao diện Web Dự đoán Tiểu đường (Desktop Web UI)
Chạy: uvicorn app:app --port 8101
Truy cập: http://localhost:8101
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import urllib.request
import json
import os
import joblib
import pandas as pd

app = FastAPI(title="Diabetes Web Dashboard", version="1.0.0")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

API_URL = "http://localhost:8001/predict"

# Fallback local model loading
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
PREP_PATH = os.path.join(MODEL_DIR, "preprocessor.joblib")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

prep_artifact = joblib.load(PREP_PATH)
model = joblib.load(MODEL_PATH)
preprocessor = prep_artifact['preprocessor']
gender_map = prep_artifact['gender_map']
smoking_map = prep_artifact['smoking_map']
feature_columns = prep_artifact['feature_columns']


class PatientInput(BaseModel):
    gender: str = "Female"
    age: int = 45
    hypertension: int = 0
    heart_disease: int = 0
    smoking_history: str = "never"
    bmi: float = 24.5
    hbA1c_level: float = 5.4
    blood_glucose_level: int = 95
    race: str = "Caucasian"


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/predict")
def predict_proxy(data: PatientInput):
    # Try calling central REST API first
    payload = data.model_dump()
    try:
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        # Fallback to local inference
        gender_val = gender_map.get(data.gender, 2)
        smoking_val = smoking_map.get(data.smoking_history, 0)
        race_cols = {'race:AfricanAmerican': 0, 'race:Asian': 0, 'race:Caucasian': 0, 'race:Hispanic': 0, 'race:Other': 0}
        race_key = f'race:{data.race}'
        if race_key in race_cols:
            race_cols[race_key] = 1
        row = {
            'gender': gender_val, 'age': data.age, **race_cols,
            'hypertension': data.hypertension, 'heart_disease': data.heart_disease,
            'smoking_history': smoking_val, 'bmi': data.bmi,
            'hbA1c_level': data.hbA1c_level, 'blood_glucose_level': data.blood_glucose_level
        }
        df = pd.DataFrame([row])[feature_columns]
        X_trans = preprocessor.transform(df)
        pred = int(model.predict(X_trans)[0])
        proba = model.predict_proba(X_trans)[0]
        return {
            "prediction": pred,
            "label": "Có nguy cơ tiểu đường" if pred == 1 else "Không có nguy cơ tiểu đường",
            "confidence": round(float(max(proba)) * 100, 1),
            "probabilities": {"khong_benh": round(float(proba[0]) * 100, 1), "co_benh": round(float(proba[1]) * 100, 1)},
            "model_used": type(model).__name__ + " (Local Fallback)"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8101)

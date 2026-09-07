"""
Unified Server — Sàng lọc Bệnh Tiểu đường (All-in-One Server)
Cho phép chạy trực tiếp từ thư mục diabetes:
    python -m uvicorn app:app --port 8001
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Diabetes Prediction API & Web", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
prep_artifact = joblib.load(os.path.join(MODEL_DIR, "preprocessor.joblib"))
model = joblib.load(os.path.join(MODEL_DIR, "model.joblib"))

preprocessor = prep_artifact['preprocessor']
gender_map = prep_artifact['gender_map']
smoking_map = prep_artifact['smoking_map']
feature_columns = prep_artifact['feature_columns']

templates_web = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "web", "templates"))
templates_mobile = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "mobile", "templates"))


class PatientInput(BaseModel):
    gender: str = Field("Female")
    age: int = Field(45, ge=0, le=120)
    hypertension: int = Field(0, ge=0, le=1)
    heart_disease: int = Field(0, ge=0, le=1)
    smoking_history: str = Field("never")
    bmi: float = Field(24.5, ge=5.0, le=80.0)
    hbA1c_level: float = Field(5.4, ge=0.0, le=15.0)
    blood_glucose_level: int = Field(95, ge=30, le=500)
    race: str = Field("Caucasian")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates_web.TemplateResponse(request=request, name="index.html")


@app.get("/mobile", response_class=HTMLResponse)
def mobile(request: Request):
    return templates_mobile.TemplateResponse(request=request, name="mobile.html")


@app.post("/predict")
@app.post("/diabetes/v1/predict")
def predict(data: PatientInput):
    gender_val = gender_map.get(data.gender, 2)
    smoking_val = smoking_map.get(data.smoking_history, 0)

    race_cols = {
        'race:AfricanAmerican': 0, 'race:Asian': 0, 'race:Caucasian': 0,
        'race:Hispanic': 0, 'race:Other': 0
    }
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

    X_transformed = preprocessor.transform(df)
    pred = int(model.predict(X_transformed)[0])
    proba = model.predict_proba(X_transformed)[0]

    return {
        "prediction": pred,
        "label": "Có nguy cơ tiểu đường" if pred == 1 else "Không có nguy cơ tiểu đường",
        "confidence": round(float(max(proba)) * 100, 1),
        "probabilities": {
            "khong_benh": round(float(proba[0]) * 100, 1),
            "co_benh": round(float(proba[1]) * 100, 1)
        },
        "model_used": type(model).__name__
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "Diabetes Prediction"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

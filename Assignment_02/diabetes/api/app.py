"""
REST API Microservice — Dự đoán Bệnh Tiểu đường (Diabetes Prediction API)
Endpoint chuẩn Appendix C: /predict
Chạy: uvicorn app:app --port 8001
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(
    title="Diabetes Prediction REST API",
    description="Microservice REST API dự đoán nguy cơ tiểu đường từ chỉ số lâm sàng",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model artifacts
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
    gender: str = Field("Female", description="Female, Male, hoặc Other")
    age: int = Field(45, ge=0, le=120, description="Tuổi bệnh nhân")
    hypertension: int = Field(0, ge=0, le=1, description="0 = Không, 1 = Có")
    heart_disease: int = Field(0, ge=0, le=1, description="0 = Không, 1 = Có")
    smoking_history: str = Field("never", description="never, former, current, not current, ever, No Info")
    bmi: float = Field(24.5, ge=5.0, le=80.0, description="Chỉ số BMI")
    hbA1c_level: float = Field(5.4, ge=0.0, le=15.0, description="Mức HbA1c (%)")
    blood_glucose_level: int = Field(95, ge=30, le=500, description="Đường huyết (mg/dL)")
    race: str = Field("Caucasian", description="Caucasian, AfricanAmerican, Asian, Hispanic, Other")


@app.get("/health")
def health():
    return {"status": "ok", "service": "Diabetes Prediction API", "model": type(model).__name__}


@app.post("/predict")
def predict(data: PatientInput):
    try:
        gender_val = gender_map.get(data.gender, 2)
        smoking_val = smoking_map.get(data.smoking_history, 0)

        race_cols = {
            'race:AfricanAmerican': 0,
            'race:Asian': 0,
            'race:Caucasian': 0,
            'race:Hispanic': 0,
            'race:Other': 0
        }
        race_key = f'race:{data.race}'
        if race_key in race_cols:
            race_cols[race_key] = 1

        row = {
            'gender': gender_val,
            'age': data.age,
            **race_cols,
            'hypertension': data.hypertension,
            'heart_disease': data.heart_disease,
            'smoking_history': smoking_val,
            'bmi': data.bmi,
            'hbA1c_level': data.hbA1c_level,
            'blood_glucose_level': data.blood_glucose_level
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

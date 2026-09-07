"""
FastAPI Server — Dự đoán Bệnh Tiểu đường
Chạy: uvicorn app:app --reload --port 8001
Truy cập: http://localhost:8001
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import os

# ================================================================
# Load pipeline đã lưu từ notebook
# ================================================================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "diabetes_pipeline.joblib")
artifact = joblib.load(MODEL_PATH)
pipeline = artifact['pipeline']
gender_map = artifact['gender_map']
smoking_map = artifact['smoking_map']
feature_columns = artifact['feature_columns']
model_name = artifact['model_name']

print(f"[OK] Model loaded: {model_name}")
print(f"[OK] Features: {feature_columns}")

# ================================================================
# FastAPI App
# ================================================================
app = FastAPI(
    title="Dự đoán Bệnh Tiểu đường API",
    description="API dự đoán nguy cơ mắc bệnh tiểu đường dựa trên đặc điểm lâm sàng.",
    version="1.0.0"
)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


# ================================================================
# Pydantic Schema — Validation đầu vào
# ================================================================
class PatientInput(BaseModel):
    gender: str = Field(..., description="Female, Male, hoặc Other")
    age: int = Field(..., ge=0, le=120, description="Tuổi bệnh nhân")
    hypertension: int = Field(..., ge=0, le=1, description="0 = Không, 1 = Có")
    heart_disease: int = Field(..., ge=0, le=1, description="0 = Không, 1 = Có")
    smoking_history: str = Field(..., description="never, former, current, not current, ever, No Info")
    bmi: float = Field(..., ge=5, le=80, description="Chỉ số BMI")
    hbA1c_level: float = Field(..., ge=0, le=15, description="Mức HbA1c (%)")
    blood_glucose_level: int = Field(..., ge=30, le=500, description="Đường huyết (mg/dL)")
    race: str = Field(..., description="Caucasian, AfricanAmerican, Asian, Hispanic, Other")


# ================================================================
# Endpoints
# ================================================================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Trang chủ — hiển thị form nhập liệu."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/predict")
def predict(data: PatientInput):
    """
    Nhận dữ liệu bệnh nhân → Dự đoán nguy cơ tiểu đường.
    
    Luồng: User Input → Validation (Pydantic) → Preprocessing (Pipeline) → Model → Prediction
    """
    # 1. Encode categorical features (giống notebook)
    gender_val = gender_map.get(data.gender, 2)  # default: Other
    smoking_val = smoking_map.get(data.smoking_history, 0)  # default: No Info

    # 2. One-hot encode race
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

    # 3. Build feature DataFrame (đúng thứ tự cột như khi train)
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
    df = pd.DataFrame([row])
    df = df[feature_columns]  # Đảm bảo thứ tự cột khớp

    # 4. Predict qua pipeline (preprocessor → model)
    pred = pipeline.predict(df)[0]
    proba = pipeline.predict_proba(df)[0]

    # 5. Trả kết quả
    return {
        "prediction": int(pred),
        "label": "Có nguy cơ tiểu đường" if pred == 1 else "Không có nguy cơ tiểu đường",
        "confidence": round(float(max(proba)) * 100, 1),
        "probabilities": {
            "khong_benh": round(float(proba[0]) * 100, 1),
            "co_benh": round(float(proba[1]) * 100, 1)
        },
        "model_used": model_name
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "model": model_name, "features": feature_columns}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

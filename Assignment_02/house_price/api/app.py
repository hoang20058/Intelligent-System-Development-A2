"""
REST API Microservice — Định giá Nhà ở Hoa Kỳ (House Price Prediction API)
Endpoint chuẩn Appendix C: /predict
Chạy: uvicorn app:app --port 8002
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(
    title="House Price Prediction REST API",
    description="Microservice REST API định giá bất động sản Hoa Kỳ",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
PREP_PATH = os.path.join(MODEL_DIR, "preprocessor.joblib")
MODEL_PATH = os.path.join(MODEL_DIR, "model.joblib")

prep_artifact = joblib.load(PREP_PATH)
model = joblib.load(MODEL_PATH)

preprocessor = prep_artifact['preprocessor']
status_map = prep_artifact['status_map']
state_classes = prep_artifact['state_classes']
city_freq_map = prep_artifact['city_freq_map']
feature_columns = prep_artifact['feature_columns']


class HouseInput(BaseModel):
    bed: int = Field(3, ge=1, le=10, description="Số phòng ngủ")
    bath: int = Field(2, ge=1, le=10, description="Số phòng tắm")
    house_size: float = Field(1850.0, ge=100.0, le=10000.0, description="Diện tích sàn (sqft)")
    acre_lot: float = Field(0.25, ge=0.0, le=10.0, description="Diện tích đất (acre)")
    state: str = Field("California", description="Bang (state)")
    city: str = Field("Los Angeles", description="Thành phố")
    status: str = Field("for_sale", description="Trạng thái: for_sale hoặc ready_to_build")


@app.get("/health")
def health():
    return {"status": "ok", "service": "House Price Prediction API", "model": type(model).__name__}


@app.post("/predict")
def predict(data: HouseInput):
    try:
        status_val = status_map.get(data.status, 0)
        state_encoded = state_classes.index(data.state) if data.state in state_classes else 0
        city_freq = city_freq_map.get(data.city, 0.0001)

        row = {
            'bed': data.bed,
            'bath': data.bath,
            'acre_lot': data.acre_lot,
            'house_size': data.house_size,
            'status': status_val,
            'state_encoded': state_encoded,
            'city_freq': city_freq
        }
        df = pd.DataFrame([row])[feature_columns]

        X_transformed = preprocessor.transform(df)
        pred_log = model.predict(X_transformed)[0]
        pred_price = float(np.expm1(pred_log))
        pred_price = max(pred_price, 0)

        return {
            "prediction": round(pred_price, 2),
            "formatted": f"${pred_price:,.0f}",
            "model_used": type(model).__name__
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

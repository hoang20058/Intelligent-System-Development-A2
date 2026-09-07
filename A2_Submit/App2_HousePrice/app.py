"""
FastAPI Server — Dự đoán Giá Nhà (House Price Prediction)
Chạy: uvicorn app:app --reload --port 8002
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "house_price_pipeline.joblib")
artifact = joblib.load(MODEL_PATH)
pipeline = artifact['pipeline']
status_map = artifact['status_map']
state_classes = artifact['state_classes']
city_freq_map = artifact['city_freq_map']
feature_columns = artifact['feature_columns']
model_name = artifact.get('model_name', 'Random Forest')

print(f"[OK] Model loaded: {model_name}")

app = FastAPI(title="Dự đoán Giá Nhà API", version="1.0.0")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


class HouseInput(BaseModel):
    bed: int = Field(..., ge=1, le=10, description="Số phòng ngủ")
    bath: int = Field(..., ge=1, le=10, description="Số phòng tắm")
    house_size: float = Field(..., ge=100, le=10000, description="Diện tích sàn (sqft)")
    acre_lot: float = Field(0.25, ge=0, le=10, description="Diện tích đất (acre)")
    state: str = Field("California", description="Bang (state)")
    city: str = Field("", description="Thành phố")
    status: str = Field("for_sale", description="Trạng thái bất động sản")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html",
                                      context={"states": state_classes})


@app.post("/predict")
@app.post("/houseprice/v1/predict")
def predict(data: HouseInput):
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

    pred_log = pipeline.predict(df)[0]
    pred_price = float(np.expm1(pred_log))
    pred_price = max(pred_price, 0)

    return {
        "prediction": round(pred_price, 2),
        "formatted": f"${pred_price:,.0f}",
        "model_used": model_name
    }


@app.get("/health")
def health():
    return {"status": "ok", "model": model_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

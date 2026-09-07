"""
Unified Server — Định giá Bất động sản Hoa Kỳ (All-in-One Server)
Cho phép chạy trực tiếp từ thư mục house_price:
    python -m uvicorn app:app --port 8002
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

app = FastAPI(title="House Price Prediction API & Web", version="1.0.0")

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
status_map = prep_artifact['status_map']
state_classes = prep_artifact['state_classes']
city_freq_map = prep_artifact['city_freq_map']
feature_columns = prep_artifact['feature_columns']

templates_web = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "web", "templates"))
templates_mobile = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "mobile", "templates"))


class HouseInput(BaseModel):
    bed: int = Field(3, ge=1, le=10)
    bath: int = Field(2, ge=1, le=10)
    house_size: float = Field(1850.0, ge=100.0, le=10000.0)
    acre_lot: float = Field(0.25, ge=0.0, le=10.0)
    state: str = Field("California")
    city: str = Field("Los Angeles")
    status: str = Field("for_sale")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates_web.TemplateResponse(request=request, name="index.html", context={"states": state_classes})


@app.get("/mobile", response_class=HTMLResponse)
def mobile(request: Request):
    return templates_mobile.TemplateResponse(request=request, name="mobile.html", context={"states": state_classes})


@app.post("/predict")
@app.post("/houseprice/v1/predict")
def predict(data: HouseInput):
    status_val = status_map.get(data.status, 0)
    state_encoded = state_classes.index(data.state) if data.state in state_classes else 0
    city_freq = city_freq_map.get(data.city, 0.0001)

    row = {
        'bed': data.bed, 'bath': data.bath, 'acre_lot': data.acre_lot,
        'house_size': data.house_size, 'status': status_val,
        'state_encoded': state_encoded, 'city_freq': city_freq
    }
    df = pd.DataFrame([row])[feature_columns]
    X_trans = preprocessor.transform(df)
    pred_log = model.predict(X_trans)[0]
    pred_price = float(np.expm1(pred_log))
    pred_price = max(pred_price, 0)

    return {
        "prediction": round(pred_price, 2),
        "formatted": f"${pred_price:,.0f}",
        "model_used": type(model).__name__
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "House Price Prediction"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)

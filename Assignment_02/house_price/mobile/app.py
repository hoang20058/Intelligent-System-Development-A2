"""
Mobile Application Server — Giao diện Di động Định giá Nhà (Touch / Mobile Client)
Chạy: uvicorn app:app --port 8202
Truy cập: http://localhost:8202
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import urllib.request
import json
import os
import joblib
import pandas as pd
import numpy as np

app = FastAPI(title="House Price Mobile Application", version="1.0.0")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

API_URL = "http://localhost:8002/predict"

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
prep_artifact = joblib.load(os.path.join(MODEL_DIR, "preprocessor.joblib"))
model = joblib.load(os.path.join(MODEL_DIR, "model.joblib"))

preprocessor = prep_artifact['preprocessor']
status_map = prep_artifact['status_map']
state_classes = prep_artifact['state_classes']
city_freq_map = prep_artifact['city_freq_map']
feature_columns = prep_artifact['feature_columns']


class HouseInput(BaseModel):
    bed: int = 3
    bath: int = 2
    house_size: float = 1850.0
    acre_lot: float = 0.25
    state: str = "California"
    city: str = "Los Angeles"
    status: str = "for_sale"


@app.get("/", response_class=HTMLResponse)
@app.get("/mobile", response_class=HTMLResponse)
def mobile_view(request: Request):
    return templates.TemplateResponse(request=request, name="mobile.html", context={"states": state_classes})


@app.post("/predict")
def predict_proxy(data: HouseInput):
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
            "model_used": type(model).__name__ + " (Local Fallback)"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8202)

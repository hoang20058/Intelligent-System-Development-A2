"""
Mobile Application Server — Giao diện Di động Dự đoán CSAT (Touch / Mobile Client)
Chạy: uvicorn app:app --port 8203
Truy cập: http://localhost:8203
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import urllib.request
import json
import os
import re
import joblib
import pandas as pd
from scipy.sparse import hstack, csr_matrix

app = FastAPI(title="Customer Behavior Mobile Application", version="1.0.0")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

API_URL = "http://localhost:8003/predict"

MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "model"))
prep_artifact = joblib.load(os.path.join(MODEL_DIR, "preprocessor.joblib"))
model = joblib.load(os.path.join(MODEL_DIR, "model.joblib"))

preprocessor_tabular = prep_artifact['preprocessor_tabular']
tfidf_vectorizer = prep_artifact['tfidf_vectorizer']
channel_map = prep_artifact['channel_map']
tenure_map = prep_artifact['tenure_map']
shift_map = prep_artifact['shift_map']
category_map = prep_artifact['category_map']
subcat_freq_map = prep_artifact['subcat_freq_map']


class CSATInput(BaseModel):
    channel: str = "Inbound"
    category: str = "Returns"
    tenure: str = ">90"
    shift: str = "Morning"
    response_time: float = 10.0
    remarks: str = ""


@app.get("/", response_class=HTMLResponse)
@app.get("/mobile", response_class=HTMLResponse)
def mobile_view(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="mobile.html",
        context={
            "channels": list(channel_map.keys()),
            "categories": list(category_map.keys()),
            "tenures": list(tenure_map.keys()),
            "shifts": list(shift_map.keys())
        }
    )


@app.post("/predict")
def predict_proxy(data: CSATInput):
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
        channel_val = channel_map.get(data.channel, 0)
        category_val = category_map.get(data.category, 0)
        tenure_val = tenure_map.get(data.tenure, 4)
        shift_val = shift_map.get(data.shift, 0)
        remarks_clean = re.sub(r'[^a-z0-9\s]', ' ', data.remarks.lower()).strip()

        row = pd.DataFrame([{
            'channel_name': channel_val, 'category': category_val,
            'Tenure Bucket': tenure_val, 'Agent Shift': shift_val,
            'response_time_minutes': data.response_time,
            'hour_reported': 10, 'day_of_week': 1, 'subcat_freq': 0.05
        }])

        tab_scaled = preprocessor_tabular.transform(row)
        text_vec = tfidf_vectorizer.transform([remarks_clean])
        combined = hstack([csr_matrix(tab_scaled), text_vec])

        pred = int(model.predict(combined)[0])
        prob = model.predict_proba(combined)[0].tolist()

        return {
            "prediction": pred,
            "label": "Satisfied" if pred == 1 else "At-Risk",
            "confidence": round(max(prob) * 100, 1),
            "probability_satisfied": round(prob[1] * 100, 1),
            "probability_at_risk": round(prob[0] * 100, 1),
            "model_used": type(model).__name__ + " (Local Fallback)"
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8203)

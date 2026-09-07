"""
FastAPI Server — Dự đoán Mức độ Hài lòng Khách hàng (CSAT Prediction)
Chạy: uvicorn app:app --reload --port 8003
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import re
import os
from scipy.sparse import hstack, csr_matrix

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "csat_pipeline.joblib")
artifact = joblib.load(MODEL_PATH)
model = artifact['model']
preprocessor_tabular = artifact['preprocessor_tabular']
tfidf_vectorizer = artifact['tfidf_vectorizer']
channel_map = artifact['channel_map']
tenure_map = artifact['tenure_map']
shift_map = artifact['shift_map']
category_map = artifact['category_map']
subcat_freq_map = artifact['subcat_freq_map']
model_name = artifact.get('model_name', 'Combined Model')

print(f"[OK] Model loaded: {model_name}")

app = FastAPI(title="Dự đoán CSAT API", version="1.0.0")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


class CSATInput(BaseModel):
    channel: str = Field("Inbound", description="Kênh liên hệ")
    category: str = Field("Returns", description="Danh mục sự cố")
    tenure: str = Field(">90", description="Kinh nghiệm nhân viên")
    shift: str = Field("Morning", description="Ca trực")
    response_time: float = Field(10.0, ge=0, description="Thời gian phản hồi (phút)")
    remarks: str = Field("", description="Nhận xét của khách hàng")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "channels": list(channel_map.keys()),
            "categories": list(category_map.keys()),
            "tenures": list(tenure_map.keys()),
            "shifts": list(shift_map.keys())
        }
    )


@app.post("/predict")
@app.post("/csat/v1/predict")
def predict(data: CSATInput):
    channel_val = channel_map.get(data.channel, 0)
    category_val = category_map.get(data.category, 0)
    tenure_val = tenure_map.get(data.tenure, 4)
    shift_val = shift_map.get(data.shift, 0)
    remarks_clean = re.sub(r'[^a-z0-9\s]', ' ', data.remarks.lower()).strip()

    row = pd.DataFrame([{
        'channel_name': channel_val,
        'category': category_val,
        'Tenure Bucket': tenure_val,
        'Agent Shift': shift_val,
        'response_time_minutes': data.response_time,
        'hour_reported': 10,
        'day_of_week': 1,
        'subcat_freq': 0.05
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
        "model_used": model_name
    }


@app.get("/health")
def health():
    return {"status": "ok", "model": model_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

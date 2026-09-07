"""
REST API Microservice — Dự đoán Mức độ Hài lòng Khách hàng (CSAT Prediction API)
Endpoint chuẩn Appendix C: /predict
Chạy: uvicorn app:app --port 8003
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import re
import os
from scipy.sparse import hstack, csr_matrix

app = FastAPI(
    title="Customer Behavior (CSAT) Prediction REST API",
    description="Microservice REST API dự đoán mức độ hài lòng khách hàng dựa trên dữ liệu vận hành và văn bản",
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

preprocessor_tabular = prep_artifact['preprocessor_tabular']
tfidf_vectorizer = prep_artifact['tfidf_vectorizer']
channel_map = prep_artifact['channel_map']
tenure_map = prep_artifact['tenure_map']
shift_map = prep_artifact['shift_map']
category_map = prep_artifact['category_map']
subcat_freq_map = prep_artifact['subcat_freq_map']


class CSATInput(BaseModel):
    channel: str = Field("Inbound", description="Kênh liên hệ")
    category: str = Field("Returns", description="Danh mục sự cố")
    tenure: str = Field(">90", description="Kinh nghiệm nhân viên")
    shift: str = Field("Morning", description="Ca trực")
    response_time: float = Field(10.0, ge=0, description="Thời gian phản hồi (phút)")
    remarks: str = Field("", description="Nhận xét của khách hàng")


@app.get("/health")
def health():
    return {"status": "ok", "service": "Customer Behavior CSAT API", "model": type(model).__name__}


@app.post("/predict")
def predict(data: CSATInput):
    try:
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
            "model_used": type(model).__name__
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)

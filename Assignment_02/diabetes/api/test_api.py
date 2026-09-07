"""
Client CLI kiểm thử Diabetes REST API
Chạy: python test_api.py
"""
import urllib.request
import json

url = "http://localhost:8001/predict"
sample_patient = {
    "gender": "Female",
    "age": 45,
    "hypertension": 0,
    "heart_disease": 0,
    "smoking_history": "never",
    "bmi": 24.5,
    "hbA1c_level": 5.4,
    "blood_glucose_level": 95,
    "race": "Caucasian"
}

print(f"Gửi yêu cầu POST tới {url}...")
req = urllib.request.Request(
    url,
    data=json.dumps(sample_patient).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("[THÀNH CÔNG] Phản hồi từ API:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"[LỖI] Không thể kết nối tới API: {e}")
    print("Vui lòng đảm bảo server API đang chạy: uvicorn app:app --port 8001 (trong thư mục api/)")

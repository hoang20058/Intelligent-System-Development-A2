"""
Client CLI kiểm thử House Price REST API
Chạy: python test_api.py
"""
import urllib.request
import json

url = "http://localhost:8002/predict"
sample_house = {
    "bed": 3,
    "bath": 2,
    "house_size": 1850.0,
    "acre_lot": 0.25,
    "state": "California",
    "city": "Los Angeles",
    "status": "for_sale"
}

print(f"Gửi yêu cầu POST tới {url}...")
req = urllib.request.Request(
    url,
    data=json.dumps(sample_house).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("[THÀNH CÔNG] Phản hồi từ API:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"[LỖI] Không thể kết nối tới API: {e}")
    print("Vui lòng đảm bảo server API đang chạy: uvicorn app:app --port 8002 (trong thư mục api/)")

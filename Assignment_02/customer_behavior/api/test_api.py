"""
Client CLI kiểm thử Customer Behavior REST API
Chạy: python test_api.py
"""
import urllib.request
import json

url = "http://localhost:8003/predict"
sample_ticket = {
    "channel": "Inbound",
    "category": "Returns",
    "tenure": ">90",
    "shift": "Morning",
    "response_time": 8.0,
    "remarks": "The agent was super polite and helped resolve my return immediately!"
}

print(f"Gửi yêu cầu POST tới {url}...")
req = urllib.request.Request(
    url,
    data=json.dumps(sample_ticket).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode("utf-8"))
        print("[THÀNH CÔNG] Phản hồi từ API:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"[LỖI] Không thể kết nối tới API: {e}")
    print("Vui lòng đảm bảo server API đang chạy: uvicorn app:app --port 8003 (trong thư mục api/)")

import json
import requests

def predict_house_price(bed, bath, house_size, state="California", acre_lot=0.25, status="for_sale"):
    url = "http://127.0.0.1:5002/houseprice/v1/predict"
    data = {
        "bed": int(bed),
        "bath": int(bath),
        "house_size": float(house_size),
        "state": state,
        "acre_lot": float(acre_lot),
        "status": status
    }
    headers = {"Content-type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("=" * 65)
    print("   CHƯƠNG TRÌNH DỰ ĐOÁN GIÁ BẤT ĐỘNG SẢN (PYTHON CLIENT)")
    print("=" * 65)

    bed_in = input("Nhập số phòng ngủ (bed, ví dụ: 3): ") or "3"
    bath_in = input("Nhập số phòng tắm (bath, ví dụ: 2): ") or "2"
    size_in = input("Nhập diện tích sàn (sqft, ví dụ: 2000): ") or "2000"
    state_in = input("Nhập bang (state, ví dụ: California / Texas / Florida): ") or "California"

    result = predict_house_price(bed_in, bath_in, size_in, state_in)

    if "error" in result:
        print(f"[Lỗi kết nối]: {result['error']}")
        print("Vui lòng đảm bảo bạn đã khởi chạy 'python REST_API.py' trên Terminal trước.")
    else:
        print(f"[Kết quả Dự đoán]: {result['formatted']}")
        print(f"Mô hình sử dụng: {result['model_used']}")

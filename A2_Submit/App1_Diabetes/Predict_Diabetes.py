import json
import requests

def predict_diabetes(BMI, Age, Glucose, HbA1c=5.5):
    url = 'http://127.0.0.1:5000/diabetes/v1/predict'
    data = {
        "BMI": float(BMI),
        "Age": int(Age),
        "Glucose": float(Glucose),
        "HbA1c": float(HbA1c)
    }
    data_json = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    try:
        response = requests.post(url, data=data_json, headers=headers)
        result = json.loads(response.text)
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("=" * 60)
    print("   CHƯƠNG TRÌNH DỰ ĐOÁN NGUY CƠ TIỂU ĐƯỜNG (PYTHON CLIENT)")
    print("=" * 60)
    
    # Cho phép nhập liệu từ bàn phím
    bmi_in = input('BMI? ') or "30"
    age_in = input('Age? ') or "29"
    glucose_in = input('Glucose? ') or "100"
    
    predictions = predict_diabetes(bmi_in, age_in, glucose_in)
    
    if "error" in predictions:
        print(f"\n[Lỗi kết nối tới Server]: {predictions['error']}")
        print("Vui lòng đảm bảo bạn đã khởi chạy 'python REST_API.py' trên một Terminal khác trước.")
    else:
        status = "Diabetic (Có nguy cơ)" if predictions.get("prediction") == 1 else "Not Diabetic (Không có nguy cơ)"
        print(f"\nKết quả chẩn đoán: {status}")
        print(f"Độ tin cậy:        {predictions.get('confidence', 'N/A')}%")

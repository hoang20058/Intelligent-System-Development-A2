import json
import requests

def predict_csat(channel, category, tenure, shift, response_time, remarks=""):
    url = "http://127.0.0.1:5003/csat/v1/predict"
    data = {
        "channel": channel,
        "category": category,
        "tenure": tenure,
        "shift": shift,
        "response_time": float(response_time),
        "remarks": remarks
    }
    headers = {"Content-type": "application/json"}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return json.loads(response.text)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("=" * 65)
    print("  DU DOAN MUC DO HAI LONG KHACH HANG (CSAT PREDICTION)")
    print("=" * 65)

    channel = input("Kenh lien he (Inbound/Outcall/Email)? ") or "Inbound"
    category = input("Danh muc su co (Returns/Order Related/Refund Related)? ") or "Returns"
    tenure = input("Kinh nghiem nhan vien (On Job Training/0-30/31-60/61-90/>90)? ") or ">90"
    shift = input("Ca truc (Morning/Afternoon/Evening/Night)? ") or "Morning"
    response_time = input("Thoi gian phan hoi (phut)? ") or "10"
    remarks = input("Nhan xet cua khach hang (de trong neu khong co)? ") or ""

    result = predict_csat(channel, category, tenure, shift, response_time, remarks)

    if "error" in result:
        print(f"
[Loi]: {result['error']}")
    else:
        label = result['label']
        conf = result['confidence']
        icon = "[HAI LONG]" if label == "Satisfied" else "[CANH BAO - NGUY CO]"
        print(f"
{icon} Ket qua: {label} (Do tin cay: {conf}%)")
        print(f"  P(Hai long):     {result['probability_satisfied']}%")
        print(f"  P(Khong hai long): {result['probability_at_risk']}%")

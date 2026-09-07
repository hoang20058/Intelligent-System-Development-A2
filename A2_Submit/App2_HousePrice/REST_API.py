import pickle
import os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Đường dẫn nạp mô hình đã lưu ---
filename = os.path.join(os.path.dirname(__file__), 'models', 'house_price.sav')
if not os.path.exists(filename):
    filename = 'house_price.sav'

with open(filename, 'rb') as f:
    artifact = pickle.load(f)

loaded_pipeline = artifact['pipeline']
feature_columns = artifact['feature_columns']
status_map = artifact['status_map']
state_classes = artifact['state_classes']
city_freq_map = artifact['city_freq_map']
model_name = artifact['model_name']

@app.route('/houseprice/v1/predict', methods=['POST'])
def predict():
    # --- Nhận dữ liệu JSON từ client ---
    features = request.json
    if not features:
        return jsonify({'error': 'No input data provided'}), 400

    bed = float(features.get('bed', 3))
    bath = float(features.get('bath', 2))
    acre_lot = float(features.get('acre_lot', 0.25))
    house_size = float(features.get('house_size', 1800))
    status_raw = features.get('status', 'for_sale')
    status_val = status_map.get(status_raw, 0)
    state = features.get('state', 'California')
    state_encoded = state_classes.index(state) if state in state_classes else 0
    city = features.get('city', '')
    city_freq = city_freq_map.get(city, 0.0001)

    input_row = {
        'bed': bed,
        'bath': bath,
        'acre_lot': acre_lot,
        'house_size': house_size,
        'status': status_val,
        'state_encoded': state_encoded,
        'city_freq': city_freq
    }

    df_input = pd.DataFrame([input_row])[feature_columns]

    # --- Dự đoán và chuyển đổi ngược từ Log-space về USD ---
    pred_log = loaded_pipeline.predict(df_input)[0]
    pred_price_usd = float(np.expm1(pred_log))
    pred_price_usd = max(pred_price_usd, 0)

    # --- Đóng gói phản hồi JSON ---
    response = {
        'prediction': round(pred_price_usd, 2),
        'formatted': f"${pred_price_usd:,.0f}",
        'model_used': model_name
    }
    return jsonify(response)

if __name__ == '__main__':
    print(f"[OK] Flask REST API đang chạy tại http://127.0.0.1:5002 ...")
    app.run(host='0.0.0.0', port=5002)

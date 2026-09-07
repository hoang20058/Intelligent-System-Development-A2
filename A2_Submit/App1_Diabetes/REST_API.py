import pickle
import os
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Đường dẫn nạp mô hình đã lưu ---
filename = os.path.join(os.path.dirname(__file__), 'models', 'diabetes.sav')
if not os.path.exists(filename):
    filename = 'diabetes.sav'

with open(filename, 'rb') as f:
    artifact = pickle.load(f)

loaded_pipeline = artifact['pipeline']
feature_columns = artifact['feature_columns']
gender_map = artifact.get('gender_map', {'Female': 0, 'Male': 1, 'Other': 2})
smoking_map = artifact.get('smoking_map', {'No Info': 0, 'never': 1, 'former': 2, 'not current': 3, 'ever': 4, 'current': 5})

@app.route('/diabetes/v1/predict', methods=['POST'])
def predict():
    # --- Nhận dữ liệu JSON từ client ---
    features = request.json
    if not features:
        return jsonify({'error': 'No input data provided'}), 400

    # Hỗ trợ cả định dạng cơ bản (BMI, Age, Glucose) lẫn định dạng đầy đủ
    age = float(features.get("Age", features.get("age", 45)))
    bmi = float(features.get("BMI", features.get("bmi", 25.0)))
    glucose = float(features.get("Glucose", features.get("blood_glucose_level", 100)))
    hba1c = float(features.get("HbA1c", features.get("hbA1c_level", 5.5)))
    gender_raw = features.get("Gender", features.get("gender", "Female"))
    gender = gender_map.get(gender_raw, 0) if isinstance(gender_raw, str) else int(gender_raw)
    hypertension = int(features.get("hypertension", 0))
    heart_disease = int(features.get("heart_disease", 0))
    smoking_raw = features.get("smoking_history", "never")
    smoking = smoking_map.get(smoking_raw, 1) if isinstance(smoking_raw, str) else int(smoking_raw)
    race = features.get("race", "Caucasian")

    race_cols = {f'race:{r}': 0 for r in ['AfricanAmerican', 'Asian', 'Caucasian', 'Hispanic', 'Other']}
    race_key = f'race:{race}'
    if race_key in race_cols:
        race_cols[race_key] = 1

    input_row = {
        'gender': gender,
        'age': age,
        **race_cols,
        'hypertension': hypertension,
        'heart_disease': heart_disease,
        'smoking_history': smoking,
        'bmi': bmi,
        'hbA1c_level': hba1c,
        'blood_glucose_level': glucose
    }

    df_input = pd.DataFrame([input_row])[feature_columns]

    # --- Thực hiện dự đoán ---
    prediction = loaded_pipeline.predict(df_input)
    confidence = loaded_pipeline.predict_proba(df_input)

    # --- Đóng gói phản hồi JSON ---
    response = {}
    response['prediction'] = int(prediction[0])
    response['label'] = "Diabetic" if int(prediction[0]) == 1 else "Not Diabetic"
    response['confidence'] = str(round(np.amax(confidence[0]) * 100, 2))
    return jsonify(response)

if __name__ == '__main__':
    print("Flask API Server is running on port 5000...")
    app.run(host='0.0.0.0', port=5000)

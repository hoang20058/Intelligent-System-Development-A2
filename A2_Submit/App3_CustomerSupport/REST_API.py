import pickle
import os
import re
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from scipy.sparse import hstack, csr_matrix

app = Flask(__name__)

filename = os.path.join(os.path.dirname(__file__), 'models', 'csat_model.sav')
with open(filename, 'rb') as f:
    artifact = pickle.load(f)

model = artifact['model']
preprocessor_tabular = artifact['preprocessor_tabular']
tfidf_vectorizer = artifact['tfidf_vectorizer']
tabular_features = artifact['tabular_features']
channel_map = artifact['channel_map']
tenure_map = artifact['tenure_map']
shift_map = artifact['shift_map']
category_map = artifact['category_map']
subcat_freq_map = artifact['subcat_freq_map']
model_name = artifact.get('model_name', 'Combined Model')

@app.route('/csat/v1/predict', methods=['POST'])
def predict():
    features = request.json
    if not features:
        return jsonify({'error': 'No input data provided'}), 400

    channel = channel_map.get(features.get('channel', 'Inbound'), 0)
    category = category_map.get(features.get('category', 'Returns'), 0)
    tenure = tenure_map.get(features.get('tenure', '>90'), 4)
    shift = shift_map.get(features.get('shift', 'Morning'), 0)
    response_time = float(features.get('response_time', 10))
    hour = int(features.get('hour', 10))
    day = int(features.get('day_of_week', 1))
    subcat = features.get('subcategory', '')
    subcat_freq = subcat_freq_map.get(subcat, 0.01)
    remarks = features.get('remarks', '')

    remarks_clean = re.sub(r'[^a-z0-9\s]', ' ', remarks.lower()).strip()

    row = pd.DataFrame([{
        'channel_name': channel, 'category': category,
        'Tenure Bucket': tenure, 'Agent Shift': shift,
        'response_time_minutes': response_time,
        'hour_reported': hour, 'day_of_week': day,
        'subcat_freq': subcat_freq
    }])

    tab_scaled = preprocessor_tabular.transform(row)
    text_vec = tfidf_vectorizer.transform([remarks_clean])
    combined = hstack([csr_matrix(tab_scaled), text_vec])

    pred = int(model.predict(combined)[0])
    prob = model.predict_proba(combined)[0].tolist()

    return jsonify({
        'prediction': pred,
        'label': 'Satisfied' if pred == 1 else 'At-Risk',
        'confidence': round(max(prob) * 100, 1),
        'probability_satisfied': round(prob[1] * 100, 1),
        'probability_at_risk': round(prob[0] * 100, 1),
        'model_used': model_name
    })

if __name__ == '__main__':
    print(f"[OK] Flask CSAT API dang chay tai http://127.0.0.1:5003")
    app.run(host='0.0.0.0', port=5003)

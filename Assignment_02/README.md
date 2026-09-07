# ASSIGNMENT 02 — PHÁT TRIỂN HỆ THỐNG THÔNG MINH

## Intelligent System Development: From Data Representation to Deployable Systems

* **Học phần**: Phát triển Hệ thống Thông minh (Intelligent System Development)
* **Giảng viên**: PGS. TS. Trần Đình Quế
* **Năm học**: 2025 – 2026

---

## 📑 MỤC LỤC
1. [Cấu trúc Thư mục Nộp bài (Repository Structure)](#1-cấu-trúc-thư-mục-nộp-bài-repository-structure)
2. [Tổng quan 3 Hệ thống Thông minh](#2-tổng-quan-3-hệ-thống-thông-minh)
3. [Cài đặt Môi trường (Prerequisites)](#3-cài-đặt-môi-trường-prerequisites)
4. [Hướng dẫn Khởi chạy Từng Ứng dụng](#4-hướng-dẫn-khởi-chạy-từng-ứng-dụng)
   - [Đề tài 1: Diabetes Risk Prediction](#đề-tài-1-diabetes-risk-prediction)
   - [Đề tài 2: US House Price Prediction](#đề-tài-2-us-house-price-prediction)
   - [Đề tài 3: Customer Behavior CSAT Prediction](#đề-tài-3-customer-behavior-csat-prediction)
5. [Quy chuẩn API & Biểu mẫu Báo cáo](#5-quy-chuẩn-api--biểu-mẫu-báo-cáo)

---

## 1. CẤU TRÚC THƯ MỤC NỘP BÀI (REPOSITORY STRUCTURE)

Tuân thủ nghiêm ngặt **Appendix A — Repository Structure** của tài liệu hướng dẫn:

```text
Assignment_02/
|
+-- diabetes/                      # Đề tài 1: Sàng lọc Bệnh Tiểu đường
|   +-- data/                      # Dữ liệu huấn luyện gốc (diabetes_dataset.csv)
|   +-- notebook/                  # Jupyter Notebook 23 mục theo Appendix B
|   +-- model/                     # Mô hình & Tiền xử lý đã lưu
|   |   +-- preprocessor.joblib    # Pipeline tiền xử lý & Encoding
|   |   +-- model.joblib           # Mô hình phân loại Decision Tree (Tuned)
|   +-- api/                       # Microservice REST API độc lập (Port 8001)
|   |   +-- app.py                 # FastAPI Server phục vụ endpoint /predict
|   |   +-- test_api.py            # Script CLI kiểm thử API
|   +-- web/                       # Giao diện Web Desktop UI (Port 8101)
|   |   +-- app.py                 # Web Server FastAPI
|   |   +-- templates/index.html   # Giao diện Bootstrap 5 Desktop
|   +-- mobile/                    # Ứng dụng Di động
|   |   +-- app.py                 # Mobile Web touch client (Port 8201)
|   |   +-- templates/mobile.html  # Giả lập giao diện điện thoại cảm ứng
|   |   +-- App.js                 # Mã nguồn React Native (Expo)
|   |   +-- package.json           # Cấu hình Expo SDK 52
|   |   +-- app.json               # Cấu hình ứng dụng di động
|   +-- requirements.txt           # Thư viện phụ thuộc
|
+-- house_price/                   # Đề tài 2: Định giá Nhà ở Hoa Kỳ
|   +-- data/                      # realtor-data.zip.csv
|   +-- notebook/                  # house_price_prediction.ipynb
|   +-- model/
|   |   +-- preprocessor.joblib    # Preprocessor StandardScaler + Maps
|   |   +-- model.joblib           # Gradient Boosting Regressor
|   +-- api/                       # REST API (Port 8002)
|   |   +-- app.py
|   |   +-- test_api.py
|   +-- web/                       # Web Desktop UI (Port 8102)
|   |   +-- app.py
|   |   +-- templates/index.html
|   +-- mobile/                    # Mobile Application (Port 8202 / React Native)
|   |   +-- app.py
|   |   +-- templates/mobile.html
|   |   +-- App.js
|   |   +-- package.json
|   |   +-- app.json
|   +-- requirements.txt
|
+-- customer_behavior/             # Đề tài 3: Hài lòng Khách hàng (CSAT)
|   +-- data/                      # Customer_support_data.csv
|   +-- notebook/                  # customer_support_csat.ipynb
|   +-- model/
|   |   +-- preprocessor.joblib    # Preprocessor bảng + TF-IDF Vectorizer
|   |   +-- model.joblib           # Logistic Regression Classifier
|   +-- api/                       # REST API (Port 8003)
|   |   +-- app.py
|   |   +-- test_api.py
|   +-- web/                       # Web Desktop UI (Port 8103)
|   |   +-- app.py
|   |   +-- templates/index.html
|   +-- mobile/                    # Mobile Application (Port 8203 / React Native)
|   |   +-- app.py
|   |   +-- templates/mobile.html
|   |   +-- App.js
|   |   +-- package.json
|   |   +-- app.json
|   +-- requirements.txt
|
+-- report/                        # Báo cáo Kỹ thuật Bàn giao
|   +-- Assignment_02.docx         # Báo cáo Word 15 mục chi tiết
|   +-- Assignment_02.pdf          # Tệp PDF chính thức nộp bài
|
+-- README.md                      # Tài liệu hướng dẫn tổng quan toàn dự án
```

---

## 2. TỔNG QUAN 3 HỆ THỐNG THÔNG MINH

| Thông số | Đề tài 1: Diabetes | Đề tài 2: House Price | Đề tài 3: Customer Behavior |
| :--- | :--- | :--- | :--- |
| **Bài toán** | Phân loại Nhị phân (Binary Classification) | Hồi quy Giá trị (Continuous Regression) | Phân loại Đa phương thức (Tabular + NLP) |
| **Mục tiêu** | Sàng lọc nguy cơ đái tháo đường | Định giá bất động sản Hoa Kỳ (USD) | Dự đoán mức độ hài lòng khách hàng CSAT |
| **Dữ liệu** | 100,000 bản ghi lâm sàng | 100,000 giao dịch nhà đất thực tế | 85,907 phiếu hỗ trợ khách hàng e-Commerce |
| **Mô hình Tốt nhất** | Decision Tree (Tuned, max_depth=6) | Gradient Boosting Regressor | Logistic Regression (Text + Tabular) |
| **Độ chính xác / Sai số** | Accuracy: 97.23%, F1-Macro: 0.9023 | $R^2$: 0.612, RMSE (log): 0.603 | Accuracy: 78.4%, ROC-AUC: 0.821 |
| **Cổng REST API** | Port `8001` | Port `8002` | Port `8003` |
| **Cổng Web Dashboard** | Port `8101` | Port `8102` | Port `8103` |
| **Cổng Mobile Touch** | Port `8201` | Port `8202` | Port `8203` |

---

## 3. CÀI ĐẶT MÔI TRƯỜNG (PREREQUISITES)

Yêu cầu máy tính cài đặt Python 3.10+ (khuyến nghị Python 3.11 – 3.13 hoặc Anaconda):

```bash
# Cài đặt toàn bộ thư viện cần thiết
pip install fastapi uvicorn pydantic scikit-learn pandas numpy scipy joblib jinja2 requests
```

---

## 4. HƯỚNG DẪN KHỞI CHẠY TỪNG ỨNG DỤNG

Mỗi đề tài được tổ chức hoàn toàn độc lập và có thể chạy riêng rẽ từng phần `api/`, `web/`, và `mobile/`:

### Đề tài 1: Diabetes Risk Prediction

1. **Khởi chạy REST API Microservice:**
   ```bash
   cd diabetes/api
   uvicorn app:app --port 8001
   ```
   * Swagger Documentation: `http://localhost:8001/docs`
   * Kiểm thử nhanh từ dòng lệnh: `python test_api.py`

2. **Khởi chạy Giao diện Web Desktop:**
   ```bash
   cd diabetes/web
   uvicorn app:app --port 8101
   ```
   * Mở trình duyệt truy cập: `http://localhost:8101`

3. **Khởi chạy Ứng dụng Di động (Mobile):**
   * **Cách 1: Trình duyệt Mobile Touch Simulator (Không cần cài Node.js):**
     ```bash
     cd diabetes/mobile
     uvicorn app:app --port 8201
     ```
     Truy cập: `http://localhost:8201`
   * **Cách 2: Ứng dụng React Native / Expo Go trên điện thoại:**
     ```bash
     cd diabetes/mobile
     npm install
     npx expo start
     ```
     Quét mã QR bằng Expo Go trên Android / iOS.

---

### Đề tài 2: US House Price Prediction

1. **Khởi chạy REST API Microservice:**
   ```bash
   cd house_price/api
   uvicorn app:app --port 8002
   ```
   * Swagger Documentation: `http://localhost:8002/docs`
   * Kiểm thử nhanh từ dòng lệnh: `python test_api.py`

2. **Khởi chạy Giao diện Web Desktop:**
   ```bash
   cd house_price/web
   uvicorn app:app --port 8102
   ```
   * Mở trình duyệt truy cập: `http://localhost:8102`

3. **Khởi chạy Ứng dụng Di động (Mobile):**
   * **Cách 1: Mobile Touch Simulator:**
     ```bash
     cd house_price/mobile
     uvicorn app:app --port 8202
     ```
     Truy cập: `http://localhost:8202`
   * **Cách 2: React Native (Expo):**
     ```bash
     cd house_price/mobile
     npm install
     npx expo start
     ```

---

### Đề tài 3: Customer Behavior CSAT Prediction

1. **Khởi chạy REST API Microservice:**
   ```bash
   cd customer_behavior/api
   uvicorn app:app --port 8003
   ```
   * Swagger Documentation: `http://localhost:8003/docs`
   * Kiểm thử nhanh từ dòng lệnh: `python test_api.py`

2. **Khởi chạy Giao diện Web Desktop:**
   ```bash
   cd customer_behavior/web
   uvicorn app:app --port 8103
   ```
   * Mở trình duyệt truy cập: `http://localhost:8103`

3. **Khởi chạy Ứng dụng Di động (Mobile):**
   * **Cách 1: Mobile Touch Simulator:**
     ```bash
     cd customer_behavior/mobile
     uvicorn app:app --port 8203
     ```
     Truy cập: `http://localhost:8203`
   * **Cách 2: React Native (Expo):**
     ```bash
     cd customer_behavior/mobile
     npm install
     npx expo start
     ```

---

## 5. QUY CHUẨN API & BIỂU MẪU BÁO CÁO

### Luồng Dữ liệu Chuẩn (Appendix C):
$$\text{JSON Input} \longrightarrow \text{Pydantic Validation} \longrightarrow \text{Preprocessor Pipeline} \longrightarrow \text{Machine Learning Model} \longrightarrow \text{JSON Output}$$

* **Đề tài 1: Diabetes Prediction**
  * Endpoint: `POST http://localhost:8001/predict`
  * Body mẫu:
    ```json
    {
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
    ```
  * Response mẫu:
    ```json
    {
      "prediction": 0,
      "label": "Không có nguy cơ tiểu đường",
      "confidence": 100.0,
      "probabilities": { "khong_benh": 100.0, "co_benh": 0.0 },
      "model_used": "DecisionTreeClassifier"
    }
    ```

* **Đề tài 2: House Price Prediction**
  * Endpoint: `POST http://localhost:8002/predict`
  * Body mẫu:
    ```json
    {
      "bed": 3,
      "bath": 2,
      "house_size": 1850.0,
      "acre_lot": 0.25,
      "state": "California",
      "city": "Los Angeles",
      "status": "for_sale"
    }
    ```
  * Response mẫu:
    ```json
    {
      "prediction": 1045351.26,
      "formatted": "$1,045,351",
      "model_used": "GradientBoostingRegressor"
    }
    ```

* **Đề tài 3: Customer Behavior CSAT Prediction**
  * Endpoint: `POST http://localhost:8003/predict`
  * Body mẫu:
    ```json
    {
      "channel": "Inbound",
      "category": "Returns",
      "tenure": ">90",
      "shift": "Morning",
      "response_time": 8.0,
      "remarks": "The agent was super polite and helped resolve my return immediately!"
    }
    ```
  * Response mẫu:
    ```json
    {
      "prediction": 1,
      "label": "Satisfied",
      "confidence": 82.4,
      "probability_satisfied": 82.4,
      "probability_at_risk": 17.6,
      "model_used": "LogisticRegression"
    }
    ```

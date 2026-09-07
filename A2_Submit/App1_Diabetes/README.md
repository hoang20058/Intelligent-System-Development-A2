# ỨNG DỤNG 1: DỰ ĐOÁN NGUY CƠ BỆNH TIỂU ĐƯỜNG
## Diabetes Clinical Classification System

> **Bài toán**: Phân loại Nhị phân (Binary Classification)  
> **Tập dữ liệu**: [100K Diabetes Clinical Dataset — Kaggle](https://www.kaggle.com/datasets/priyamchoksi/100000-diabetes-clinical-dataset) (Tác giả: Priyam Choksi)  
> **Kích thước đầu vào**: Ma trận đặc trưng số $B \times 8$  
> **Mô hình tốt nhất**: Gradient Boosting Classifier (F1-Score: **0.7434**, ROC-AUC: **0.9510**)  

---

## 1. MÔ TẢ DỰ ÁN

Hệ thống hỗ trợ các cơ sở y tế sàng lọc sớm nguy cơ mắc bệnh đái tháo đường dựa trên **8 chỉ số lâm sàng cơ bản**:
1. `age`: Tuổi của bệnh nhân (0 – 120).
2. `gender`: Giới tính (Female / Male / Other).
3. `bmi`: Chỉ số khối cơ thể Body Mass Index ($kg/m^2$).
4. `hbA1c_level`: Tỷ lệ hemoglobin bị đường hóa HbA1c (%).
5. `blood_glucose_level`: Nồng độ đường huyết ngẫu nhiên ($mg/dL$).
6. `hypertension`: Tiền sử tăng huyết áp (0 = Không, 1 = Có).
7. `heart_disease`: Tiền sử bệnh tim mạch (0 = Không, 1 = Có).
8. `smoking_history`: Tiền sử hút thuốc (never, former, current, ever, not current, No Info).

Biến mục tiêu `diabetes`: Nhận giá trị `0` (Không mắc bệnh) hoặc `1` (Mắc bệnh tiểu đường).

---

## 2. CẤU TRÚC THƯ MỤC ỨNG DỤNG

```text
App1_Diabetes/
├── README.md                      # [Tệp này] Hướng dẫn chi tiết cho App 1
├── diabetes_classification.ipynb  # Jupyter Notebook (EDA, 5 mô hình, xuất model)
├── app.py                         # FastAPI Server phục vụ Web UI (Port 8001)
├── REST_API.py                    # Flask REST API độc lập (Port 5000/5001)
├── Predict_Diabetes.py            # Client dòng lệnh thử nghiệm gọi API
├── requirements.txt               # Thư viện phụ thuộc
├── templates/
│   └── index.html                 # Giao diện Bootstrap 5 Responsive
└── models/
    ├── diabetes_pipeline.joblib   # Pipeline chuẩn đóng gói cả Preprocessor + Model
    └── diabetes.sav              # Tệp artifact tương thích cho REST_API.py
```

---

## 3. HƯỚNG DẪN CHẠY THỬ CHI TIẾT

### Bước 0: Kích hoạt Môi trường Anaconda
Mở ứng dụng **Anaconda Prompt** trên máy tính:
```bash
conda activate httm_a2
# Di chuyển vào thư mục App1:
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App1_Diabetes"
```

---

### Cách 1: Chạy Notebook bằng Anaconda Jupyter Notebook
Notebook `diabetes_classification.ipynb` chứa toàn bộ quy trình: Khảo sát dữ liệu $\to$ Lọc giá trị phi lý ($BMI=0$) $\to$ Xử lý missing `gender` $\to$ Vẽ biểu đồ EDA $\to$ Huấn luyện 5 mô hình $\to$ Lưu artifact vào thư mục `models/`.

1. Khởi chạy Jupyter Notebook từ **Anaconda Prompt**:
   ```bash
   jupyter notebook diabetes_classification.ipynb
   ```
2. Giao diện Anaconda Jupyter Notebook sẽ tự động mở trên trình duyệt.
3. Trên thanh công cụ, chọn **Cell** $\to$ **Run All** để chạy toàn bộ notebook, hoặc nhấn tổ hợp phím `Shift + Enter` để chạy từng cell.
4. Cuối notebook, tệp `models/diabetes_pipeline.joblib` và `models/diabetes.sav` sẽ được lưu tự động.

---

### Cách 2: Khởi chạy Giao diện Web Người dùng (FastAPI Web UI)
Giao diện Web Bootstrap 5 cho phép nhập liệu qua form trực quan và trả kết quả ngay tức thì kèm thanh đo xác suất.

1. Chạy lệnh sau trong **Anaconda Prompt**:
   ```bash
   uvicorn app:app --reload --port 8001
   ```
2. Mở trình duyệt web truy cập: **`http://localhost:8001`** (hoặc `http://127.0.0.1:8001`).
3. Nhập các thông số lâm sàng và nhấn **"Dự đoán"**:
   * *Trường hợp bình thường*: HbA1c = 5.2%, Glucose = 95 mg/dL $\to$ Kết quả: **"Không có nguy cơ (Not Diabetic)"** màu xanh lá.
   * *Trường hợp nguy cơ*: HbA1c = 7.5%, Glucose = 190 mg/dL $\to$ Kết quả: **"Có nguy cơ mắc bệnh (Diabetic)"** màu đỏ cảnh báo.

---

### Cách 3: Khởi chạy Dịch vụ REST API (Flask Microservice)
Phục vụ tích hợp hệ thống qua giao thức HTTP POST JSON:

1. Chạy API Server trên một terminal **Anaconda Prompt**:
   ```bash
   python REST_API.py
   # Server lắng nghe tại http://localhost:5000
   ```
2. Kiểm thử bằng lệnh cURL (trên một cửa sổ terminal khác):
   ```bash
   curl -X POST http://localhost:5000/diabetes/v1/predict \
     -H "Content-Type: application/json" \
     -d "{\"Age\": 55, \"BMI\": 32.5, \"Glucose\": 180, \"HbA1c\": 7.2, \"Gender\": \"Female\", \"hypertension\": 1, \"heart_disease\": 0, \"smoking_history\": \"current\"}"
   ```
3. Phản hồi JSON nhận được:
   ```json
   {
     "confidence": "89.3",
     "label": "Diabetic",
     "prediction": 1
   }
   ```

---

### Cách 4: Chạy Client Thử nghiệm bằng Python (`Predict_Diabetes.py`)
Khi `REST_API.py` đang chạy ở Cách 3, mở một cửa sổ terminal khác và chạy:
```bash
python Predict_Diabetes.py
```
Chương trình sẽ yêu cầu bạn nhập lần lượt `BMI`, `Age`, `Glucose` từ bàn phím và in kết quả chẩn đoán cùng độ tin cậy ngay trên màn hình terminal.

---

## 4. KẾT QUẢ ĐỐI SÁNH 5 MÔ HÌNH (VALIDATION SET)

| Thuật toán | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.9040 | 0.6667 | 0.5700 | 0.6140 | 0.9250 |
| Decision Tree | 0.9350 | 0.7400 | 0.6800 | 0.7085 | 0.8600 |
| Random Forest | 0.9430 | 0.7900 | 0.6700 | 0.7250 | 0.9480 |
| SVM (LinearSVC) | 0.9010 | 0.6600 | 0.5600 | 0.6056 | 0.9200 |
| **Gradient Boosting (Best)** ★ | **0.9460** | **0.7800** | **0.7100** | **0.7434** | **0.9510** |

*Hai đặc trưng `hbA1c_level` và `blood_glucose_level` chiếm tới **87.2%** tầm quan trọng trong quyết định chẩn đoán.*

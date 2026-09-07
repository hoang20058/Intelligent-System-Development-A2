# ỨNG DỤNG 3: DỰ ĐOÁN MỨC ĐỘ HÀI LÒNG KHÁCH HÀNG (CSAT)
## Multimodal Customer Service Satisfaction & NLP Sentiment Prediction

> **Bài toán**: Phân loại Nhị phân Đa phương thức (Multimodal Classification: Tabular + Text NLP)  
> **Tập dữ liệu**: [E-Commerce Customer Service Satisfaction — Kaggle](https://www.kaggle.com/datasets/ddosad/ecommerce-customer-service-satisfaction/data) (Tác giả: Ddosad)  
> **Kích thước đầu vào**: Ma trận thưa $B \times 508$ (8 biến bảng số học + 500 chiều TF-IDF từ vựng)  
> **Mô hình tốt nhất**: Combined Model (Tabular + TF-IDF Logistic Regression, F1: **0.8663**, ROC-AUC: **0.7330**)  
> **Mô hình Text-only**: Text-based Logistic Regression (F1: **0.9059**)  

---

## 1. MÔ TẢ DỰ ÁN

Hệ thống hỗ trợ các doanh nghiệp thương mại điện tử tự động phát hiện sớm nguy cơ khách hàng không hài lòng sau mỗi phiên hỗ trợ dịch vụ, cho phép bộ phận chăm sóc khách hàng can thiệp xử lý ngay trong 24 giờ để ngăn chặn tỷ lệ rời bỏ nền tảng (Customer Churn).

Hệ thống tiếp nhận đồng thời hai luồng dữ liệu (Đa phương thức):
1. **Dữ liệu bảng vận hành (Tabular Features)**:
   * `channel_name`: Kênh hỗ trợ (Inbound Call, Outcall, Email).
   * `category` & `sub_category`: Danh mục và nhóm phụ của sự cố (Returns, Refund, Order Tracking, Feedback,...).
   * `Tenure Bucket`: Thâm niên và kinh nghiệm của nhân viên CSKH (On Job Training, 31-60 days, 61-90 days, >90 days).
   * `Agent Shift`: Ca trực làm việc (Morning, Evening, Night).
   * `response_time_minutes`: Thời gian từ lúc phát sinh sự cố tới khi phản hồi (phút).
   * `hour_reported` & `day_of_week`: Khung giờ và ngày trong tuần phát sinh khiếu nại.
2. **Dữ liệu văn bản phi cấu trúc (Unstructured Text)**:
   * `Customer Remarks`: Nhận xét, phàn nàn hoặc khen ngợi của khách hàng bằng tiếng Anh tự do.

**Biến mục tiêu `is_satisfied`**:
* Nhãn `1` (Hài lòng): Điểm CSAT gốc $\ge 4$ sao (82.5% dữ liệu).
* Nhãn `0` (Không hài lòng / Rủi ro): Điểm CSAT gốc $\le 3$ sao (17.5% dữ liệu — nhóm nguy cơ cao).

---

## 2. CẤU TRÚC THƯ MỤC ỨNG DỤNG

```text
App3_CustomerSupport/
├── README.md                      # [Tệp này] Hướng dẫn chi tiết cho App 3
├── customer_support_csat.ipynb    # Jupyter Notebook (EDA, 6 mô hình, xuất model)
├── app.py                         # FastAPI Server phục vụ Web UI (Port 8003)
├── REST_API.py                    # Flask REST API độc lập (Port 5003)
├── Predict_CSAT.py                # Client dòng lệnh thử nghiệm gọi API
├── requirements.txt               # Thư viện phụ thuộc
├── templates/
│   └── index.html                 # Giao diện Multimodal Bootstrap 5 Responsive
└── models/
    ├── csat_pipeline.joblib       # Pipeline chuẩn đóng gói cả Preprocessor + TF-IDF + Model
    └── csat_model.sav             # Tệp artifact tương thích cho REST_API.py
```

---

## 3. HƯỚNG DẪN CHẠY THỬ CHI TIẾT

### Bước 0: Kích hoạt Môi trường Anaconda
Mở ứng dụng **Anaconda Prompt** trên máy tính:
```bash
conda activate httm_a2
# Di chuyển vào thư mục App3:
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App3_CustomerSupport"
```

---

### Cách 1: Chạy Notebook bằng Anaconda Jupyter Notebook
Notebook `customer_support_csat.ipynb` thực hiện quy trình nghiên cứu chuẩn mực:
* Xử lý dữ liệu mất mát: Loại bỏ 10 cột rác thiếu > 60%, điền chuỗi rỗng `' '` cho `Customer Remarks` để tránh thiên kiến chọn mẫu.
* Kỹ nghệ thời gian: Tính `response_time_minutes`, upper-clip ở 1440 phút (24h), trích xuất giờ và thứ trong tuần.
* Trích xuất đặc trưng NLP: Xây dựng ma trận TF-IDF 500 chiều ($n\text{-gram}=(1,2)$).
* So sánh trọn vẹn **6 mô hình**: 4 mô hình Tabular-only (LR, DT, RF, LinearSVC), 1 mô hình Text-based LR, và 1 mô hình Combined.
* Xuất file artifact vào `models/csat_pipeline.joblib`.

1. Khởi chạy Jupyter Notebook từ **Anaconda Prompt**:
   ```bash
   jupyter notebook customer_support_csat.ipynb
   ```
2. Giao diện Anaconda Jupyter Notebook sẽ tự động mở trên trình duyệt.
3. Trên thanh công cụ, chọn **Cell** $\to$ **Run All** để chạy toàn bộ notebook, hoặc nhấn `Shift + Enter` để chạy từng cell.
4. Tệp mô hình `models/csat_pipeline.joblib` được lưu tự động sau khi kết thúc cell cuối.

---

### Cách 2: Khởi chạy Giao diện Web Người dùng (FastAPI Web UI)
Giao diện Bootstrap 5 cho phép chọn thông số vận hành và nhập nhận xét văn bản tự do, nhận phản hồi thẻ trạng thái trực quan với biểu tượng cảm xúc (😊 hoặc ⚠️).

1. Chạy lệnh sau trong **Anaconda Prompt**:
   ```bash
   uvicorn app:app --reload --port 8003
   ```
   *(Nếu cổng 8003 bị xung đột, hãy đổi sang: `uvicorn app:app --reload --port 8083`)*
2. Mở trình duyệt web truy cập: **`http://localhost:8003`** (hoặc `http://127.0.0.1:8003`).
3. Thử nghiệm hai kịch bản:
   * **Kịch bản Hài lòng**: Chọn Kênh *Inbound*, Danh mục *Returns*, Thời gian phản hồi *10 phút*, Nhập nhận xét:
     `"Great support, polite agent and resolved my issue immediately!"`
     $\to$ Kết quả hiển thị: **"Khách hàng HÀI LÒNG (Satisfied)"** với icon 😊 xanh lá, độ tin cậy **96.4%**.
   * **Kịch bản Nguy cơ Bất mãn**: Chọn Kênh *Email*, Danh mục *Refund Related*, Thời gian phản hồi *250 phút*, Nhập nhận xét:
     `"Terrible delay, worst experience ever, product damaged and rude agent!"`
     $\to$ Kết quả hiển thị: **"CẢNH BÁO: Nguy cơ KHÔNG HÀI LÒNG (At-Risk)"** với icon ⚠️ màu đỏ, độ tin cậy **97.2%**.

---

### Cách 3: Khởi chạy Dịch vụ REST API (Flask Microservice)
Phục vụ tích hợp tự động vào hệ thống CRM / Helpdesk của doanh nghiệp:

1. Chạy API Server trên một terminal **Anaconda Prompt**:
   ```bash
   python REST_API.py
   # Server lắng nghe tại http://localhost:5003
   ```
2. Kiểm thử bằng lệnh cURL trên một terminal khác:
   ```bash
   curl -X POST http://localhost:5003/csat/v1/predict \
     -H "Content-Type: application/json" \
     -d "{\"channel\": \"Email\", \"category\": \"Returns\", \"tenure\": \">90\", \"shift\": \"Morning\", \"response_time\": 15.0, \"remarks\": \"Great support, polite agent and resolved my issue immediately!\"}"
   ```
3. Phản hồi JSON nhận được:
   ```json
   {
     "confidence": 96.4,
     "label": "Satisfied",
     "model_used": "Combined Model (Tabular + TF-IDF)",
     "prediction": 1,
     "probability_at_risk": 3.6,
     "probability_satisfied": 96.4
   }
   ```

---

### Cách 4: Chạy Client Thử nghiệm bằng Python (`Predict_CSAT.py`)
Khi `REST_API.py` đang chạy ở Cách 3, mở một cửa sổ terminal khác và chạy:
```bash
python Predict_CSAT.py
```
Nhập nhận xét của khách hàng từ bàn phím $\to$ Client gửi request JSON tới cổng 5003 và in ngay kết quả phân loại cảm xúc trên terminal.

---

## 4. KẾT QUẢ ĐỐI SÁNH 6 MÔ HÌNH (VALIDATION SET)

| STT | Tên mô hình | Không gian dữ liệu đầu vào | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
|---|---|---|---|---|---|---|---|
| 1 | Logistic Regression | Tabular-only ($B \times 8$) | 0.8250 | 0.8410 | 0.6820 | 0.7532 | 0.7120 |
| 2 | Decision Tree | Tabular-only ($B \times 8$) | 0.8310 | 0.8450 | 0.7200 | 0.7774 | 0.6850 |
| 3 | Random Forest | Tabular-only ($B \times 8$) | 0.8350 | 0.8500 | 0.7130 | 0.7756 | 0.7280 |
| 4 | SVM (LinearSVC) | Tabular-only ($B \times 8$) | 0.8240 | 0.8390 | 0.6810 | 0.7519 | 0.7090 |
| 5 | **Text-based LR (Best F1)** ★ | **Text-only ($B \times 500$ TF-IDF)** | **0.8378** | **0.8744** | **0.9399** | **0.9059** | 0.6905 |
| 6 | **Combined Model (Deploy)** ★ | **Combined ($B \times 508$ Hstack)** | **0.8320** | **0.8650** | **0.8680** | **0.8663** | **0.7330** |

### 💡 Biện luận Triển khai:
* Mô hình **Text-only (Mô hình 5)** đạt F1-Score cao nhất (0.9059) vì câu chữ của khách hàng phản ánh trực tiếp cảm xúc.
* Tuy nhiên, trong thực tế, **66.5% khách hàng không để lại nhận xét**. Mô hình Text-only sẽ bất lực khi nhận xét trống. Do đó, **Mô hình Kết hợp Combined (Mô hình 6)** được chọn để đóng gói triển khai vì nó hoạt động trơn tru trong 100% tình huống (tự động dùng thông số vận hành khi không có text, và cộng hưởng thêm tín hiệu NLP khi có text).

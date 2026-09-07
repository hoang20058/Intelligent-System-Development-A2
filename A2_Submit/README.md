# ASSIGNMENT 02 — PHÁT TRIỂN HỆ THỐNG THÔNG MINH

## From Data Representation to Deployable Intelligent Systems

> **Học phần**: Phát triển Hệ thống Thông minh (Intelligent System Development)
> **Giảng viên hướng dẫn**: PGS. TS. Trần Đình Quế
> **Năm học**: 2025 – 2026

---

## 📑 MỤC LỤC TỔNG QUAN

1. [Giới thiệu Dự án](#1-giới-thiệu-dự-án)
2. [Cấu trúc Thư mục Nộp bài](#2-cấu-trúc-thư-mục-nộp-bài)
3. [Tổng hợp 3 Ứng dụng &amp; Nguồn Dataset](#3-tổng-hợp-3-ứng-dụng--nguồn-dataset)
4. [Kiến trúc Luồng Kỹ thuật (End-to-End Pipeline)](#4-kiến-trúc-luồng-kỹ-thuật-end-to-end-pipeline)
5. [Yêu cầu Môi trường &amp; Cài đặt (Anaconda / Python)](#5-yêu-cầu-môi-trường--cài-đặt-anaconda--python)
6. [Hướng dẫn Khởi chạy Từng Bước](#6-hướng-dẫn-khởi-chạy-từng-bước)
   - [A. Chạy Notebook bằng Anaconda Jupyter Notebook](#a-chạy-notebook-bằng-anaconda-jupyter-notebook)
   - [B. Khởi chạy Dịch vụ REST API (Flask)](#b-khởi-chạy-dịch-vụ-rest-api-flask)
   - [C. Khởi chạy Giao diện Người dùng (FastAPI Web UI)](#c-khởi-chạy-giao-diện-người-dùng-fastapi-web-ui)
   - [D. Chạy Client Thử nghiệm (Python Script)](#d-chạy-client-thử-nghiệm-python-script)
7. [Báo cáo Kỹ thuật Bàn giao](#7-báo-cáo-kỹ-thuật-bàn-giao)

---

## 1. GIỚI THIỆU DỰ ÁN

Dự án hiện thực hóa trọn vẹn chu trình phát triển của **ba hệ thống thông minh độc lập** dựa trên ba tập dữ liệu thực tế từ Kaggle, bao gồm đầy đủ các bước:

$$
\text{Data} \xrightarrow{} \text{Understand} \xrightarrow{} \text{Clean} \xrightarrow{} \text{Represent} \xrightarrow{} \text{Learn} \xrightarrow{} \text{Evaluate} \xrightarrow{} \text{Persist} \xrightarrow{} \text{Deploy}
$$

* **Ứng dụng 1 (Phân loại Nhị phân Lâm sàng)**: Sàng lọc nguy cơ mắc bệnh tiểu đường dựa trên 8 chỉ số lâm sàng.
* **Ứng dụng 2 (Hồi quy Bất động sản Quy mô lớn)**: Định giá nhà ở tự động tại Hoa Kỳ dựa trên các đặc trưng vật lý và vị trí địa lý.
* **Ứng dụng 3 (Phân loại Đa phương thức Bảng + NLP)**: Dự đoán mức độ hài lòng khách hàng thương mại điện tử (CSAT), kết hợp dữ liệu bảng vận hành và nhận xét văn bản tự do bằng TF-IDF.

---

## 2. CẤU TRÚC THƯ MỤC NỘP BÀI

Tuân thủ nghiêm ngặt cấu trúc quy định tại **Appendix A — Repository Structure** của tài liệu hướng dẫn:

```text
A2_Submit/
├── README.md                      # [Tệp này] Tài liệu tổng quan toàn bộ dự án
│
├── App1_Diabetes/                 # Ứng dụng 1: Dự đoán Bệnh Tiểu đường
│   ├── README.md                  # Hướng dẫn chi tiết riêng cho App 1
│   ├── diabetes_classification.ipynb  # Jupyter Notebook nghiên cứu & huấn luyện
│   ├── app.py                     # Web Server giao diện người dùng (FastAPI, Port 8001)
│   ├── REST_API.py                # Microservice REST API độc lập (Flask, Port 5000/5001)
│   ├── Predict_Diabetes.py        # Client kiểm thử API bằng dòng lệnh Python
│   ├── requirements.txt           # Danh sách thư viện phụ thuộc của App 1
│   ├── templates/
│   │   └── index.html             # Giao diện Web Responsive Bootstrap 5
│   └── models/
│       ├── diabetes_pipeline.joblib  # Pipeline hoàn chỉnh (Preprocessor + Model)
│       └── diabetes.sav           # Artifact tương thích phục vụ REST API
│
├── App2_HousePrice/               # Ứng dụng 2: Dự đoán Giá Nhà Hoa Kỳ
│   ├── README.md                  # Hướng dẫn chi tiết riêng cho App 2
│   ├── house_price_prediction.ipynb  # Jupyter Notebook nghiên cứu & huấn luyện
│   ├── app.py                     # Web Server giao diện người dùng (FastAPI, Port 8002)
│   ├── REST_API.py                # Microservice REST API độc lập (Flask, Port 5002)
│   ├── Predict_HousePrice.py      # Client kiểm thử API bằng dòng lệnh Python
│   ├── requirements.txt           # Danh sách thư viện phụ thuộc của App 2
│   ├── templates/
│   │   └── index.html             # Giao diện Web Responsive Bootstrap 5
│   └── models/
│       ├── house_price_pipeline.joblib  # Pipeline hoàn chỉnh (Scaler + Model)
│       └── house_price.sav        # Artifact tương thích phục vụ REST API
│
├── App3_CustomerSupport/          # Ứng dụng 3: Phân tích Hài lòng CSAT (NLP)
│   ├── README.md                  # Hướng dẫn chi tiết riêng cho App 3
│   ├── customer_support_csat.ipynb  # Jupyter Notebook nghiên cứu & 6 mô hình
│   ├── app.py                     # Web Server giao diện người dùng (FastAPI, Port 8003)
│   ├── REST_API.py                # Microservice REST API độc lập (Flask, Port 5003)
│   ├── Predict_CSAT.py            # Client kiểm thử API bằng dòng lệnh Python
│   ├── requirements.txt           # Danh sách thư viện phụ thuộc của App 3
│   ├── templates/
│   │   └── index.html             # Giao diện Web Responsive Bootstrap 5 (Multimodal)
│   └── models/
│       ├── csat_pipeline.joblib   # Pipeline đa phương thức (Tabular + TF-IDF)
│       └── csat_model.sav         # Artifact tương thích phục vụ REST API
│
└── report/                        # Báo cáo Kỹ thuật Bàn giao
    ├── Assignment_02_Report.docx  # Tệp Word chính thức (~2.1 MB, 10 chương chuẩn)
    ├── report.tex                 # Mã nguồn LaTeX đầy đủ
    └── figures/                   # 20 hình ảnh, biểu đồ EDA và Screenshots UI
```

---

## 3. TỔNG HỢP 3 ỨNG DỤNG & NGUỒN DATASET

| Thuộc tính                     | Ứng dụng 1: Diabetes                                                                                         | Ứng dụng 2: House Price                                                                            | Ứng dụng 3: E-Commerce CSAT                                                                                 |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Bài toán**             | Phân loại nhị phân (Classification)                                                                        | Hồi quy số thực (Regression)                                                                      | Phân loại nhị phân + NLP (Multimodal)                                                                     |
| **Nguồn Kaggle**          | [100K Diabetes Clinical Dataset](https://www.kaggle.com/datasets/priyamchoksi/100000-diabetes-clinical-dataset) | [USA Real Estate Dataset](https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset) | [E-Commerce CSAT Dataset](https://www.kaggle.com/datasets/ddosad/ecommerce-customer-service-satisfaction/data) |
| **Đơn vị quan sát**    | Một bệnh nhân khám lâm sàng                                                                              | Một bất động sản rao bán                                                                       | Một lượt tương tác hỗ trợ khách hàng                                                                |
| **Biến mục tiêu**       | `diabetes` (0: Khỏe mạnh, 1: Mắc bệnh)                                                                   | `price` (USD)                                                                                      | `CSAT Score` $\to$ `is_satisfied` (0 / 1)                                                               |
| **Biểu diễn đầu vào** | Vector số thực$B \times 8$                                                                                 | Vector số thực$B \times 5$ (log-target)                                                          | Ma trận thưa$B \times 508$ (8 Tabular + 500 TF-IDF)                                                       |
| **Mô hình tốt nhất**   | **Gradient Boosting Classifier**                                                                         | **Gradient Boosting Regressor**                                                                | **Combined Model** (Tabular + TF-IDF LR)                                                                |
| **Thước đo chính**     | Recall =**0.71**, F1 = **0.74**, AUC = **0.95**                                              | $R^2$ = **0.557**, MAE = **$168,241**                                                  | Text F1 =**0.906**, Combined F1 = **0.866**                                                       |
| **Cổng Web UI**           | `http://localhost:8001`                                                                                      | `http://localhost:8002`                                                                            | `http://localhost:8003`                                                                                     |
| **Cổng REST API**         | `http://localhost:5000` (hoặc 5001)                                                                         | `http://localhost:5002`                                                                            | `http://localhost:5003`                                                                                     |

---

## 4. KIẾN TRÚC LUỒNG KỸ THUẬT (END-TO-END PIPELINE)

Hệ thống hoạt động theo nguyên tắc cách ly chống rò rỉ dữ liệu (*Data Leakage Prevention*):

1. **Dữ liệu huấn luyện**: Chỉ gọi `.fit()` trên 70% tập Train cho toàn bộ các khâu tiền xử lý (Scaler, Encoder, TF-IDF Vectorizer).
2. **Đóng gói Artifact (.joblib)**: Gói gọn đối tượng Preprocessor + Model thuật toán vào một file nhị phân duy nhất.
3. **Suy luận thời gian thực (Inference)**: Khi người dùng gửi dữ liệu qua Web hoặc REST API, hệ thống chỉ gọi `.transform()` bằng đúng tham số thống kê đã đóng băng, trả kết quả sau < 30ms.

---

## 5. YÊU CẦU MÔI TRƯỜNG & CÀI ĐẶT (ANACONDA / PYTHON)

### A. Yêu cầu Hệ thống

* Python 3.10 trở lên (khuyến nghị Python 3.11 trong môi trường Anaconda).
* Đã cài đặt **Anaconda** hoặc **Miniconda** trên hệ điều hành Windows / Linux / macOS.

### B. Cài đặt Môi trường qua Anaconda Prompt

Mở ứng dụng **Anaconda Prompt** (trên Windows: nhấn phím Windows, gõ "Anaconda Prompt") và chạy các lệnh sau:

```bash
# 1. Tạo môi trường ảo conda mới (tùy chọn nhưng khuyến nghị)
conda create -n httm_a2 python=3.11 -y

# 2. Kích hoạt môi trường vừa tạo
conda activate httm_a2

# 3. Di chuyển vào thư mục dự án nộp bài
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit"

# 4. Cài đặt các thư viện lõi cho toàn bộ dự án
pip install pandas numpy scikit-learn matplotlib seaborn scipy joblib flask fastapi uvicorn jinja2 requests
```

---

## 6. HƯỚNG DẪN KHỞI CHẠY TỪNG BƯỚC

### A. Chạy Notebook bằng Anaconda Jupyter Notebook

Các tệp `.ipynb` lưu trữ toàn bộ mã nguồn phân tích dữ liệu (EDA), tiền xử lý, huấn luyện 5-6 mô hình và xuất ra tệp `models/*.joblib`.

**Các bước thực hiện:**

1. Mở **Anaconda Prompt**, kích hoạt môi trường:
   ```bash
   conda activate httm_a2
   ```
2. Di chuyển đến thư mục nộp bài và khởi chạy Jupyter Notebook:
   ```bash
   cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit"
   jupyter notebook
   ```
3. Trình duyệt web sẽ tự động mở trang quản lý thư mục của Jupyter (`http://localhost:8888/tree`):
   * Để chạy **App 1**: Bấm vào thư mục `App1_Diabetes/` $\to$ Mở tệp `diabetes_classification.ipynb`.
   * Để chạy **App 2**: Bấm vào thư mục `App2_HousePrice/` $\to$ Mở tệp `house_price_prediction.ipynb`.
   * Để chạy **App 3**: Bấm vào thư mục `App3_CustomerSupport/` $\to$ Mở tệp `customer_support_csat.ipynb`.
4. Trên thanh menu của Jupyter Notebook:
   * Nhấn **Cell** $\to$ **Run All** để thực thi toàn bộ các khối mã từ đầu đến cuối.
   * Hoặc bấm `Shift + Enter` để chạy tuần tự từng cell và quan sát biểu đồ trực quan.

---

### B. Khởi chạy Dịch vụ REST API (Flask)

Mỗi ứng dụng có một REST API độc lập cung cấp endpoint `/predict` nhận JSON và trả về kết quả dự đoán.

Mở một cửa sổ **Anaconda Prompt** riêng cho từng app:

```bash
# Chạy REST API cho App 1 (Cổng 5000/5001):
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App1_Diabetes"
python REST_API.py

# Chạy REST API cho App 2 (Cổng 5002):
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App2_HousePrice"
python REST_API.py

# Chạy REST API cho App 3 (Cổng 5003):
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App3_CustomerSupport"
python REST_API.py
```

---

### C. Khởi chạy Giao diện Người dùng (FastAPI Web UI)

Mỗi ứng dụng sở hữu giao diện Web Bootstrap 5 Responsive hỗ trợ tương tác trên cả máy tính để bàn lẫn điện thoại di động.

Mở một cửa sổ **Anaconda Prompt** mới và khởi chạy máy chủ Uvicorn:

```bash
# Khởi chạy Web UI App 1:
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App1_Diabetes"
uvicorn app:app --reload --port 8001
# 👉 Mở trình duyệt truy cập: http://localhost:8001

# Khởi chạy Web UI App 2:
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App2_HousePrice"
uvicorn app:app --reload --port 8002
# 👉 Mở trình duyệt truy cập: http://localhost:8002

# Khởi chạy Web UI App 3:
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App3_CustomerSupport"
uvicorn app:app --reload --port 8003
# 👉 Mở trình duyệt truy cập: http://localhost:8003
```

*(Lưu ý: Nếu một cổng bất kỳ bị trùng lặp hoặc báo lỗi `[WinError 10013] Access forbidden`, bạn chỉ cần thay đổi số cổng sang cổng khác như `--port 8081`, `--port 8082`, `--port 8083`).*

---

### D. Chạy Client Thử nghiệm (Python Script)

Khi REST API tương ứng đang chạy, bạn có thể chạy tệp client bằng dòng lệnh để thử nghiệm dự đoán ngay trên terminal:

```bash
# Thử nghiệm App 1:
python App1_Diabetes/Predict_Diabetes.py

# Thử nghiệm App 2:
python App2_HousePrice/Predict_HousePrice.py

# Thử nghiệm App 3:
python App3_CustomerSupport/Predict_CSAT.py
```

---

## 7. BÁO CÁO KỸ THUẬT BÀN GIAO

Toàn bộ tài liệu báo cáo kỹ thuật hoàn chỉnh nằm trong thư mục `report/`:

* [**`Assignment_02_Report.docx`**](report/Assignment_02_Report.docx): Tệp Microsoft Word chính thức dung lượng **2.1 MB**, trình bày đúng chuẩn học thuật với 10 chương, tích hợp 11 bảng thống kê chi tiết, và **nhúng đầy đủ 20 hình ảnh trực quan kèm khối phân tích 3 phần sâu sắc**.
* [**`report.tex`**](report/report.tex): Tệp mã nguồn LaTeX đồng bộ hoàn toàn với bản Word.
* [**`figures/`**](report/figures/): Thư mục chứa 20 tệp đồ họa độ phân giải cao, gồm đầy đủ ảnh phân tích tương quan, phân phối dữ liệu, độ quan trọng đặc trưng và **6 ảnh chụp màn hình Web Desktop & Mobile Responsive**.

---

*Chúc bạn có trải nghiệm khảo sát và bảo vệ đồ án môn học đạt kết quả cao nhất!*

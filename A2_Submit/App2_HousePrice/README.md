# ỨNG DỤNG 2: ĐỊNH GIÁ BẤT ĐỘNG SẢN HOA KỲ
## USA House Price Automated Valuation Model (AVM)

> **Bài toán**: Hồi quy Đại lượng Liên tục (Regression)  
> **Tập dữ liệu**: [USA Real Estate Dataset — Kaggle](https://www.kaggle.com/datasets/ahmedshahriarsakib/usa-real-estate-dataset) (Tác giả: Ahmed Shahriar Sakib)  
> **Kích thước đầu vào**: Ma trận đặc trưng số $B \times 5$ (sau mã hóa và biến đổi logarit mục tiêu)  
> **Mô hình tốt nhất**: Gradient Boosting Regressor ($R^2$: **0.5574**, MAE: **$168,241**, MAPE: **38.2%**)  

---

## 1. MÔ TẢ DỰ ÁN

Hệ thống hỗ trợ người mua nhà, nhà đầu tư và môi giới thẩm định giá trị thị trường của bất động sản dân dụng tại Hoa Kỳ dựa trên các đặc trưng vật lý và địa lý:
1. `bed`: Số phòng ngủ (1 – 10 phòng).
2. `bath`: Số phòng vệ sinh / phòng tắm (1 – 10 phòng).
3. `house_size`: Diện tích sàn xây dựng ($sqft$, 100 – 15,000 $sqft$).
4. `acre_lot`: Diện tích khuôn viên đất ($acre$).
5. `state`: Bang tại Hoa Kỳ (California, New York, Texas, Florida,...).
6. `city`: Thành phố (được mã hóa theo tần suất - Frequency Encoding).
7. `status`: Trạng thái bất động sản (`for_sale` hoặc `ready_to_build`).

**Biến mục tiêu `price`**: Giá trị bất động sản bằng đồng Đô la Mỹ (USD).  
*Đặc thù toán học: Do giá nhà lệch phải cực độ (Skewness > 8.5), toàn bộ quá trình huấn luyện được thực hiện trên không gian logarit $y_{log} = \ln(1 + \text{price})$ và tự động ánh xạ ngược bằng $\exp(x) - 1$ khi suy luận.*

---

## 2. CẤU TRÚC THƯ MỤC ỨNG DỤNG

```text
App2_HousePrice/
├── README.md                      # [Tệp này] Hướng dẫn chi tiết cho App 2
├── house_price_prediction.ipynb   # Jupyter Notebook (EDA, 5 mô hình hồi quy, lưu model)
├── app.py                         # FastAPI Server phục vụ Web UI (Port 8002)
├── REST_API.py                    # Flask REST API độc lập (Port 5002)
├── Predict_HousePrice.py          # Client dòng lệnh thử nghiệm gọi API
├── requirements.txt               # Thư viện phụ thuộc
├── templates/
│   └── index.html                 # Giao diện Bootstrap 5 Responsive
└── models/
    ├── house_price_pipeline.joblib # Pipeline chuẩn đóng gói Preprocessor + Model
    └── house_price.sav            # Tệp artifact tương thích cho REST_API.py
```

---

## 3. HƯỚNG DẪN CHẠY THỬ CHI TIẾT

### Bước 0: Kích hoạt Môi trường Anaconda
Mở ứng dụng **Anaconda Prompt** trên máy tính:
```bash
conda activate httm_a2
# Di chuyển vào thư mục App2:
cd "d:\JJin\Documents\Học\I-4\Thiet_ke_httm\jupyter\A2\A2_Submit\App2_HousePrice"
```

---

### Cách 1: Chạy Notebook bằng Anaconda Jupyter Notebook
Notebook `house_price_prediction.ipynb` thực hiện: Lọc bỏ giá 0 và kích thước 0 $\to$ Phân tích độ lệch phải $\to$ Log-transform $\to$ Mã hóa bang và thành phố $\to$ Huấn luyện 5 thuật toán hồi quy $\to$ Xuất file artifact vào `models/`.

1. Khởi chạy Jupyter Notebook từ **Anaconda Prompt**:
   ```bash
   jupyter notebook house_price_prediction.ipynb
   ```
2. Giao diện Anaconda Jupyter Notebook sẽ tự động mở trên trình duyệt.
3. Trên thanh công cụ, chọn **Cell** $\to$ **Run All** để chạy toàn bộ notebook, hoặc nhấn `Shift + Enter` để chạy từng cell.
4. Tệp `models/house_price_pipeline.joblib` sẽ được cập nhật tự động sau cell cuối cùng.

---

### Cách 2: Khởi chạy Giao diện Web Người dùng (FastAPI Web UI)
Giao diện Bootstrap 5 cho phép chọn Bang qua Dropdown động, nhập diện tích và xem giá ước lượng định dạng tiền tệ USD nổi bật.

1. Chạy lệnh sau trong **Anaconda Prompt**:
   ```bash
   uvicorn app:app --reload --port 8002
   ```
2. Mở trình duyệt web truy cập: **`http://localhost:8002`** (hoặc `http://127.0.0.1:8002`).
3. Chọn bang (ví dụ: *California*), nhập:
   * Số phòng ngủ: `3`, Số phòng tắm: `2`, Diện tích sàn: `2100` sqft, Diện tích đất: `0.25` acre.
4. Bấm **"Dự đoán Giá"** $\to$ Kết quả hiển thị giá ước lượng: **`$425,800`** nổi bật màu xanh lục kèm thông tin mô hình.

---

### Cách 3: Khởi chạy Dịch vụ REST API (Flask Microservice)
Phục vụ tích hợp tự động cho các ứng dụng bất động sản bên thứ ba:

1. Chạy API Server trên một terminal **Anaconda Prompt**:
   ```bash
   python REST_API.py
   # Server lắng nghe tại http://localhost:5002
   ```
2. Kiểm thử bằng lệnh cURL trên một terminal khác:
   ```bash
   curl -X POST http://localhost:5002/houseprice/v1/predict \
     -H "Content-Type: application/json" \
     -d "{\"bed\": 3, \"bath\": 2, \"house_size\": 2100, \"acre_lot\": 0.25, \"state\": \"California\", \"city\": \"Los Angeles\", \"status\": \"for_sale\"}"
   ```
3. Phản hồi JSON nhận được:
   ```json
   {
     "formatted": "$425,800",
     "model_used": "Gradient Boosting Regressor",
     "prediction": 425800.0
   }
   ```

---

### Cách 4: Chạy Client Thử nghiệm bằng Python (`Predict_HousePrice.py`)
Khi `REST_API.py` đang chạy ở Cách 3, mở một cửa sổ terminal khác và chạy:
```bash
python Predict_HousePrice.py
```
Nhập lần lượt số phòng ngủ, phòng tắm, diện tích sàn $\to$ Script gửi request tới cổng 5002 và in giá ước lượng bằng USD ngay trên màn hình.

---

## 4. KẾT QUẢ ĐỐI SÁNH 5 MÔ HÌNH HỒI QUY (VALIDATION SET)

| Thuật toán Hồi quy | MAE ($) | RMSE ($) | $R^2$ Score | MAPE (%) | Thời gian huấn luyện |
|---|---|---|---|---|---|
| Ridge Regression (Tuyến tính L2) | $241,500 | $442,100 | 0.1245 | 54.2% | 2.1 s |
| Lasso Regression (Tuyến tính L1) | $241,800 | $442,300 | 0.1238 | 54.5% | 3.5 s |
| Decision Tree Regressor | $185,200 | $365,400 | 0.4612 | 42.1% | 8.2 s |
| Random Forest Regressor | $172,400 | $348,900 | 0.5028 | 39.5% | 125.4 s |
| **Gradient Boosting Regressor ★** | **$168,241** | **$337,528** | **0.5312** | **38.2%** | **48.6 s** |

*Nhận xét: Các mô hình tuyến tính (Ridge, Lasso) thất bại do không mô hình hóa được quan hệ phi tuyến của giá đất. Gradient Boosting đạt hiệu năng cao nhất nhờ tối ưu hóa phần dư từng bước.*

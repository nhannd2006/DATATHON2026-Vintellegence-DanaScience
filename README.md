# 🧠 Datathon 2026: The Gridbreakers - Vòng 1

## 📌 Tổng quan dự án

Repository này chứa toàn bộ mã nguồn, tài liệu và kết quả phân tích của đội **DanaScience** tham gia cuộc thi **Datathon 2026: The Gridbreakers** do Vin Telligence và VinUni DS&AI Club tổ chức.

Dự án tập trung giải quyết bài toán **dự báo doanh thu (Sales Forecasting)** cho một doanh nghiệp thương mại điện tử thời trang tại Việt Nam, đồng thời khai thác dữ liệu để đưa ra **insight kinh doanh có thể hành động (actionable insights)**.

---

## 🎯 Mục tiêu

Xây dựng một hệ thống dự báo doanh thu theo ngày với độ chính xác cao nhằm hỗ trợ:

* 📦 **Tối ưu phân bổ tồn kho:** Giảm thiểu tình trạng thiếu hàng (stockout) hoặc tồn kho dư thừa.
* 🎯 **Lập kế hoạch khuyến mãi:** Tối ưu hóa các chiến dịch dựa trên dữ liệu lịch sử.
* 🚚 **Tối ưu logistics:** Nâng cao hiệu quả vận hành trên toàn quốc.

**Output chính của dự án:**
* Dự báo cột `Revenue` trong giai đoạn **01/01/2023 – 01/07/2024** (File `submission.csv`).
* Pipeline hoàn chỉnh, tự động và có thể tái lập hoàn toàn (Reproducible).
* Báo cáo phân tích chuyên sâu hỗ trợ ra quyết định kinh doanh.

---

## 👥 Thành viên đội

| Họ và Tên            | Vai trò | Chuyên ngành        | Trường                         |
| :------------------- | :------ | :------------------ | :----------------------------- |
| **Nguyễn Đăng Nhân** | Leader  | Khoa học dữ liệu    | ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Nguyễn Thành Bảo** | Member  | Công nghệ thông tin | ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Đặng Thanh Huyền** | Member  | Khoa học dữ liệu    | ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Lê Tự Phong**      | Member  | Khoa học dữ liệu    | ĐH Khoa học tự nhiên, ĐHQG-HCM |

---

## 📁 Cấu trúc thư mục

```text
├── dataset/               # Chứa 15 file CSV dữ liệu thô (KHÔNG push lên GitHub)
├── notebooks/             # Thư mục chứa Jupyter Notebooks
│   ├── 2.0-EDA.ipynb      # Phân tích khám phá, trực quan hóa dữ liệu (Phần 2)
│   └── 3.0-Modeling.ipynb # Thử nghiệm mô hình dự báo doanh thu (Phần 3)
├── src/                   # Source code chính xử lý pipeline
│   ├── data_prep.py       # Script làm sạch, kết nối dữ liệu và Feature Engineering
│   └── model_train.py     # Pipeline huấn luyện, đánh giá và dự báo chính thức
├── report/                # Thư mục chứa báo cáo kỹ thuật 
│   └── main.tex           # Mã nguồn báo cáo LaTeX (Template NeurIPS)
├── submissions/           # Lưu trữ kết quả dự báo
│   └── submission.csv     # File nộp chính thức trên nền tảng Kaggle
├── .gitignore             # Loại bỏ folder dataset/ và các file rác sinh ra khi chạy code
├── requirements.txt       # Danh sách thư viện Python cần thiết
└── README.md              # Tài liệu hướng dẫn này
```

---
## ⚙️ Hướng dẫn Cài đặt & Tái lập kết quả (Reproducibility)

Để đảm bảo tính minh bạch, giám khảo có thể chạy lại toàn bộ pipeline theo các bước sau:

### 1. Chuẩn bị dữ liệu
Vui lòng tải 15 file `.csv` gốc từ ban tổ chức và đặt vào thư mục `dataset/` ở gốc dự án. Nhóm cam kết **không** sử dụng dữ liệu bên ngoài.

### 2. Cài đặt môi trường
Khởi tạo môi trường ảo (khuyến nghị) và cài đặt thư viện:
```bash
# Tạo môi trường ảo
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows

# Cài đặt thư viện
pip install -r requirements.txt
```

### 3. Chạy Pipeline tự động
Chạy lần lượt các lệnh sau trong Terminal để tạo file dự báo từ đầu:
```bash
# Bước 1: Tiền xử lý, merge bảng và tạo đặc trưng (Features)
python src/data_prep.py

# Bước 2: Huấn luyện mô hình và xuất file submission.csv
python src/model_train.py
```
*(Mô hình đã được set cố định `random_seed` để đảm bảo kết quả đồng nhất).*

---

## 📊 Phân tích dữ liệu (EDA & Insights)

Chi tiết các biểu đồ và mã nguồn phân tích nằm tại: `notebooks/2.0-EDA.ipynb`. Chúng tôi phân tích dữ liệu qua 4 lăng kính:

* **What happened? (Descriptive):** [... Cập nhật sau ...]
* **Why did it happen? (Diagnostic):** [... Cập nhật sau ...]
* **What is likely to happen? (Predictive):** [... Cập nhật sau ...]
* **What should we do? (Prescriptive):** [... Cập nhật sau ...]

---

## 🧠 Phương pháp Xây dựng Mô hình (Modeling Approach)

### Đặc trưng học máy (Feature Engineering)
* **Time-series:** Trích xuất độ trễ (Lag features), trung bình trượt (Rolling windows), và tính mùa vụ (Seasonality).
* **Nghiệp vụ:** Tích hợp dữ liệu về Chương trình khuyến mãi (Promotions), Lưu lượng truy cập (Web traffic), và Tồn kho (Inventory).
* [... Cập nhật kĩ thuật xử lý khác ...]

### Mô hình hóa (Models)
Các mô hình được thử nghiệm: Linear Regression, XGBoost, LightGBM.
* **Mô hình được chọn cuối cùng:** [... Cập nhật sau ...]
* **Lý do chọn:** [... Cập nhật sau ...]

### Đánh giá (Validation & Metrics)
* **Validation:** Sử dụng phương pháp Time-series Cross Validation để ngăn chặn rò rỉ dữ liệu (No data leakage) ở mức tối đa.
* **Metrics mục tiêu:** Tối ưu hóa dựa trên MAE, RMSE và tối đa hóa $R^2$.

---

## 🔍 Khả năng diễn giải (Explainability)

Ứng dụng **SHAP (SHapley Additive exPlanations)** để phá vỡ "hộp đen" của mô hình học máy:
* Xác định tầm quan trọng của các đặc trưng (Feature Importance).
* Giải thích các yếu tố động lực (Drivers) ảnh hưởng mạnh nhất đến doanh thu ngày.
* **Phát hiện chính từ SHAP:** [... Cập nhật sau ...]

---

## 📄 Báo cáo Kỹ thuật

* **Định dạng:** Tuân thủ cấu trúc của hội nghị NeurIPS.
* **Mã nguồn:** `report/main.tex`
* **File kết quả PDF:** Đã được đính kèm trong form nộp bài chính thức của BTC.

---

## 🧪 Tech Stack

* **Ngôn ngữ:** Python 3.x
* **Xử lý dữ liệu:** Pandas, NumPy
* **Học máy:** Scikit-learn, XGBoost / LightGBM
* **Diễn giải mô hình:** SHAP
* **Trực quan hóa:** Matplotlib, Seaborn

---

## 📌 Ghi chú tuân thủ
* ☑️ **Không** sử dụng dữ liệu bên ngoài.
* ☑️ Đảm bảo **Reproducibility** (cung cấp mã nguồn, file requirements, pipeline rõ ràng).
* ☑️ **Không** sử dụng Revenue/COGS của tập test làm đặc trưng huấn luyện.

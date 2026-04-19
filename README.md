# Datathon 2026: The Gridbreakers - Vòng 1

## 📌 Tổng quan dự án
Repository này chứa toàn bộ mã nguồn, tài liệu và kết quả phân tích của đội [DanaScience] tham gia cuộc thi **Datathon 2026: The Gridbreakers** do VinTelligence và VinUni DS&AI Club tổ chức. 

Mục tiêu của dự án là giải quyết bài toán dự báo doanh thu (Sales Forecasting) ở mức độ chi tiết và trực quan hoá các dữ liệu kinh doanh của một doanh nghiệp thời trang thương mại điện tử tại Việt Nam.

## 👥 Thành viên đội
| Họ và Tên | Vai trò | Chuyên ngành | Trường |
| :--- | :--- | :--- | :--- |
| **Nguyễn Đăng Nhân** | Leader | Khoa học dữ liệu | Trường ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Nguyễn Thành Bảo** | Member | Công nghệ thông tin | Trường ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Đặng Thanh Huyền** | Member | Khoa học dữ liệu | Trường ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Lê Tự Phong** | Member | Khoa học dữ liệu | Trường ĐH Khoa học tự nhiên, ĐHQG-HCM |

## 📁 Cấu trúc thư mục
Repository được cấu trúc có chủ đích để mô tả quy trình thực hiện dự án[cite: 322]:

```text
├── dataset/               # Chứa 15 file CSV dữ liệu thô (KHÔNG push lên GitHub) [cite: 20]
├── notebooks/             # Thư mục chứa Jupyter Notebooks
│   ├── 1.0-EDA.ipynb      # Phần 2: Trực quan hoá và phân tích dữ liệu
│   └── 2.0-Modeling.ipynb # Phần 3: Thử nghiệm mô hình dự báo doanh thu
├── src/                   # Source code chính xử lý pipeline
│   ├── data_prep.py       # Script tiền xử lý và kết nối dữ liệu
│   └── model_train.py     # Pipeline huấn luyện và dự báo chính thức
├── report/                # Thư mục chứa báo cáo kỹ thuật (LaTeX)
│   └── main.tex           # Soạn thảo theo template NeurIPS [cite: 315]
├── submissions/           # Lưu trữ kết quả dự báo
│   └── submission.csv     # File nộp chính thức trên Kaggle [cite: 239]
├── .gitignore             # Loại bỏ folder dataset/ và các file rác
├── LICENSE                # Giấy phép MIT
├── README.md              # Tài liệu hướng dẫn này
└── requirements.txt       # Danh sách thư viện cần thiết (Pandas, Scikit-learn, SHAP...)
```

## ⚙️ Hướng dẫn cài đặt và Tính tái lập (Reproducibility)
Để đảm bảo tính minh bạch và khả năng tái lập kết quả theo đúng yêu cầu của đề bài, ban giám khảo / mọi người có thể chạy lại toàn bộ pipeline theo các bước sau:

### 1. Chuẩn bị dữ liệu
Tải bộ dữ liệu gồm 15 file CSV từ ban tổ chức và đặt vào thư mục `dataset/` ở thư mục gốc của dự án. 
*Lưu ý: Nhóm cam kết không sử dụng bất kỳ nguồn dữ liệu bên ngoài nào khác ngoài danh mục được cung cấp.*

### 2. Thiết lập môi trường
Khuyến nghị sử dụng Python 3.10 trở lên. Cài đặt các thư viện cần thiết bằng lệnh:
```bash
pip install -r requirements.txt

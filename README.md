# 🧠 Datathon 2026: The Gridbreakers — Vòng 1

---

## 📖 Giới thiệu đội
 
**DanaScience** = **Đà Nẵng** + **Data Science**: 4 sinh viên đến từ Đà Nẵng, cùng chung niềm đam mê với khoa học dữ liệu. 


| Họ và Tên            | Vai trò | Chuyên ngành        | Trường                         |
| :------------------- | :------ | :------------------ | :----------------------------- |
| **Nguyễn Đăng Nhân** | Leader  | Khoa học dữ liệu    | ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Lê Tự Phong**      | Member  | Khoa học dữ liệu    | ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Nguyễn Thành Bảo** | Member  | Công nghệ thông tin | ĐH Khoa học tự nhiên, ĐHQG-HCM |
| **Đặng Thanh Huyền** | Member  | Khoa học dữ liệu    | ĐH Khoa học tự nhiên, ĐHQG-HCM |

---

## 🏆 Tổng quan về cuộc thi
 
**Datathon 2026: The Gridbreakers** là cuộc thi Khoa học Dữ liệu đầu tiên được tổ chức tại VinUniversity, do **VinTelligence** và **VinUni DS&AI Club** đứng ra tổ chức.

### Bài toán
 
Bộ dữ liệu mô phỏng hoạt động của một doanh nghiệp thời trang thương mại điện tử tại Việt Nam trong giai đoạn **2012–2022**, gồm 13 bảng dữ liệu trải dài từ đơn hàng, sản phẩm, khách hàng cho đến tồn kho và lưu lượng web. Các đội thi cần giải quyết **3 phần thi**:
 
| Phần | Nội dung | Điểm |
|:----:|:---------|:----:|
| **1** | 10 câu trắc nghiệm tính toán trực tiếp từ dữ liệu | 20đ |
| **2** | Trực quan hóa & Phân tích dữ liệu (EDA) — đánh giá theo 4 cấp độ Descriptive → Diagnostic → Predictive → Prescriptive | 60đ |
| **3** | Mô hình dự báo doanh thu hàng ngày (01/2023–07/2024) — đánh giá bằng MAE, RMSE, R² trên Kaggle leaderboard | 20đ |


### Thang điểm chi tiết Phần 2
 
| Tiêu chí | Điểm tối đa |
|:---------|:-----------:|
| Chất lượng trực quan hóa (nhãn, title, loại biểu đồ phù hợp) | 15đ |
| Chiều sâu phân tích (bao phủ đủ 4 cấp độ, có số liệu hỗ trợ) | 25đ |
| Insight kinh doanh (đề xuất cụ thể, actionable) | 15đ |
| Tính sáng tạo & data storytelling | 5đ |

### Thang điểm chi tiết Phần 3
 
| Tiêu chí | Điểm tối đa |
|:---------|:-----------:|
| Hiệu suất mô hình (MAE, RMSE, R² — Kaggle leaderboard) | 12đ |
| Báo cáo kỹ thuật (pipeline, cross-validation, SHAP/feature importance) | 8đ |
 
**Metric đánh giá Phần 3:**

$$\text{MAE} = \frac{1}{n}\sum|F_i - A_i|, \quad \text{RMSE} = \sqrt{\frac{1}{n}\sum(F_i - A_i)^2}, \quad R^2 = 1 - \frac{\sum(A_i - F_i)^2}{\sum(A_i - \bar{A})^2}$$
 
> 🔗 **Kaggle Competition:** [datathon-2026-round-1](https://www.kaggle.com/competitions/datathon-2026-round-1)

---
 
## 🎯 Mục tiêu dự án
 
Xây dựng hệ thống dự báo doanh thu theo ngày với độ chính xác cao nhằm hỗ trợ:
 
- 📦 **Tối ưu phân bổ tồn kho:** Giảm thiểu tình trạng thiếu hàng (stockout) hoặc tồn kho dư thừa.
- 🎯 **Lập kế hoạch khuyến mãi:** Tối ưu hóa chiến dịch dựa trên dữ liệu lịch sử.
- 🚚 **Tối ưu logistics:** Nâng cao hiệu quả vận hành trên toàn quốc.
**Output chính:**
- Dự báo cột `Revenue` giai đoạn **01/01/2023 – 01/07/2024** → `submission.csv`
- Pipeline hoàn chỉnh, tự động và có thể tái lập (Reproducible)
- Báo cáo phân tích chuyên sâu hỗ trợ ra quyết định kinh doanh

---

## 📁 Cấu trúc thư mục

```
DATATHON2026-Vintellegence-DanaScience/
│
├── 📂 Part1/
│   └── part1.ipynb                        # Giải 10 câu trắc nghiệm, tính toán trực tiếp từ data
│
├── 📂 Part2/
│   ├── part2.ipynb                        # Notebook EDA chính (4 cấp độ phân tích)
│   ├── draft_in_ggColab_DTH_NDN.ipynb     # Draft thử nghiệm trên Google Colab
│   ├── dataviz_chart1_descriptive.pdf     # Chart 1: Revenue Trend & Seasonality Index
│   ├── dataviz_chart2_diagnostic.pdf      # Chart 2: Revenue × Gross Margin Bubble
│   ├── dataviz_chart3_diagnostic.pdf      # Chart 3: RFM Customer Health
│   ├── dataviz_chart4_predictive.pdf      # Chart 4: Trend Decomposition & 12M Forecast
│   └── dataviz_chart5_prescriptive.pdf    # Chart 5: Inventory Matrix & Promo ROI Curve
│
├── 📂 Part3/
│   ├── 📂 NTBao/                          # Thử nghiệm riêng
│   │   ├── Part3_Final.py                 # Script huấn luyện mô hình
│   │   ├── Report.md                      # Ghi chú kết quả
│   │   ├── WorkFlow.md                    # Mô tả workflow
│   │   ├── feature_importance.png         # Biểu đồ feature importance
│   │   ├── generate_eda_nb.py             # Script sinh EDA notebook
│   │   └── pdp_plots.png                  # Partial Dependence Plots
│   ├── part3.ipynb                        # Pipeline chính: feature engineering + stacking
│   ├── draft_NDN.ipynb                    # Draft thử nghiệm của leader
│   ├── report_LTP.docx                    # Ghi chú kỹ thuật
│   ├── requirements.txt                   # Thư viện cần thiết
│   ├── salesstack_fig1.png                # SHAP beeswarm plot
│   ├── salesstack_fig2.png                # Feature importance (mean |SHAP|)
│   ├── salesstack_fig3.png                # Forecast vs Actual (toàn bộ giai đoạn)
│   ├── salesstack_fig4.png                # Residual analysis
│   ├── salesstack_fig5.png                # Walk-forward CV folds
│   ├── salesstack_fig6.png                # COGS ratio distribution
│   ├── submission.csv                     # File nộp bài chính thức
│   └── submission_736634.csv              # Phiên bản với random seed khác
│
├── 📂 Report/
│   ├── DanaScience_DATATHON2026.pdf       # Báo cáo PDF đã biên dịch
│   ├── DanaScience_DATATHON2026.tex       # Mã nguồn LaTeX (định dạng NeurIPS)
│   ├── neurips_2025.sty                   # Style file NeurIPS 2025
│   └── Styles.zip                         # Gói style đầy đủ
│
├── 📂 dataset/                            # Các file CSV gốc từ BTC
│   ├── DataScript.md                      # Mô tả schema các bảng dữ liệu
│   ├── customers.csv
│   ├── geography.csv
│   ├── inventory.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── payments.csv
│   ├── products.csv
│   ├── promotions.csv
│   ├── returns.csv
│   ├── reviews.csv
│   ├── sales.csv
│   ├── sample_submission.csv
│   ├── shipments.csv
│   └── web_traffic.csv
│
├── baseline.ipynb                         # Notebook baseline từ BTC
├── Đề thi Vòng 1.pdf                      # Đề thi chính thức
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ⚙️ Hướng dẫn Cài đặt & Tái lập kết quả

> ⚠️ **Yêu cầu:** Python 3.8+

### Bước 1 — Chuẩn bị dữ liệu
 
Tải các file `.csv` gốc từ ban tổ chức (hoặc từ Kaggle) và đặt vào thư mục `dataset/` ở gốc dự án.

> ✅ Nhóm cam kết **không** sử dụng bất kỳ dữ liệu bên ngoài nào.

### Bước 2 — Cài đặt môi trường
 
```bash
# Tạo và kích hoạt môi trường ảo
python -m venv venv
source venv/bin/activate        # macOS / Linux
# hoặc
venv\Scripts\activate           # Windows
 
# Cài đặt thư viện
pip install -r requirements.txt
```

### Bước 3 — Chạy pipeline
 
#### Phần 1 — Trắc nghiệm tính toán
 
```bash
jupyter nbconvert --to notebook --execute Part1/part1.ipynb
```
 
#### Phần 2 — EDA & Trực quan hóa
 
```bash
jupyter nbconvert --to notebook --execute Part2/part2.ipynb
```
 
#### Phần 3 — Mô hình dự báo (Pipeline chính)
 
```bash
jupyter nbconvert --to notebook --execute Part3/part3.ipynb
# File submission.csv sẽ được sinh ra trong thư mục Part3/
```
 
> 🔒 Tất cả mô hình đã được cố định `random_seed` để đảm bảo kết quả tái lập hoàn toàn.

---

---
 
## 📊 Phân tích dữ liệu (EDA & Insights)
 
Chi tiết mã nguồn và biểu đồ nằm tại: `Part2/part2.ipynb`
 
Chúng mình phân tích dữ liệu qua **4 lăng kính**:
 
| Cấp độ | Câu hỏi | Nội dung |
|:---|:---|:---|
| 🔵 **Descriptive** | *What happened?* | Xu hướng doanh thu, tính thời vụ, phân bổ sản phẩm & địa lý |
| 🟡 **Diagnostic** | *Why did it happen?* | Phân tích RFM khách hàng, tác động khuyến mãi, mối quan hệ Gross Margin |
| 🟠 **Predictive** | *What is likely to happen?* | Phân rã xu hướng, dự báo 12 tháng, cảnh báo stockout |
| 🟢 **Prescriptive** | *What should we do?* | Ma trận tồn kho, đề xuất chiến dịch khuyến mãi tối ưu ROI |
 
**Các biểu đồ chính (PDF):**
 
| File | Cấp độ | Nội dung |
|:---|:---:|:---|
| `dataviz_chart1_descriptive.pdf` | 🔵 Descriptive | Xu hướng doanh thu theo tháng & Seasonality Index (2012–2022) |
| `dataviz_chart2_diagnostic.pdf` | 🟡 Diagnostic | Ma trận Revenue × Gross Margin theo danh mục sản phẩm (bubble chart) |
| `dataviz_chart3_diagnostic.pdf` | 🟡 Diagnostic | Phân tích sức khỏe khách hàng theo mô hình RFM (Pareto) |
| `dataviz_chart4_predictive.pdf` | 🟠 Predictive | Phân rã xu hướng & dự báo doanh thu 12 tháng (Seasonal Multiplier) |
| `dataviz_chart5_prescriptive.pdf` | 🟢 Prescriptive | Ma trận tồn kho Q2 & Đường cong ROI khuyến mãi theo mức chiết khấu |
 
---

## 🧠 Phương pháp xây dựng mô hình
 
Pipeline chính được thực hiện trong `Part3/part3.ipynb`.
 
**Kiến trúc: Hybrid Prophet-Aware Stacking**
 
```
Raw Data
   ↓
Feature Engineering
   ↓  (time features, lag/rolling stats, promo kernels, Prophet components)
   ├── Prophet  ──────────────────────────────────────┐
   │   (trend + seasonality baseline)                 │
   ├── XGBoost  ──── dự báo residual ─────────────────┤
   ├── LightGBM ─────────────────────────────────────►│
   └── CatBoost ─────────────────────────────────────►│
                                                      ↓
                                    HuberRegressor (meta-learner, log scale)
                                                      ↓
                                               Revenue Forecast
                                                      ↓
                                                submission.csv
```
 
**Kết quả trực quan nằm tại `Part3/`:**
 
| File | Nội dung |
|:---|:---|
| `salesstack_fig1.png` | SHAP Beeswarm Plot |
| `salesstack_fig2.png` | Feature Importance (mean \|SHAP\|) |
| `salesstack_fig3.png` | Forecast vs Actual |
| `salesstack_fig4.png` | Residual Analysis |
| `salesstack_fig5.png` | Walk-forward CV Folds |
| `salesstack_fig6.png` | COGS Ratio Distribution |
 
---
 
## 📈 Kết quả nộp bài (Kaggle Leaderboard)
 
Đánh giá theo tiêu chí **MAE**:
 
| File | MAE | Ghi chú |
|:---|:---:|:---|
| `submission.csv` | **708,237.17320** | ✅ Bài nộp chính thức |
| `submission_736634.csv` | 736,634.12112 | Bản dự phòng (seed khác) |


*Leaderboard chính thức sẽ kết hợp cả 3 tiêu chí*

---

## 📄 Báo cáo kỹ thuật
 
- **Định dạng:** Tuân thủ cấu trúc hội nghị **NeurIPS**
- **Mã nguồn LaTeX:** `Report/DanaScience_DATATHON2026.tex`
- **File PDF:** `Report/DanaScience_DATATHON2026.pdf`
- Báo cáo PDF đã được đính kèm trong form nộp bài chính thức của BTC.

---

## 🧪 Tech Stack
 
| Hạng mục | Công nghệ |
|:---|:---|
| Ngôn ngữ | Python 3.x |
| Xử lý dữ liệu | Pandas, NumPy |
| Học máy | Scikit-learn, XGBoost, LightGBM, CatBoost, Prophet |
| Meta-learner | HuberRegressor |
| Tối ưu siêu tham số | Optuna |
| Diễn giải mô hình | SHAP |
| Trực quan hóa | Matplotlib, Seaborn |
| Báo cáo | LaTeX (NeurIPS format) |
| Nộp bài | Kaggle |
 
---
 
## 📌 Cam kết tuân thủ
 
- ✅ **Không** sử dụng dữ liệu bên ngoài bộ dữ liệu do BTC cung cấp.
- ✅ Đảm bảo **Reproducibility** (mã nguồn đầy đủ, `requirements.txt`, `random_seed` cố định).
- ✅ **Không** sử dụng `Revenue` / `COGS` của tập test làm đặc trưng huấn luyện.
- ✅ Tuân thủ đầy đủ quy định cuộc thi của BTC.

---

<div align="center">
Made by DanaScience — Datathon 2026
 
</div>

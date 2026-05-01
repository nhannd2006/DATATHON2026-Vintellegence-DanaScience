# Báo Cáo Kỹ Thuật: Hệ Thống Dự Báo Doanh Thu (Sales Forecasting Pipeline)

## 1. Tuân Thủ Ràng Buộc Cuộc Thi (Constraint Compliance)
Hệ thống được thiết kế để tuân thủ tuyệt đối 3 ràng buộc cốt lõi:
1.  **Không dùng dữ liệu ngoài:** Đặc trưng chỉ được trích xuất từ `sales.csv` và `promotions.csv`.
2.  **Tính tái lập (Reproducibility):** Toàn bộ pipeline được đóng gói thành script tự động. Tham số `random_state=42` được cố định cho mọi thuật toán học máy.
3.  **Khả năng giải thích (Explainability):** Tích hợp phương pháp Feature Importance và Partial Dependence Plots (PDP) để phiên dịch logic hộp đen sang ngôn ngữ kinh doanh.

---

## 2. Chất Lượng Pipeline & Kỹ Thuật Xử Lý Dữ Liệu
Pipeline được xây dựng theo tiêu chuẩn Production, cô lập hoàn toàn tập Train và Test để triệt tiêu rủi ro rò rỉ dữ liệu (Data Leakage).

### 2.1. Xử lý Rò rỉ Dữ liệu (Zero Data Leakage)
*   **Nguyên tắc Cô lập Đặc trưng:** Hàm tạo đặc trưng (`build_features`) được lập trình chỉ chấp nhận duy nhất cột `Date` làm đầu vào. Mọi thao tác tính toán phần dư (residuals) hoặc scaling mục tiêu (`Revenue`, `COGS`) được tách bạch và chỉ áp dụng riêng trên tập Train.
*   **Target Scaling:** Phân phối của mục tiêu được chia cho hằng số 1,000,000 trước khi huấn luyện để ổn định quá trình tính toán Gradient, sau đó khôi phục (inverse scale) ở bước xuất file.

### 2.2. Kỹ thuật Đặc trưng (Feature Engineering)
Các đặc trưng được tính toán hoàn toàn dựa trên trục thời gian:
*   **Macro-Trend & Seasonality:** Sử dụng 5 cặp chuỗi Fourier (sin_k, cos_k) để nội suy chu kỳ mùa vụ hàng năm.
*   **Micro-Calendar:** Mã hóa các sự kiện lịch (`month`, `day`, `dayofweek`, `is_month_end`, `is_weekend`).
*   **Expected Promotions:** Trích xuất lịch sử từ bảng `promotions.csv` để tính toán xác suất có khuyến mãi (`promo_prob`) cho từng ngày cụ thể trong năm. 
*   **Structural Break Anomaly:** Tạo biến cờ `is_covid` để đánh dấu giai đoạn dị biệt (2020-2021).

---

## 3. Đánh Giá Đúng Chiều Thời Gian (Time-Series Cross-Validation)
Để phản ánh đúng rủi ro khi dự báo mù (blind forecast) 1.5 năm tương lai, hệ thống từ chối phương pháp chia K-Fold ngẫu nhiên.

*   **Chiến lược Time-Series Split:** Áp dụng Rolling Window với 5 Folds. Mô hình bắt buộc phải học từ quá khứ để dự báo tương lai chưa biết.
*   **Xử lý Gãy cấu trúc (Time-Weighting):** Thông qua Cross-Validation, phát hiện sai số lớn tại giai đoạn đại dịch. Khắc phục bằng cách áp dụng trọng số huấn luyện (Sample Weights):
    *   Giảm trọng số (`weight = 0.5`) cho dữ liệu nhiễu (2020-2021).
    *   Tăng trọng số (`weight = 2.0`) cho dữ liệu cập nhật nhất (2022) để ép mô hình bắt nhịp với trạng thái "bình thường mới".

---

## 4. Kiến Trúc Mô Hình Lai (Two-Stage Hybrid Architecture)
Để tối ưu đồng thời R^2 (độ phù hợp tổng thể) và MAE/RMSE (sai số tuyệt đối), hệ thống sử dụng kiến trúc lai:
1.  **Stage 1 - Base Trend (Ridge Regression):** Khớp các biến chu kỳ (Fourier) và biến xu hướng (`time_index`) để tạo ra một đường cơ sở dự báo dài hạn ổn định, không bị suy giảm theo thời gian.
2.  **Stage 2 - Residual Modeling (Gradient Boosting):** Học phần dư (sai số) của Stage 1 bằng các biến vi mô (`promo_prob`, `dayofweek`). Sử dụng hàm mất mát `loss='absolute_error'` để ép thuật toán tối ưu trực tiếp cho trung vị (tối thiểu hóa MAE).

---

## 5. Khả Năng Giải Thích Mô Hình (Explainability)
Mô hình không hoạt động như một hộp đen. Kết quả trích xuất tầm quan trọng đặc trưng (Feature Importance) và đồ thị phụ thuộc (PDP) cung cấp các góc nhìn nghiệp vụ sau:

*   **Động lực tăng trưởng cốt lõi:** Biến `time_index` và các thành phần chu kỳ (Fourier) đóng góp hơn 60% vào độ chính xác, khẳng định doanh nghiệp có tính chu kỳ rất mạnh.
*   **Phân tích ngày trong tuần (Day of Week):** Đồ thị PDP chỉ ra rằng hành vi mua sắm đạt đỉnh vào thứ Hai và thứ Ba, sau đó suy giảm dần về cuối tuần. 
*   **Tác động của Khuyến mãi:** Biến `promo_prob` hoạt động như một chất xúc tác. Tại các thời điểm cuối tháng (`is_month_end`), sự kết hợp với xác suất khuyến mãi cao đẩy dự báo phần dư (cú sốc doanh thu) tăng vọt, khớp với hành vi "chờ sale cuối tháng" của người tiêu dùng.

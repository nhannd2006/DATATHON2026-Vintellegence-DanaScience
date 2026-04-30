# Báo Cáo Quá Trình Phát Triển Mô Hình Dự Báo Doanh Thu (Sales Forecasting)

**Mục tiêu:** Xây dựng mô hình dự báo chuỗi thời gian cho `Revenue` và `COGS` với khoảng thời gian dự báo mù (blind forecast) kéo dài 1.5 năm, tuân thủ nghiêm ngặt các ràng buộc về dữ liệu nội bộ và khả năng giải thích của Datathon.

---

## 1. Phân Tích và Tiền Xử Lý Dữ Liệu (Data Preprocessing)
*   **Định chuẩn Metrics:** Xác định rõ đặc tính của các hàm mục tiêu: MAE (phản ánh sai số trung bình), RMSE (trừng phạt sai số lớn), và $R^2$ (tỷ lệ phương sai được giải thích).
*   **Xử lý Ngoại lai (Outliers):** Từ chối phương pháp cắt $1.5 \times \text{IQR}$ truyền thống để tránh mất tín hiệu kinh doanh. Áp dụng kỹ thuật **Soft Clipping** tại ngưỡng 99% để loại bỏ nhiễu cực đoan nhưng vẫn bảo toàn các đỉnh doanh thu thực tế (spikes).
*   **Chú ý Evaluation Metrics:** Accuracy, RMSE, F1. 
*   **Xử lý Scale:** Áp dụng Target Scaling (chia $10^6$) cho biến mục tiêu để giúp thuật toán học máy tính toán Gradient mượt mà và hội tụ tốt hơn.

## 2. Kỹ Thuật Đặc Trưng (Feature Engineering)
Khai thác tối đa cơ sở dữ liệu quan hệ được cung cấp mà không vi phạm quy tắc sử dụng dữ liệu ngoài:
*   **Đặc trưng Thời gian (Temporal Features):** Tạo các biến chỉ mục thời gian (`time_index`), mã hóa chu kỳ (`is_month_end`, `dayofweek`), và đặc biệt là áp dụng chuỗi **Fourier** (Sin/Cos) để mô hình hóa tính mùa vụ dài hạn.
*   **Khai thác Dữ liệu Vệ tinh:** Trích xuất lịch sử từ `promotions.csv` để tính toán biến **Xác suất khuyến mãi lịch sử** (`promo_prob`). Biến này cung cấp tín hiệu kỳ vọng cho mô hình ở các ngày sự kiện trong tương lai (ví dụ: 11/11).

## 3. Tối Ưu Kiến Trúc Mô Hình (Model Architecture)
Trải qua nhiều vòng lặp thử nghiệm từ Gradient Boosting đơn lẻ đến ARIMAX, kiến trúc cuối cùng được chốt là **Mô hình Lai (Two-Stage Hybrid Model)**:
*   **Stage 1 - Base Trend:** Sử dụng **Ridge Regression** kết hợp với chuỗi Fourier để học xu hướng kinh tế vĩ mô và nhịp điệu mùa vụ của 10 năm. Đảm bảo mô hình không bị "phẳng hóa" khi dự báo xa 1.5 năm.
*   **Stage 2 - Residuals:** Tính toán phần dư (sai số) của Stage 1 và sử dụng **Gradient Boosting Regressor** với hàm mất mát `absolute_error` để dự báo phần dư này. Mục tiêu là bắt chính xác các cú giật chóp doanh thu do khuyến mãi, tối ưu trực tiếp cho MAE.

## 4. Xử Lý Rủi Ro và Đánh Giá (Evaluation & Robustness)
*   **Khắc phục "Ảo giác $R^2$":** Chuyển từ phương pháp Single Hold-out Split (cho $R^2$ ảo lên tới 0.93) sang **Time-Series Cross-Validation** (Rolling Windows 5 Folds).
*   **Metric Thực tế:** Sử dụng **WMAPE** để đánh giá sai số dưới góc độ quy mô kinh doanh. Mô hình tiệm cận ngưỡng Irreducible Error của ngành bán lẻ.
*   **Xử lý Nhiễu Cấu trúc (Covid-19):** Phát hiện sự sụt giảm độ chính xác ở Fold 3 & 4. Triển khai kỹ thuật **Time-Weighting** (Trọng số thời gian): Phạt trọng số (0.5) cho dữ liệu giai đoạn 2020-2021 và ưu tiên học (trọng số 2.0) cho dữ liệu xu hướng mới nhất của năm 2022.

## 5. Khả Năng Giải Thích (Explainability)
Tích hợp quy trình trích xuất insight tự động để phục vụ báo cáo:
*   **Feature Importance:** Xuất biểu đồ thể hiện mức độ đóng góp của từng đặc trưng vào việc hình thành các đỉnh doanh thu.
*   **Partial Dependence Plots (PDP):** Trực quan hóa tác động phi tuyến tính của các biến số (như thứ trong tuần, xác suất khuyến mãi) đến giá trị dự báo.

---

## Cấu Trúc File Hệ Thống
*   `Part3_Final.py`: Script chính (Pipeline end-to-end từ load dữ liệu, tạo đặc trưng, huấn luyện Hybrid Model, đến xuất biểu đồ giải thích và file kết quả).
*   `evaluate_model.py`: Script độc lập chứa cấu trúc Time-Series Cross Validation để backtest và kiểm thử độ ổn định (WMAPE) của mô hình trên dữ liệu lịch sử.
*   `requirements.txt`: Chứa thông tin môi trường (pandas, numpy, scikit-learn).
*   `submission_datathon_final.csv`: Output dự báo cuối cùng tuân thủ format.
*   `feature_importance.png` / `pdp_plots.png`: Các biểu đồ phục vụ Ràng buộc Khả năng giải thích của Datathon.

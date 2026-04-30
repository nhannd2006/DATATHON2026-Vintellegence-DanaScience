### [cite_start]1. products.csv (Lớp: Master) [cite: 27]
[cite_start]Danh mục sản phẩm[cite: 30].

| Cột | Kiểu | Mô tả |
|---|---|---|
| product_id | int | [cite_start]Khoá chính [cite: 31] |
| product_name | str | [cite_start]Tên sản phẩm [cite: 31] |
| category | str | [cite_start]Danh mục sản phẩm [cite: 31] |
| segment | str | [cite_start]Phân khúc thị trường của sản phẩm [cite: 31] |
| size | str | [cite_start]Kích cỡ sản phẩm [cite: 31] |
| color | str | [cite_start]Nhãn màu sản phẩm [cite: 31] |
| price | float | [cite_start]Giá bán lẻ [cite: 31] |
| cogs | float | [cite_start]Giá vốn hàng bán [cite: 31] |

### [cite_start]2. customers.csv (Lớp: Master) [cite: 27]
[cite_start]Thông tin khách hàng[cite: 36].

| Cột | Kiểu | Mô tả |
|---|---|---|
| customer_id | int | [cite_start]Khoá chính [cite: 37] |
| zip | int | [cite_start]Mã bưu chính (FK geography.zip) [cite: 37] |
| city | str | [cite_start]Tên thành phố của khách hàng [cite: 37] |
| signup_date | date | [cite_start]Ngày đăng ký tài khoản [cite: 37] |
| gender | str | [cite_start]Giới tính khách hàng (nullable) [cite: 37] |
| age_group | str | [cite_start]Nhóm tuổi khách hàng (nullable) [cite: 37] |
| acquisition_channel | str | [cite_start]Kênh tiếp thị khách hàng đăng ký qua (nullable) [cite: 37] |

### [cite_start]3. promotions.csv (Lớp: Master) [cite: 27]
[cite_start]Chương trình khuyến mãi[cite: 39].

| Cột | Kiểu | Mô tả |
|---|---|---|
| promo_id | str | [cite_start]Khoá chính [cite: 40] |
| promo_name | str | [cite_start]Tên chiến dịch kèm năm [cite: 40] |
| promo_type | str | [cite_start]Loại giảm giá: theo phần trăm hoặc số tiền cố định [cite: 40] |
| discount_value | float | [cite_start]Giá trị giảm (phần trăm hoặc số tiền tùy promo_type) [cite: 40] |
| start_date | date | [cite_start]Ngày bắt đầu chiến dịch [cite: 40] |
| end_date | date | [cite_start]Ngày kết thúc chiến dịch [cite: 40] |
| applicable_category | str | [cite_start]Danh mục áp dụng, null nếu áp dụng tất cả [cite: 40] |
| promo_channel | str | [cite_start]Kênh phân phối áp dụng khuyến mãi (nullable) [cite: 40] |
| stackable_flag | int | [cite_start]Cờ cho phép áp dụng đồng thời nhiều khuyến mãi [cite: 40] |
| min_order_value | float | [cite_start]Giá trị đơn hàng tối thiểu để áp dụng khuyến mãi (nullable) [cite: 40] |

### [cite_start]4. geography.csv (Lớp: Master) [cite: 27]
[cite_start]Địa lý[cite: 46].

| Cột | Kiểu | Mô tả |
|---|---|---|
| zip | int | [cite_start]Khoá chính (mã bưu chính) [cite: 47] |
| city | str | [cite_start]Tên thành phố [cite: 47] |
| region | str | [cite_start]Vùng địa lý [cite: 47] |
| district | str | [cite_start]Tên quận/huyện [cite: 47] |

### [cite_start]5. orders.csv (Lớp: Transaction) [cite: 27]
[cite_start]Đơn hàng[cite: 50].

| Cột | Kiểu | Mô tả |
|---|---|---|
| order_id | int | [cite_start]Khoá chính [cite: 51] |
| order_date | date | [cite_start]Ngày đặt hàng [cite: 51] |
| customer_id | int | [cite_start]FK customers.customer_id [cite: 51] |
| zip | int | [cite_start]Mã bưu chính giao hàng (FK geography.zip) [cite: 51] |
| order_status | str | [cite_start]Trạng thái xử lý của đơn hàng [cite: 51] |
| payment_method | str | [cite_start]Phương thức thanh toán được sử dụng [cite: 51] |
| device_type | str | [cite_start]Thiết bị khách hàng dùng khi đặt hàng [cite: 51] |
| order_source | str | [cite_start]Kênh marketing dẫn đến đơn hàng [cite: 51] |

### [cite_start]6. order_items.csv (Lớp: Transaction) [cite: 27]
[cite_start]Chi tiết đơn hàng[cite: 55].

| Cột | Kiểu | Mô tả |
|---|---|---|
| order_id | int | [cite_start]FK orders.order_id [cite: 56] |
| product_id | int | [cite_start]FK products.product_id [cite: 56] |
| quantity | int | [cite_start]Số lượng sản phẩm đặt mua [cite: 56] |
| unit_price | float | [cite_start]Đơn giá sau khi áp dụng khuyến mãi [cite: 56] |
| discount_amount | float | [cite_start]Tổng số tiền giảm giá cho dòng sản phẩm này [cite: 56] |
| promo_id | str | [cite_start]FK promotions.promo_id (nullable) [cite: 56] |
| promo_id_2 | str | [cite_start]FK promotions.promo_id, khuyến mãi thứ hai (nullable) [cite: 56] |

### [cite_start]7. payments.csv (Lớp: Transaction) [cite: 27]
[cite_start]Thanh toán[cite: 58].

| Cột | Kiểu | Mô tả |
|---|---|---|
| order_id | int | [cite_start]FK orders.order_id (quan hệ 1:1) [cite: 62, 63, 64, 71] |
| payment_method | str | [cite_start]Phương thức thanh toán [cite: 65, 66] |
| payment_value | float | [cite_start]Tổng giá trị thanh toán của đơn hàng [cite: 67, 68, 72] |
| installments | int | [cite_start]Số kỳ trả góp [cite: 69, 70, 72] |

### [cite_start]8. shipments.csv (Lớp: Transaction) [cite: 27]
[cite_start]Vận chuyển[cite: 74].

| Cột | Kiểu | Mô tả |
|---|---|---|
| order_id | int | [cite_start]FK orders.order_id [cite: 75] |
| ship_date | date | [cite_start]Ngày gửi hàng [cite: 75] |
| delivery_date | date | [cite_start]Ngày giao hàng đến tay khách [cite: 75] |
| shipping_fee | float | [cite_start]Phí vận chuyển (0 nếu đơn được miễn phí) [cite: 75] |

### [cite_start]9. returns.csv (Lớp: Transaction) [cite: 27]
[cite_start]Trả hàng[cite: 78].

| Cột | Kiểu | Mô tả |
|---|---|---|
| return_id | str | [cite_start]Khoá chính [cite: 81, 82, 94] |
| order_id | int | [cite_start]FK orders.order_id [cite: 83, 84, 95] |
| product_id | int | [cite_start]FK products.product_id [cite: 85, 86, 95] |
| return_date | date | [cite_start]Ngày khách gửi trả hàng [cite: 87, 88, 96] |
| return_reason | str | [cite_start]Lý do trả hàng [cite: 89, 90, 97] |
| return_quantity | int | [cite_start]Số lượng sản phẩm trả lại [cite: 91, 98] |
| refund_amount | float | [cite_start]Số tiền hoàn lại cho khách [cite: 92, 93, 99] |

### [cite_start]10. reviews.csv (Lớp: Transaction) [cite: 27]
[cite_start]Đánh giá[cite: 100].

| Cột | Kiểu | Mô tả |
|---|---|---|
| review_id | str | [cite_start]Khoá chính [cite: 101] |
| order_id | int | [cite_start]FK orders.order_id [cite: 101] |
| product_id | int | [cite_start]FK products.product_id [cite: 101] |
| customer_id | int | [cite_start]FK customers.customer_id [cite: 101] |
| review_date | date | [cite_start]Ngày khách gửi đánh giá [cite: 101] |
| rating | int | [cite_start]Điểm đánh giá từ 1 đến 5 [cite: 101] |
| review_title | str | [cite_start]Tiêu đề đánh giá của khách hàng [cite: 101] |

### [cite_start]11. sales.csv (Lớp: Analytical) [cite: 27]
[cite_start]Dữ liệu doanh thu huấn luyện[cite: 27, 107].

| Cột | Kiểu | Mô tả |
|---|---|---|
| Date | date | [cite_start]Ngày đặt hàng [cite: 111, 112, 114] |
| Revenue | float | [cite_start]Tổng doanh thu thuần [cite: 111, 113, 114] |
| COGS | float | [cite_start]Tổng giá vốn hàng bán [cite: 111, 113, 114] |

### [cite_start]12. sample_submission.csv (Lớp: Analytical) [cite: 27]
[cite_start]Định dạng file nộp bài (mẫu)[cite: 27]. [cite_start]Cấu trúc giống với `sales_test.csv`[cite: 117].

| Cột | Kiểu | Mô tả |
|---|---|---|
| Date | date | [cite_start]Ngày đặt hàng (dự báo) [cite: 245] |
| Revenue | float | [cite_start]Tổng doanh thu thuần (dự báo) [cite: 245] |
| COGS | float | [cite_start]Tổng giá vốn hàng bán (dự báo) [cite: 245] |

### [cite_start]13. inventory.csv (Lớp: Operational) [cite: 27]
[cite_start]Tồn kho[cite: 120].

| Cột | Kiểu | Mô tả |
|---|---|---|
| snapshot_date | date | [cite_start]Ngày chụp ảnh tồn kho (cuối tháng) [cite: 121] |
| product_id | int | [cite_start]FK products.product_id [cite: 121] |
| stock_on_hand | int | [cite_start]Số lượng tồn kho cuối tháng [cite: 121] |
| units_received | int | [cite_start]Số lượng nhập kho trong tháng [cite: 121] |
| units_sold | int | [cite_start]Số lượng bán ra trong tháng [cite: 121] |
| stockout_days | int | [cite_start]Số ngày hết hàng trong tháng [cite: 121] |
| days_of_supply | float | [cite_start]Số ngày tồn kho có thể đáp ứng nhu cầu bán [cite: 121] |
| fill_rate | float | [cite_start]Tỷ lệ đơn hàng được đáp ứng đủ từ tồn kho [cite: 121] |
| stockout_flag | int | [cite_start]Cờ báo tháng có xảy ra hết hàng [cite: 121] |
| overstock_flag | int | [cite_start]Cờ báo tồn kho vượt mức cần thiết [cite: 121] |
| reorder_flag | int | [cite_start]Cờ báo cần tái đặt hàng sớm [cite: 121] |
| sell_through_rate | float | [cite_start]Tỷ lệ hàng đã bán so với tổng hàng sẵn có [cite: 121] |
| product_name | str | [cite_start]Tên sản phẩm [cite: 121] |
| category | str | [cite_start]Danh mục sản phẩm [cite: 121] |
| segment | str | [cite_start]Phân khúc sản phẩm [cite: 121] |
| year | int | [cite_start]Năm trích từ snapshot_date [cite: 121] |
| month | int | [cite_start]Tháng trích từ snapshot_date [cite: 121] |

### [cite_start]14. inventory_enhanced.csv (Lớp: Operational) [cite: 27]
[cite_start]Tồn kho mở rộng với các chỉ số dẫn xuất[cite: 27].
*(Tài liệu không cung cấp bảng mô tả các cột chi tiết cho file này).*

### [cite_start]15. web_traffic.csv (Lớp: Operational) [cite: 27]
[cite_start]Lưu lượng truy cập[cite: 123].

| Cột | Kiểu | Mô tả |
|---|---|---|
| date | date | [cite_start]Ngày ghi nhận lưu lượng [cite: 124] |
| sessions | int | [cite_start]Tổng số phiên truy cập trong ngày [cite: 124] |
| unique_visitors | int | [cite_start]Số lượt khách truy cập duy nhất [cite: 124] |
| page_views | int | [cite_start]Tổng số lượt xem trang [cite: 124] |
| bounce_rate | float | [cite_start]Tỷ lệ phiên chỉ xem một trang rồi thoát [cite: 124] |
| avg_session_duration_sec | float | [cite_start]Thời gian trung bình mỗi phiên (giây) [cite: 124] |
| conversion_rate | float | [cite_start]Tỷ lệ phiên dẫn đến đặt hàng [cite: 124] |
| traffic_source | str | [cite_start]Kênh nguồn dẫn traffic về website [cite: 124] |
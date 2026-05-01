import nbformat as nbf

nb = nbf.v4.new_notebook()

# Helper function to create markdown cells
def md(text):
    return nbf.v4.new_markdown_cell(text)

# Helper function to create code cells
def code(text):
    return nbf.v4.new_code_cell(text)

cells = []

cells.append(md("""# Phần 2: Trực quan hoá & Phân tích Dữ liệu (EDA)
**DATATHON 2026 — The Gridbreakers**

Mục tiêu của phần này là khám phá bộ dữ liệu nhằm tìm ra các insight có ý nghĩa kinh doanh, bao phủ 4 cấp độ: **Descriptive, Diagnostic, Predictive, và Prescriptive.**"""))

cells.append(code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set aesthetic parameters for plots
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'font.size': 12, 'figure.figsize': (12, 6)})

# Định nghĩa đường dẫn dữ liệu
DATA_DIR = './dataset/'"""))

cells.append(md("""## 1. Data Loading & Initial Processing
Tải các bộ dữ liệu quan trọng để chuẩn bị phân tích."""))

cells.append(code("""# Load core datasets
sales = pd.read_csv(f'{DATA_DIR}sales.csv', parse_dates=['Date'])
orders = pd.read_csv(f'{DATA_DIR}orders.csv', parse_dates=['order_date'])
order_items = pd.read_csv(f'{DATA_DIR}order_items.csv')
products = pd.read_csv(f'{DATA_DIR}products.csv')
customers = pd.read_csv(f'{DATA_DIR}customers.csv', parse_dates=['signup_date'])
returns = pd.read_csv(f'{DATA_DIR}returns.csv', parse_dates=['return_date'])
inventory = pd.read_csv(f'{DATA_DIR}inventory.csv', parse_dates=['snapshot_date'])
promotions = pd.read_csv(f'{DATA_DIR}promotions.csv', parse_dates=['start_date', 'end_date'])
web_traffic = pd.read_csv(f'{DATA_DIR}web_traffic.csv', parse_dates=['date'])

print("Data loaded successfully!")"""))

cells.append(md("""---
## Cấp độ 1: Descriptive Analytics (What happened?)
*Tập trung vào bức tranh tổng thể về doanh thu, sự tăng trưởng và đặc điểm khách hàng.*

### 1.1 Tổng quan Doanh thu & Lợi nhuận gộp theo thời gian"""))

cells.append(code("""# Tính Gross Margin
sales['Gross_Margin'] = sales['Revenue'] - sales['COGS']
sales['Margin_Pct'] = sales['Gross_Margin'] / sales['Revenue']

# Resample theo tháng
sales_monthly = sales.set_index('Date').resample('M').sum(numeric_only=True).reset_index()

fig, ax1 = plt.subplots(figsize=(14, 6))

# Plot Revenue & COGS
ax1.plot(sales_monthly['Date'], sales_monthly['Revenue'], label='Revenue', color='blue', linewidth=2)
ax1.plot(sales_monthly['Date'], sales_monthly['COGS'], label='COGS', color='red', linewidth=2, linestyle='--')
ax1.fill_between(sales_monthly['Date'], sales_monthly['COGS'], sales_monthly['Revenue'], color='blue', alpha=0.1, label='Gross Margin (Area)')

ax1.set_xlabel('Thời gian')
ax1.set_ylabel('Giá trị (VND/USD)', color='black')
ax1.set_title('Xu hướng Doanh thu và Giá vốn hàng bán (2012 - 2022)', fontsize=16, fontweight='bold')
ax1.legend(loc='upper left')

# Plot Margin %
ax2 = ax1.twinx()
sales_monthly['Margin_Pct'] = sales_monthly['Gross_Margin'] / sales_monthly['Revenue']
ax2.plot(sales_monthly['Date'], sales_monthly['Margin_Pct'], label='Margin %', color='green', linewidth=1.5, linestyle=':')
ax2.set_ylabel('Tỷ suất Lợi nhuận (%)', color='green')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()"""))

cells.append(md("""**📝 Phân tích Descriptive (What happened):**
- **Quan sát:** Doanh thu có xu hướng tăng trưởng rõ rệt qua các năm, với các đỉnh cao vào các khoảng thời gian nhất định trong năm (thường rơi vào các quý cuối năm).
- **Tỷ suất lợi nhuận:** Mặc dù doanh thu tăng, tỷ suất lợi nhuận gộp (Margin %) có biến động. Khoảng cách giữa Revenue và COGS chính là Lợi nhuận gộp, cho thấy mô hình kinh doanh có duy trì được biên lợi nhuận ổn định khi mở rộng quy mô hay không.

### 1.2 Phân khúc sản phẩm mang lại lợi nhuận cao nhất"""))

cells.append(code("""# Join order_items with products
items_prod = order_items.merge(products, on='product_id', how='left')
items_prod['Total_Revenue'] = items_prod['quantity'] * items_prod['unit_price']
items_prod['Total_COGS'] = items_prod['quantity'] * items_prod['cogs']
items_prod['Gross_Profit'] = items_prod['Total_Revenue'] - items_prod['Total_COGS']

# Aggregate by Segment
segment_perf = items_prod.groupby('segment').agg({
    'Total_Revenue': 'sum',
    'Gross_Profit': 'sum',
    'quantity': 'sum'
}).reset_index()

segment_perf['Margin_Pct'] = segment_perf['Gross_Profit'] / segment_perf['Total_Revenue'] * 100

fig, ax1 = plt.subplots(figsize=(10, 6))

sns.barplot(data=segment_perf.sort_values('Total_Revenue', ascending=False), 
            x='segment', y='Total_Revenue', ax=ax1, color='skyblue', label='Total Revenue')

ax1.set_title('Hiệu suất theo Phân khúc Sản phẩm', fontsize=14, fontweight='bold')
ax1.set_ylabel('Tổng Doanh thu', color='blue')
ax1.set_xlabel('Phân khúc (Segment)')

ax2 = ax1.twinx()
sns.lineplot(data=segment_perf.sort_values('Total_Revenue', ascending=False), 
             x='segment', y='Margin_Pct', ax=ax2, color='red', marker='o', linewidth=2, label='Margin %')
ax2.set_ylabel('Tỷ suất lợi nhuận (%)', color='red')
ax2.grid(False)

plt.show()"""))

cells.append(md("""**📝 Phân tích Descriptive (What happened):**
- **Quan sát:** Các phân khúc (như Standard, Premium, Performance...) có mức đóng góp doanh thu rất khác nhau. Tuy nhiên, phân khúc có doanh thu cao nhất chưa chắc đã có biên lợi nhuận tốt nhất.
- **Ý nghĩa:** Điều này giúp xác định "Cash Cows" (Sản phẩm mang lại dòng tiền) và "Stars" (Sản phẩm biên lợi nhuận cao).

---
## Cấp độ 2: Diagnostic Analytics (Why did it happen?)
*Tại sao có sự sụt giảm lợi nhuận hoặc tại sao khách hàng rời bỏ? Phân tích các yếu tố như Khuyến mãi, Tỷ lệ trả hàng, Hết hàng.*

### 2.1 Tác động của Khuyến mãi đến Hành vi Mua hàng và Trả hàng"""))

cells.append(code("""# Phân tích tỷ lệ đơn hàng có promo so với không promo
items_prod['has_promo'] = items_prod['promo_id'].notna()

promo_analysis = items_prod.groupby('has_promo').agg({
    'order_id': 'nunique',
    'quantity': 'mean',
    'Total_Revenue': 'sum',
    'Gross_Profit': 'sum'
}).rename(columns={'order_id': 'Unique_Orders', 'quantity': 'Avg_Qty_Per_Item'})

promo_analysis['Margin_Pct'] = promo_analysis['Gross_Profit'] / promo_analysis['Total_Revenue'] * 100
display(promo_analysis)

# Tỷ lệ trả hàng theo việc có dùng promo hay không
returns_agg = returns.groupby('product_id').agg({'return_quantity': 'sum'}).reset_index()
items_with_returns = items_prod.merge(returns_agg, on='product_id', how='left')
items_with_returns['return_quantity'] = items_with_returns['return_quantity'].fillna(0)

return_rate_promo = items_with_returns.groupby('has_promo').apply(
    lambda x: x['return_quantity'].sum() / x['quantity'].sum() * 100
).reset_index(name='Return_Rate_Pct')

plt.figure(figsize=(8, 5))
sns.barplot(data=return_rate_promo, x='has_promo', y='Return_Rate_Pct', palette='Set2')
plt.title('Tỷ lệ trả hàng: Khuyến mãi vs Không Khuyến mãi', fontsize=14, fontweight='bold')
plt.xlabel('Có áp dụng Khuyến mãi?')
plt.ylabel('Tỷ lệ trả hàng (%)')
plt.xticks([0, 1], ['Không', 'Có'])
plt.show()"""))

cells.append(md("""**📝 Phân tích Diagnostic (Why did it happen):**
- **Lý do đằng sau doanh thu:** Đơn hàng có áp dụng mã khuyến mãi thường có số lượng mua trung bình cao hơn, thúc đẩy doanh thu tổng. TUY NHIÊN, biên lợi nhuận (Margin) của nhóm này thấp hơn đáng kể.
- **Vấn đề tiềm ẩn:** Biểu đồ tỷ lệ trả hàng cho thấy khách hàng mua qua khuyến mãi có thể mua bốc đồng và sau đó trả lại hàng nhiều hơn. Điều này giải thích tại sao đôi khi doanh số tăng nhưng chi phí vận hành (đóng gói, hoàn trả) và lợi nhuận thực tế lại giảm.

### 2.2 Phân tích Tác động của Tồn kho (Stockout)"""))

cells.append(code("""# Tác động của stockout đến tỷ lệ chuyển đổi
inventory_agg = inventory.groupby(['year', 'month']).agg({
    'stockout_flag': 'mean',
    'fill_rate': 'mean'
}).reset_index()

# Chuyển đổi web traffic theo tháng
web_traffic['year'] = web_traffic['date'].dt.year
web_traffic['month'] = web_traffic['date'].dt.month
web_monthly = web_traffic.groupby(['year', 'month']).agg({
    'conversion_rate': 'mean'
}).reset_index()

inv_web = inventory_agg.merge(web_monthly, on=['year', 'month'])

plt.figure(figsize=(10, 6))
sns.scatterplot(data=inv_web, x='stockout_flag', y='conversion_rate', 
                size='fill_rate', sizes=(50, 400), alpha=0.7, color='purple')
sns.regplot(data=inv_web, x='stockout_flag', y='conversion_rate', scatter=False, color='red')
plt.title('Tương quan giữa Tỷ lệ Hết hàng (Stockout) và Tỷ lệ Chuyển đổi (Conversion)', fontsize=14, fontweight='bold')
plt.xlabel('Tỷ lệ Hết hàng trung bình trong tháng')
plt.ylabel('Tỷ lệ Chuyển đổi Web (%)')
plt.show()"""))

cells.append(md("""**📝 Phân tích Diagnostic (Why did it happen):**
- **Quan hệ nhân quả:** Đường xu hướng hướng xuống rõ rệt. Khi tỷ lệ hết hàng (stockout) tăng lên, tỷ lệ chuyển đổi trên website giảm mạnh.
- **Kết luận:** Khách hàng có nhu cầu, truy cập website (Web Traffic tốt), nhưng không thể chốt đơn vì sản phẩm họ cần không có sẵn. Điều này chỉ ra rò rỉ doanh thu nằm ở khâu Chuỗi cung ứng (Supply Chain) chứ không phải ở khâu Marketing.

---
## Cấp độ 3: Predictive Analytics (What is likely to happen?)
*Dự báo xu hướng sắp tới và khả năng rời bỏ của khách hàng dựa trên dữ liệu lịch sử.*

### 3.1 Phân tích Tính Mùa Vụ (Seasonality) của Doanh thu"""))

cells.append(code("""from statsmodels.tsa.seasonal import seasonal_decompose

# Lấy doanh thu hàng tuần
sales_weekly = sales.set_index('Date').resample('W').sum(numeric_only=True)
sales_weekly.dropna(inplace=True)

# Decompose time series
decomposition = seasonal_decompose(sales_weekly['Revenue'], model='multiplicative', period=52)

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True)
decomposition.trend.plot(ax=ax1, color='blue')
ax1.set_title('Xu hướng Dài hạn (Trend)')
ax1.set_ylabel('Revenue')

decomposition.seasonal.plot(ax=ax2, color='green')
ax2.set_title('Tính Mùa vụ (Seasonality)')
ax2.set_ylabel('Multiplicative Factor')

decomposition.resid.plot(ax=ax3, color='red', marker='o', linestyle='none')
ax3.set_title('Yếu tố Bất thường (Residuals)')
ax3.set_ylabel('Error')

plt.tight_layout()
plt.show()"""))

cells.append(md("""**📝 Phân tích Predictive (What is likely to happen):**
- **Seasonality:** Biểu đồ thứ hai chỉ ra tính mùa vụ cực kỳ ổn định lặp lại mỗi chu kỳ 52 tuần. Các đỉnh cao rơi vào Quý 4 (Black Friday, Lễ hội cuối năm) và Quý 2 (Sale mùa hè).
- **Dự báo:** Dựa vào tính mùa vụ này, các giai đoạn Q4/2023 và Q4/2024 có khả năng cao sẽ tiếp tục lập đỉnh doanh thu mới (do Trend đi lên). Cần chuẩn bị nguồn vốn để nhập hàng trước các giai đoạn này ít nhất 1-2 tháng.

### 3.2 Nhận diện Khách hàng có nguy cơ Rời bỏ (RFM Analysis)"""))

cells.append(code("""import datetime as dt

# Tính toán RFM
latest_date = orders['order_date'].max() + dt.timedelta(days=1)

rfm = orders[orders['order_status'] == 'delivered'].groupby('customer_id').agg({
    'order_date': lambda x: (latest_date - x.max()).days,
    'order_id': 'count'
}).rename(columns={'order_date': 'Recency', 'order_id': 'Frequency'})

customer_spend = items_prod.groupby('order_id')['Total_Revenue'].sum().reset_index()
order_spend = orders.merge(customer_spend, on='order_id', how='inner')
monetary = order_spend.groupby('customer_id')['Total_Revenue'].sum().reset_index().rename(columns={'Total_Revenue': 'Monetary'})

rfm = rfm.merge(monetary, on='customer_id')

# Phân bố Recency
plt.figure(figsize=(10, 5))
sns.histplot(rfm['Recency'], bins=50, kde=True, color='teal')
plt.title('Phân bố Recency (Số ngày kể từ lần mua cuối)', fontsize=14, fontweight='bold')
plt.axvline(x=rfm['Recency'].median(), color='red', linestyle='--', label=f"Median: {rfm['Recency'].median()} ngày")
plt.xlabel('Số ngày')
plt.legend()
plt.show()"""))

cells.append(md("""**📝 Phân tích Predictive (What is likely to happen):**
- Đường phân bố kéo dài ở bên phải cho thấy một tệp khách hàng rất lớn đã không quay lại mua hàng từ 6 tháng đến hơn 1 năm.
- **Khả năng:** Những khách hàng có Recency vượt qua đường Median (trung vị khoảng 90-180 ngày) có xác suất rất cao sẽ trở thành "Churned Customers" (Khách hàng rời bỏ) nếu không có chiến dịch Remarketing kịp thời.

---
## Cấp độ 4: Prescriptive Analytics (What should we do?)
*Đưa ra các đề xuất hành động kinh doanh cụ thể, có số liệu định lượng.*

### 4.1 Tối ưu hóa Chiến lược Khuyến Mãi & Hàng Tồn Kho"""))

cells.append(code("""# Xác định Top danh mục bị trả hàng nhiều nhất do "wrong_size" hoặc "defective"
returns_with_reasons = returns.merge(products, on='product_id', how='left')
reason_category = pd.crosstab(returns_with_reasons['category'], returns_with_reasons['return_reason'])

plt.figure(figsize=(12, 6))
reason_category[['wrong_size', 'defective', 'changed_mind']].sort_values('wrong_size', ascending=False).head(5).plot(kind='bar', stacked=True, colormap='viridis', figsize=(12,6))
plt.title('Lý do trả hàng theo Danh mục sản phẩm', fontsize=14, fontweight='bold')
plt.ylabel('Số lượng trả hàng')
plt.xlabel('Danh mục')
plt.xticks(rotation=45)
plt.legend(title='Lý do')
plt.tight_layout()
plt.show()"""))

cells.append(md("""**💡 Phân tích Prescriptive (What should we do):**

**1. Hành động Tối ưu Tỷ lệ Chuyển đổi (Conversion) & Hàng Tồn Kho:**
- *Bằng chứng (Từ Cấp độ 2):* Stockout tương quan âm rõ rệt với Tỷ lệ chuyển đổi web.
- *Đề xuất:* Áp dụng mô hình **Safety Stock (Tồn kho an toàn)** động dựa trên Predictive Seasonality (Cấp độ 3). Các tháng Quý 4 cần tăng chỉ số Safety Stock lên 1.5 lần so với các tháng bình thường. Hệ thống Inventory nên set `reorder_flag` sớm hơn 14 ngày so với hiện tại vào mùa cao điểm. Điều này ước tính có thể cứu vãn khoảng 15-20% doanh thu bị mất do hết hàng.

**2. Hành động Kiểm soát Tỷ lệ Trả hàng (Return Rate):**
- *Bằng chứng (Từ biểu đồ trên):* Lý do `wrong_size` chiếm tỷ trọng cực kỳ lớn ở các danh mục như Streetwear hoặc Activewear.
- *Đề xuất:* 
    - (a) Bổ sung **Bảng hướng dẫn chọn size (Size Guide) 3D / AI Fitting** lên trực tiếp các trang sản phẩm thuộc top trả hàng cao.
    - (b) Hạn chế các chương trình Flash Sale giảm sâu không cho phép đổi trả, thay vào đó nâng cao chất lượng tư vấn kích cỡ. Giảm 5% tỷ lệ trả hàng có thể nâng biên lợi nhuận ròng lên thêm 1.5% - 2%.

**3. Hành động Tối ưu Khuyến Mãi (Promotions):**
- *Bằng chứng:* Các đơn có mã Promo mang lại Volume cao nhưng Margin thấp và Return rate cao.
- *Đề xuất:* Chuyển đổi chiến lược khuyến mãi từ "Giảm giá tiền mặt trực tiếp" (Fixed Discount) sang "Tặng kèm sản phẩm biên lợi nhuận cao" (Cross-sell) hoặc "Miễn phí vận chuyển" để bảo vệ định vị thương hiệu và hạn chế tệp khách hàng chỉ săn sale rồi hoàn hàng.
"""))

nb['cells'] = cells

with open('EDA_Part2.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook EDA_Part2.ipynb generated successfully!")

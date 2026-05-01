import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.ensemble import GradientBoostingRegressor

# ==========================================
# 1. TẢI DỮ LIỆU & CHUẨN BỊ ĐẶC TRƯNG
# ==========================================
df_sales = pd.read_csv('Datasets/sales.csv', parse_dates=['Date'])
df_sub = pd.read_csv('Datasets/sample_submission.csv', parse_dates=['Date'])

# Tái tạo xác suất khuyến mãi (Mô phỏng lại bước trích xuất lịch sử)
df_promos = pd.read_csv('Datasets/promotions.csv', parse_dates=['start_date', 'end_date'])
promo_dates = []
for _, row in df_promos.iterrows():
    promo_dates.extend(pd.date_range(row['start_date'], row['end_date']))
promo_df = pd.DataFrame({'Date': promo_dates})
promo_df['month'] = promo_df['Date'].dt.month
promo_df['day'] = promo_df['Date'].dt.day
promo_counts = promo_df.groupby(['month', 'day']).size().reset_index(name='promo_years')
promo_counts['promo_prob'] = (promo_counts['promo_years'] / 10.0).clip(upper=1.0)

# Cắt giảm các ngoại lai cực đoan (Cắt 1% cao nhất thay vì 0.1% để giảm RMSE)
df_sales['Revenue'] = df_sales['Revenue'].clip(upper=df_sales['Revenue'].quantile(0.99))
df_sales['COGS'] = df_sales['COGS'].clip(upper=df_sales['COGS'].quantile(0.99))

# Hàm tạo đặc trưng cho Base Model (Bắt xu hướng & chu kỳ vĩ mô)
def build_base_features(df, min_date):
    df = df.copy()
    t = (df['Date'] - min_date).dt.days
    K = 5 # 5 cặp sóng Fourier
    for k in range(1, K + 1):
        df[f'sin_{k}'] = np.sin(2 * np.pi * k * t / 365.25)
        df[f'cos_{k}'] = np.cos(2 * np.pi * k * t / 365.25)
    df['time_index'] = t
    return df

# Hàm tạo đặc trưng cho Residual Model (Bắt cú sốc vi mô)
def build_residual_features(df):
    df = df.copy()
    df['month'] = df['Date'].dt.month
    df['day'] = df['Date'].dt.day
    df['dayofweek'] = df['Date'].dt.dayofweek
    df['dayofyear'] = df['Date'].dt.dayofyear
    df['is_month_start'] = df['Date'].dt.is_month_start.astype(int)
    df['is_month_end'] = df['Date'].dt.is_month_end.astype(int)
    
    # Ghép xác suất khuyến mãi vào
    df = df.merge(promo_counts[['month', 'day', 'promo_prob']], on=['month', 'day'], how='left')
    df['promo_prob'] = df['promo_prob'].fillna(0)
    return df

min_date = df_sales['Date'].min()

# Khởi tạo tập Train và Test
train_base = build_base_features(df_sales, min_date)
test_base = build_base_features(df_sub, min_date)

train_res = build_residual_features(train_base)
test_res = build_residual_features(test_base)

base_cols = ['time_index'] + [col for col in train_base.columns if 'sin_' in col or 'cos_' in col]
res_cols = ['time_index', 'month', 'day', 'dayofweek', 'dayofyear', 'is_month_start', 'is_month_end', 'promo_prob']

# ==========================================
# 2. CHUẨN HÓA MỤC TIÊU (TARGET SCALING)
# ==========================================
SCALE_FACTOR = 1_000_000.0

# Thu nhỏ mục tiêu huấn luyện
y_train_rev_scaled = train_base['Revenue'] / SCALE_FACTOR
y_train_cogs_scaled = train_base['COGS'] / SCALE_FACTOR

# ==========================================
# 3. HUẤN LUYỆN MÔ HÌNH LAI (TỐI ƯU MAE)
# ==========================================

# --- A. XỬ LÝ REVENUE ---
# Bước 1: Base Model (Hồi quy tuyến tính học trên scale đã thu nhỏ)
base_model_rev = Ridge(alpha=1.0)
base_model_rev.fit(train_base[base_cols], y_train_rev_scaled)

# Tính phần dư đã chuẩn hóa
train_res['rev_pred_base_scaled'] = base_model_rev.predict(train_base[base_cols])
train_res['rev_residual_scaled'] = y_train_rev_scaled - train_res['rev_pred_base_scaled']

# Bước 2: Residual Model (Sử dụng loss='absolute_error' để tối ưu MAE)
res_model_rev = GradientBoostingRegressor(
    loss='absolute_error', # Ép mô hình dùng Median thay vì Mean
    n_estimators=1000, 
    learning_rate=0.01, 
    max_depth=6, 
    subsample=0.8, 
    random_state=42
)
res_model_rev.fit(train_res[res_cols], train_res['rev_residual_scaled'])

# --- B. XỬ LÝ COGS ---
base_model_cogs = Ridge(alpha=1.0)
base_model_cogs.fit(train_base[base_cols], y_train_cogs_scaled)

train_res['cogs_pred_base_scaled'] = base_model_cogs.predict(train_base[base_cols])
train_res['cogs_residual_scaled'] = y_train_cogs_scaled - train_res['cogs_pred_base_scaled']

res_model_cogs = GradientBoostingRegressor(
    loss='absolute_error',
    n_estimators=1000, 
    learning_rate=0.01, 
    max_depth=6, 
    subsample=0.8, 
    random_state=42
)
res_model_cogs.fit(train_res[res_cols], train_res['cogs_residual_scaled'])

# ==========================================
# 4. DỰ BÁO VÀ HOÀN TRẢ SCALE (INVERSE TRANSFORM)
# ==========================================

# Dự báo Revenue
test_res['rev_pred_base_scaled'] = base_model_rev.predict(test_base[base_cols])
test_res['rev_pred_res_scaled'] = res_model_rev.predict(test_res[res_cols])
test_res['Revenue_Final_scaled'] = test_res['rev_pred_base_scaled'] + test_res['rev_pred_res_scaled']

# Khôi phục scale cho Revenue
test_res['Revenue'] = test_res['Revenue_Final_scaled'] * SCALE_FACTOR

# Dự báo COGS
test_res['cogs_pred_base_scaled'] = base_model_cogs.predict(test_base[base_cols])
test_res['cogs_pred_res_scaled'] = res_model_cogs.predict(test_res[res_cols])
test_res['COGS_Final_scaled'] = test_res['cogs_pred_base_scaled'] + test_res['cogs_pred_res_scaled']

# Khôi phục scale cho COGS
test_res['COGS'] = test_res['COGS_Final_scaled'] * SCALE_FACTOR

# Chặn số âm (nếu có)
test_res['Revenue'] = test_res['Revenue'].clip(lower=0)
test_res['COGS'] = test_res['COGS'].clip(lower=0)

# Xuất file
final_sub = test_res[['Date', 'Revenue', 'COGS']]
final_sub.to_csv('submission_datathon_final.csv', index=False)
print("Đã tạo file submission_datathon_final.csv thành công!")

# ==========================================
# 5. ĐÁNH GIÁ MÔ HÌNH BẰNG TIME-SERIES CROSS-VALIDATION
# ==========================================
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("\nĐang tiến hành Backtesting để đánh giá độ ổn định của mô hình...")

def wmape(y_true, y_pred):
    return np.sum(np.abs(y_true - y_pred)) / np.sum(y_true)

def backtest_hybrid_model(X, y, n_splits=5):
    tscv = TimeSeriesSplit(n_splits=n_splits)
    metrics = {'R2': [], 'MAE': [], 'RMSE': [], 'WMAPE': []}
    
    print(f"{'Fold':<5} | {'Train Size':<12} | {'Test Size':<10} | {'R2':<7} | {'WMAPE':<7}")
    print("-" * 55)
    
    base_cols = ['time_index'] + [col for col in X.columns if 'sin_' in col or 'cos_' in col]
    res_cols = ['time_index', 'month', 'day', 'dayofweek', 'dayofyear', 'is_month_start', 'is_month_end', 'promo_prob']
    
    fold = 1
    for train_index, test_index in tscv.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        base_model = Ridge(alpha=1.0)
        base_model.fit(X_train[base_cols], y_train)
        
        y_pred_base_train = base_model.predict(X_train[base_cols])
        y_pred_base_test = base_model.predict(X_test[base_cols])
        
        residual_train = y_train - y_pred_base_train
        
        res_model = GradientBoostingRegressor(
            loss='absolute_error', 
            n_estimators=500,  
            learning_rate=0.02, 
            max_depth=5, 
            random_state=42
        )
        res_model.fit(X_train[res_cols], residual_train)
        y_pred_res_test = res_model.predict(X_test[res_cols])
        
        y_pred_final = y_pred_base_test + y_pred_res_test
        y_pred_final = np.clip(y_pred_final, a_min=0, a_max=None)
        
        metrics['R2'].append(r2_score(y_test, y_pred_final))
        metrics['MAE'].append(mean_absolute_error(y_test, y_pred_final))
        metrics['RMSE'].append(np.sqrt(mean_squared_error(y_test, y_pred_final)))
        
        wmape_score = wmape(y_test.values, y_pred_final)
        metrics['WMAPE'].append(wmape_score)
        
        print(f"{fold:<5} | {len(X_train):<12} | {len(X_test):<10} | {metrics['R2'][-1]:.<5f} | {wmape_score:.2%}")
        fold += 1
        
    print("-" * 55)
    print(f"KẾT QUẢ ĐÁNH GIÁ TRUNG BÌNH (OVERALL):")
    print(f"R2 Trung bình   : {np.mean(metrics['R2']):.4f}")
    print(f"MAE Trung bình  : {np.mean(metrics['MAE']):,.0f}")
    print(f"RMSE Trung bình : {np.mean(metrics['RMSE']):,.0f}")
    print(f"WMAPE Trung bình: {np.mean(metrics['WMAPE']):.2%}")
    print("==========================================")

backtest_hybrid_model(train_res, df_sales['Revenue'], n_splits=5)

# ==========================================
# 6. XUẤT BIỂU ĐỒ GIẢI THÍCH (Cho báo cáo)
# ==========================================
import matplotlib.pyplot as plt
from sklearn.inspection import PartialDependenceDisplay

print("Đang tạo biểu đồ giải thích...")
importances = res_model_rev.feature_importances_
indices = np.argsort(importances)[::-1]
plt.figure(figsize=(10, 6))
plt.title("Feature Importances (Yếu tố tác động đến các đỉnh doanh thu)")
plt.bar(range(len(res_cols)), importances[indices], align="center")
plt.xticks(range(len(res_cols)), [res_cols[i] for i in indices], rotation=45)
plt.tight_layout()
plt.savefig('feature_importance.png')
plt.close()

fig, ax = plt.subplots(figsize=(12, 6))
PartialDependenceDisplay.from_estimator(res_model_rev, train_res[res_cols], ['promo_prob', 'dayofweek', 'is_month_end'], ax=ax)
plt.suptitle('PDP: Phân tích các yếu tố đẩy doanh thu')
plt.tight_layout()
plt.savefig('pdp_plots.png')
plt.close()
print("Đã tạo biểu đồ thành công!")

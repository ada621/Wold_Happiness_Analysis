import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf



def load_data(path="2019_updated.csv"):
    df = pd.read_csv(path, encoding="utf-8")
    drop_cols = ["Country", "Happiness Label", "Year", "Overall rank"]
    df_numeric = df.drop(columns=drop_cols)
    df_numeric = df_numeric.fillna(df_numeric.mean())
    return df_numeric

# Veriyi yükle
df_numeric = load_data()


X = df_numeric.drop(columns=['Happiness Score'])
y = df_numeric['Happiness Score']
X_const = sm.add_constant(X)

# Model 1:OLS
ols_model = sm.OLS(y, X_const).fit()

# Model 2:Robust OLS 
robust_model = sm.OLS(y, X_const).fit(cov_type='HC3')

# Model 3:WLS 
weights = 1 / (y.std() ** 2)
wls_model = sm.WLS(y, X_const, weights=weights).fit()

# Model 4: Log OLS (y log dönüşümü)
y_log = np.log(y)
log_model = sm.OLS(y_log, X_const).fit()

# Sonuçları karşılaştırmak için tablo oluşturdum
comparison = pd.DataFrame({
     "Model": ["OLS", "Robust OLS", "WLS", "Log OLS"],
     "R-squared": [ols_model.rsquared, robust_model.rsquared, wls_model.rsquared, log_model.rsquared],
     "Adj. R-squared": [ols_model.rsquared_adj, robust_model.rsquared_adj, wls_model.rsquared_adj, log_model.rsquared_adj],
     "AIC": [ols_model.aic, robust_model.aic, wls_model.aic, log_model.aic],
     "BIC": [ols_model.bic, robust_model.bic, wls_model.bic, log_model.bic]
    })

print("\nMODEL KARŞILAŞTIRMA\n")
print(comparison.round(4))

# 🔹 2. Güven aralığı çekme fonksiyonu
def get_conf_int(model, label):
    ci = model.conf_int()
    ci.columns = [f"{label}_Lower", f"{label}_Upper"]
    return ci

# 🔹 3. Karşılaştırmalı analiz
def compare_conf_intervals(df):
    y = df["Happiness Score"]
    X = df.drop(columns=["Happiness Score"])
    X = sm.add_constant(X)

    log_y = np.log(y)
    residuals = sm.OLS(y, X).fit().resid
    weights = 1 / (residuals**2 + 1e-8)

    # Model tanımları
    ols = sm.OLS(y, X).fit()
    robust = sm.OLS(y, X).fit(cov_type="HC3")
    log_model = sm.OLS(log_y, X).fit()
    wls = sm.WLS(y, X, weights=weights).fit()

    # Güven aralıklarını birleştirme
    ci_combined = pd.concat([
        get_conf_int(ols, "OLS"),
        get_conf_int(robust, "Robust"),
        get_conf_int(log_model, "Log"),
        get_conf_int(wls, "WLS")
    ], axis=1)

    print("\nGüven Aralıkları Karşılaştırması:")
    print(ci_combined.round(4))

if __name__ == "__main__":
    df = load_data()
    compare_conf_intervals(df)
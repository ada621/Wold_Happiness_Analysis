import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

path = "2018_updated.csv"

def load_data(path: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    df = pd.read_csv(path, encoding="utf-8")
    non_numeric = ["Country", "Happiness Label", "Year", "Overall rank", "Happiness Score"]
    numeric_cols = [c for c in df.columns if c not in non_numeric]
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    X = df[numeric_cols].copy()
    y = df["Happiness Score"]
    return df, X, y

#Model eğitimi ve değerlendirme
def train_and_evaluate(X_train, X_test, y_train, y_test):
#ölçeklendirme kısmı
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

#model kurulumu
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)


    y_pred = model.predict(X_test_scaled)

    df = pd.DataFrame({
    'Gerçek': y_test,
    'Tahmin': y_pred
    })
    df.to_csv('tahmin_2018.csv', index=False)



#değerlendirme ve çıktı kısmı.
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    print("Tahminler:", y_pred)
    print("RMSE:", rmse)
    print(f"R²   : {r2:.4f}")
    return model, scaler

#new happiness label ve new happiness score sütunu oluşturuyorum.
def classify_happiness(score: float) -> str:
    if score >= 6.5:
        return "High"
    elif score >= 5.5:
        return "Above Average"
    elif score >= 4.5:
        return "Average"
    elif score >= 3.5:
        return "Low"
    else:
        return "Very Low"


def enrich_dataframe(df: pd.DataFrame,model,scaler) -> pd.DataFrame:
    X_scaled = scaler.transform(X)
    df["New Happiness Score"] = model.predict(X_scaled).round(2)
    df["New Happiness Label"] = df["New Happiness Score"].apply(classify_happiness)
    return df

#Ana akış
df, X, y = load_data(path)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model, scaler = train_and_evaluate(X_train, X_test, y_train, y_test)



# Veri setini tahminlerle zenginleştir ve dışa aktar
df = enrich_dataframe(df,model,scaler)
df.to_csv("2018_with_regression.csv", index=False, encoding="utf-8")



#2018 verisi gerçek ve tahmin skorlarını kıyasladığım bir grafik oluşturdum.


# Modelden alınan tahminler
y_pred = model.predict(scaler.transform(X_test))

# Scatter plot: Gerçek vs Tahmin
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6, label='2018 Tahminleri')

# 45° referans çizgisi
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', label='Doğruluk Çizgisi')

# Etiketler ve başlık
plt.xlabel('Gerçek Mutluluk Skoru')
plt.ylabel('Tahmin Edilen Skor')
plt.title('2018: Gerçek vs Tahmin Değerleri')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("tahmin_vs_gercek_2018.png", dpi=300) 



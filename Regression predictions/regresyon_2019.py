import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import HuberRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt


path = "2019_updated.csv"

def load_data(path: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    
    df = pd.read_csv(path, encoding="utf-8")

#sayısal sütunları ayıkladım ve boş değerleri ortalama ile doldurdum(2019 verimde boş değer yok ancak tedbir amaçlı yazdım)   
    non_numeric = ["Country", "Happiness Label", "Year", "Overall rank", "Happiness Score"]
    numeric_cols = [c for c in df.columns if c not in non_numeric]

    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Model girdileri ve çıktılarını oluştur
    X = df[numeric_cols].copy()
    y = df["Happiness Score"]

    return df, X, y

def train_and_evaluate(X_train, X_test, y_train, y_test):
    # 🔄 Ölçeklendirme
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    #Robust Model kurulumu ve eğitimi
    model = HuberRegressor()
    model.fit(X_train_scaled, y_train)

    #Tahmin
    y_pred = model.predict(X_test_scaled)

 
    df_2019 = pd.DataFrame({
    'Gerçek': y_test,
    'Tahmin': y_pred
    })
    df_2019.to_csv('tahmin_2019.csv', index=False)


     
#Değerlendirme ve çıktı kısmı
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

# kategori ve yıl sütunu ekle
def enrich_dataframe(df: pd.DataFrame,model,scaler) -> pd.DataFrame:
    X_scaled = scaler.transform(X)
    df["New Happiness Score"] = model.predict(X_scaled).round(2)
    df["New Happiness Label"] = df["New Happiness Score"].apply(classify_happiness)
    return df

# Ana kod
df, X, y = load_data(path)

# Veri bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model eğitimi ve değerlendirme
model, scaler = train_and_evaluate(X_train, X_test, y_train, y_test)


# Veri çerçevesini tahminler ve etiketlerle zenginleştir
df = enrich_dataframe(df,model,scaler)
df.to_csv("2019_with_regression.csv", index=False, encoding="utf-8")



#2019 verisi gerçek ve tahmin skorlarını kıyasladığım bir grafik oluşturdum.


# Modelden alınan tahminler
y_pred = model.predict(scaler.transform(X_test))

# Scatter plot: Gerçek vs Tahmin
plt.figure(figsize=(8, 6))
plt.scatter(y_test, y_pred, alpha=0.6, label='2019 Tahminleri')

# 45° referans çizgisi
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', label='Doğruluk Çizgisi')

# Etiketler ve başlık
plt.xlabel('Gerçek Mutluluk Skoru')
plt.ylabel('Tahmin Edilen Skor')
plt.title('2019: Gerçek vs Tahmin Değerleri')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("tahmin_vs_gercek_2019.png", dpi=300) 


#2018 ve 2019'daki happiness label dağılımlarını gösteren bir grafik oluşturdum.

df_2018 = pd.read_csv("2018_with_regression.csv", encoding="utf-8")

labels_2018 = df_2018["New Happiness Label"].value_counts()
labels_2019 = df["New Happiness Label"].value_counts()

labels = sorted(set(labels_2018.index).union(set(labels_2019.index)))
counts_2018 = [labels_2018.get(label, 0) for label in labels]
counts_2019 = [labels_2019.get(label, 0) for label in labels]

import numpy as np
x = np.arange(len(labels))
width = 0.35

plt.bar(x - width/2, counts_2018, width, label='2018')
plt.bar(x + width/2, counts_2019, width, label='2019')
plt.xticks(x, labels)
plt.ylabel("Ülke Sayısı")
plt.title("Mutluluk Etiketi Dağılımı: 2018 vs 2019")
plt.legend()
plt.savefig("mutluluk_etiket_dagilimi.png", dpi=300)
plt.close()




#2018 ve 2019'daki bağımsız değişken katsayılarını kıyasladığım bir grafik oluşturdum

# Model 2018
X18 = df_2018[["Social support", "Freedom to make life choices","GDP per capita","Healthy life expectancy","Generosity","Perceptions of corruption"]]
X18 = sm.add_constant(X18)
y18 = df_2018["Happiness Score"]
model18 = sm.OLS(y18, X18).fit()

# Model 2019
X19 = df[["Social support", "Freedom to make life choices","GDP per capita","Healthy life expectancy", "Generosity","Perceptions of corruption"]]
X19 = sm.add_constant(X19)
y19 = df["Happiness Score"]
model19 = sm.OLS(y19, X19).fit()

# Katsayıları al
coefs18 = model18.params.drop("const")
coefs19 = model19.params.drop("const")


df_plot = pd.DataFrame({
    "2018": coefs18,
    "2019": coefs19
})



df_plot.plot(kind="bar", figsize=(10, 6), color=["skyblue", "salmon"])
plt.title("Bağımsız Değişkenlerin Yıl Bazında Etkisi")
plt.ylabel("Regresyon Katsayısı")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("degisken_etkileri_yillar.png", dpi=300)
plt.close()




 

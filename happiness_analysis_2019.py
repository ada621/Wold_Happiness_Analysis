import pandas as pd
import statsmodels.api as sm
import numpy as np
from scipy import stats
from scipy.stats import skew

#veri temizliğini daha kolay yapabilmek,eksik değerleri doldurabilmek,ve hedef sütunları daha kolay seçebilmek için load data kullandım.
def load_data(path="2019_updated.csv"):
    df = pd.read_csv(path, encoding="utf-8")
        
        
#Country, Year, Happiness Label,Happiness Rank hariç hepsi numeric kalacak çünkü analizde datatype problem olabilir.
#year numeric yapılmadı çünkü burada eğer verileri birleştirmek istersem diye kategori oluşturmak için
#year sütunu oluşturmuştum. yani sayısal bir işlemde kullanılmayacak year colonu.
    non_numeric = ["Country", "Happiness Label", "Year","Overall rank"]
    numeric_cols = [c for c in df.columns if c not in non_numeric]
        
#eksik değerleri kontrol ettim eğer eksik değer varsa doldurmak için. 
    df_numeric = df[numeric_cols]
    print(f"Eksik değerler:\n{df_numeric.isnull().sum()}")
    
#eksik değerleri o sütunun ortalaması ile doldurdum.
    df_numeric = df_numeric.fillna(df_numeric.mean())
    return df_numeric






def descriptive_stats(df):  
   
#skewness sütunu oluşturdum ve bu sayede çarpıklık değerlerine bakıyorum.
#kurtosis sütunu oluşturdum ve basıklık değerlerine bakıyorum.
    desc_stats = df.describe()
    desc_stats.loc['skewness'] = df.skew(numeric_only=True)
    desc_stats.loc['kurtosis'] = df.kurtosis(numeric_only=True)
    
    print(desc_stats.round(3))
   
#dataframe deki tüm numeric sütunların arasındaki kolerasyonu hesaplar.Pearson kolerasyon katsayısı kullanılıyor(-1 ile +1 arası).
    correlation_matrix = df.corr()
    print("\n--- CORRELATİON ---")
    print(correlation_matrix.round(3))
 

#burada 0.7 den büyük kolerasyonlara bakmalıyız. çünkü yüksek kolerasyon olan ilşkileri görmek istiyorum.
#.abs() fonksiyonu negatif kolerasyonları da pozitif yapar. burada bunu kullandım çünkü negatif olanlarda dahil yüksek (0.7 den büyük) 
#tüm kolerasyonları görmek istiyorum.
#i+1(sadece kendinden sonraki sütunları karşılaştırır(üst üçgen tarama)) yaptım çünkü kendisiyle olan kolerasyonun bir anlamı yok.
#ayrıca i+1 ile tekrarları önlüyorum. örneğin family-economy ve econmy-family nin aynı anda print edilemsi gerek yok.
###iloc= i nci satırı ve j nci sütunu getir demek.yani satır ve sütun seçmem için.(pozisyon bazlı indexleme(integer location))
    print("\n--- Yüksek Korelasyonlar (|r| > 0.7) ---")
    high_corr = correlation_matrix.abs() > 0.7
    for i in range(len(correlation_matrix.columns)):
        for j in range(i+1, len(correlation_matrix.columns)):
            if high_corr.iloc[i, j]:
                print(f"{correlation_matrix.columns[i]} - {correlation_matrix.columns[j]}: {correlation_matrix.iloc[i, j]:.3f}")






def run_regression(df):   

#Happiness Score'u bağımlı değişen ve onun dışında kalan tüm numericleri bağımsız değişken yapmak için x ve y kullandım.
    y = df["Happiness Score"]
    X = df.drop(columns=["Happiness Score"])
    
   
#sabit terim eklemek daha gerçekçi tahmin için gereklilik.çünkü eklenmezse model,y'nin sıfırdan başladığını varsayar 
#ancak gerçekte çoğu zaman başlangıç değeri 0 olmaz.
    X = sm.add_constant(X)

   
#Regresyon Modeli Oluşturma (Robuts OLS)
#Heteroskedastisiteye çıkması sonucu Robuts OLS yapmayı tercih ettim>>heterosdastisiteyi kabul edip modeli
#ona karşı dayanıklı hale getirir.
    model = sm.OLS(y, X)
    results = model.fit(cov_type='HC3')  



         

#regresyon analizi bağımlı değişkenin, bağımsız değişkenler tarafından nasıl tahmin edileceğini modeller.
#her değişkenin etkisini ayrı ayrı gösterir ve bu etkilerin anlamlılığını test eder.(p değeri ile)
#kolerasyon analizinde ise iki değişkenin beraber nasıl değiştiğini ve ne yöne değiştiğini görürüz.regresyon analizi ise
#bağımlı değişkenin, bağımsız değişkenler yardımıyla tahmin edilmesini sağlar."
    print("REGRESSİON ANALYSİS")
    print("="*50)
    print(f"Bağımlı değişken: Happiness Score")
    print(f"Bağımsız değişkenler: {list(X.columns[1:])}")#const sütununu almamak için
   



    #Model değerlendirme(MODEL EVALUATİON)
#R-squared:modelin açıklayıcı gücünü gösterir.
#Adjusted R-squared:çoklu regresyonda daha güvenilir bir sonuç için ekledim.çünkü R-squared'ın daha gelişmiş bir versiyonu gibi.
#bağımsız değişken sayısını da hesaba katarak yalnızca anlamlı katkı yapan değişken varsa değeri artar. R-squared da ise genelde 
#anlamlı katkı adjusted R-squared gibi ön planda olmaz.

#AIC:modelin bu veriye uyumunu ölçer. karmaşık olması istenmez.
#BIC:daha detaycı bir şekilde ölçer. özellikle büyük verilerde.
#AIC ve BIC sonuçlarıma göre bu model benim verime fazlasıyla uyumlu.
#F-istatistic:bu modeldeki tüm bağımsız değişkenlerin hepsi BERABER anlamlı mı? burada tek tek p-values lara değil hepsinin ortak 
#toplu katkılarına bakıyoruz.
    print("\n--- MODEL PERFORMANCE ---")
    print(f"R-squared: {results.rsquared:.4f}")
    print(f"Adjusted R-squared: {results.rsquared_adj:.4f}")
    print(f"AIC: {results.aic:.2f}")
    print(f"BIC: {results.bic:.2f}")
    print(f"F-statistic: {results.fvalue:.2f}")
    print(f"F-statistic p-value: {results.f_pvalue:.6f}")
    return results, X, y


#Regression varsayımlarını kontrol etmemiz gerekir çünkü OLS sonucu çıkan değerler bazı koşullar altında istatistiksel
#olarak anlamlıdır.çünkü OLS modeli bazı varsayımlarda bulunarah tahmin yürütür.
def check_assumptions(model, X, y):
    
    print("REGRESYON VARSAYIM KONTROLLERI")
    print("="*50)

    residual = model.resid


    
# 1. Normallik testi (Jarque-Bera)

# OLS regression, dağılımı normal varsayar.O yüzden gerçekten normal dağılım  olup olmadığını inceledim.
#jarque-bera testini tercih ettim çünkü veri setim küçük değil ve residualların normal dağılım varsayıma özel olarak kullanılabilir.
#ayrıca çarpıklık ve basıklık odaklı olması benim projem için daha uygun bir seçenek yapıyor.
#eğer hata (residual)dağılımı normal olmazsa güvenilirlik düşer. p-value değerleri anlamsız hale gelir ve tahminler yanlı olabilir.

    jb_stat, jb_pvalue = stats.jarque_bera(residual)
    print(f"1. Normallik Testi (Jarque-Bera):")
    print(f"   Test istatistiği: {jb_stat:.4f}")
    print(f"   p-value: {jb_pvalue:.6f}")
    print(f"   Sonuç: {'Normal dağılım' if jb_pvalue > 0.05 else 'Normal dağılım değil'}")
    
#residualların sistematik olarak çarpık olup olmadığını incelemek istedim çünkü normal dağılım olmamasının bir sebebi bu olabilir.
    residual_skew = skew(residual)
    print(f"Residual Skewness: {residual_skew:.4f}")  
   

# 2. Homoskedastisite testi (Breusch-Pagan)

#OLS regression model, hata varyansının sabit olduğunu varsayar.burada hata varyansını inceledim ve sonuç olarak Heteroskedastik çıktı.
#ben de heteroskedastisite'ye uyumlu olması açısından Robust OLS tercih ettim. detayları comperation.py de yazıyor.

    from statsmodels.stats.diagnostic import het_breuschpagan
    bp_stat, bp_pvalue, _, _ = het_breuschpagan(residual, X)
    print(f"\n2. Homoskedastisite Testi (Breusch-Pagan):")
    print(f"   Test istatistiği: {bp_stat:.4f}")
    print(f"   p-value: {bp_pvalue:.6f}")
    print(f"   Sonuç: {'Homoskedastik' if bp_pvalue > 0.05 else 'Heteroskedastik'}")
   


    
# 3. Durbin-Watson testi (otokorelasyon)

#OLS otokolerasyon olmadığını,her gözlemin hatasının rastgele olduğunu varsayar.
#model, otokolerasyon olmadığını varsayar çünkü eğer otokolerasyon varsa hatalar birbirinden bağımsız değil ve bir hata öbür hatayı
#etkiliyor demektir.

# Burada yine varsayım karşılanıyor mu bunu test ettim.ancak verim time series olmadığı yani tek bir yıl içinde farklı ülkelerin 
#mutluluk scorlarını içerdiği için(mekansal) çok anlamlı olmayabilir???
    from statsmodels.stats.stattools import durbin_watson
    dw_stat = durbin_watson(residual)
    print(f"\n3. Otokorelasyon Testi (Durbin-Watson):")
    print(f"   Test istatistiği: {dw_stat:.4f}")
    print(f"   p-value: {dw_stat:.6f}")
    print(f"   Sonuç: {'Otokorelasyon yok' if 1.5 < dw_stat < 2.5 else 'Otokorelasyon var'}")






def feature_importance_analysis(model, X): 
     
# Katsayıları aldım. (sabit terim hariç)
    coefs = model.params[1:] 
    feature_names = X.columns[1:]  
    
   
    p_values = model.pvalues[1:]
    
    
    importance_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefs,
        'Abs_Coefficient': np.abs(coefs),
        'P_Value': p_values,
        'Significant': p_values < 0.05
    }).sort_values('Abs_Coefficient', ascending=False)
    
#katsayılar her değişkenin Happiness Score üzerindeki etkisinin büyüklüğünü gösterir. burada bu etkiyi print ediyoruz.
    print("DEĞİŞKEN ÖNEMİ ANALİZİ")
    print("="*50)
    print(importance_df[['Coefficient', 'P_Value', 'Significant']].round(4))


#burada en yüksek etki katsayısana sahip değişkenleri görmek için bu değişkenleri yazdırıyoruz. 
    print("\n ÖNEMLİ DEĞİŞKENLER (p < 0.05)")
    print("-"*45)
    significant_vars = importance_df[importance_df['Significant']]
    for _, row in significant_vars.iterrows():
        effect = "pozitif" if row['Coefficient'] > 0 else "negatif"
        print(f"{row['Feature']}: {row['Coefficient']:.4f} ({effect} etki)")
        


#%95 güven aralığı analizi
# Katsayıların güven aralıklarını gösterir.
#perceptions of corruoption ve generosity değerlerinin güven aralıklarını görmek istedim çünkü katsayı analizinde istatistisel
# olarak anlamlı çıkmadılar.
    conf_int = model.conf_int()
    print("GÜVEN ARALIKLARI (95%):")
    print(conf_int.round(4))



# Tek seferde temizlenmiş veriyi yükle
df2019 = load_data("2019_updated.csv")
descriptive_stats(df2019)   
model, X, y = run_regression(df2019)
check_assumptions(model, X, y)
feature_importance_analysis(model, X)
   
   
df2019.to_csv("2019_cleaned.csv", index=False, encoding="utf-8")
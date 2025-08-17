import pandas as pd
import statsmodels.api as sm
import numpy as np
from scipy import stats


#veri temizliğini daha kolay yapabilmek,eksik değerleri doldurabilmek,ve hedef sütunları daha kolay seçebilmek için load data kullandım.
def load_data(path="2018_updated.csv"):
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
    # Temel istatistikler
#skewness sütunu oluşturdum ve bu sayede çarpıklık değerlerine bakıyorum.
#kurtosis sütunu oluşturdum ve basıklık değerlerine bakıyorum.
    desc_stats = df.describe()
    desc_stats.loc['skewness'] = df.skew(numeric_only=True)
    desc_stats.loc['kurtosis'] = df.kurtosis(numeric_only=True)
    
    print(desc_stats.round(7))
   
#dataframe deki tüm numeric sütunların arasındaki kolerasyonu hesaplar.Pearson kolerasyon katsayısı kullanılıyor(-1 ile +1 arası).
    correlation_matrix = df.corr()
    print("\n--- CORRELATİON ---")
    print(correlation_matrix.round(7))
 

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
#(y her zaman bağımlı değişken olur.Genel standart.)
    y = df["Happiness Score"]
    X = df.drop(columns=["Happiness Score"])
    
    # Sabit terim ekle
#sabit terim eklemek daha gerçekçi tahmin için gereklilik.çünkü eklenmezse model,y'nin sıfırdan başladığını varsayar 
#ancak gerçekte çoğu zaman başlangıç değeri 0 olmaz.
    X = sm.add_constant(X)

   
    # OLS modeli
#OLS regresyon,yani Ordinary Least Squares(En Küçük Kareler)regresyonu,istatistikte en sık kullanılan doğrusal regresyon yöntemi.
#Temel amacı, bir bağımlı değişken(örneğin mutluluk skoru)ile bir veya birden fazla bağımsız değişken
#(örneğin gelir, sosyal destek, beklenen yaşam süresi) arasındaki ilişkiyi matematiksel olarak modeller.
#regresyon modelleri arasından OLS i seçtim çünkü başlangıç seviyesi için uygulaması,yorumlaması kolay.Ayrıca varsayım kontrollerini 
#öğrenme imkanı yaratıyor.

#statsmodel(sm)istatistiksel modelleme kütüphanesi.Regresyon ve zaman serisi yöntemlerini içerir.Ben burada regresyon için kullandım.
    model = sm.OLS(y, X).fit()
    

#Regresyon modeli oluşturma(MODEL BUILDING)

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



#f istatistic:benim analiz sounucuma göre istatistiksel olarak beaber anlamlılar.
#F-istatistic p-value değerine bakacak olursak bu analiz sonucunda bağımsız değişkenlerin topluca anlamlı olduğunu görüyoruz.
#Rastgele bir etki değil istatistiksel bir anlamlılık var.Bu da modelin rastege oluşmadığını,gerçekten mutluluk skorunu açıklamakta 
#başarılı olduğunu gösteriyor.

    print("\n--- MODEL PERFORMANCE ---")
    print(f"R-squared: {model.rsquared:.4f}")
    print(f"Adjusted R-squared: {model.rsquared_adj:.4f}")
    print(f"AIC: {model.aic:.2f}")
    print(f"BIC: {model.bic:.2f}")
    print(f"F-statistic: {model.fvalue:.2f}")
    print(f"F-statistic p-value: {model.f_pvalue:.6f}")
    return model, X, y


#Regression varsayımlarını kontrol etmemiz gerekir çünkü OLS sonucu çıkan değerler bazı koşullar altında istatistiksel
#olarak anlamlıdır.çünkü OLS modeli bazı varsayımlarda bulunarah tahmin yürütür.
def check_assumptions(model, X, y):
    
    print("REGRESYON VARSAYIM KONTROLLERI")
    print("="*50)

    residual = model.resid
    
# 1. Normallik testi (Jarque-Bera)

#jarque-bera testini tercih ettim çünkü veri setim küçük değil ve residualların normal dağılım varsayıma özel olarak kullanılabilir.
#ayrıca çarpıklık ve basıklık odaklı olması benim projem için daha uygun bir seçenek yapıyor.
#eğer hata (residual)dağılımı normal olmazsa güvenilirlik düşer. p-value değerleri anlamsız hale gelir ve tahminler yanlı olabilir.
# OLS regression, dağılımı normal varsayar.O yüzden gerçekten normal dağılım  olup olmadığını inceledim.
#burada p-value>0.05 olmalı normal bir dağılım için. ancak benim analizimde bu değer düşük çıktı(p:0.03) böyle bir durum 
#birkaç sebepten kaynaklanıyor olabilir.Resudualler sistematik olarak çarpıksa uç değer yaratıyor olabilir.gereksiz değişkenler hata
#terimlerinde gereksiz bir varyans yaratmış olabilir(ancak Adjusted R-squared anlamlı çıktı ve manuel kontrol ettiğimde anlamsız bir
#bağımlı değişken göremedim)>>>>>!!Ancak corruption değerinin kurtosis ve skewness değerlerini analiz ettiğimde hem basıklığın hem de
#çarpıklığın normalin üstünde olduğunu görüyorum.Muhtemelen buradaki değerler sebebiyle resudusal normalty değerleri anlamlı çıkmıyor.

    jb_stat, jb_pvalue = stats.jarque_bera(residual)
    print(f"1. Normallik Testi (Jarque-Bera):")
    print(f"   Test istatistiği: {jb_stat:.4f}")
    print(f"   p-value: {jb_pvalue:.6f}")
    print(f"   Sonuç: {'Normal dağılım' if jb_pvalue > 0.05 else 'Normal dağılım değil'}")
    
   
   
# 2. Homoskedastisite testi (Breusch-Pagan)

#modelim lineer(yani x ye y değerlerim arasında doğrusal ilişki var(katsayılarım sabit))olduğu için breusch-pagan testini tercih ettim.
#OLG Regresyon Modelinin bir diğer varsayımı hataların sabit varyanslı olduğudur.Bu yüzden sonuçların güveniliriliği için varyans
#dağılımını kontrol ettim.
# Regresyon analizinde modelin yaptığı tahmin ile gerçek değer arasındaki fark residual(hata)dır. 
#bu hataların büyüklüğünün dağılımı ise bana hata varyansını verir. burada bu varyansı inceledim ve sonuç olarak Homoskedastik çıktı 
#yani residual varyansım sabit yani bu da modelimin güvenilir olduğunu gösteriyor.
    from statsmodels.stats.diagnostic import het_breuschpagan
    bp_stat, bp_pvalue, _, _ = het_breuschpagan(residual, X)
    print(f"\n2. Homoskedastisite Testi (Breusch-Pagan):")
    print(f"   Test istatistiği: {bp_stat:.4f}")
    print(f"   p-value: {bp_pvalue:.6f}")
    print(f"   Sonuç: {'Homoskedastik' if bp_pvalue > 0.05 else 'Heteroskedastik'}")
   
    
# 3. Durbin-Watson testi (otokorelasyon)

#normalde otokolerasyon olmamalı çünkü eğer varsa hatalar birbirinden bağımsız değil ve bir hata öbür hatayı etkiliyor demektir.
#OLS otokolerasyon olmadığını,her gözlemin hatasının rastgele olduğunu varsayar. Burada yine varsayım karşılanıyor mu bunu test ettim.
#ancak verim time series olmadığı yani tek bir yıl içinde farklı ülkelerin mutluluk scorlarını içerdiği için(mekansal) ve daga önce regresyon
#yapılmadığı için çok da elzem olmayabilir??
    from statsmodels.stats.stattools import durbin_watson
    dw_stat = durbin_watson(residual)
    print(f"\n3. Otokorelasyon Testi (Durbin-Watson):")
    print(f"   Test istatistiği: {dw_stat:.4f}")
    print(f"   p-value: {dw_stat:.6f}")
    print(f"   Sonuç: {'Otokorelasyon yok' if 1.5 < dw_stat < 2.5 else 'Otokorelasyon var'}")






def feature_importance_analysis(model, X):  #X: bağımsız değişkenlerim
     
    # Katsayıları al (sabit terim hariç)
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
#benim analizim sonucunda social support'un Happiness score üzerintedki etki katsayısı 1.0098 >>>>>bu demek oluyor ki social
#support 1 birim artarsa Happiness Score 1.0098 puan artar.
#en yüksek etki katsayısını freedom ile(1.3687) gözlemlerken en düşük etki katsayısını generosity ile(0.5799) ile gözlemliyoruz.
#analiz sonucunda tüm katsayıların pozitif yönde olduğunu görüyoruz.
#ancak p-value değerlerine baktığımızda corruption(p:0.1996) ve generosity(p:0.2219) değerlerinin 0.05'in üzerinde olduğu gözüküyor.
#bu da bu değişkenin etki katsayısının rastgele ve anlamsız olabileceğini düşündürtebilir.

    print("DEĞİŞKEN ÖNEMİ ANALİZİ")
    print("="*50)
    print(importance_df[[ 'Coefficient', 'P_Value', 'Significant']].round(4))


#burada en yüksek etki katsayısana sahip değişkenleri görmek için bu değişkenleri yazdırıyoruz. 
# en önömli değişkenlerFreedom to make life choices: 1.3687 (pozitif etki)---GDP per capita: 1.0942 (pozitif etki)
#Social support: 1.0098 (pozitif etki)---Healthy life expectancy: 0.8150 (pozitif etki) olarak çıkıyor.
    print("\n ÖNEMLİ DEĞİŞKENLER (p < 0.05)")
    print("-"*45)
    significant_vars = importance_df[importance_df['Significant']]
    for _, row in significant_vars.iterrows():
        effect = "pozitif" if row['Coefficient'] > 0 else "negatif"
        print(f"{row['Feature']}: {row['Coefficient']:.4f} ({effect} etki)")
        


#%95 güven aralığı analizi
# Katsayıların güven aralıklarını gösterir

#bunu yaptım çünkü katsayısıları analiz ettiğim zaman generosity ve corruption değişkenlerinin etkisi istatistiksel
#olarak anlamlı çıkmadı. bende daha derinlemesine analiz edip gerçekten anlamsız olabilir mi? sorusunu cevaplamak istedim.
#güven aralığı sonuçlarına göre bu iki değişken anlamlı değil.çünkü carripution([-0.3641, 1.7289]) ve Generosity([-0.3542, 1.5140])
#değişkenlerinin güven aralığı sıfırıda içeriyor. %95 güven aralığını incelerken değerlerin sıfır içermemesini bekleriz.bu bize 
#o değişkenin istatistiksel olarak anlamlı olduğu sonuucunu verir.
    conf_int = model.conf_int()
    print("GÜVEN ARALIKLARI (95%):")
    print(conf_int.round(4))



    # Tek seferde temizlenmiş veriyi yükle
df2018 = load_data("2018_updated.csv")
descriptive_stats(df2018)    
model, X, y = run_regression(df2018)
check_assumptions(model, X, y)
feature_importance_analysis(model, X)
 

df2018.to_csv("2018_cleaned.csv", index=False, encoding="utf-8")
'''

                         #--------------- ÇALIŞMA AMACI--------------------#                    
-------------------------------------------------------------------------------------------------------------------------------------
bu çalışmada Wolrd Happiness Data 2018 ve 2019 verilerini hem kendi içlerinde incelemek hem de birbirleriyle olan farklılık ve benzer
liklerini-değişimi- analiz etmek istedim.

bağımlı değişken olarak--> Happiness Score
bağımsız değişkenler olarak --> GDP per capita, social support, healty life expectancy, freedom to make a life choices, generosity
ve perceptions of corruption değişkenlerini tercih ettim.
data set'de bulunan happiness(overall) rank, county, happiness label, year değişkenlerini dahil etmedim.


bu çalışma için modüler bir yapı kurdum. hangi modeli seçmem gerektiğine karar vermek için OLS,Robust OLS,LOG OLS ve WLS modellerini
karşılaştırdım. 2018 veri analizim için OLS, 2019 veri analizim için Robust OLS modelini tercih ettim.(detayları aşağıda)

main dosyasında verilerime sütun ekledim.
analiz kısmında ise ilk önce 2018 ve 2019 verilerinin kolerasyon analizini,temel istatistik analizini,regresyon model analizini ve 
regresyon varsayım analizini farklı file'larda (happiness_analysis_2018.py, happiness_analysis_2019.py)yaptım.

regresyon tahminlerini regresyon_2018.py ve regresyon_2019.py dosyalarında.
happiness_graph.py dosyasında ise hem 2018 hem 2019 analizinin grafiklerini oluşturdum.Bu grafik görselleri figures dosyasında
bulunmakta.





                             #--------------MODEL SEÇİMİ----------------#
-------------------------------------------------------------------------------------------------------------------------------------
2018 modelinde OLS modeli uyguladım çünkü heteroskedasticity yoktu ve OLS modeli benim verim için uygundu. basit ve anlaşılır model
olduğu için tercih ettim.
Ancak 2019 verisinde heteroskedasticity değerim oldukça yüksek çıktı..Bu sebeple OLS,Robust OLS,WLS ve Log OLS modellerini ayrı bir
file da 2019 verisinin analizi için kıyasladım.

Log OLS,Robust OLS ve OLS modellerinin squared değerleri neredeyse aynı. AIC ve BIC değerleri farklılık gösteriyor.Onda da Robust OLS
ve OLS nin AIC ve BIC değerleri aynı.>>>çünkü Robust OLS bir değişiklik yaratmıyor yalnızca heteroskedasticity e karşı daha güvenli 
hale getiriyor modeli..


 
Robust OLS ile modelim heteroskedastisiteye uyum sağlıyor ancak heteroskedastisiteyi yok etmiyor.bu yüzden modelin tahmin yeteneği
zarar görebilir..Çünkü uç değerler modele hala zarar verebilir ve robust OLS bu uç değerleri görmzden gelmez.Ancak onların etkisini 
daha az belirleyici hale getirir. Tahmin ararlıkları hala yanıltıcı olabilir.Özellikle genelleme yapılmak istenirse bu önemli bir
problem olabilir.


WLS ise en yüksek squared değerini veriyor(0.99) ve AIC(53.16) ile BIC(74.51) değerleri en düşük
olan bu.>>>ki bu aşırı uyum(overfitting) problemi yaratabilir>>uç değerler de var ve bu overfittingi tetikleyebilir.

Log OLS ise en düşük AIC ve BIC değerini veriyor bu da model karmaşıklığa karşı en iyi dengiyi kuruyor anlamına gelir>>>

daha sonra daha detaylı bir kıyas için güven aralıklarını kıyasladım.
yaptığım kıyas sonucunda -Robust OLS- modelini tercih etmeye karar verdim çünkü:,
çünkü OLS heteroskedastisiteye uyumlu değil,
WLS modeli uç değerlere hassas ve benim uç değerlerim bazı değişkenlerde görülüyor..
Log OLS ise yorumlamamı zorlaştıracağı için (çünkü benim çalışmam tahmin içeriyor ama aynı zamanda yorumlamaya dayalı) tercih etmedim.
Robust OLS ile hem heteroskedastisiteye modelim uyum sağlıyor hem de uç değerlerimin etkisini azaltıyor.





-----KORELASYON ANALİZİ,REGRESYON VARSAYIM ANALİZİ,REGRESYON MODEL ANALİZİ VE TEMEL İSTATİSTİK YORUMLAMA------#
-------------------------------------------------------------------------------------------------------------------------------------
TEMEL İSTATİSTİKLER ile analiz sonucu gözlemlediklerim----->

social support değişkenim sola çarpık 2019(-1.135) ve 2018(-1.081) yani pozitif değerler ağırlıkta.kurtosis yani basıklık değeri ise
2019(1.229)ve 2018 (1.171) >>>bu da uç değerler olduğunu düşündürüyor.

GDP per capita değişkenim hafif sola çarpık 2019(-0.385)ve 2018(-0.201) ancak dengesizlik yaratacak kadar büyük bir çarpıklık değil.
kurtosis değeri ise 2019(-0.770) ve 2018 (-0.335)>>> dağılım basık yani uç değerler az denebilir.

Perceptions of corruption değişkenim sağa çarpık 2019(1.650) ve 2018(1.684).kurtosis değeri 2019(2.417)ve 2018 (2.541) >>>Bu demek 
oluyor ki belirgin çarpıklık ve fazlasıyla uç değer var bu değişkende.

Freedom to make a life choices değişekenim sola çarpık 2019(-0.686) ve 2018 (-0.788).kurtosis değeri 2019(-0.069) ve 2018(-0.011)
genel olarak dağılımın hafif çarpık olduğunu ve uç değer riskinin çok düşük olduğunu söyleyebiliriz.

Generosity değişkenim sağa çarpık 2019(0.746) ve 2018 (0.867).kurtosis değeri 2019(1.173) ve 2018(1.435) >>> çarpıklık çok fazla
olmasa da var(1 değerine yakın.) ve veride bazı uç değerler olduğu söylenebilir ancak çok fazla uç değer yok.

Bağımlı değişkenim olan Happiness Score değişekenimin çarpıklığı 2019(0.011) ve 2018(0.015).kurtosis değeri 2019(-0.608) ve
2018(-0.710) >>> yani çarpıklık yok denebilir ve uç değer riski çok düşük denebilir.






KORELASYON ANALİZİNDE gözlemlediklerim------>
bazı dikkat çeken zayıf ve güçlü ilişler var..
zayıf ilişkiler --->
Happiness Score ve Generosity arasındaki korelasyon 2019 (0.076) ve 2018 (0.135). bu neredeyse ilişki yok denecek kadar az bir değer.
Cömertliğin(generosity) doğrudan mutluluk scoruna bir etkisinin olmadığını söyleyebiliriz.

Perseptions sof corruption ve Happines score değişkenleri arasında korelasyon 2019(0.386)ve 2018(0.403)(r<0.70).zayıf-orta bir ilişki
olduğu söylenebilir.

güçlü ilişkiler ----->
Happiness Score ve GDP per capita değişkenleri arasındaki korelasyon 2019(0.794) ve 2018 (0.802) (r>0.70) yani ekonomik refah ve 
mutluluk scoru arasında doğrudan pozitif bir ilişki olduğu söylenebilir.

Happines Score ve Social support değişkenleri arasındaki korelasyon 2019(0.777) ve 2018 (0.745)(r>0.70) yani sosyal destek ve mutluluk
scoru arasında doğrudan pozitif bir ilişki olduğu söylenebilir.

Happines Score ve Healty life expectancy değişkenleri arasındaki korelasyon 2019(0.780) ve 2018(0.775)(r>0.70) yaşam süresi ve 
mutluluk scoru arasında doğrudan pozitif bir ilişki olduğu söylenebilir.

daha ortalama ilişker ---->,
Freedom to make a life choices ve Happines score değişkenleri arasında korelasyon 2019(0.567) ve 2018 (0.544)(r<0.70)-->mutlutluluk 
skoru ile orta seviye bir ilişkisi olduğu söylenebilir.


ancak kolerasyon yalnızca değişkenler arası ilişkileri gösterir-->bir nedensel çıkarım yapamayız.



REGRESYON MODEL ANALİZİ sonuçları ----->

2019 R-squared sonucunu(0.7792)ve 2018(0.7892) incelediğimizde, model değişkenlerin %77.9'unu açıklıyor.Yani güçlü bir doğrusal 
ilişki olduğu söylenebilir.
2019 Adjusted R-squared(0.7703) ve 2018(0.7807) değerine baktığımızda ise eklenen değişkenlerin anlamlı olduğunu söyleyebiliriz.>>
Model yeterince açıklayıcı ve de aşırı değişken kullanımı olmadığı gözüküyor.

2019 AIC(253.53) ve BIC(274.88)ile 2018 AIC(248.08) ve BIC(269.43) sonuçlarını incelediğimizde değerlerin yüksek olmadığını görüyoruz.
Yani modelin verim ile uyumlu olduğunu söyleyebilirim.>>>(AIC ve BIC değerleri WLS hariç diğer tüm modellerde hemen hemen aynıydı
bu sebeple yüksek olmadığını söyleyebilirim.)<<<

2019 F-statistic (87.62)ve 2018(92.95) değerlerine göre regresyon genel olarak anlamlı.

2019 ve 2018 F-statistic p-value değerine bakarak da (0.00..) bağımsız değişkenlerin toplam olarak modele katkı sağladığı söylenebilir.




 REGRESYON MODEL VARSAYIM ANALİZİnde gözlemlenen sonuçlar ---->

----------Normalite Testi(Jarque,Bera)-------------
bu testi neden tercih ettiğim happiness_analysis_2019.py file'nda yazıyor.

normallik testi sonucunda normal bir dağılım için p-value>0.05 olması beklenir ki varsayım (normal dağılım)sağlabilsin.
ancak benim analizimde hem 2019 hem de 2018 yıllarında bu değer düşük çıktı(p=0.03)
böyle bir durum birkaç sebepten kaynaklanıyor olabilir.----->Resudualler sistematik olarak çarpıksa uç değer yaratıyor olabilir.

residualların sistematik olarak çarpık olup olmadığını analiz ettim ve -resudual skewness:-0.4983- değerine ulaştım.>>> residualların
dağılımının neredeyse simetrik olduğu söylenebilir.

gereksiz değişkenler hata terimlerinde gereksiz bir varyans yaratmış olabilir.
ancak Adjusted R-squared anlamlı çıktı ve manuel kontrol ettiğimde anlamsız bir bağımlı değişken göremedim.
Ancak perceptions of corruption değerinin kurtosis ve skewness değerlerini incelediğimde hem basıklığın hem de çarpıklığın normalin 
oldukça üstünde olduğunu görüyorum.
Bu değişken sebebiyle resudusal normalty değerleri anlamlı çıkmıyor olabilir..




---------Homoskedastisite testi (Breusch-Pagan)------------
burada yapılan test sonucunda 2019(test istatistiği=7.9707 ve p-value=0.0185) çıktı. 
burada p-value değerinin >0.05'den olması beklenir ki varsayım (homoskedastisite) geçerli olabilsin.
Ancak benim 2019 yılındaki değerim bunun oldukça altında.>>>demek oluyor ki residual variance sabit değil ve farklı değerlerde
değişikilik gösteriyor.Bu sebeple güven aralıkları yanıltıcı olabilir,yanlış çıkarımlara sebep olabilir,standat hata tahminlerinin
bozulmasına sebep olabilir.


2018 yılındaki sonuçlara göre ise(test istatistiği=10.5516 ve p-value=0.103)>>>residual variance sabit ve farklı değerlerde değişikilik
göstermiyor.>>>varsayım karşılanıyor.


------Durbin-Watson testi (otokorelasyon)-------------

2019 yılı verisinin otokolerasyon testi sonucunda (test istatistiği=1.6484, p-value=1.6483) ve 2018 (test istatistiği=1.6453,
p-value=1.6452)çıktı.
p-value değeri 0.05'den büyük bu sebeple varsayım(otokolerasyon olmaması)geçerlilik sağlar.>>>her iki yılda da residualların 
birbirinden bağımsız olduğunu ve residualların birbirilerini etkilemediklerini söyleyebiliriz.





     # ----------------DEĞİŞKEN ÖNEMİ ANALİZİ---------------------#
-----------------------------------------------------------------------------------------------------------------------------------
Değişkenlerin katsayı büyüklüklerini incelediğimde en güçlü anlamlı etkiden en güçsüz etkiye göre şu şekilde sıralanabilir:
2019 Freedom to make a life choices(coefficient=1.4546, p-value=0.00)ve 2018(coefficient=1.3687, p-value=0.00) >>>hayat kontrol 
algısı mutluluk scorunda kilit bir etkiye sahip.

2019 social support(coefficient=1.1242, p-value=0.00) ve 2018 (coefs=1.0098, p-value=0.000)>>>sosyal bağların mutluluk skorunu 
açıklamakta oldukça oldukça güçlü olduğu söylenebilir.

2019 healthy life expectancy(coefficient=1.0781, p-value=0.0029)ve 2018(coefficient=1.8150, p-value=0.0029)>>>sağlıklı yaşam beklentisi
mutluluk skoru üzerinde doğrudan bir etkisi olduğu söylenebilir.

2019 GDP per capita(coefficient=0.7754, p-value=0.0006)ve 2018 (coefficient=0.0942, p-value=0.000)>>>2018'de ekonomik refah etkili ancak
2019 yılında refah seviyesinin 2018 yılına göre çok daha etkili olduğunu söyleyebiliriz.
2019 perceptions of corruption(coefficient=0.9723, p-value=0.1813)ve 2018 (coefficient=0.6824, p-value=0.1996)>>>katsayı değeri 
sebebiyle anlamlı gibi gözüksede p-value değeri nedeniyle istatistiksel olarak anlamlı bir etkisi yok.

2019 generosity(coefficient=0.4898, p-value=0.4268)ve 2018(coefficient=0.5799, p-value=0.2219)>>>hem katkısı yüksek değil hem de
p-value değeri sebebiyle istatistiksel olarak çok da anlamlı bir değişken değil.

freedom,social support ve healty life expectancy değişkenlerinin etki gücünün güçlü poztif;GDP per capita değişkeninin etki gücünün 
ise 2018 verisinde pozitif,2019'da güçlü pozitif olduğunu söyleyebiliriz.




                 #--------------------GÜVEN ARALIĞI yorumlama------------------------#
%95 güven aralığını incelerken değerlerin sıfır içermemesini bekleriz.bu bize o değişkenin istatistiksel olarak anlamlı olduğu 
sonucunu verir.
güven aralığı sonuçlarına göre bu iki değişken (Generosity ve perceptions of corruption)anlamlı değil.
çünkü 2019 verisi carripution([-0.4531, 2.3977]) ve Generosity([-0.7183, 1.6978])ve 2018 verisi carripution([-0.3641, 1.7289]) 
Generosity([-0.3542, 1.5140]) değişkenlerinin güven aralığı sıfırıda içeriyor.
diğer değişkenler 0 değeri içermediği için güven aralığı bakımından da bir sıkıntı yaratmıyor.




             #------2018 ve 2019 VERİLERİ REGRESYON KIYASLAMASI-------#
AIC-BIC,R-squared,Adjusted R-squared,F-statistic ve F-statictic p-value değerleri neredeyse aynı.
her iki yılda da varsayım kontrollerindeki normallik testi sonucunda dağılımların normal olmadığı gözlendi.
her iki yılda da varsayım kontrollerindeki otokolerasyon testi sonucunda otokolerasyon bulunmadı.
2018 verisi homoskedastik çıkarken 2019 verisi Heteroskedastik... Yani 2019 verisinin hata varyansı sabit değil.Bu sebeple 2018
regresyon modelinde OLS;2019 analizinde ise Robust OLS kullandım.
güven aralığı sonuçları da benzer.

her ikisinde de generosity ve corruption değişkenleri etki katyasını ve güven aralığı bakımından istatistiksel olarak anlamsız. 
Ancak GDP per capita değişkeninin 2018 verisinde 2019 verisine kıyasla happiness score üzerinde daha fazla etkisinin 
olduğunu söyleyebiliriz.




           #---------------REGRESYON TAHMİNİ YORUMLAMA--------------#
2018 regresyon tahmini:
RMSE:0.56 ve R-squared:0.69-->buna göre model, verinin %69'unu açıklayabiliyor ve 5.6 hata aralığı da oldukça düşük.Modelin veriyi 
istatistiksel olarak iyi bir seviyede tahmin ettiği söylenebilir.
Modelin verdiği tahminler 3.49 ile 6.97 arasında değişiyor — yani bazı ülkeler oldukça mutsuz, bazıları ise daha mutlu görünüyor. 


Genel olarak regresyon öncesi happiness score değerleri ve regresyon sonrası new happiness score değerleri kıyaslandığı zaman 
en yüksek skora sahip ülkelerde dahi mutluluk skorunun düştüğünü ve hatta happiness label'inin değiştiğini gözlemliyoruz.
örneğin--->United Kingdom--(happines score=7190, happiness label=hight)-(new happiness score=6290,new happiness label=above average)
costa rica--(happiness score=7072, happiness label=hight)-(new happiness score=6210, happiness label=above average)gibi.

ancak kimi ülkelerde bu tam tersi yönde olabiliyor-yani happiness score ve happiness label'de bir artış görülebiliyor.
örneğin-->Qatar--(happiness score=6374, happiness label=above average)-(new happiness score=6660, new happiness label=hight)
singapore--(happiness score=6343, happiness label=above average)-(new happiness score=7080,new happines label=hight) gibi.

Bunlar bize şu ipuçlarını veriyor:
Düşük skorlar (örneğin 3.49, 3.93)-->Bu ülkeler muhtemelen daha düşük ekonomik refaha, özgürlük seviyesine ya da sosyal desteğe 
sahip diyebiliriz.
Yüksek skorlar (örneğin 6.97, 6.71)-->Tahminlere göre bu ülkelerde bireylerin yaşam memnuniyeti yüksek.
GDP per capita yani gelir düzeyinin de belirli bir noktaya kadar daha yüksek olmasını bekleyebiliriz.Ancak bu değişkenin bağımlı
değişken üzerindeki etkisi fazla yüksek olmadığı için düşük ve yüksek happiness score alan ülkeler arasında bu değişken skoru
açısından ciddi bir farklılık beklenmeyebilir.
freedom to make a life choice değişkeninin anlamlı olarak daha yüksek olmasını da bekleyebiliriz.Çünkü bu değişken happiness 
score üzerinde en yüksek etkiye sahip değişken.


Modelin verdiği sonuçlara göre bazı ülkelerde mutluluk seviyesi beklenenden düşük çıkmıştır, bu da yapısal eşitsizlikler veya sosyal 
desteğin yetersizliğiyle açıklanabilir.
6’nın üzerindeki tahminler, güçlü ekonomik göstergeler ve toplumsal refahın olumlu etkilerini yansıtmaktadır.
RMSE değeriyle birlikte yorumlandığında, tahminlerdeki sapmaların çok büyük olmadığı; dolayısıyla genel eğilimi doğru yansıttığı
söylenebilir.


2019 regresyon tahmini:
RMSE:0.64 ve R-squared:0.60-->model, verinin %60'ını açıklayabiliyor ve 0.64 hata aralığı da  model performansının yeterli olduğu 
söylenebilir.

2018 ile benxzer bir eğilim var. puanlar genel olarak düşmüş durumda.Ancak yine de aynı değişimleri görmüyoruz.. örneğin--->
united kingdom 2018 regresyon analizi sonucu etiletleme hight'dan above average'a gerilerken, 2019 verisinde hem happiness label hem 
de new happiness label'de hight etiketine sahip.

happiness label değişimi her zaman yaşanmasada bazı ülkelerde
bu değişim yaşanmış.örneğin--->
costa rica-- 2018 regresyon sonucu oluğu gibi etiket hight'dan above average'a düşmüş.
Qatar--2018 regresyon sonucunda olduğu gibi etiket above average'dan hight'a yükselmiş.




                      #----------------GRAFİK YORUMLAMA-----------------#
MUTLULUK ETİKET DAĞILIMI bar grafiğinde above average etiketi 2018 yılına kıyasla 2019 yılında artış göstermiş. Average ve Low
etiketlerinde 2019 yılında bir miktar düşüş görülüyorken very low etiketi 2019 da küçük bir artış göstermiş. Hight etiketinde ise 
bir fark göremiyoruz.
bunlardan yola çıkarak etiketlerde 2019'da daha uçlara doğru kayma olmuş denebilir. çünkü average değeri düşerken above average ve
very low etiketlerinde artış olmuş.Ancak hight etiketinde bir değişim olmaması bu kaymanın çok şiddetli olmadığını gösteriyor olabilir. 
bu kaymanın birkaç sebei olabilir.--->
GDP per capita değişkeninin,bağımlı değişken üzerinde 2018 yılında anlamlı olarak daha güçlü bir pozitif etki oluşturduğunu bulmuştuk.
GDP per capita değişkenindeki bu etki düşüşü etiket değişimini etkilemiş olabilir.

bir diğer etiket değişimini etkiyecen faktör bağımsız değişkenlerin kombinasyonu olabilir.---> örneğin freedom to make life choices
değişkeni en güçlü etkisi bulunan değişken olmasına rağmen;United Kingdom 2018 ve 2019 verilerini kıyasladığımızda frredom değişkeninin 
2019 yılında daha düşük olduğunu ancak GDP per capita,social support ve healthy life expectancy değişken puanlarında artış olduğunu
görüyoruz.-->bu 2018'deki etiket farklılığını ve 2019'etiketin değişememesini açıklıyor olabilir.



DEĞİŞKEN ETKİLERİ GRAFİĞİni incelediğimizde:
social support, freedom to make life choices, healthy life expectancy, perseption of corruption değişkenlerinin 2019 yılında etkisi
artmış,GDP per capita ve genorosity değişkenlerinin etkisi 2019 yılında düşmüş. bu değişimler genel olarak +-0.2 aralığında. 
ancak perseptions of corruption ve genorosity değişkenlerinin etki gücü oldukça zayıf olduğu için bu değişkenlerin doğrudan değilde 
dolaylı olarak etkisinden söz edilebilir. 

Tüm bu sonuçlardan yola çıkarak mutluluk skorunda, yaşam özgürlüğünün çok önemli ve kilit etkisi olduğunu ancak aynı zamanda sosyal
desteğin--bu sebeple insanlar arası ilişkisel bağların--, ve bununla hemen hemen aynı seviyede etkisi olan gelir dağılımı ve iyi hayat
beklentisinin en etkili ve öenmsenmesi gereken faktörler olduğu söylenebilir.

generocity ve social support değişkenlerinin her ikisi de sosyal ilişkilerle ilgiliyken generocity değişkeninin etki gücünün oldukça
az olmasının birkaç sebebi olabilir-->
generocity başkalarına yardımda bulunmayı kapsarken social support daha çok yardım alma ile ilgilidir. yani kişilerin zor durumlarda 
ve ihtiyaç anlarında aldıkları desteği kapsar.

diğer bir öenmli olabilecek farklılık ise generosity daha çok bizim sosyal çevremiz ile sınırlı sayılabilirken, social support gerek 
aile, arkadaş gibi bireysel çevremizden gerekse kurum ve kuruluşlar gibi daha yapılandırılmış yerlerden sağlanabilir. bu sebeple alınan
desteğin boyutu ve kişilerde yarattığı etkide farklılıklar görülebilir.










'''

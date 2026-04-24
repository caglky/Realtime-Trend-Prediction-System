## Notes
# API 
Bir sitenin ya da servisin veriyi düzenli şekilde vermesi demek
Site HTML sayfası yerine çoğu zaman JSON formatında veri döndürür
İşleyiş:
- İstek atarsın
- Sunucu cevap verir
- Cevap içindeki veriyi pythonda kullanırız 

* Kavramlar 
1) Request => gönderilen istek
2) Response => gelen cevap
3) Endpoint =>Istek atılan URL
4) JSON => API'ların en sık döndüğü veri biçimi, python'da sözlük/list gibi kullanırız
5) API Key => Bazı servisler kim old. belli olsun diye senden "key" isterler, ücretsiz hesap açarsın, key verir, request'e ekleyerek kullanırsın 

* Python'da veri çekmenin en kolay yolu:
```bash 
import requests
```
Örnek:
```bash
import requests
response = requests.get(url) //GET isteği atar
print(response.status_code) //başarılı mı kontrol eder
print(response.text) //ham cevabı görür
```

* API için temel yöntemler
- GET => veri almak için
- POST => veri göndermek için
- PUT/PATCH => veri güncellemek için
- DELETE => veri silmek için

# RealTime Data
Sistem:
- Her 1 dk
- Her 5 dk
- Her 10 dk
veriyi yeniden çeker

Buna genelde "polling (scheduled fetch)" denir

# Trend verisine nasıl bakılır 
1) Frekans => Kelime kaç kez geçti 
2) Growth Rate => Düne göre ne kadar arttı
3) Kaynak Çeşitliliği => Aynı kelime farklı kaynaklarda da geçiyor mu 
4) Zaman Yakınlılığı => Kelime son 1 saat içinde mi patladı?

# Google Trends verisi nasıl çekiliyor?
```bash 
from pytrends.request import TrendReq
pytrends = TrendReq()
trends = pytrends.trending_searches (pn = "turkey")
```

TrendReq() => bağlantı kurar 
trending_searches => populer aramaları alır 
pn = "" => bölgeyi seçer 

# Web scraping nedir, API'dan farkı ne?
API => veriyi düzenli verir
Web Scraping => Site API vermiyorsa, web sayfasının HTML sitesinden veri çekersin
Python'da genelde "request" ve "BeautifulSoup" kullanılır .
```bash 
import request 
from bs4 import BeautifulSoup
url = "https://www.hurriyet.com.tr"
response = requests.get(url)
soup = BeautifulSoup(response.test, "html.parser")
titles = [t.textfortinsoup.find_all("h3")]
```

# NewsAPI
Haberleri programla çekmeni sağlayan bi servis 
Farklı kaynaklardan haberleri toplar ve sana verir

NewsApı ne yapar? 
- Kaynaklardan veri toplar (aggregation)
  Sürekli haber siteleri tarar:
  RSS feed ile => çoğu haber sitesi sağlıyor 
  API'yı olan sitelerden => büyük siteler API'yı kendi verir
  Web Scraping ile => HTML'den çeker 
- Veriyi temizler, standardize eder
- Kendi veri tabanına yükler 
- Request gelince de database'de arama yapar, sonuç döndürür

# web_scraping 
    titles =  [t.text for t in soup.find_all("h1")] => Hürriyet sitesi, çoğu içeriği JavaScript yüklüyor, o yüzden de request.get ile gelen HTML içinde gerçek başlıklar yok 
    requests.get(url) => sayfanın ilk HTML halini getirir, javascript kısmını alamıyorum, bu yüzden [] boş liste geliyor 

    headers = {
        "User-Agent" : "Mozlla/5.0"
    } => bazen siteler request'leri bot sanar ve engeller onun için ekledik 

    response = requests.get(url, timeout=10) #Keyboard error aldım, sayfa çok geç yüklendi, o yüzden timeout geldi 

# trends
    time.sleep(random.uniform(2,5)) #google isteğimi engelliyor bot gibi görünmemek için 

# twitter(x) den veri çekmek
X kuralları gereğince API'dan veri çekebiliriz
İki iyi seçenek var:

Seçenek A - Belirli bi sorgu için post çekmek 
Örnek => "deprem lang:tr -is:retweet"
         "Mansur Yavaş lang:tr -is:retweet"
         "İran lang:tr -is:retweet"
Bu "recent search" ile yapılır. Bu endpoint son 7 günün postlarını getirir

Seçenek B - Belirli sorguların kaç kez geçtiğini saymak 
Örnek => deprem, iran, futbol => bunu da "get count of recent posts" ile yaparız.

"Günün en çok konuşulan başlıkları" için en mantıklı yaklaşım:
- Haberlerden aday başlık/kelime çıkartalım
- X API'dan bunları arayalım 
- Hangi konu dah açok konuşulmuş bakalım
- Bugünün dosyasına kaydedilim

NE LAZIM?
1) X dökümanına göre => developer account, approved app/project, Bearer Token
2) Endpoint => GET /2/tweets/search/recent => son 7 günün postları gelir 
            => GET /2/tweets/counts/recent => sayı endopoint'ini ekleriz, eşleşen post sayısını verir

BEARER_TOKEN = X'in tanıması için gerekli olan key
query = ne aradığını söyler 

# cleaning 
    text = re.sub(r"[^a-zA-ZğüşöçıİĞÜŞÖÇ\s]", "", text)  => türkçe karakterleri korur!!!! 
    Counter =>  elimizdeki listesi kelimeden kaç tane geçtiği ile birlikte bi dict çevirir

# veri depolama
raw_titles => buraya başlıklar gelir 
daily_count => temizlenmiş ve sayılmış günlük veri gelir 
datasets => model için hazırlanan tablo gelir 

import json => pythondaki list ve dict'i .json yapmak için importluyoruz 
import os => klasor yoksa otomotik oluşturmaya yarar
os.makedirs(os.path.dirname(filepath), exist_ok=True) => klasörü hazırlar 
json.dump(data, file, ensure_ascii=False, indent = 4) => veriyi json'a çevirri, indent = dosya düzenli ve okunur olsun 
if not os.path.exists(filepath): => dosya var mı yok mu kontrolu 


all_words = set(today_counts.keys()) | set(yesterday_counts.keys())  => iki günün kelimeleri birleşir 

Note=> 21'inde çalıştırmayı unuttuğum için 21 22 dosyası aynı sadece sonra keliemler sildim 

Note => label = 1 if ... yazdığım için model benim kuralı öğreniyor, gerçek dünyayı değil, ilk versiyon için kalabilir

# SQL 
python içinde küçük bi veritabanı kurup, trend sonuçlarını tablo halinde saklamak için kullanıyoruz
SQL => veri tabanı ile konuşma dili 

create_connection()  =>  database/trends.db dosyasına bağlanır, yoksa oluşturur.
create_table() => trends adında tablo oluşturur, zaten varsa tekrar oluşturmaz 

SQLite => hafif bir veritabanı sistemi
Avantajı:
ayrı kurulum gerektirmez,
python içinde sqlite3 ile hazır gelir 
küçük projeler için uygun 

Neden veritabanına geçiyoruz?
Sadece terminalde görmeyelim, bugün çıkan trendleri saklayalım, yarın yine ekleyelim, sonra geçmişe dönüp bakalım 
Mesela => 22 nisan'da hangi trendler vardı, en çok tekrar eden kelime, hangi kelime kaç gğn trend olmuş
!!! JSON ile de yapılır ama veritabanı ile çok daha temiz 

os.makedirs(os.path.dirname(db_path), exist_ok=True) => klasör yoksa oluştur varsa sorun çıkartma 
conn = sqlite3.connect(db_path) => trends.db dosyasına bağlan, dosya yoksa oluştur varsa bağlan 

conn = conn.cursor() => cursor, veritabanına komut gönderen araç gibi düşünülebilir, !!!SQL komutları cursor ile çalışır 

VALUES (?, ?, ?, ?, ?, ?, ?) => yer tutucu 

# API
Projedeki sonuçları dışarı çıkartmak istiyoruz 
FastAPI => Python ile API yazmayı kolaylaştıran kütüphane, yani web sitesi yazmama gerek kalmadan, sadece python ile, şu adrese gelinirse bunu döndür demeni sağlar 
Neden API kullandık? => çünkü projede veri var ve bu veriyi dışarı aktarmak istiyoruz. Bu sayede ileride dashboard kullanabiliyoruz, başka uygulamaya bağlayabiliyoruz, browser'dan test edebiliyoruz.

app = FastAPI() => bir FastAPI uygulamaso oluşturuyoruz, endpoint'leri bu app nesnesine bağlıcaz 

@app.get("/")  => eğer biri "/" adresine (home) GET isteği atarsa, fonk. çalıştır 

def home() => endpoint çalışınca çalışacak Python fonks.
!!! fonk. dict. dönüyor ama FastAPI bunu otomatik JSON yapar.

çalıştırma kodu : uvicorn api.app:app --reload

def get_db_connection() => veritabanına bağlanmak için yardımcı fonks.

import joblib => model dosyası yüklemek için 

http://127.0.0.1:8000/docs => dosyaları görmek için bu adrese girmelisin 

dataset_files.sort(key = os.path.getatime) => son değiştirilme tarihine göre sırala 

# Dashboard/ Streamlit 
Dashboard temel mantığı => Streamlit arayüzü açılıyor, FastAPI'dan veri istiyor, gelen JSON'u tablo/grafik olarak gösteriyor
streamlit => ekranda başlık, tablo, input, buton gibi şeyler göstermemizi sağlar 
requests => fastAPI'ya istek atmak için kullanılır. 

response = requests.get(f"{API_URL}/top-words") => FastAPI'daki /top-words endpoint'ine gider
if response.status_code == 200 => API başarılı demek 

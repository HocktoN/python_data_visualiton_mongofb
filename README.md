# Scraper Project

- Python 3.8 sürümü kullanıldı.
- Linux işletim sistemi Ubuntu dağıtımı 20.04 sürümünde yazıldı ve test edildi.

## main.py

- Projenin baslatıldığı dosya 
- Elapsed time ve diğer statslar buradan stats collectionuna kaydolur

## requirements.txt

- Projenin icerdiği kütüphane ve sürümler bulunur

## logs.log

- loglar tutulur

## dockerfile

- projenin dockerda calistirlabilmesi icin dosya

## src

- config.py icinde projenin genel değişkenleri tutulur
- db_ops.py database islemleri buradan cagırılır
- tools.py icerisinde logger, selector islemler ve db connect bulunur.
- scraper.py ana islemin yapıldıgı dosyadır. urlleri toplar, haberleri alır daha önce gönderilmemisleri kaydeder.

## data_analysis

- data_aggregate.py collectiondaki update_date fieldini datetime donusturur ve buna göre verileri gruplar. hangi tarihte kac data oldugunu yazar ve dokumanları yazar. dosyayı run etmek yeteri
- data_visualization.py en cok kullanılan 10 kelimeyi bulur print eder istenirse eğer cubuk ve kelime bulutunu cizer ve bu grafiklerin görsellerini bu klasorun icine kaydeder.

## tests

- db connect ve data cekilmesi islemlerini test eden 2 .py dosyası bulunur.


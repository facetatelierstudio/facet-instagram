# facet-instagram

Facet Atelier Studio Instagram gönderileri. `yayin` dalındaki görseller Instagram API'ye herkese açık adres olarak verilir.

- `kuyruk.json`: tarihli gönderi kuyruğu (carousel / reel, caption, durum)
- `gonderiler/`: 1080×1350 carousel görselleri ve 1080×1920 reel videoları
- `arac/calistir.py`: zamanı gelen gönderileri paylaşır, kuyruğu günceller
- `arac/paylas.py`: Instagram API ile tek gönderi paylaşır
- `arac/ig45.py`, `arac/reel.py`: teslim renderlarından Instagram formatı üretir

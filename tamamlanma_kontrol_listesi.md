# LotoAnaliz AI — V8 Gereksinim Durumu (22.10.2026)

Üstü çizilen maddeler **yalnızca kod ve uygun otomatik testlerle doğrulanan** işlevlerdir. Gerçek internet/telefon gerektiren testler ayrıca listelenir.

## Mevcut mobil uygulama
- [x] ~~V2/V3 mobil HTML, CSS ve navigasyon düzeninin korunması~~
- [x] ~~Her açılışta iki oyun için aynı kaynaklı sunucuya güncelleme denemesi~~
- [x] ~~Manuel çekiliş ekleme ve yerel veri koruma~~
- [x] ~~Cihazda CSV/JSON yedekleme ve mevcut kayıtları koruyan içe aktarma~~
- [x] ~~PWA manifest ve Service Worker~~
- [ ] Android ve iOS gerçek cihaz kurulum, bildirim ve çevrimdışı kabul testleri

## Veri doğrulama ve tarihsel sonuçlar
- [x] ~~Her oyunda altı farklı ana sayının ve sayı aralığının doğrulanması~~
- [x] ~~Ek joker/süperstar sayılarının altı ana sayıdan ayrılması (mevcut format)~~
- [x] ~~Resmî sayfa uyuşmazlığı ve şablon hata kontrolü~~
- [x] ~~Küçük partilerle yetkili tarihsel tarama, imleç, hata kaydı ve kaldığı yerden devam API'si~~
- [x] ~~CSV yüklemelerini doğrulanmamış kayıt olarak ayırma~~
- [ ] Resmî siteden gerçek sonuçların bu çalışma ortamında başarıyla çekilmesi
- [ ] Resmî sitedeki **tüm geçmiş çekilişlerin** eksiksiz indirilip tek tek doğrulanması
- [ ] Tarihsel oyun kuralı sürümleri ve bütün dönemler için parser doğrulaması
- [ ] Bağımsız kaynak bazında arşiv tamlık ispatı

## Analiz ve geriye dönük test
- [x] ~~Frekans, son görülme, 10/25/50/100/250 dönemi~~
- [x] ~~Tek/çift, düşük/yüksek, toplam ve ardışık analizleri~~
- [x] ~~İkili/üçlü birlikte görülme~~
- [x] ~~Tüm sekiz stratejiyle geçerli kolon oluşturma~~
- [x] ~~Kronolojik geriye dönük test ve rastgele kıyaslama~~
- [x] ~~Monte Carlo frekans sapması testi, gözlenen etki büyüklüğü ve p değeri API'si~~
- [x] ~~Sayı farkı, min/max, onluk aralık kapsama analizi API'si~~
- [ ] Çoklu karşılaştırmalar için tüm hipotez ailelerinde düzeltme, güven aralıkları ve dönemsel cross-validation
- [ ] Tüm istatistik ve yönetim ekranlarının orijinal mobil arayüze tam entegre edilmesi

## Sunucu ve dağıtım
- [x] ~~FastAPI, REST uç noktaları ve /docs API dokümanı~~
- [x] ~~Kalıcı SQLite veritabanı ve temel benzersizlik kontrolü~~
- [x] ~~Yönetici anahtarı ile tarihsel tarama/CSV içe aktarma koruması~~
- [x] ~~Docker dosyaları, yerel zamanlayıcı, güvenlik başlıkları~~
- [x] ~~Otomatik pytest testleri (19 başarılı) ve JavaScript sözdizimi denetimi~~
- [ ] PostgreSQL, migrasyonlar ve çok sunuculu senkronizasyon
- [ ] Gerçek Web Push bildirimi ve abonelik/abonelik iptal yönetimi
- [ ] Tam rate limiting, tehdit modeli, sızma testi ve yedek kurtarma tatbikatı
- [ ] Gerçek HTTPS alan adı üzerinde canlı dağıtım ve uçtan uca cihaz testleri

**Dürüst teslim durumu:** İşlevsel test sürümüdür; eksik maddeler nedeniyle eksiksiz üretim sürümü değildir. Resmî çekiliş sunucusuna doğrudan DNS erişimi bu ortamda başarısız olduğu için canlı veri çekme doğrulanamadı.

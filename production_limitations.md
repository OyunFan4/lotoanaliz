# Son sürüm kontrol ve sınırlamalar

- **Canlı resmî site çekimi doğrulanmadı.** Resmî sayfalara buradaki Python ortamından doğrudan ağ erişimi yok. Gerçek HTTPS sunucuda uçtan uca deneme yapılmalı.
- **Geçmiş arşiv tamlığı doğrulanmadı.** Yönetici kontrollü tarama partiler hâlindedir; 403 / 429 engelleri aşılmaz. Resmî kaynağın kullanım koşullarına uyun.
- **Veritabanı SQLite.** Kalıcı disk ile tek sunuculu kullanım içindir; PostgreSQL migration bu pakette yoktur.
- **Mobil Android / iOS gerçek cihaz testleri yapılmadı.** Ana ekran kurulumu HTTPS gerektirir.
- **Bildirimler / hesaplar arası senkronizasyon** mevcut değil. Veri cihaz üzerinde saklanır; yedek kullanın.
- **CSV API yüklemeleri asla resmî doğrulanmış sayılmaz.** Yönetici anahtarı gerektirir.
- **Gelecek tarihler / eski oyun kuralı değişimleri** tam tarihsel modelle yönetilmedi; ilk tarihsel dönemleri aktarmadan kontrol edin.
- **Kazanma garantisi yoktur.** İstatistik ve geriye dönük sonuçlar adil çekilişte bir kombinasyonun çekilme olasılığını artırmaz.

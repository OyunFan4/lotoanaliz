# Netlify + GitHub kurulumu

Bu sürüm mevcut HTML/CSS ekranını korur. Eklenen `netlify.toml`, `/api/sync` ve `/api/health` yollarını Netlify Functions'a yönlendirir.

1. Depodaki mevcut dosyaları yedekleyin. ZIP içindeki dosyaları GitHub deponuza aktarın. `netlify/functions` klasör yapısını koruyun.
2. Netlify → mevcut **lotoanaliz** projesi → Project configuration → Build & deploy → Repository bağlantısının bu GitHub deposuna işaret ettiğini doğrulayın.
3. Deploy ayarlarında **publish directory** proje kökü (`.`), **functions directory** `netlify/functions` olmalı. `netlify.toml` bunları tanımlar. Yeni commit sonrası Deploys ekranında yayımlamayı kontrol edin.
4. Önce `https://lotoanaliz.netlify.app/api/health` adresini açın. JSON ve `ok:true` beklenir. 404/HTML gelirse fonksiyon yüklenmemiştir.
5. Sonra `/api/sync?game=super` ve `/api/sync?game=sayisal` adreslerini açın. `status:unavailable` ve açıklama çıkarsa servis çalışıyor ama resmî sonuç ayrıştırılamamıştır. Yalnız `status:ok` ve `results` içindeki doğrulanmış kayıtlar analize eklenir.
6. Telefonda kurulu eski uygulamayı açın. Gerekiyorsa sayfayı yenileyin. Yeni uygulamayı kurmadan önce **Diğer → JSON yedeğini indir** ile cihaz kayıtlarınızı yedekleyin.

## Önemli teknik sınırlamalar
- Milli Piyango resmî sayfaları bazı erişimlerde sayıları değil `{{#each winningNumber}}` şeklindeki şablonları gösteriyor. Bu halde veri alınamaz. 403/429 engelleri aşılmaz.
- Bu Netlify Function sadece sınırlı sayıda güncel çekilişi dener. Tüm geçmiş arşivi toplamaz, kalıcı sunucu veritabanı değildir. Doğrulanan sonuçlar PWA'da cihazın IndexedDB alanına kaydedilir.
- Python `server.py` Netlify üzerinde çalışmaz. Gelişmiş `/api/backtests/run` gibi Python API yolları ayrıca backend olmadan kullanılamaz.
- Herhangi bir sonuç taraması çalışmadan önce resmî sitenin veri kullanım koşulları kontrol edilmelidir.

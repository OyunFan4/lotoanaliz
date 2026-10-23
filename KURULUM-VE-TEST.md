# LotoAnaliz AI V9 — Netlify + telefon testi

1. Dosyaları GitHub deposunun **kök dizinine** yükleyin (`index.html` ve `netlify.toml` kökte kalmalı). `netlify/functions/` klasörünü koruyun. GitHub deposu Netlify projenize bağlı olmalı.
2. Netlify Deploys ekranında son dağıtımın **Published** olduğuna bakın.
3. `https://lotoanaliz.netlify.app/api/health` adresini açın. JSON içinde `ok: true` beklenir. 404 veya HTML hata sayfası görürseniz Netlify Function yayımlanmamıştır.
4. `https://lotoanaliz.netlify.app/api/sync?game=super` adresini açın. `results` dolu ve `status: ok` ise veri alınmıştır. `status: unavailable` ise kaynak doğrulanamamış demektir; `errors` nedenini açıklar.
5. Telefonda sitenin son sürümünü açın, yenileyin. Eski PWA görünüyorsa Android'de tarayıcı sitesini yeniden yükleyin. **Cihaz verilerini silmeyin**; önce Diğer → JSON yedeğini indir.
6. **Özet**, **Arşiv** veya **Diğer** bölümünde **Şimdi sonuçları kontrol et** butonuna dokunun. İki oyunun ayrı ayrı durumunu görün.
7. Alınamayan çekiliş için Arşiv → Bir çekilişi elle ekle formunu doldurun. Manuel kayıtlar silinmez.

## Sınırlamalar

Resmî sonuç sayfaları sunucu isteğinde işlenmemiş şablon gönderebilir veya 403/429 döndürebilir; bunlar engellenmez ve sahte sonuç üretilmez. Fonksiyon yalnızca sınırlı güncel çekiliş adaylarını sorgular, bütün geçmişi taramaz. Netlify tarayıcı sürümündeki kayıtlar IndexedDB içinde yalnızca bu cihazda saklanır. Manuel kayıtlar resmî doğrulanmış sayılmaz. Bu paketin canlı Netlify dağıtımı ve sonuç çekme başarısı bu ortamda doğrulanmamıştır.

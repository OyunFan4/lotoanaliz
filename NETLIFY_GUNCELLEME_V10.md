# LotoAnaliz AI — Netlify V10 bağlantı düzeltmesi

## Dosyaların amacı
- `netlify/functions/sync.mjs`: Resmî iki örnek çekiliş sayfasına kontrollü bağlantı, HTTP / timeout / veri doğrulama aşamalarının ayrı raporlanması. Legacy named `handler` export; Netlify sağlık fonksiyonuyla aynı imza.
- `app.js`: Oyunları birbirinden bağımsız ve eşzamanlı kontrol etme; 14 saniyelik istemci zaman aşımı; işlem durumunu gösterme.
- `service-worker.js`: Yeni cache anahtarıyla PWA dosyalarının yenilenmesi.
- `test_sync.mjs`: Sahte HTML kullanarak veri doğrulama testleri.

## GitHub'a güncelleme
1. Önce telefondaki uygulamada varsa **Diğer → Yedek Al** ile mevcut verilerinizi kaydedin.
2. ZIP içeriğini GitHub `OyunFan4/lotoanaliz` deposunun **kök dizinine** yükleyin. `netlify/functions/sync.mjs` klasör yolu korunmalıdır. ZIP'i tek dosya olarak göndermek işlevsel deploy sağlamaz.
3. `main` dalında Commit changes yapın.
4. Netlify Deploys bölümündeki yeni yayın `Published` olduğunda, önce `/.netlify/functions/health`, sonra `/.netlify/functions/sync?game=super` ve `...game=sayisal` adreslerini ayrı ayrı deneyin.
5. Telefonda PWA'yı tamamen kapatıp tekrar açın; gerekirse Chrome'da normal tarayıcı sekmesinden güncel sürüme erişin. **Uygulama verilerini temizlemeyin**, IndexedDB'de saklanırlar.

## Nasıl yorumlanır?
- `status: ok`: yalnızca belirtilen örnek çekiliş gerçekten doğrulanmış ve `results` dolu.
- `status: unavailable`, `stage: timeout`: Netlify çalışıyor; resmî siteden 7,5 saniyede yanıt alınamadı.
- `stage: source_http`: Resmî sunucu HTTP hatası yanıtladı.
- `stage: verification`: Sayfa alındı fakat altı sayı/tarih/çekiliş numarası güvenle ayrıştırılamadı.
- Bu sürüm sadece **iki örnek çekilişi** sorgular. Tüm tarihsel arşivi toplamaz.

## Gerçek veri erişimi sınırı
Bu ortamdan Millî Piyango alan adına doğrudan erişim DNS hatası veriyor. Netlify'daki sizin önceki canlı testiniz ise timeout döndürdü. Bu sebeple canlı veri aktarımı başarılı diye işaretlenmedi. Kaynak izinli bir API veya erişilebilir resmî export sunana kadar CSV/JSON girişini kullanın. 403/CAPTCHA veya erişim kısıtlarını aşma yoluna gidilmez.

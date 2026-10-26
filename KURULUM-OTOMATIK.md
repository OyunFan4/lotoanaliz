# LotoAnaliz AI — otomatik veri altyapısı / kontrollü geliştirme

> Mevcut mobil arayüz, PWA, geçmiş cihaz kayıtları ve sekmeler korunmuştur. `sync` yanıtının biçimi eski UI ile uyumludur. Otomatik veri toplama kaynak doğrulanmadan **tamamlandı** olarak beyan edilmez.

## Gerçek durum (26.10.2026)

- **İki oyunun CollectAPI adaptörü:** Çılgın Sayısal Loto ve Süper Loto. Son kullanıcı testlerinde iki uç nokta da HTTP 500 dönmüştü. Bugün canlı yanıt doğrulanmadı; otomatik aktarım garantisi yok.
- **Şans Topu ve On Numara:** Kural/doğrulama altyapıları hazır; resmî veya izinli çalışan API adresleri doğrulanmadı, bağlanmadılar.
- **Resmî doğrulama:** CollectAPI üçüncü taraf kaynağıdır. Bu kaynaktan çekilen hiçbir veriyi `official_verified` diye işaretlemeyin.
- **Geçmiş çekilişler:** İzinli sayfalama/tarih aralığına sahip çalışan veri kaynağı henüz bulunmadığı için otomatik geriye dönük tam aktarım yapılmamıştır.
- **İşlem:** Netlify'daki zamanlanmış kontrol her dört saatte bir (UTC, saat başından 15 dakika sonra) dört oyun için çalışır. İki oyunda veri kaynağını dener; diğer iki oyun için `not_configured` kaydı tutar. Aynı çekilişi yeniden eklemez.
- **Güvenlik:** Public sync endpointi sadece sorgulama yapar, kalıcı DB'ye yazmaz; kalıcı kayıt yalnızca arka plan zamanlayıcısından yapılır. Gizli anahtarlar sadece Netlify Functions ortamında tutulur.

## Kurulum

1. Mevcut `lotoanaliz` deposunun bir yedeğini alın ve bu ZIP'in içeriklerini ana dizine ekleyin. `index.html`, `app.js`, `style.css` ana dizinde, `netlify/functions/` aynı konumda olmalıdır. GitHub'a **asla gerçek .env veya API anahtarı** yüklemeyin.
2. https://supabase.com adresinde bir proje oluşturun. Supabase SQL Editor'da `supabase/001_initial.sql` çalıştırın.
3. Netlify → Project configuration → Environment variables:
   - `SUPABASE_URL`: Supabase proje URL'si
   - `SUPABASE_SERVICE_ROLE_KEY`: Supabase **secret** service_role key (GitHub'a ve tarayıcıya koymayın)
   - `COLLECTAPI_KEY`: CollectAPI'de **yenilediğiniz** anahtar (geçmişte sohbet içinde paylaşılmış anahtar kullanılmamalı). Başına `apikey ` eklemeyin.
4. Netlify'da yeniden deploy edin. Production deploy tamamlanınca `/.netlify/functions/health` ve `/.netlify/functions/summary` adreslerini deneyin.
5. `/.netlify/functions/sync?game=sayisal` ve `?game=super` arayüzle uyumluluğu gösterir; bunlar tarayıcıdan tetiklenen *okuma* kontrolleridir. Kalıcı veritabanını zamanlanmış görev yazar.
6. `/.netlify/functions/history?game=sayisal` arşivi, `/.netlify/functions/summary` son 20 kontrol günlüğünü gösterir.
7. Netlify Function loglarında `Scheduled LotoAnaliz check` mesajını arayın. **Netlify'da çalışmadığını görmediğiniz bir işi tamamlandı diye kabul etmeyin.**

## Yedekleme ve geri yükleme

Supabase'de SQL Export veya PostgreSQL `pg_dump` kullanarak düzenli yedek alın. Geri yükleme öncesinde test ortamında `pg_restore` ile kurtarma doğrulaması yapın. Mevcut cihaz kayıtları ayrı bir yerel tarayıcı depolamasındadır; bu paket onları kendiliğinden silmez veya server'a taşımış gibi davranmaz.

## Bilinen sınırlamalar ve sonraki adım

- Kaynak CollectAPI 500 vermeye devam ederse yeni veri gelmeyecektir; geçmiş veriler **korunur**.
- Kamuya açık API için ilk seviye CDN 5 dakikalık önbellek vardır; yoğun trafik için Netlify rate limit/WAF gibi ek kontrol gerekir.
- Resmî/izinli veri erişimi, çekiliş numarası ve tarih eşleştirmesi, dört oyunun tüm arşivi, kaynak çelişkilerinin ayrı tabloya alınması ve uçtan uca üretim testleri **henüz tamamlanmadı**.
- `archive/history` ilk 500 kayıtla sınırlıdır; tam tarihi aktarım ve sayfalama ileride gerçek veri kaynağına bağlanarak geliştirilmeli.
- PWA cihaz üzerindeki verileri kaldırmak için **tarayıcı verilerini temizlemeyin**.
- Terminal testi: `node --test tests/core.test.mjs`. Bu testlerde gerçek çekiliş sonucu uydurulmaz.

## v13: durum belgesi ve etiket düzeltmesi
- `app.js`: üçüncü taraf kayıtları artık kullanıcı verisi olarak yanlış etiketlenmiyor.
- `tests/integration_contract.test.mjs`: API sözleşmesi ve veri etiketi testleri eklendi.
- `LOTOANALIZ-TUM-ADIMLAR-DURUM.md`: kullanıcı talimatının tamamı; yalnızca uygulanmış/doğrulanmış kod adımları üstü çizili.
- `LOTOANALIZ-TUM-DOSYALAR-METIN.txt`: paketteki dosyaların tam metin dökümü ve PNG varlıkların Base64 gösterimi.
- Canlı dağıtım, API veri akışı, tüm geçmiş arşiv ve veritabanı kurulumu tamamlanmadı.

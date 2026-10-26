# LotoAnaliz v14 — web scraping kurulumu

Bu sürüm CollectAPI çağrılarını kaldırır; bütün oyunların toplanması **izin verilen HTML çekiliş sayfaları** üzerinden yapılacak şekilde hazırlanmıştır. **Scraping varsayılan olarak kapalıdır**. Milli Piyango'nun site içeriğine yönelik kullanım kısıtlamaları vardır; yazılı izin/lisans olmadan bu siteyi otomatik taramak için bu yazılımı etkinleştirmeyin. CAPTCHA, oturum veya erişim engellerini aşma özelliği yoktur.

## 1. Kaynak izni ve adresler
Kaynak sağlayıcısından otomatik veri çekme ve yeniden kullanma iznini alın. İzin verilen tek tek çekiliş sayfalarının HTTPS adreslerini oyun bazında belirleyin. Sayfa sonuçları sunucu HTML'sinde açıkça içermelidir (JavaScript template olan sayfalar reddedilir).

## 2. Supabase
`supabase/001_initial.sql`, sonra `supabase/002_scraper.sql` çalıştırın.

## 3. Netlify Environment variables
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY` (yalnızca sunucu tarafı)
- `SCRAPE_PERMISSION_CONFIRMED=true` (yalnızca izin aldıysanız)
- `SCRAPE_ALLOWED_HOSTS` (ör. `authorized.example.org`)
- `SCRAPE_SOURCES_JSON` örnek: `{"sayisal":["https://authorized.example.org/sayisal/draw-1"],"super":[],"sans":[],"onnumara":[]}`

Üretimde gerçek kaynakları/izinleri doğrulayın, URL'leri sohbet yoluyla göndermeyin. Her oyun için URL listesi eskiden yeniye sıralanmalı. Her planlı çalışma her oyun için sıradaki **bir** sayfayı işler; başarılı olan sayfa için işaretçi ilerler. Bilinmeyen kaynaklar için hiçbir sayı uydurulmaz.

## 4. Sınırlar
- Dört oyun için ayrıştırıcı ve doğrulayıcı vardır; canlı kaynak uyumluluğu doğrulanmadı.
- Tarama yalnızca kaynağın erişilebilir ve izinli olduğu koşullarda başlayabilir.
- Kayıtlar `source_unverified` olarak etiketlenir; resmî teyit olmadan `official_verified` yapılmaz.
- Sürekli güncel kalmak için URL listesinin de izinli bir indeks kaynağından güvenilir şekilde güncellenmesi gerekir; bu otomatik keşif mekanizması henüz yoktur.
- Ağ hatalarında işaretçi ilerlemez. Zaman aşımı veya sayfa formatı değişimi hata olarak kaydedilir.
- Sunucu erişimi ve lisans sorunu çözülmedikçe geçmiş arşiv ve zamanlanmış toplama tamamlanmış sayılmaz.

## Test
`node --test tests/scraper.test.mjs`

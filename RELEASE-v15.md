# LotoAnaliz AI v15 — Durum ve kurulum

## Yerel olarak yapılanlar
- v14 kaynak ağacı ve mevcut tasarım korundu.
- Arayüzün artık sadece eski CollectAPI URL’sini kabul etmesi hatası düzeltildi.
- İzinli HTTPS kaynaklarından gelen, henüz resmî olarak doğrulanmamış kayıtlar açık etiketle gösterilir.
- Çekilişler ve cihaz içindeki kayıtlar silinmez.
- Cihazın açık/koyu tema tercihini ilk açılışta kullanma altyapısı iyileştirildi.
- Erişilebilir odak çizgileri ve küçük ekran düzenleri güçlendirildi.

## Önemli: henüz tamamlanmayan işler
- İzinli ve canlı dört oyun veri kaynağının bağlantısı ve çekiliş tarihi/numarasının kaynak üzerinden doğrulanması.
- Geçmiş tüm çekilişlerin otomatik aktarımı.
- Gerçek Supabase kurulumunun tamamlanması ve zamanlayıcının canlı loglarla doğrulanması.
- iPhone/Android, koyu/açık tema ve canlı uçtan uca testler.

## Kurulum
1. Mevcut GitHub reposunun yedeğini alın.
2. ZIP içindekileri repo ana dizinine aynı klasör yapısıyla yükleyin.
3. Supabase migration dosyalarını sırasıyla çalıştırın.
4. Netlify ortam değişkenlerini `.env.example` ve `SCRAPING-KURULUM.md` belgelerinden tanımlayın. Gizli değerleri GitHub'a koymayın.
5. Kaynağın içerik aktarım iznini doğrulamadan `SCRAPE_PERMISSION_CONFIRMED=true` kullanmayın.
6. Canlı `/.netlify/functions/health`, `/api/sync?game=super`, `/api/sync?game=sayisal`, `/.netlify/functions/history?game=super` uç noktalarını ve zamanlanmış görev loglarını test edin.
7. Veri kaynağı boşsa sonuç üretmeyin; bu üretim sürümü tam otomatik olarak **doğrulanmamıştır**.


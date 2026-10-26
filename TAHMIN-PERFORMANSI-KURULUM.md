# Tahmin Performansı v16

Bu sürümde menü, dört kart, 0–6 dağılımı, grafik, tarih/oyun/durum/yöntem filtreleri ve hedef çekiliş kaydı vardır. Önceki yerel veriler korunur.

## Veri güvenilirliği
- Yeni kolonları kaydederken hedef çekiliş numarası ve tarihi seçilmelidir. Gelecekteki tarih zorunludur.
- Eski kolonlar hedef çekilişi belli olmadığından değerlendirilmez.
- Yalnızca `official_verified` durumundaki altı ana sayılı ve çelişkisiz sonuçlar karşılaştırılır. Üçüncü taraf scraping verileri dahil değildir.
- Bu uygulamadaki mevcut resmî doğrulama pipeline'ı canlıda sonuç üretmediğinden özetler boş kalabilir.
- Sadece 6 ana sayının eşleşmesi hesaplanır; farklı oyunlara özel bonuslar desteklenmez.
- Üçüncü taraf veya manuel sonuçlar performans kazanımı sayılmaz.

## Önemli üretim sınırlaması
Tahminler mevcut IndexedDB cihaz deposunda tutulur; Supabase dosyası sadece gelecekteki güvenli sunucu entegrasyonu için hazırlanan şemadır. Çekiliş öncesi kayıtların sunucuda değiştirilemez zaman damgasıyla kanıtlanması, kimlik doğrulama, sunucu üzerinden otomatik değerlendirme ve resmî verilerin canlı toplaması henüz kurulmamıştır. Gerçek üretim raporları için bu bölümler şarttır.

## Test
`node --test tests/performance.test.cjs`

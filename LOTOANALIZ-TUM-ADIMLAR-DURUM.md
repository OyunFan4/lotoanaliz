# LotoAnaliz — Orijinal Talimat / Uygulama Durumu (26.10.2026)

**İşaretleme kuralı:** `~~üstü çizili~~` = kodda uygulanmış ve/veya yerel testle doğrulanmış adım; canlı altyapı kurulumu gerektiren işler *işaretlenmedi*. Kodu hazırlanmış ancak **canlı çalışması doğrulanmamış** adımları ancak dar kapsamıyla çizdim.

**Önemli:** Nihai kabul kriteri henüz karşılanmıyor. CollectAPI'nin Sayısal ve Süper Loto uç noktaları kullanıcı testinde HTTP 500 vermişti. Şans Topu ve On Numara kaynak adaptörleri yok; Supabase/Netlify güncel dağıtımı bu oturumda doğrulanmadı.

**v13 gerçek değişiklikleri:** Mevcut v12 temel alındı; üçüncü taraf kayıt etiketi düzeltildi, beş ek sözleşme testi eklendi. Tüm mevcut kodlar tek metin belgesine aktarıldı.

---

# LotoAnaliz — Tam Otomatik Sistem Kurulum ve Geliştirme Promptu

Mevcut GitHub deposundaki LotoAnaliz projesini incele ve çalışan yapıyı bozmadan eksik özellikleri tamamlayarak üretime hazır hâle getir.

**ANA HEDEF:** LotoAnaliz, geçmiş ve yeni loto çekiliş sonuçlarını güvenilir kaynaklardan otomatik olarak toplasın, veritabanına kaydetsin, doğrulasın ve istatistikleri otomatik güncellesin. Kullanıcının sonuçları elle girmesi gerekmemeli.

## 1. Mevcut projeyi incele

- GitHub deposundaki tüm dosyaları ve klasörleri analiz et.
- Kullanılan teknolojileri, mevcut arayüzü, veri modelini, API'leri ve Netlify yapılandırmasını belirle.
- ~~Çalışan özellikleri ve tasarımı koru.~~  ✅ **Kod/yerel kapsam**
- Eksik özellikleri tespit et ve uygulama planı oluştur.
- ~~Projeyi gereksiz yere baştan yazma.~~  ✅ **Kod/yerel kapsam**
- ~~Değişiklikleri mevcut teknolojiyle uyumlu şekilde uygula.~~  ✅ **Kod/yerel kapsam**

## 2. Loto sonuçlarını otomatik topla

Mevcut projeye uygun olarak aşağıdaki oyunları destekle:

- Çılgın Sayısal Loto
- Süper Loto
- Şans Topu
- On Numara

Her oyun için resmî sonuç kaynağını araştır. Öncelikle resmî API veya erişime izin verilen yapılandırılmış veri kaynağını kullan. Uygun API yoksa kaynak sitesinin kullanım koşullarına uyan sunucu tarafı web scraping çözümü geliştir.

Kurallar:

- Sonuçları otomatik al.
- Kullanıcıdan sonuçları elle girmesini isteme.
- Kaynakları, çekiliş numaralarını ve veri formatlarını oyun bazında doğru eşleştir.
- Sonuçların açıklanma zamanlarını dikkate al.
- Kaynak siteye aşırı istek gönderme.
- Kaynak sayfa yapısı değişirse hatayı yakala ve kaydet.
- ~~Sonuç açıklanmamışsa sahte veri oluşturma.~~  ✅ **Kod/yerel kapsam**
- ~~Kaynak erişilemezse rastgele sayı üretme veya tahminde bulunma.~~  ✅ **Kod/yerel kapsam**
- Kaynak URL'sini, veri alınma zamanını ve doğrulama durumunu kaydet.

## 3. Geçmiş çekilişleri otomatik aktar

İlk kurulumda mümkün olan en eski tarihten itibaren erişilebilir geçmiş çekilişleri otomatik olarak topla.

- Verileri küçük partiler hâlinde aktar.
- Sayfalama veya tarih aralığına göre toplama yöntemini kullan.
- ~~Kaynakta mevcut olmayan verileri varmış gibi gösterme.~~  ✅ **Kod/yerel kapsam**
- İşlem yarıda kalırsa kaldığı yerden devam edebilsin.
- ~~Daha önce aktarılan kayıtları yeniden eklemesin.~~  ✅ **Kod/yerel kapsam**
- Her oyun için aktarımın tamamlanma durumunu raporlasın.
- ~~Geçmiş veri aktarımı tamamlanmadan sistemin tamamlandığını iddia etme.~~  ✅ **Kod/yerel kapsam**
- ~~Kaynak geçmiş sonuçların tamamını sağlamıyorsa sınırlamayı açıkça bildir.~~  ✅ **Kod/yerel kapsam**

Bu işlem ilk kurulumda otomatik başlamalı; kullanıcı sonuçları tek tek girmek zorunda kalmamalı.

## 4. Yeni sonuçları otomatik kontrol et

- ~~Netlify Scheduled Functions veya uygun bir zamanlayıcıyla düzenli kontrol kur.~~  ✅ **Kod/yerel kapsam**
- Çekiliş takvimine göre uygun kontrol sıklığını belirle.
- Saat dilimi olarak UTC kullanıldığında Türkiye saatine karşılığını belgele.
- Yeni sonuçlar yayımlandığında otomatik al ve doğrula.
- Sonuçlar henüz yayımlanmamışsa bir sonraki kontrolü bekle.
- ~~Aynı görevin birden fazla çalışması mükerrer kayıt oluşturmamalı.~~  ✅ **Kod/yerel kapsam**
- Geçici bağlantı hatalarında sınırlı sayıda yeniden deneme yap.
- Son başarılı kontrol zamanını kaydet.
- Güncelleme sonrası istatistikleri otomatik yenile.
- Yeni sonuç bulunmadığında da son kontrol durumunu kaydet.

Netlify fonksiyonlarının çalışma süresi ve dağıtım koşullarını dikkate al. İşlem süre sınırını aşacaksa Background Functions veya uygun harici worker kullan. Zamanlanmış görevlerin yalnızca gerekli koşullarda çalışacağını dikkate al.

## 5. Kalıcı veritabanı oluştur

Sonuçları yalnızca tarayıcı belleğinde veya geçici dosyalarda tutma.

Mevcut veritabanı varsa onu değerlendir. Yoksa Netlify ile uyumlu yönetilen bir PostgreSQL çözümü, örneğin Supabase, kullanmayı değerlendir.

Her çekiliş için uygun alanları sakla:

- ~~Oyun adı~~  ✅ **Kod/yerel kapsam**
- ~~Çekiliş numarası~~  ✅ **Kod/yerel kapsam**
- ~~Çekiliş tarihi~~  ✅ **Kod/yerel kapsam**
- ~~Kazanan sayılar~~  ✅ **Kod/yerel kapsam**
- ~~Oyuna özgü ek sayılar veya alanlar~~  ✅ **Kod/yerel kapsam**
- ~~Veri kaynağı~~  ✅ **Kod/yerel kapsam**
- ~~Verinin alınma zamanı~~  ✅ **Kod/yerel kapsam**
- ~~Doğrulama durumu~~  ✅ **Kod/yerel kapsam**
- ~~Oluşturulma ve güncellenme zamanları~~  ✅ **Kod/yerel kapsam**

Gereksinimler:

- ~~Oyun ve çekiliş numarası üzerinden mükerrer kayıtları engelle.~~  ✅ **Kod/yerel kapsam**
- ~~Veritabanı şeması ve migration dosyaları oluştur.~~  ✅ **Kod/yerel kapsam**
- ~~Veritabanı bağlantı bilgilerini ortam değişkenlerinden al.~~  ✅ **Kod/yerel kapsam**
- ~~Gizli anahtarları GitHub'a yükleme.~~  ✅ **Kod/yerel kapsam**
- ~~Veritabanı hatalarında mevcut geçerli kayıtları silme.~~  ✅ **Kod/yerel kapsam**
- Aktarım yarıda kalırsa güvenli şekilde devam edebil.
- Veri yedekleme ve geri yükleme yönergeleri hazırla.

## 6. Otomatik veri doğrulama

Her sonuç veritabanına kaydedilmeden önce kontrol edilsin.

- ~~Sayı adedi ve sayı aralıkları ilgili oyunun resmî kurallarına uygun olmalı.~~  ✅ **Kod/yerel kapsam**
- Çekiliş numarası ve tarihi doğrulanmalı.
- ~~Eksik veya bozuk veri otomatik olarak doğrulanmış sonuç sayılmamalı.~~  ✅ **Kod/yerel kapsam**
- Kaynakta aynı çekiliş için farklı sonuçlar görülürse çelişki kaydedilmeli ve inceleme için işaretlenmeli.
- ~~Kaynağın erişilememesi veri silinmesine yol açmamalı.~~  ✅ **Kod/yerel kapsam**
- ~~Kaynak doğrulanamadığında son geçerli sonuçlar korunmalı.~~  ✅ **Kod/yerel kapsam**
- ~~Veri çekme işlemi başarılı görünse bile sonuç doğrulaması başarısızsa işlem başarısız olarak raporlanmalı.~~  ✅ **Kod/yerel kapsam**

## 7. Elle veri girişini kaldır

**Temel şart: Sonuçların manuel olarak girilmesi sistemin çalışması için hiçbir zaman zorunlu olmamalı.**

- Yeni çekilişleri otomatik topla.
- Geçmiş çekilişleri otomatik aktar.
- İstatistikleri otomatik hesapla.
- Veri tabanını otomatik güncelle.
- Sonuçları kullanıcıya otomatik göster.
- Yönetici panelindeki manuel veri ekleme zorunluluğunu kaldır.
- İsteğe bağlı bir “Şimdi güncelle” düğmesi bulunabilir; bu düğme aynı otomatik veri toplama sürecini çalıştırmalı.
- Kaynakta veri bulunamazsa kullanıcıdan sonuçları elle girmesini istemek yerine hata ve veri eksikliği durumu göster.

## 8. İstatistikleri otomatik güncelle

Tüm istatistikleri gerçek ve doğrulanmış geçmiş sonuçlardan hesapla.

Özellikler:

- En sık çıkan sayılar
- En az çıkan sayılar
- Sayıların çıkma sıklıkları
- Tek ve çift sayı dağılımı
- Sayı aralıklarının dağılımı
- Ardışık sayı analizleri
- Tarih aralığına göre analiz
- Oyun türüne göre filtreleme
- Geçmiş çekilişleri listeleme
- İstatistik grafikleri
- Sonuçların güncellik durumu
- Son otomatik veri çekme zamanı

Yeni sonuçlar kaydedildiğinde ilgili analizler otomatik yenilensin. Veriler eksikse analizlerde bunu belirt. Geçmiş frekansların gelecekteki sonuçları garanti etmediğini açıkça göster.

## 9. Yönetim ve izleme paneli

Mevcut tasarıma uygun bir yönetim paneli oluştur veya var olanı geliştir.

Gösterilecek bilgiler:

- Oyun bazında toplam çekiliş sayısı
- Son başarılı veri toplama zamanı
- Son başarısız işlem
- Kaynak siteye erişim durumu
- Geçmiş veri aktarımının ilerlemesi
- Son görevlerin çalışma geçmişi
- Doğrulanmamış kayıt sayısı
- Eksik veya bekleyen sonuçlar
- Hata mesajları
- Son otomatik güncellemenin durumu

Yönetim işlemlerini kimlik doğrulamasıyla koru. Manuel güncelleme uç noktasını yetkisiz erişime ve aşırı isteğe karşı koru.

## 10. Hata bildirimi ve yedekleme

- Otomatik görevlerin başarılı ve başarısız çalışmasını kaydet.
- Veri kaynağı uzun süre erişilemezse sistemde belirgin uyarı göster.
- Tekrarlanan hatalarda uygun bir bildirim mekanizması hazırla.
- E-posta bildirimi kullanılacaksa gerekli ayarları ortam değişkenleriyle yapılandır; hesap bilgileri yoksa kurulum adımlarını yaz.
- ~~Veritabanı için yedekleme stratejisi belirle.~~  ✅ **Kod/yerel kapsam**
- ~~Geri yükleme prosedürü dokümante et.~~  ✅ **Kod/yerel kapsam**
- ~~Yedekleme yapılmadıysa yapıldı gibi raporlama.~~  ✅ **Kod/yerel kapsam**
- ~~Hatalar nedeniyle son geçerli sonuçların kaybolmasını önle.~~  ✅ **Kod/yerel kapsam**

## 11. Güvenlik

- ~~Gizli anahtarları ve veritabanı parolalarını istemci tarafına koyma.~~  ✅ **Kod/yerel kapsam**
- ~~`.env` dosyasını Git'e ekleme.~~  ✅ **Kod/yerel kapsam**
- ~~`.env.example` oluştur ve yalnızca örnek değişken adları kullan.~~  ✅ **Kod/yerel kapsam**
- ~~Gerekli ortam değişkenlerini doğrula.~~  ✅ **Kod/yerel kapsam**
- Parametreli sorgular veya uygun ORM kullan.
- Yönetim uç noktalarında yetkilendirme ve hız sınırlaması uygula.
- ~~Loglarda gizli bilgileri saklama.~~  ✅ **Kod/yerel kapsam**
- Veri kaynağının kullanım koşullarına uy.
- Herkese açık API uç noktalarını kötüye kullanıma karşı koru.

## 12. Netlify ve GitHub yapılandırması

Mevcut proje yapısına göre:

- ~~`netlify.toml` dosyasını oluştur veya güncelle.~~  ✅ **Kod/yerel kapsam**
- ~~Gerekli sunucu fonksiyonlarını ekle.~~  ✅ **Kod/yerel kapsam**
- ~~Zamanlanmış görevleri tanımla.~~  ✅ **Kod/yerel kapsam**
- ~~Veritabanı migration dosyalarını ekle.~~  ✅ **Kod/yerel kapsam**
- ~~Ortam değişkenlerini belgele.~~  ✅ **Kod/yerel kapsam**
- Build ve deploy ayarlarını kontrol et.
- Netlify fonksiyonlarının gerçekten çalışıp çalışmadığını loglarla doğrula.
- Gerektiğinde harici worker kullanımını belgele.
- Dağıtımın başarılı olduğunu yalnızca gerçekten kontrol ettiysen belirt.

GitHub'a erişim ve yazma yetkisi varsa değişiklikleri uygula. Yetki yoksa dosyaları ve uygulanabilir adımları hazırla; push yapıldığını iddia etme.

## 13. Testler

Otomatik testler yaz ve mümkün olanları çalıştır:

- Her oyun için veri ayrıştırma
- ~~Geçersiz sonuçların reddedilmesi~~  ✅ **Kod/yerel kapsam**
- Mükerrer kayıtların önlenmesi
- Geçmiş veri aktarımının devam ettirilebilmesi
- Veritabanına kaydetme ve okuma
- Kaynak siteye erişilememe
- Bozuk veya eksik veri
- Zamanlanmış fonksiyon
- İstatistik hesaplamaları
- Yönetim paneli yetkilendirmesi
- Yedekleme ve geri yükleme yönergeleri

Test verilerini gerçek sonuçlardan ayır. Gerçek çekiliş sonucu yerine rastgele veri oluşturup başarı göstermeye çalışma.

## 14. README ve kurulum rehberi

Türkçe bir README oluştur ve şu adımları anlat:

1. Projeyi yerel bilgisayarda çalıştırma
2. GitHub deposunu kullanma
3. Netlify bağlantısı ve yayınlama
4. Veritabanı oluşturma
5. Ortam değişkenlerini tanımlama
6. Migration çalıştırma
7. Geçmiş sonuçları otomatik aktarma
8. Zamanlanmış görevleri etkinleştirme
9. Logları kontrol etme
10. Otomatik güncellemeyi test etme
11. Yedekleme ve geri yükleme
12. Kaynak site değişirse yapılacaklar
13. E-posta bildirimi varsa yapılandırma
14. Sistemin manuel veri girişi olmadan çalıştığını doğrulama

Gerçekten bilinmeyen API anahtarlarını, bağlantıları veya hesap bilgilerini uydurma.

## 15. Uygulama sırası ve teslim raporu

Sadece öneri verme; erişebildiğin projede kod değişikliklerini gerçekten uygula.

İzlenecek sıra:

1. Projeyi analiz et.
2. Eksikleri listele.
3. Veri kaynaklarını ve kullanım koşullarını doğrula.
4. Veritabanı ve otomasyon altyapısını kur.
5. Geçmiş veri aktarımını hazırla.
6. Yeni sonuçların otomatik toplanmasını kur.
7. Veri doğrulama ve mükerrer kayıt kontrolünü uygula.
8. İstatistikleri otomatik güncelle.
9. Hata kaydı, yedekleme ve yönetim ekranını ekle.
10. Testleri çalıştır ve hataları düzelt.
11. README dosyasını tamamla.
12. Dağıtım durumunu ve kalan kurulum adımlarını raporla.

İş sonunda Türkçe rapor ver:

- Tamamlanan özellikler
- Değiştirilen dosyalar
- Kullanılan veri kaynakları
- Geçmiş verilerin aktarım durumu
- Veritabanı ve gerekli ortam değişkenleri
- Otomatik güncellemenin çalışma düzeni
- Test sonuçları
- Yedekleme ve hata bildirimi durumu
- Netlify yayın durumu
- Eksik bağlantılar ve tamamlanmamış işler
- Benim yapmam gereken adımlar
- Otomatik sistemi nasıl doğrulayacağım

**Nihai kabul kriteri:** Sistem geçmiş ve yeni sonuçları elle veri girişi olmadan otomatik toplamalı, doğrulamalı, kalıcı olarak saklamalı ve istatistikleri yenilemelidir. Bir veri kaynağı veya hesap bağlantısı eksikse bunu açıkça belirtmeli; hiçbir işlemin tamamlandığını doğrulamadan iddia etmemelidir.

---

## Canlı kurulumda kesinlikle tamamlanmamış işler
- Supabase projesinin oluşturulması, SQL migration çalıştırılması ve gerçek veri kaydetme testi.
- İzinli ve erişilebilir dört oyun kaynağından gerçek sonuç alınması.
- En eski çekilişten itibaren geçmiş kayıtların aktarılması ve devam ettirilmesi.
- Netlify zamanlanmış fonksiyonunun production ortamda çalışmasının kanıtlanması.
- Oyunların hepsinin arayüzde eksiksiz desteklenmesi ve otomatik istatistik yenilemesi.
- Yetkilendirilmiş yönetim paneli, alarm entegrasyonu ve üretim gözlemlenebilirliği.
- Uçtan uca tarayıcı, sunucu ve canlı bildirim testi.

## Kullanıcının yapması gerekenler
1. GitHub deposunun yedeğini alın.
2. Yeni ZIP içindeki dosyaları ana dizine yükleyin, Netlify dağıtımını doğrulayın.
3. Supabase projesini oluşturup `supabase/001_initial.sql` çalıştırın.
4. Netlify ortam değişkenlerine gerçek `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` ve güvenli biçimde yenilenmiş `COLLECTAPI_KEY` ekleyin.
5. Canlı `/api/health`, `/api/sync?game=sayisal`, `/api/sync?game=super`, `/.netlify/functions/history?game=sayisal` ve Scheduled Function loglarını doğrulayın.
6. Veri kaynakları hizmet vermiyorsa geçmiş aktarım ve 4 oyun için otomasyon tamamlanmış sayılmaz.

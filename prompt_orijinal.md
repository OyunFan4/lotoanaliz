# LOTOANALİZ AI — MEVCUT V2 YAPISINI KORUYARAK TAM GELİŞTİRME PROMPTU

## 1. ROL, HEDEF VE DEĞİŞMEZ KURALLAR
Kıdemli full-stack yazılım geliştiricisi, veri mühendisi, istatistikçi, PWA uzmanı, güvenlik ve kalite mühendisi olarak çalış. Sana mevcut **LotoAnaliz-AI-Otomatik-Kontrol-V2.zip** ve önceki gereksinimler verilecek. Hedef, Türkiye'deki **Çılgın Sayısal Loto** ve **Süper Loto** sonuçlarını resmî siteden izin verilen ölçüde otomatik alan; alamadığı çekilişlerin güvenli biçimde elle girilmesini sağlayan; kalıcı arşiv, ileri istatistik, tahmin kombinasyonu ve tarafsız geçmiş performans testleri sunan, Türkçe ve kurulabilir PWA geliştirmektir.

**En önemli şart: MEVCUT YAPIYI BOZMA.** Mevcut V2'nin `index.html`, `style.css`, gezinme düzeni, renk sistemi, mobil alt menüsü, çalışma mantığı, kayıtlı çekilişleri ve kolonları korunacak. Gerektiğinde mevcut dosyalara geriye uyumlu ekleme yap; bileşenleri/tasarımı baştan yaratma. Görsel iyileştirme ancak mevcut kimliği ve ekran akışını koruyorsa uygula. Kullanıcı verilerini hiçbir koşulda sessizce silme veya sıfırlama. İlk olarak ZIP'in tamamını oku, çalışan işlevleri belirle, regresyon testleri yaz ve dosya karşılaştırmasıyla korunduğunu doğrula.

Üretim düzeyinde olmayan özelliğe 'tamamlandı' deme. Gerçek resmî veri çekme testi başarısızsa bunu belirt, sahte sonuç üretme. Kullanıcı hiçbir aşamada verilerin eksiksiz olduğu yanılgısına düşürülmesin. Geliştirme aşamaları arasında kullanıcıdan gereksiz yeniden onay istemeden mevcut dosyalar üzerinde ilerle.

## 2. MEVCUT MİMARİ VE UYUMLULUK
Mevcut V2: bağımsız HTML/CSS/JavaScript istemci, IndexedDB (zorunluysa localStorage yedeği), Service Worker, manifest, mobil PWA; Python FastAPI `server.py` ile aynı origin üzerinden `/api/sync`, `/api/official`, `/api/health`; sunucuda SQLite. Bu sistemi **yerinde ve geriye uyumlu** geliştir. Kullanıcıdan sıfırdan kurulum veya ekran değişikliği isteme. Statik dosyalar mevcut yapıyla çalışabilsin; fakat sadece statik barındırmada resmî otomatik veri çekilemeyeceği açıkça gösterilsin. Tarayıcının resmî siteye doğrudan istek atmasına güvenme: sonuçları arka uç çeksin, doğrulasın ve istemciye aktarsın.

İleride PostgreSQL'e geçiş gerekiyorsa SQLAlchemy/Alembic veya eşdeğer migration ile veri kaybı olmadan geç; mevcut SQLite dosyasını taşıma ve yedekleme aracı oluştur. Mevcut uygulamanın kayıt biçimi ve oyun kodları (`sayisal`, `super`) korunmalı; veri şeması sürümlensin. Üretim için HTTPS, kalıcı disk/veritabanı, zamanlanmış iş ve gizli ortam değişkenleri sağla.

## 3. TEK RESMÎ KAYNAK VE ERİŞİM POLİTİKASI
Birincil ve yalnızca otomatik **resmî veri** kaynağı: `https://www.millipiyangoonline.com/`. Önce `https://www.millipiyangoonline.com/cekilis-takvimi`, ardından aynı resmî alan adındaki oyun sonuç sayfalarını, sayfalama ve tarih filtrelerini incele. Varsa **izinli resmî API veya yayımlanan dosya** tercih et. Web isteğinin yanıt kodu, tarih, içerik, kaynak URL, yönlendirme, robots/kullanım şartları, sıklık sınırları ve HTML şema değişikliklerini denetle.

403, 429, CAPTCHA, bot engeli, oturum gereksinimi veya erişim kısıtlamasını **aşma**; proxy rotasyonu, CAPTCHA çözme, sahte oturum ya da izinsiz API kullanma. Kontrollü tekrar dene ve geri çekil; sorunu kaydet ve manuel/CSV/JSON içe aktarma imkânını koru. Resmî alan adı dışında otomatik sonuç toplayıp 'resmî doğrulanmış' etiketi verme. Erişilebilen birkaç sonucu bütün arşiv tamamlandı şeklinde sunma.

## 4. HER AÇILIŞTA KONTROL + ARKA PLAN SENKRONİZASYONU
Uygulama her açılışta ve çevrimiçi durumuna döndüğünde otomatik senkronizasyon **denemesi** başlatsın. Her girişte istek atılabilir, ancak sunucu oran sınırı/cooldown uygular; sunucu istemcinin her açılışında resmî siteye yüzlerce istek atmaz. Oyunun ikisini de kontrol et; önce veri tabanındaki son kayıtları göster, güncelliği ve işin durumunu açıkça göster. 'Şimdi kontrol et' düğmesi olsun, fakat yönetimsel tam geçmiş taramasını herkes başlatamasın.

Tarayıcı kapalıyken yeni sonuçları incelemek için **sunucu zamanlayıcısı/cron** çalışsın. Sunucu işlemleri tekilleştirilsin (aynı oyuna paralel tarama olmasın). 200 başarılı ama veri bulunamadı, erişim engellendi, biçim değişti ve yeni kayıt eklendi durumları ayrı raporlansın. `last_checked_at` ve `last_successful_verified_at` ayrı tutulmalı. Cihaz çevrimdışıyken eski kayıtlar kullanılabilir, ancak güncelmiş gibi gösterilmez.

## 5. BÜTÜN TARİHSEL ÇEKİLİŞLERİ KONTROLLÜ TAMAMLAMA
**Yalnızca en son sekiz tahmini çekiliş numarasını denemek yeterli değildir.** Sayısal ve Süper Loto için resmî kaynakların sunduğu doğrulanabilir yıl, tarih, sonuç bağlantıları ve çekiliş numaralarından bir **keşif indeksi** oluştur. Tahmini çekiliş numarasını kesin çekiliş kabul etme. Oyunların tarihsel kurallarını ve başlangıç tarihlerini kaynakla doğrula. Yıl/dönem bazında tarama kuyruğu, sayfalama, devam etme işaretçisi, eksik kayıt raporu, istek hız sınırı, kısa partiler ve duraklat/yeniden başlat desteği ekle.

Her gerçek çekiliş için benzersiz anahtar `(oyun, kural sürümü/yıl, çekiliş numarası)` gibi belgelenmiş ve çakışmasız olmalı. Çekiliş kimliklerinin yıllara göre tekrar kullanılabileceğini dikkate al. Tarama kapsamını: keşfedilen çekiliş adedi, doğrulananlar, manuel kayıtlar, ulaşılamayanlar, şüpheliler ve taranmamış dönemler şeklinde raporla. 'Tüm çekilişler tamamlandı' yalnızca bağımsız ve doğrulanabilir kapsam kontrolüyle gösterilsin.

## 6. VERİ DOĞRULAMA VE TARİHSEL KURALLAR
Resmî sayfadan alınan çekilişin oyun türü, tarih, gerçek çekiliş numarası ve **tam altı farklı ana sayı** bulunduğunu doğrula. Çılgın Sayısal Loto'nun güncel ana sayıları 1–90, Süper Loto'nun güncel ana sayıları 1–60 aralığında; tarihsel kural değişikliklerinde o dönemin kurallarını uygula. Sayısal Loto sayfasındaki Joker/SüperStar gibi ek sonuçları ana altı sayıdan ayrı alanlarda sakla; ana altılıyı ayırt edemiyorsan sonuçları reddet/karantinaya al. Kaynak HTML değişikliklerinde yanlış altılı tahmin etme.

Her kayda oyun, yıl, çekiliş no, tarih, altı ana sayı, varsa ek sayılar, kaynak URL, indirildiği ve doğrulandığı zaman, kaynak içerik özeti/hash'i, doğrulama yöntemi ve durumunu ekle. 'Resmî siteden otomatik doğrulandı', 'Kullanıcı girdi', 'Dosyadan içe aktarıldı', 'Resmî kayıtla çelişiyor', 'Doğrulanamadı' gibi ayrı etiketler kullan.

## 7. ELLE GİRİŞ, CSV/JSON VE VERİ KORUMA
Otomatik alınamayan çekilişler kullanıcı tarafından oyun, tarih, çekiliş numarası, altı sayı ve isteğe bağlı kaynak/not ile kaydedilebilsin; cihazda **kalıcı kalsın**. Sayı aralığı, tekrarlanan sayı ve geçersiz tarih engellensin. Otomatik senkronizasyon **hiçbir manuel kaydı sessizce değiştirmesin/silmesin**. Aynı çekilişin resmî sonucu birebir uyarsa manuel kayıt, kaynağı koruyan doğrulama geçmişiyle eşleştirilsin. Farklıysa iki sürüm de/audit geçmişi korunup açık uyuşmazlık ekranında kullanıcıya gösterilsin; resmî ve manuel değer ayrı ayrı görülebilsin.

İçe aktarma varsayılanı 'güvenli birleştir' olsun; 'mevcut verileri değiştir' seçeneği ancak açıklamalı, iki aşamalı onay, otomatik ön-yedek ve geri alma imkânıyla kullanılsın. İçe aktarılan veriye otomatik olarak `official_verified` verme; resmî kaynak yeniden doğrulamadıkça statüsünü yükseltme. CSV, JSON yedek alma/geri yükleme, sürüm uyumluluğu ve veri bütünlüğü testlerini ekle. IndexedDB ile sunucu veritabanının hangisinin hangi verinin otoritesi olduğu net belgelensin; cihaz değiştirirken manuel verinin nasıl taşındığı açık olsun.

## 8. VERİTABANI TASARIMI VE MIGRATION
Oyunlar/KuralSürümleri, Çekilişler, ÇekilişSayıları, KaynakKontrolleri, Senkronizasyonİşleri, EksikÇekilişler, ManuelKayıtlar, VeriÇatışmaları, AnalizÇalışmaları, TahminGrupları, Tahminler, BacktestÇalışmaları ve BacktestTahminleri tablolarını kur; eski Games, Draws, DrawNumbers, SyncJobs, AnalysisRuns, PredictionSets, Predictions, BacktestRuns, BacktestPredictions modelini geriye uyumlu biçimde kapsa. FK, benzersizlik, indeks, şema sürümü, kayıt zamanı, algoritma sürümü, parametreler ve rastgelelik tohumu saklansın. Sunucu yedeği ve geri yükleme prosedürünü test et. Mevcut SQLite verilerinden PostgreSQL'e güvenli migration hazırla; geçiş zorunluysa veriyi koruyarak gerçekleştir.

## 9. TÜM SAYILAR İÇİN FREKANS ANALİZİ
İki oyunun verilerini ASLA birbirine karıştırma. Seçili tarih aralığı ve doğrulama filtreleriyle her 1–90 / 1–60 sayısı için toplam görülme, görülme oranı, beklenen görülme oranı, son tarih, kaç çekiliştir görülmediği, son 10/25/50/100/250 çekilişte sıklık, tüm geçmiş-yakın dönem farkını hesapla. Hiç görülmeyen sayıları da tabloda göster. Varsayılan ana analiz yalnızca resmî doğrulanan veriyi kapsasın; kullanıcı verisini katma seçeneği varsa sonuçları ayrı ve net etiketle. Yetersiz örneklem/eksik dönem uyarısı göster.

## 10. GELİŞMİŞ SAYI, ÇİFT VE ÜÇLÜ ANALİZİ
Tek/çift, düşük/yüksek (kullanıcı tanımlı eşik), sayı toplamı, minimum/maksimum, aralık kapsama, ardışık sayılar, sayılar arası farklar, tekrar eden sayılar, tüm ikili/üçlü ortak görülme sayısı ve beklenen değere göre karşılaştırmalar yap. Frekans sıralaması, çift/üçlü filtreleri ve örneklem sayısı göster. Gerekli durumlarda ki-kare/Monte Carlo testleri, etki büyüklüğü, güven aralığı ve çoklu karşılaştırma düzeltmesini kullan. Rastgele dalgalanmayı istatistiksel üstünlük diye pazarlama.

## 11. KOMBİNASYON OLUŞTURUCU — 8 STRATEJİ
Mevcut sekiz stratejiyi ve ekranını koru: (1) rastgele, (2) tüm geçmiş frekansı, (3) yakın dönem ağırlıklı, (4) tek/çift, (5) düşük/yüksek, (6) toplam/aralık, (7) birlikte görülme, (8) hibrit. Güncel oyun kuralına uygun altı benzersiz sayı, kullanıcı seçimiyle çoklu benzersiz kolon, kayıt, kopyalama ve dışa aktarma işlevleri olsun. Stratejinin dayandığı örneklem, parametre, analiz tarihi, algoritma sürümü ve tohum kaydedilsin. Veri azsa frekans temelli stratejilerin sınırlarını belirt. Puan varsa 'kazanma olasılığı değildir' ibaresi ekle. Adil ve bağımsız çekilişlerde her geçerli altılının eşit şansa sahip olduğu her zaman doğru belirtilsin.

## 12. GERİYE DÖNÜK TEST — VERİ SIZINTISIZ
Gerçek kronolojik backtest motoru oluştur. Her hedef çekilişin tahmini yalnızca hedef tarihten **önceki** doğrulanmış çekilişleri kullanmalı. Test dönemine ait sonuçlarla parametreleri optimize etme. Eşit kolon sayısı/eşit koşullu rastgele temel modelle karşılaştır. 0–6 eşleşme dağılımı, ortalama eşleşme, dönemsel sonuçlar, örneklem, belirsizlik ve uygun istatistiksel anlamlılığı göster. Başarılı değilse açıkça söyle. Veri yetersizse backtesti sonuç varmış gibi gösterme. Tarih sızıntısı için otomatik test yaz.

## 13. MOBİL ARAYÜZ — TASARIMI DEĞİŞTİRME
Mevcut V2'nin ekran yerleşimini, navigasyonunu, mevcut başlıklarını ve açık/koyu görünümünü mümkün olduğunca aynı bırak. Şunları mevcut ilgili ekranların İÇİNE küçük, uyumlu bölümler halinde ekle: 'Otomatik kontrol edildi / bağlantı yok', 'Son başarılı resmî veri', 'Arşiv kapsamı', 'Eksik çekilişler', 'Uyuşmazlıklar', 'Manuel çekiliş ekle', 'Tüm sayılar karşılaştırması', 'Performans karşılaştırması'. Mobil erişilebilirlik, dokunma alanları, ekran okuyucu etiketleri ve yükleniyor/boş/hata durumlarını geliştir. Logo/renk sistemi veya menü düzenini izinsiz yeniden tasarlama.

## 14. PWA VE ÇEVRİMDIŞI
Manifest, mevcut ikonlar, Service Worker ve IndexedDB'yi koru. Uygulama çevrimdışıyken açılabilsin, son kaydedilen çekilişleri/analizleri/kolonları gösterebilsin. Veriye 'son doğrulanma tarihi' iliştir. Gizli veya yönetici API sonuçlarını cache'e alma. Güncelleme sırasında kullanıcı kayıtlarını sıfırlama. İlk yükleme/kurulumda HTTPS ve tarayıcı kısıtlarını açıkça göster. iOS ve Android kurulum farkları belgelensin; kontrollü çevrimiçi yeniden eşitleme olsun.

## 15. BİLDİRİMLER
Kullanıcı izin verirse yeni resmî çekiliş doğrulandığında aynı sonucu tekrarsız bildirme. Push için uygun Web Push servis/subscription ve sunucu bileşeni oluştur; yapılandırma eksikse bildirim özelliğini kapalı/kurulum gerekli göster. Kullanıcı izni vermeden isteme. Pazarlama veya oynama yönünde baskı içermesin.

## 16. API, GÜVENLİK VE İZLEME
Mevcut `/api/health`, `/api/sync`, `/api/official` uç noktaları bozulmayacak. İhtiyaca göre `GET /api/games`, `/api/draws`, `/api/draws/latest`, `/api/draws/{id}`, `/api/analytics/frequency`, `/api/analytics/distribution`, `/api/analytics/cooccurrence`, `POST /api/predictions/generate`, `GET /api/predictions`, `POST /api/backtests/run`, `GET /api/backtests`, `GET /api/sync/status`, `POST /api/import/csv` ekle. Parametre/kayıt doğrulama, filtreleme, sayfalama, anlaşılır hata yanıtı, hız sınırı ve OpenAPI şeması sağla. Tam arşiv taraması, manuel sunucu içe aktarma ve push yönetimi gibi işlemleri yetkisiz herkese açma. `/api/sync` GET endpoint'i tarama işini tetiklediği için korunmalı/cooldown'lu olmalı; tercihen halka açık GET sadece durum okumalı, tetikleme güvenli sunucu işi olmalı. HTTPS, secret yönetimi, XSS, CSRF, SQL injection, log gizliliği ve kaynağa yöneltilen SSRF risklerini denetle; kaynak host sabit ve izinli olsun. SyncJobs, başarı/hata kayıtları ve yapı değişikliği uyarıları tut.

## 17. PERFORMANS, KULLANILABİLİRLİK VE SINIRLAR
Büyük geçmiş arşivini parti parti tara ve veritabanına idempotent yaz. Analizleri önbelleğe al, yeni çekilişle ilgili analizleri geçersiz kıl. Mobilde sayfalama, filtreleme, hesaplama sırasında yükleme göstergesi, zaman aşımı ve işlem iptali olsun. Kaynak kesilince uygulama kilitlenmesin. Yalnızca erişilebilir/izinli veri üzerinden ilerle; gerekli yerde manuel dosya kabul et.

## 18. TESTLER VE KABUL KRİTERLERİ
Pytest, uygun JS testleri ve mümkünse Playwright ile şu kontrolleri çalıştır: mevcut menü ve ekranlar değişmemiş; kullanıcı kayıtları sürüm yükseltince korunuyor; manuel çekiliş eklenip yeniden açınca duruyor; import varsayılanı güvenli birleştirme; otomatik sonuç manueli silmiyor; uyuşmazlık tespit ediliyor; yinelenen çekiliş oluşmuyor; hatalı tarihler/sayılar reddediliyor; Joker/SüperStar ana sayı değil; tarihsel kurallar uygulanıyor; iki oyun karışmıyor; tüm sayılar 1..N aralığında raporlanıyor; tarih filtresi, çift/üçlü hesapları doğru; sekiz strateji geçerli/benzersiz kombinasyon üretiyor; backtest geleceği kullanmıyor; 403/429/CAPTCHA ve HTML değişikliğinde başarısızlık doğru gösteriliyor; çevrimdışı veri korunuyor; manifest ve service worker geçerli; masaüstü/Android boyutlarında UI bozulmuyor; API yetki/rate limiting var.

Dış kaynağa erişim mümkün değilse sentetik fikstürlerle birim testlerini çalıştır ama bunları canlı entegrasyon testi diye gösterme. **Kabul koşulu:** çalışan kod + doğrulanabilir test çıktısı + gerçek bağlantı testi durum raporu + korunmuş veriler + tasarım regresyon kontrolü. 'Tam geçmiş arşiv' ancak gerçek kapsam doğrulamasıyla kabul edilebilir.

## 19. GELİŞTİRME SIRASI, TESLİMAT VE RAPORLAMA
Aşama 1: V2 ZIP'i aç, dosya/ekran/veri formatı envanteri ve yedek al.
Aşama 2: Resmî kaynak erişilebilirliğini ve kurallarını test et; erişim raporu yaz.
Aşama 3: Otomatik çekiliş keşfi, geçmiş dönem tarama kuyruğu, doğrulama ve eksik çekiliş sistemi kur.
Aşama 4: Manuel kayıtları koruyan güvenli eşleştirme, uyuşmazlık ve içe aktarma/geri alma geliştir.
Aşama 5: Veritabanı/migration, periyodik sunucu işi ve API'yi tamamla.
Aşama 6: Tüm sayılar, ikililer, üçlüler, istatistik ve filtreleri ekle.
Aşama 7: Sekiz stratejiyi doğrula; gerçek kronolojik backtest oluştur.
Aşama 8: Mevcut ekranlara minimum müdahale ile durum/kapsam/analiz/performans bölümleri ekle.
Aşama 9: PWA, offline, isteğe bağlı bildirimler, yetki, güvenlik ve otomatik testleri tamamla.
Aşama 10: HTTPS için dağıtım paketini ve kullanım talimatlarını oluştur.

Her aşamada: değiştirilmiş dosyalar, korunan özellikler, gerçekleştirilen testler, başarılı/başarısız kontroller, veriye erişim durumu ve bilinen eksikler raporlanmalı. V2 ile fark raporu üret. Son teslim **çalışır ZIP** içermeli: istemci kaynakları, backend, `requirements.txt`, `.env.example`, migration/taşıma araçları, README/KURULUM, veri kaynak raporu, testler ve sonuçları, API dokümanı, güvenli yedekleme/geri yükleme talimatı ve dağıtım rehberi. Test edilmemiş entegrasyonu tamamlanmış gösterme.

### DEĞİŞTİRİLEMEZ SON KURALLAR
- **Görsel yapı/menü/marka korunacak; kullanıcı veri kaybı olmayacak.**
- **Her girişte otomatik kontrol denemesi yapılacak; erişilebilir sonuçlar kalıcı kaydedilecek.**
- **Erişilemeyen sonuçlar elle girilebilecek ve sonraki girişlerde kalacak.**
- **Resmî ve kullanıcı kayıtları kaynağıyla ayırt edilecek; çatışma asla sessizce ezilmeyecek.**
- **Tüm erişilebilir tarihsel sonuçlar kademeli taranacak; taranamayanlar açıkça raporlanacak.**
- **Bütün sayılar karşılaştırılacak, analizin kapsamı ve veri kalitesi görülecek.**
- **Çekiliş sonuçları önceden kesin tahmin edilemez; herhangi bir kombinasyona sahte kazanma avantajı atfedilmeyecek.**
- **Engeller aşılmayacak; teknik olarak başarılamayanlar dürüstçe açıklanacak.**

Şimdi öncelikle mevcut V2 ZIP'ini incele, güvenli yedek al, ekranların/kayıtların regresyon testini oluştur ve resmî kaynak doğrulamasından başlayarak yukarıdaki aşamaları gerçekten kodlayıp test et. Yalnızca yapılacaklar listesi veya maket sunma.

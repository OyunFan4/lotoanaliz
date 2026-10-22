# LotoAnaliz AI — Nihai Test Paketi (V4)

Bu sürüm V3'ün HTML/CSS arayüzünü **değiştirmeden** geliştirilmiştir. Kurulabilir PWA, kayıtlı çekilişler, manuel veri girişi, yerel yedekleme, analiz ve kolon üretimi korunur.

## Bilgisayarda çalıştırma

Python 3.11+ kurulu olmalı. ZIP'i açıp klasör içinde:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn server:app --host 127.0.0.1 --port 8000
```

Tarayıcıda http://127.0.0.1:8000 açın. API için http://127.0.0.1:8000/docs ve http://127.0.0.1:8000/api/health adreslerine bakın. Windows'ta Python komutu yerine `py` kullanılabilir.

## Test

```bash
pip install pytest httpx
python -m pytest -q
node --check app.js
```

Ana ekrandan oyun değiştirin, Arşiv'e manuel çekiliş ekleyin, Analiz'e bakın, Üret'te kolon oluşturun, Diğer bölümünden JSON yedeği alın ve geri yükleyin. `/api/coverage?game=super` ile sunucudaki doğrulanmış sonuç sayısını inceleyin. İnternet erişimi yoksa eski verilerin hâlâ görüntülendiğini test edin.

## Otomatik veri ve tarihsel tarama

Uygulama her açılışta iki oyunu kontrol etmeyi dener; sunucu 20 dakikalık önbellek kullanır. Otomatik kontrol son çekilişler için **sınırlı adayları** dener, resmî site erişimi kesilirse kaydı doğrulanmış gibi göstermez. Geçmişe yönelik tarama için yönetici anahtarı ile `GET /api/admin/history/scan?game=super&year=2026&start=1&batch=3` kullanılabilir. Tarama kotalarına, yayıncının kullanım koşullarına ve erişim engellerine uyun.

Arşivdeki manuel kayıtlar cihazda kalır. Otomatik aktarım çatışma gördüğünde kullanıcı girişinin üstüne yazmaz. JSON yedeğini düzenli alın. CSV'nin yönetici API'siyle yüklenmesi resmî olarak doğrulanmış kayda dönüşmez.

## Üretim dağıtımı

`docker compose` üzerinden tek konteyner + kalıcı disk ile çalıştırabilirsiniz. `.env` dosyanıza uzun ve rastgele bir `LOTO_ADMIN_KEY` yazın (`.env.example` örneğine bakın). Docker Compose portu yalnızca `127.0.0.1:8000` adresine açar; dış erişim için Caddy/nginx gibi HTTPS ters proxy gereklidir. HTTPS alan adı kullanıldığında telefona PWA kurulumu mümkündür. Yönetici anahtarını tarayıcıya gömmeyin. Tek işçi ile zamanlayıcı yalnızca `LOTO_ENABLE_SCHEDULER=1` ise aktiftir. Bu paket tek konteyner, kalıcı SQLite tabanlı kurulum içindir.

## Uç noktalar

`/api/games`, `/api/draws`, `/api/draws/latest`, `/api/draws/export.csv`, `/api/analytics/frequency`, `/api/analytics/distribution`, `/api/analytics/cooccurrence`, `/api/predictions/generate`, `/api/backtests/run`, `/api/backtests`, `/api/sync`, `/api/sync/status`, `/api/coverage`, `/api/official`, `/api/import/csv` (yönetici), `/api/imports/unverified` (yönetici), `/api/admin/history/scan` (yönetici).

## Önemli sınırlamalar

Canlı resmî veri akışı bu çalışma ortamından doğrulanamadı. Mevcut veri arşivi eksiksiz değil. PostgreSQL migration, push bildirimleri, çapraz cihaz senkronizasyonu ve iOS/Android cihaz testleri bu teslimatta yok. Bunlar için `TAMAMLANMA_KONTROL_LISTESI.md` ve `PRODUCTION_LIMITATIONS.md` dosyalarını inceleyin. Üretilen kolonlar kazanma ihtimalini artırmaz.

## V8 eklemeleri — 22 Ekim 2026

Windows üzerinde `start-windows.bat` dosyasına çift tıklayabilirsiniz. Ardından `http://127.0.0.1:8000` ve `http://127.0.0.1:8000/docs` adreslerini açın. Yönetici anahtarını ortam değişkenine atamadan yetkili tarama API'si çalışmaz. İnternetten erişmek için bir alan adı ve HTTPS ters proxy gerekir (`Caddyfile.example` örnektir).

Yeni API uç noktaları:
- `/api/analytics/significance?game=super` — örneklem yeterliyse Monte Carlo istatistiksel sapma testi.
- `/api/analytics/details?game=sayisal` — sayı farkı, minimum/maksimum ve aralık istatistikleri.
- `/api/admin/history/progress?game=super&year=2026` — yetkili tarama imleci.
- `/api/admin/history/resume?game=super&year=2026&batch=3` — yetkili kontrollü taramayı kaldığı yerden sürdürme.

Yeni `test_v8.py` ile toplam **19 pytest** testi başarılı. `KULLANICI_TEST_PLANI.md` manuel kontrol adımlarını içerir. `TAMAMLANMA_KONTROL_LISTESI.md` tamamlanan ve eksik kalan gereksinimleri açıkça ayırır.

**Sınırlama:** Bu ZIP, ismi V8 olsa da tam resmî arşivi ve üretim dağıtımını içeren bitmiş ürün değildir. Bu çalışma ortamında `www.millipiyangoonline.com` doğrudan DNS bağlantısı başarısız oldu. Site engelleri aşılmadı; gerçek arşiv verisi üretilmedi. Gerçek Web Push, PostgreSQL, canlı HTTPS dağıtım, Android/iOS cihaz testi yapılmadı.

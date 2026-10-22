# LotoAnaliz AI V8 — Kullanıcı kabul testleri

- [ ] `start-windows.bat` çalışıyor, `http://127.0.0.1:8000` açılıyor.
- [ ] Sayısal Loto ve Süper Loto sekmeleri çalışıyor.
- [ ] İnternet kesildiğinde önbelleklenmiş arayüz açılıyor.
- [ ] Manuel çekiliş girip yeniden açınca kayıt korunuyor.
- [ ] JSON yedeği alınıp geri yüklenince mevcut kayıtlar silinmiyor.
- [ ] Aynı çekiliş farklı sayılarla eklenirse çakışma uyarısı çıkıyor.
- [ ] `http://127.0.0.1:8000/api/coverage?game=super` doğrulanan kayıt sayısını gösteriyor.
- [ ] `http://127.0.0.1:8000/api/analytics/significance?game=super` örneklem yetersizse bunu bildiriyor.
- [ ] Siteden çekilemeyen kayıtlar resmî doğrulanmış gibi işaretlenmiyor.
- [ ] Telefon üzerinden HTTPS adresi ile ana ekrana kurulum (manuel cihaz testi gerektirir).
- [ ] Resmî sonuçların canlı bağlantıyla alınması (erişilebilir sunucu ve izin gerekli).

## Yönetici tarihsel tarama

Sadece resmî sitede izin verilen erişim için. Uzun bir yönetici anahtarı tanımlayın (`LOTO_ADMIN_KEY`). Anahtarı kullanıcıya açık tarayıcı koduna koymayın.

```bash
curl -H "x-admin-key: SIZIN_GIZLI_ANAHTARINIZ" 'http://127.0.0.1:8000/api/admin/history/resume?game=super&year=2026&batch=3'
```

Her çağrı kontrollü küçük partiyi dener ve kaldığı imleci saklar. Bütün geçmişin tamamlandığını iddia etmez.

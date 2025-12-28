# GitHub Repository Traffic Monitoring Kılavuzu

## Genel Bakış

Bu araçlar GitHub repository'lerinizin trafik istatistiklerini izlemenizi sağlar. İki farklı kullanım şekli vardır:

1. **Otomatik İzleme (GitHub Actions)**: Bu repository için otomatik olarak çalışır
2. **Manuel Tüm Repolar İzleme**: Tüm repolarınız için manuel olarak çalıştırabilirsiniz

## 1. Otomatik Traffic İzleme

### Nasıl Çalışır?

- `.github/workflows/traffic-monitor.yml` workflow dosyası her gün otomatik olarak çalışır
- Repository'nin trafik istatistiklerini toplar
- Workflow loglarında sonuçları görüntüler

### Manuel Çalıştırma

1. GitHub repository sayfanıza gidin
2. "Actions" sekmesine tıklayın
3. "Repository Traffic Monitor" workflow'unu seçin
4. "Run workflow" butonuna tıklayın

### Toplanan Veriler

- **Views**: Son 14 gün içinde görüntüleme sayıları
- **Clones**: Son 14 gün içinde clone sayıları
- **Popular Paths**: En çok ziyaret edilen dosyalar/klasörler
- **Referrers**: Ziyaretçilerin geldiği siteler

## 2. Tüm Repolar İçin Manuel İzleme

### Gereksinimler

```bash
pip install -r requirements.txt
```

veya

```bash
pip install requests
```

### GitHub Token Oluşturma

1. GitHub hesabınıza giriş yapın
2. Sağ üst köşede profil fotoğrafınıza tıklayın → **Settings**
3. Sol menüden **Developer settings**'e tıklayın
4. **Personal access tokens** → **Tokens (classic)**'e tıklayın
5. **Generate new token (classic)** butonuna tıklayın
6. Token için açıklayıcı bir isim girin (örn: "Traffic Monitor")
7. **Expiration**: İstediğiniz süreyi seçin
8. **Select scopes** bölümünde şu yetkileri seçin:
   - ✅ `repo` (Full control of private repositories)
9. Sayfanın altındaki **Generate token** butonuna tıklayın
10. ⚠️ **ÖNEMLİ**: Token'ı kopyalayın ve güvenli bir yere kaydedin! Sayfayı kapatınca bir daha göremezsiniz.

### Kullanım

```bash
python fetch_all_repos_traffic.py <GITHUB_TOKEN> [USERNAME]
```

**Parametreler:**
- `GITHUB_TOKEN`: Oluşturduğunuz GitHub token
- `USERNAME`: (Opsiyonel) GitHub kullanıcı adınız. Belirtmezseniz token sahibinin repoları listelenir.

**Örnekler:**

```bash
# Authenticated user'ın tüm repoları için
python fetch_all_repos_traffic.py ghp_xxxxxxxxxxxxxxxxxxxx

# Belirli bir kullanıcının tüm repoları için
python fetch_all_repos_traffic.py ghp_xxxxxxxxxxxxxxxxxxxx muratkarahan
```

### Çıktı Örneği

```
================================================================================
TRAFFIC STATISTICS FOR ALL REPOSITORIES
Generated: 2025-12-28 10:00:00 UTC
================================================================================

Repository                               Views           Clones         
--------------------------------------------------------------------------------
muratkarahan/sdr_dsp                     45 (23 unique)  12 (8 unique)  
muratkarahan/project1                    32 (18 unique)  8 (5 unique)   
muratkarahan/project2                    15 (10 unique)  3 (2 unique)   
--------------------------------------------------------------------------------
TOTAL                                    92 (51 unique)  23 (15 unique) 
================================================================================

📊 Total Repositories: 3
👁️  Total Views: 92 (Unique: 51)
📥 Total Clones: 23 (Unique: 15)
================================================================================

✅ Detailed traffic data saved to all_repos_traffic_20251228_100000.json
```

### JSON Çıktısı

Script ayrıca detaylı bilgileri JSON formatında kaydeder:

```json
[
  [
    "muratkarahan/sdr_dsp",
    {
      "views": {
        "count": 45,
        "uniques": 23
      },
      "clones": {
        "count": 12,
        "uniques": 8
      }
    }
  ],
  ...
]
```

## Güvenlik Notları

⚠️ **Token Güvenliği:**
- GitHub token'larınızı asla public repository'lerde paylaşmayın
- Token'ları kod içine yazmayın
- Token'ları environment variable olarak kullanın veya güvenli bir şekilde saklayın
- Kullanmadığınız token'ları silin

## Sık Sorulan Sorular

**S: Traffic verileri ne kadar geriye gider?**
C: GitHub API son 14 günün verilerini sağlar.

**S: Token yetkisi neden gerekli?**
C: Private repository'ler için de trafik verisine erişebilmek için `repo` yetkisi gerekir.

**S: Workflow neden çalışmıyor?**
C: GitHub Actions'ın repository'de aktif olduğundan emin olun. Settings → Actions → General'dan kontrol edebilirsiniz.

**S: Rate limit hatası alıyorum?**
C: GitHub API'sinin rate limit'i vardır. Çok fazla repository varsa aramalar arasında bekleme süresi eklenmelidir.

## Sorun Giderme

### "Bad credentials" hatası
- Token'ın doğru olduğundan emin olun
- Token'ın süresi dolmamış olmalı
- Token'ın `repo` yetkisi olmalı

### "Not Found" hatası
- Repository adının doğru yazıldığından emin olun
- Private repository'ler için token'ın gerekli yetkilere sahip olduğundan emin olun

### "Rate limit exceeded" hatası
- Bir süre bekleyin
- Daha az repository için sorgulama yapın
- Authenticated request'ler saatte 5000 istekle sınırlıdır

## Katkıda Bulunma

Bu araçları geliştirmek için pull request gönderebilirsiniz!

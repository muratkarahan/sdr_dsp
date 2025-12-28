# sdr_dsp
sdr dsp

## GitHub Repository Traffic Monitoring

Bu depo, GitHub repository trafiğini izlemek için araçlar içerir.

### Otomatik Traffic İzleme (GitHub Actions)

Bu depo için otomatik olarak her gün trafik istatistikleri toplanır:
- GitHub Actions workflow günlük olarak çalışır
- Views, clones, popüler pathler ve referrer'ları toplar
- Workflow manuel olarak da tetiklenebilir

### Tüm Repolar İçin Traffic İzleme

Tüm repolarınızın trafik istatistiklerini görmek için `fetch_all_repos_traffic.py` scriptini kullanabilirsiniz:

#### Kullanım

```bash
python fetch_all_repos_traffic.py <github_token> [username]
```

#### Parametreler

- `github_token`: GitHub personal access token (repo yetkisi ile)
- `username`: GitHub kullanıcı adı (opsiyonel, varsayılan olarak authenticated user)

#### Örnek

```bash
python fetch_all_repos_traffic.py ghp_xxxxxxxxxxxx muratkarahan
```

#### GitHub Token Oluşturma

1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token (classic)" butonuna tıklayın
3. Token için bir isim verin (örn: "Traffic Monitor")
4. `repo` yetkisini seçin
5. Token'ı oluşturun ve kopyalayın

#### Çıktı

Script şu bilgileri gösterir:
- Her repository için view sayıları (toplam ve benzersiz)
- Her repository için clone sayıları (toplam ve benzersiz)
- Tüm repository'ler için toplam istatistikler
- Detaylı JSON dosyası olarak kaydedilir

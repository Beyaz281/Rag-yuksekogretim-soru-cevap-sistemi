# KBU Yönetmelik RAG Asistanı

Karabük Üniversitesi yönetmeliklerine soru sorulabilen RAG tabanlı chatbot. Streamlit arayüzü, Google Gemini veya yerel Ollama modelleri ve ChromaDB vektör veritabanı kullanır.

## Özellikler

- Çoklu oturum yönetimi (sohbet geçmişi JSON'da kalıcı)
- Sohbet geçmişine duyarlı sorgu yeniden yazma
- Türkçe / İngilizce dil desteği (mevcut mesajlar da çevrilir)
- **Model seçici:** Chat alanının üstünden Gemini veya yerel Qwen2.5 7B arasında anında geçiş
- Hover ile açılan ⋮ menü: sabitle, yeniden adlandır, yazdır, sil
- Renk, yazı tipi ve boyut özelleştirme paneli
- Yanıtlarda madde numarası + kaynak dosya gösterimi
- Kullanılan kaynaklar kalıcı olarak saklanır (sekme/oturum değişiminde kaybolmaz)
- Günlük API kotası aşılınca yenilenme saati gösterilir

## Desteklenen Modeller

| Model | Sağlayıcı | Gereksinim |
|---|---|---|
| ☁️ Gemini 2.5 Flash | Google API | `GOOGLE_API_KEY` |
| 🖥️ Qwen2.5 7B | Ollama (yerel) | Ollama + `ollama pull qwen2.5:7b` |

> Embedding her zaman Gemini (`gemini-embedding-001`) ile yapılır — ChromaDB bu embedding ile oluşturulmuştur. Sadece yanıt üretimi (LLM) modeli değişir.

## Mimari

```
PDF  ──►  pdf_to_markdown.py  ──►  Markdown
                                      │
                          MarkdownHeaderTextSplitter
                                      │
                                   Chunk'lar
                                      │
                          Gemini Embedding (gemini-embedding-001)
                                      │
                                  ChromaDB  ◄──── app.py (Streamlit UI)
                                               ├── config.py   (modeller, temalar, çeviri)
                                               ├── sessions.py
                                               └── rag.py      (Gemini veya Ollama LLM)
```

## Desteklenen PDF'ler

`./data` klasörüne eklenecek yönetmelikler:

| Dosya | İçerik |
|---|---|
| `sinav.pdf` | Ön Lisans & Lisans Eğitim-Öğretim ve Sınav Yönetmeliği |
| `yatay_gecis.pdf` | Yatay Geçiş, Çift Anadal & Yan Dal Yönetmelikleri |
| `dgs.pdf` | DGS (Dikey Geçiş) Yönetmeliği |
| `ogrenci_konseyi.pdf` | Öğrenci Konseyi Yönetmeliği |

> Farklı isimde PDF eklenebilir; `ingest.py` klasördeki tüm PDF'leri otomatik işler.

## Kurulum (uv ile)

### 1. uv yükle (henüz yoksa)
```bash
pip install uv
```

### 2. Sanal ortam oluştur (Python 3.10)
```bash
uv venv --python 3.10
```

### 3. Ortamı aktif et
```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 4. Bağımlılıkları yükle
```bash
uv pip install -r requirements.txt
```

### 5. API anahtarını ayarla
`.env` dosyası oluştur:
```
GOOGLE_API_KEY=buraya_anahtarini_yaz
```

### 6. PDF'leri `./data` klasörüne koy
```
kbu_rag/
  data/
    sinav.pdf
    yatay_gecis.pdf
    ...
```

### 7. Vektör veritabanını oluştur (bir kez çalıştır)
```bash
python ingest.py
```

### 8. Uygulamayı başlat
```bash
streamlit run app.py
```

---

## Yerel Model Kurulumu (Qwen2.5 7B)

İnternet bağlantısı olmadan veya gizlilik için yerel model kullanmak istiyorsan:

### 1. Ollama'yı kur
[ollama.com](https://ollama.com) adresinden indir ve kur.

### 2. Modeli çek (~4.7 GB)
```bash
# Windows — Ollama kurulumdan sonra PATH güncellenmemişse tam path kullan:
"C:\Users\<KullaniciAdi>\AppData\Local\Programs\Ollama\ollama.exe" pull qwen2.5:7b
```

### 3. langchain-ollama yükle
```bash
uv pip install langchain-ollama
```

Bundan sonra uygulamada dropdown'dan `🖥️ Qwen2.5 7B (Local)` seçilebilir. Ollama'nın arka planda çalışıyor olması gerekir (kurulumdan sonra otomatik başlar).

---

## Başka PC'ye Taşıma

**Seçenek A — `chroma_db` klasörüyle taşı (hızlı):**
- `chroma_db/` klasörünü projeyle birlikte kopyala
- `ingest.py` çalıştırmana gerek yok
- 1–6 ve 8. adımları uygula, 7. adımı atla

**Seçenek B — Sıfırdan kur:**
- `chroma_db/` olmadan taşı
- Tüm adımları uygula (7. adım dahil)

---

## Proje Yapısı

```
kbu_rag/
├── app.py               # Streamlit arayüzü (UI + model seçici)
├── config.py            # Çeviri sözlüğü, tema sabitleri, model tanımları (MODELS)
├── sessions.py          # Sohbet oturumu yönetimi (JSON kalıcılığı)
├── rag.py               # RAG motoru (LangChain + Gemini veya Ollama)
├── ingest.py            # PDF → Markdown → ChromaDB pipeline
├── pdf_to_markdown.py   # PDF'i Markdown'a çeviren modül
├── requirements.txt     # Bağımlılıklar (langchain-ollama dahil)
├── .env                 # API anahtarı (git'e ekleme!)
├── .streamlit/
│   └── config.toml      # Streamlit toolbar ayarları
├── icons/
│   ├── user.png         # Kullanıcı avatarı
│   └── robot.png        # Asistan avatarı
├── data/                # PDF dosyaları
├── chroma_db/           # Vektör veritabanı (otomatik oluşur)
└── chat_sessions.json   # Sohbet geçmişi (otomatik oluşur)
```

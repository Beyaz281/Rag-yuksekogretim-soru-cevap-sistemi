# 🎓 RAG Tabanlı Yükseköğretim Yönetmeliği Soru-Cevap Sistemi

[TÜBİTAK 2209-A Destekli]


Bu araştırma projesi, **TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı** kapsamında onaylanmış ve desteklenmeye hak kazanmıştır. Bilgisayar mühendisliği bitirme çalışması olarak yürütülen projenin temel amacı; yükseköğretim mevzuatları ve Karabük Üniversitesi Önlisans/Lisans Eğitim-Öğretim ve Disiplin yönetmelikleri üzerinde halüsinasyon (doğru olmayan bilgi üretimi) riskini sıfırlayarak çalışan, Retrieval-Augmented Generation (RAG) tabanlı akademik bir yapay zeka asistanı geliştirmektir.

---

## 📌 Proje Bilgileri
- **Destekleyen Kurum:** TÜBİTAK (Bilim İnsanı Destek Programları Başkanlığı - BİDEB)
- **Program Türü:** 2209-A - Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı
- **Proje Başlığı:** RAG Tabanlı Yükseköğretim Yönetmeliği Soru-Cevap Sistemi
- **Kurum:** Karabük Üniversitesi, Mühendislik Fakültesi, Bilgisayar Mühendisliği

---

## 🛠️ Teknolojik Altyapı
- **Geliştirme Ortamı:** VS Code & Python
- **Veri İşleme & OCR:** NLTK, Pandas, PyPDF2, pdfminer
- **Vektörel Temsil & Hafıza:** Vector Embeddings & Vektör Veritabanı
- **Büyük Dil Modeli (LLM):** Gemini API / ChatGPT (OpenAI)
- **Kullanıcı Arayüzü:** Python Tabanlı Web Prototipi

---

## 📅 12 Aylık Proje Yol Haritası (TÜBİTAK Onaylı Plan)

### 1. Hazırlık ve Bilimsel Temel (1. Ay)
- **Literatür Taraması:** RAG mimarisi, Doğal Dil İşleme (NLP) teknikleri ve BDM'lerin yasal metinlerdeki performansı (özellikle halüsinasyon sorunları) incelendi.
- **Teknik Kurulum:** VS Code ve temel Python kütüphaneleri hazırlandı.

### 2. Veri Toplama ve Dijitalleştirme (2. Ay)
- **Veri Kaynakları:** Karabük Üniversitesi Önlisans/Lisans Eğitim-Öğretim ve Disiplin yönetmelikleri PDF formatında toplandı.
- **OCR ve Dönüştürme:** PDF belgeleri temiz `.txt` formatına dönüştürüldü.
- **Veri Temizliği:** Sayfa numaraları, üst/alt bilgiler, dipnot gürültüleri ayıklandı ve karakter hataları düzeltildi.

### 3. Veri Yapılandırma ve Chunking (3. Ay)
- **Parçalama Stratejisi:** Metinler, bağlamı kaybetmeyecek şekilde yönetmelik maddeleri ve fıkraları baz alınarak anlamlı bölümlere (chunks) ayrıldı.
- **Meta-veri Etiketleme:** Her parçaya; yönetmelik adı, madde numarası ve yayın tarihi gibi bilgiler eklenerek sınıflandırıldı.

### 4. Embedding ve Vektör Veritabanı (4. Ay)
- **Vektörel Temsil:** Yapılandırılan metin parçaları "Vector Embeddings" yöntemiyle sayısal vektörlere dönüştürüldü.
- **Veritabanı Kurulumu:** Vektörler, hızlı anlamsal arama yapmaya olanak tanıyan özel bir vektör veritabanında saklandı.

### 5. RAG Altyapısı ve Model Entegrasyonu (5. - 6. Ay)
- **Model Entegrasyonu:** Gemini API veya ChatGPT gibi güncel BDM'ler sisteme entegre edildi.
- **Arama ve Eşleşme:** Kullanıcı sorusu geldiğinde, vektör veritabanından en benzer maddeyi bulup getiren arama algoritması kuruldu.
- **Referanslı Yanıt:** Sistemin yanıt verirken ilgili yönetmelik maddesini değiştirmeden referans (atıf) olarak sunması sağlandı.

### 6. Prototip Geliştirme ve Test (7. - 9. Ay)
- **Web Arayüzü:** Kullanıcıların soru sorabileceği Python tabanlı bir web prototipi geliştirildi.
- **Performans Testleri:** Hazırlanan yüzlerce test sorusuyla yanıt doğruluğu, kaynak eşleşme oranı ve hızı ölçüldü.
- **İyileştirme:** Halüsinasyon veya yanlış eşleşme tespit edilen durumlarda embedding modelleri ve chunking yöntemleri güncellendi.

### 7. Sonuç ve Raporlama (10. - 12. Ay)
- **Kullanıcı Deneyimi (UX):** Karabük Üniversitesi'ndeki öğrenci ve idari personel ile pilot uygulamalar yapılarak geri bildirim toplandı.
- **TÜBİTAK Sonuç Raporu:** Elde edilen bulguları, doğruluk oranlarını ve bilimsel katkıyı içeren nihai rapor hazırlandı.

---

### ⚠️ Risk Yönetimi ve B Planı
Eski PDF belgelerinde yaşanabilecek karakter bozulmalarına ve OCR kaymalarına karşı, farklı OCR motorlarının test edilmesi ve kritik yasal maddelerin manuel doğrulanması üzere bir B Planı devrededir.

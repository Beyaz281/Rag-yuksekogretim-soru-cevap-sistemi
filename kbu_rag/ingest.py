"""
ingest.py
---------
Pipeline:
  1. ./data klasöründeki PDF'leri Markdown'a çevir  (pdf_to_markdown.py)
  2. MarkdownHeaderTextSplitter ile chunk'la
  3. Google Gemini Embedding ile vektörleştir
  4. ChromaDB'ye kaydet
"""

import os
import time
from dotenv import load_dotenv

from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from pdf_to_markdown import pdf_to_markdown

# ── Ayarlar ────────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("HATA: .env dosyasında GOOGLE_API_KEY bulunamadı!")
print("✓ API anahtarı yüklendi.")


# ── Splitter Tanımı ────────────────────────────────────────────────────────
# Markdown başlık hiyerarşisine göre böl:
#   # Belge adı     -> en üst seviye
#   ## BÖLÜM        -> bölüm
#   ### Alt başlık  -> konu
#   #### MADDE      -> madde (en ince granülerlik)
HEADERS = [
    ("#",    "belge_basligi"),
    ("##",   "bolum"),
    ("###",  "alt_baslik"),
    ("####", "madde"),
]

splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=HEADERS,
    strip_headers=False,   # Başlığı chunk içinde tut -> retrieval için faydalı
)


def verileri_isle_ve_kaydet():
    data_klasoru  = "./data"
    chroma_klasoru = "./chroma_db"

    tum_parcalar: list[Document] = []

    # ── 1. PDF → Markdown → Chunk ──────────────────────────────────────────
    for dosya_adi in os.listdir(data_klasoru):
        if not dosya_adi.endswith(".pdf"):
            continue

        pdf_yolu = os.path.join(data_klasoru, dosya_adi)
        print(f"\n📄 İşleniyor: {dosya_adi}")

        # PDF'i Markdown'a çevir
        markdown_metin = pdf_to_markdown(pdf_yolu)
        print(f"   Markdown uzunluğu: {len(markdown_metin)} karakter")

        # MarkdownHeaderTextSplitter ile chunk'la
        parcalar = splitter.split_text(markdown_metin)
        print(f"   Oluşturulan chunk sayısı: {len(parcalar)}")

        # Her chunk'a kaynak dosya adını metadata olarak ekle
        for parca in parcalar:
            parca.metadata["kaynak"] = dosya_adi

        tum_parcalar.extend(parcalar)

    if not tum_parcalar:
        print("UYARI: Hiç chunk oluşturulamadı. ./data klasöründe PDF var mı?")
        return

    print(f"\n📦 Toplam chunk: {len(tum_parcalar)}")

    # ── 2. Embedding & ChromaDB ─────────────────────────────────────────────
    print("\n🔢 Vektörler hesaplanıyor (internet hızına bağlı)...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    # Rate limit aşmamak için chunk'ları küçük batch'lere böl
    BATCH_BOYUTU = 20        # Her seferinde max 20 chunk
    BEKLEME_SURESI = 12      # Batch'ler arası saniye

    vector_db = None
    for i in range(0, len(tum_parcalar), BATCH_BOYUTU):
        batch = tum_parcalar[i : i + BATCH_BOYUTU]
        batch_no = i // BATCH_BOYUTU + 1
        toplam_batch = (len(tum_parcalar) + BATCH_BOYUTU - 1) // BATCH_BOYUTU
        print(f"   Batch {batch_no}/{toplam_batch} gönderiliyor ({len(batch)} chunk)...")

        if vector_db is None:
            vector_db = Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=chroma_klasoru,
            )
        else:
            vector_db.add_documents(batch)

        # Son batch değilse bekle
        if i + BATCH_BOYUTU < len(tum_parcalar):
            time.sleep(BEKLEME_SURESI)

    print(f"\n✅ Tamamlandı! {len(tum_parcalar)} chunk '{chroma_klasoru}' klasörüne kaydedildi.")


if __name__ == "__main__":
    verileri_isle_ve_kaydet()

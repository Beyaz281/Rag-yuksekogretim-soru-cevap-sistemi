"""
PDF -> Markdown Dönüştürücü
Yönetmelik yapısını (BÖLÜM, MADDE) Markdown başlıklarına çevirir.
"""
import re
from pypdf import PdfReader


def pdf_to_markdown(pdf_yolu: str) -> str:
    """PDF dosyasını okuyup Markdown formatına çevirir."""
    reader = PdfReader(pdf_yolu)

    # Tüm sayfaları birleştir
    ham_metin = ""
    for sayfa in reader.pages:
        metin = sayfa.extract_text()
        if metin:
            ham_metin += metin + "\n"

    return metni_markdown_yap(ham_metin)


def metni_markdown_yap(metin: str) -> str:
    """Ham metni Markdown başlıklarıyla yapılandırır."""

    # 1. Türkçe karakterleri koru, sadece kontrol karakterlerini temizle
    metin = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', metin)

    # 2. Tire ile ayrılan sözcükleri birleştir (PDF satır kırma artefaktı)
    metin = re.sub(r'-\n([a-zA-ZçğışöüÇĞİŞÖÜ])', r'\1', metin)

    # 3. Satır ortasındaki gereksiz yeni satırları birleştir
    metin = re.sub(r'(?<=[a-zA-ZçğışöüÇĞİŞÖÜ,;])\n(?=[a-zA-ZçğışöüÇĞİŞÖÜ(])', ' ', metin)

    # 4. Çoklu boşlukları tek boşluğa indir
    metin = re.sub(r'[ \t]+', ' ', metin)

    # 5. Başlık: Belge adı (ilk satır)
    metin = re.sub(
        r'(KARABÜK ÜNİVERSİTESİ[^\n]+)',
        r'# \1',
        metin
    )

    # 6. BÖLÜM başlıklarını ## yap
    metin = re.sub(
        r'\n([A-ZÇĞİÖŞÜ]+\s+BÖLÜM)\n',
        r'\n## \1\n',
        metin
    )

    # 7. Bölüm alt başlıklarını ### yap (örn: "Amaç, Kapsam, Dayanak ve Tanımlar")
    metin = re.sub(
        r'\n((?:[A-ZÇĞİÖŞÜ][a-zçğışöü]+(?:,?\s)?){2,})\n(?=MADDE)',
        r'\n### \1\n',
        metin
    )

    # 8. MADDE satırlarını #### yap
    metin = re.sub(
        r'(MADDE\s+\d+\s*[–-])',
        r'\n#### \1',
        metin
    )

    # 9. Alt madde işaretlerini (a), b), 1), 2) vb.) düzenle
    metin = re.sub(r'\n([a-zçğışöü]\))', r'\n- \1', metin)

    # 10. Üç veya daha fazla boş satırı ikiye indir
    metin = re.sub(r'\n{3,}', '\n\n', metin)

    return metin.strip()


if __name__ == "__main__":
    import os

    data_klasoru = "./data"
    cikti_klasoru = "./data_markdown"
    os.makedirs(cikti_klasoru, exist_ok=True)

    for dosya in os.listdir(data_klasoru):
        if dosya.endswith(".pdf"):
            pdf_yolu = os.path.join(data_klasoru, dosya)
            md_dosya = dosya.replace(".pdf", ".md")
            md_yolu = os.path.join(cikti_klasoru, md_dosya)

            print(f"Dönüştürülüyor: {dosya} -> {md_dosya}")
            markdown_metin = pdf_to_markdown(pdf_yolu)

            with open(md_yolu, "w", encoding="utf-8") as f:
                f.write(markdown_metin)

            print(f"  ✓ {len(markdown_metin)} karakter yazıldı: {md_yolu}")

    print("\nTüm PDF'ler Markdown'a çevrildi!")

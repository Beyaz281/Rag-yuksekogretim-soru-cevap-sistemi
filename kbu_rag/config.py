"""
config.py  -  Ceviri sozlugu, tema sabitleri
Hicbir dis bagimliligi yok; duz Python sozlukleri.
"""

T = {
    "TR": {
        "title": "KBU Yönetmelik Asistanı",
        "subtitle": "Karabük Üniversitesi Ön Lisans & Lisans Eğitim-Öğretim ve Sınav Yönetmeliği",
        "chats": "Sohbetler",
        "new_chat": "Yeni Sohbet",
        "pinned": "Sabitlenmiş",
        "others": "Diğer sohbetler",
        "pin": "Sabitle",
        "unpin": "Sabitlemeyi kaldır",
        "rename": "Yeniden adlandır",
        "save": "✓ Kaydet",
        "cancel": "✗ İptal",
        "print": "Yazdır",
        "delete": "Sil",
        "examples": "Örnek sorular",
        "placeholder": "Yönetmelik hakkında ne öğrenmek istersiniz?",
        "searching": "Yönetmelik taranıyor...",
        "sources": "Kullanılan Kaynaklar",
        "no_db": "Vektör DB bulunamadı. Önce: python ingest.py",
        "load_err": "Sistem yüklenemedi",
        "settings": "Ayarlar",
        "lang_label": "Dil",
        "s_colors": "Renkler",
        "s_btn_bg": "Buton rengi",
        "s_btn_txt": "Buton yazı rengi",
        "s_app_bg": "Arka plan rengi",
        "s_sidebar_bg": "Kenar çubuğu rengi",
        "s_text": "Yazı rengi",
        "s_fonts": "Yazı tipi",
        "s_family": "Yazı ailesi",
        "s_size": "Yazı boyutu (px)",
        "s_reset": "Sıfırla",
        "model_label": "Model",
        "model_local_warn": "⚠️ Ollama yüklü ve model çekilmiş olmalı.",
        "sys_prompt": (
            "Sen Karabük Üniversitesi yönetmelik asistanısın. "
            "Soruları YALNIZCA aşağıdaki bağlamı kullanarak yanıtla. "
            "Cevap bağlamda yoksa: 'Bu bilgi yönetmelikte yer almıyor.' de. "
            "Madde numaralarına atıfta bulunurken kaynak dosyayı da belirt, "
            "örnek: (Madde 15 – sinav.pdf). "
            "ZORUNLU: Sohbet geçmişindeki dil ne olursa olsun, yanıtını her zaman TÜRKÇE yaz.\n\n"
        ),
        "rewrite_sys": (
            "Aşağıdaki sohbet geçmişi ve son soruya bakarak, son soruyu önceki konuşmaya "
            "ihtiyaç duymadan anlaşılabilir, bağımsız bir soruya dönüştür. "
            "Geçmişteki dil ne olursa olsun, ZORUNLU OLARAK TÜRKÇE yaz. "
            "SADECE yeniden yazılmış soruyu döndür.\n\nSohbet geçmişi:\n"
        ),
        "examples_list": {
            "Sınav Yönetmeliği": [
                "Devamsızlık sınırı nedir?",
                "Bütünleme sınavına kimler girebilir?",
                "Mazeret sınavı hakkı nasıl kullanılır?",
                "Tek ders sınavı nedir, kim girebilir?",
                "Mezun olmak için GANO kaç olmalı?",
            ],
            "Yatay Geçiş, Çift Anadal & Yan Dal": [
                "Yatay geçiş için GANO şartı nedir?",
                "Çift anadal programına nasıl başvurulur?",
                "Yan dal programı nedir, kaç kredi gerekir?",
                "Kurum içi yatay geçiş koşulları nelerdir?",
            ],
            "DGS (Dikey Geçiş)": [
                "DGS ile lisansa geçiş şartları nelerdir?",
                "DGS kontenjanları nasıl belirlenir?",
                "Ön lisans mezunu lisansa nasıl geçiş yapar?",
            ],
            "Öğrenci Konseyi": [
                "Öğrenci konseyi seçimleri nasıl yapılır?",
                "Öğrenci konseyi üyelik şartları nelerdir?",
                "Öğrenci konseyi başkanının görevleri neler?",
            ],
        },
    },
    "EN": {
        "title": "KBU Regulation Assistant",
        "subtitle": "Karabük University Associate & Bachelor Degree Education and Examination Regulation",
        "chats": "Chats",
        "new_chat": "New Chat",
        "pinned": "Pinned",
        "others": "Other chats",
        "pin": "Pin",
        "unpin": "Unpin",
        "rename": "Rename",
        "save": "✓ Save",
        "cancel": "✗ Cancel",
        "print": "Print",
        "delete": "Delete",
        "examples": "Example questions",
        "placeholder": "What would you like to know about the regulations?",
        "searching": "Searching regulations...",
        "sources": "Sources Used",
        "no_db": "Vector DB not found. Run: python ingest.py",
        "load_err": "System failed to load",
        "settings": "Settings",
        "lang_label": "Language",
        "s_colors": "Colors",
        "s_btn_bg": "Button color",
        "s_btn_txt": "Button text color",
        "s_app_bg": "Background color",
        "s_sidebar_bg": "Sidebar color",
        "s_text": "Text color",
        "s_fonts": "Typography",
        "s_family": "Font family",
        "s_size": "Font size (px)",
        "s_reset": "Reset",
        "model_label": "Model",
        "model_local_warn": "⚠️ Ollama must be installed and model pulled.",
        "sys_prompt": (
            "You are a Karabük University regulation assistant. "
            "Answer questions ONLY using the context below. "
            "If the answer is not in the context say: 'This information is not in the regulation.' "
            "When citing article numbers, include the source file, "
            "e.g.: (Article 15 – sinav.pdf). "
            "MANDATORY: Always respond in ENGLISH regardless of the language used in the conversation history.\n\n"
        ),
        "rewrite_sys": (
            "Given the chat history and the last question, rewrite the last question into "
            "a standalone question that can be understood without prior context. "
            "MANDATORY: Always write in ENGLISH regardless of the language in the history. "
            "Return ONLY the rewritten question.\n\nChat history:\n"
        ),
        "examples_list": {
            "Exam Regulation": [
                "What is the attendance limit?",
                "Who can take the make-up exam?",
                "How is an excuse exam requested?",
                "What is the single-course exam?",
                "What GPA is required to graduate?",
            ],
            "Transfer, Double Major & Minor": [
                "What GPA is needed for horizontal transfer?",
                "How to apply for a double major?",
                "What is a minor program?",
                "What are the in-university transfer conditions?",
            ],
            "DGS (Vertical Transfer)": [
                "What are the DGS transfer requirements?",
                "How are DGS quotas determined?",
                "How can an associate graduate transfer to bachelor's?",
            ],
            "Student Council": [
                "How are student council elections held?",
                "What are the membership requirements?",
                "What are the president's duties?",
            ],
        },
    },
}

# ── Model tanımları ─────────────────────────────────────────────────────────
MODELS = {
    "gemini": {
        "label": "☁️ Gemini 2.5 Flash",
        "provider": "gemini",
        "model_name": "gemini-2.5-flash",
    },
    "qwen2.5:7b": {
        "label": "🖥️ Qwen2.5 7B (Local)",
        "provider": "ollama",
        "model_name": "qwen2.5:7b",
    },
}

DEFAULT_MODEL = "gemini"

DEFAULT_SETTINGS = {
    "btn_bg":      "#0E518D",
    "btn_txt":     "#ffffff",
    "app_bg":      "#ffffff",
    "sidebar_bg":  "#f0f2f6",
    "text_color":  "#000000",
    "font_family": "Varsayılan / Default",
    "font_size":   16,
}

FONT_MAP = {
    "Varsayılan / Default": "sans-serif",
    "Arial":                "Arial, sans-serif",
    "Georgia (Serif)":      "Georgia, serif",
    "Courier (Monospace)":  "'Courier New', monospace",
    "Times New Roman":      "'Times New Roman', serif",
    "Trebuchet":            "'Trebuchet MS', sans-serif",
}

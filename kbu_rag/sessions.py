"""
sessions.py  -  Sohbet oturumu yonetimi (JSON kaliciligi)
Streamlit bagimliligi yok; saf Python.
"""

import os
import json
import uuid
from datetime import datetime

SESSIONS_FILE = "./chat_sessions.json"


def sessions_yukle() -> dict:
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def sessions_kaydet(sessions: dict) -> None:
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)


def yeni_oturum_olustur(lang: str = "TR") -> str:
    sid = str(uuid.uuid4())[:8]
    s = sessions_yukle()
    s[sid] = {
        "title":      "Yeni Sohbet" if lang == "TR" else "New Chat",
        "created_at": datetime.now().isoformat(),
        "messages":   [],
        "pinned":     False,
        "lang":       lang,
    }
    sessions_kaydet(s)
    return sid

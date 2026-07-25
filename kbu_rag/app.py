"""
app.py  -  KBU Yonetmelik RAG Chatbot  |  Streamlit arayuzu
Sadece UI kodu; is mantigi config/sessions/rag modullerinde.
"""

import os
import json

import streamlit as st
import streamlit.components.v1 as components

from config import T, DEFAULT_SETTINGS, FONT_MAP, MODELS, DEFAULT_MODEL
from sessions import sessions_yukle, sessions_kaydet, yeni_oturum_olustur
from rag import sistemi_yukle, yanit_uret, kaynak_etiketleri, mesajlari_cevir

# ── Sayfa konfigurasyon ──────────────────────────────────────────────────────
st.set_page_config(page_title="KBU Yonetmelik Asistani", page_icon="🎓", layout="wide")

# ── Session state baslangici ─────────────────────────────────────────────────
if "lang" not in st.session_state:
    st.session_state.lang = "TR"
if "settings" not in st.session_state:
    st.session_state.settings = DEFAULT_SETTINGS.copy()
if "selected_model" not in st.session_state:
    st.session_state.selected_model = DEFAULT_MODEL


def t(key):
    return T[st.session_state.lang][key]


# ── Dinamik CSS ──────────────────────────────────────────────────────────────
def css_uygula():
    s = st.session_state.settings
    font = FONT_MAP.get(s["font_family"], "sans-serif")
    sz = s["font_size"]
    st.markdown(f"""
<style>
/* Ust bosluk hizala */
.block-container {{ padding-top: 3rem !important; }}
section[data-testid="stSidebar"] > div:first-child {{ padding-top: 0.75rem !important; }}

/* Arka planlar */
.stApp {{ background-color: {s["app_bg"]} !important; }}
section[data-testid="stSidebar"] {{ background-color: {s["sidebar_bg"]} !important; }}

/* Genel yazi */
.stApp, .stMarkdown, .stMarkdown p,
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] div {{
    font-family: {font} !important;
    font-size: {sz}px !important;
    color: {s["text_color"]} !important;
}}
h1, h2, h3 {{
    font-family: {font} !important;
    color: {s["text_color"]} !important;
}}

/* Primary butonlar */
.stButton > button[kind="primary"],
.stButton > button[data-testid*="primary"] {{
    background-color: {s["btn_bg"]} !important;
    color: {s["btn_txt"]} !important;
    border-color: {s["btn_bg"]} !important;
}}

/* Sidebar hover menu */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {{
    position: relative !important;
    overflow: visible !important;
}}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:first-child {{
    flex: 1 1 auto !important;
    min-width: 0 !important;
    overflow: hidden !important;
}}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child {{
    position: absolute !important;
    right: 4px !important;
    top: 0 !important;
    bottom: 0 !important;
    width: 30px !important;
    flex: none !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    opacity: 0;
    transition: opacity 0.12s ease;
    z-index: 10 !important;
}}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:hover > div:last-child {{
    opacity: 1;
}}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:hover > div:first-child button {{
    opacity: 0.78 !important;
}}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child button {{
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid #d0d0d0 !important;
    border-radius: 5px !important;
    padding: 0 !important;
    min-height: 0 !important;
    height: 26px !important;
    width: 26px !important;
    font-size: 15px !important;
    line-height: 1 !important;
    color: #555 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.12) !important;
}}
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] > div:last-child button:hover {{
    background: #ebebeb !important;
    color: #111 !important;
}}
</style>
""", unsafe_allow_html=True)


css_uygula()

# ── Oturum baslangici ────────────────────────────────────────────────────────
if "current_session_id" not in st.session_state:
    s = sessions_yukle()
    if s:
        en_son = max(s.items(), key=lambda x: x[1].get("created_at", ""))[0]
        st.session_state.current_session_id = en_son
    else:
        st.session_state.current_session_id = yeni_oturum_olustur(st.session_state.lang)

# ── DB + sistem kontrolu ─────────────────────────────────────────────────────
if not os.path.exists("./chroma_db"):
    st.error(t("no_db"))
    st.stop()

try:
    _m = MODELS[st.session_state.selected_model]
    retriever, llm = sistemi_yukle(provider=_m["provider"], model_name=_m["model_name"])
except Exception as e:
    st.error(t("load_err") + f":\n```\n{e}\n```")
    st.stop()

# ── Ceviri kontrolu ──────────────────────────────────────────────────────────
if st.session_state.get("ceviri_gerekli"):
    del st.session_state["ceviri_gerekli"]
    _sv = sessions_yukle()
    _sid = st.session_state.current_session_id
    _msgs = _sv.get(_sid, {}).get("messages", [])
    if _msgs:
        _spin = "Mesajlar çevriliyor..." if st.session_state.lang == "TR" else "Translating messages..."
        with st.spinner(_spin):
            _sv[_sid]["messages"] = mesajlari_cevir(_msgs, st.session_state.lang, llm)
            _sv[_sid]["lang"] = st.session_state.lang
            sessions_kaydet(_sv)
    st.rerun()

# ── Yazdirma ─────────────────────────────────────────────────────────────────
def sohbeti_yazdir(sid):
    s = sessions_yukle()
    chat = s.get(sid, {})
    baslik = chat.get("title", "Sohbet")
    satirlar = []
    for m in chat.get("messages", []):
        rol = "Kullanici" if m["role"] == "user" else "Asistan"
        icerik = m["content"].replace("</", "<\\/")
        satirlar.append(
            '<div class="msg ' + m["role"] + '"><strong>' + rol + '</strong>: ' + icerik + '</div>'
        )
    rows = "".join(satirlar)
    html = (
        "<!DOCTYPE html><html lang='tr'><head><meta charset='UTF-8'>"
        "<title>" + baslik + "</title><style>"
        "body{font-family:Arial;max-width:800px;margin:40px auto;padding:0 20px}"
        "h2{border-bottom:2px solid #ccc;padding-bottom:8px}"
        ".msg{padding:10px 14px;margin:8px 0;border-radius:8px;line-height:1.5}"
        ".user{background:#f0f0f0}.assistant{background:#e8f4f8}"
        "@media print{body{margin:0}}"
        "</style></head><body><h2>" + baslik + "</h2>" + rows + "</body></html>"
    )
    components.html(
        "<script>var w=window.open('','_blank','width=860,height=700');"
        "w.document.write(" + json.dumps(html) + ");"
        "w.document.close();w.focus();w.print();</script>",
        height=0,
    )

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## " + t("chats"))
    if st.button(t("new_chat"), use_container_width=True, type="primary"):
        st.session_state.current_session_id = yeni_oturum_olustur(st.session_state.lang)
        st.rerun()
    st.divider()

    sessions = sessions_yukle()
    pinned = sorted(
        [(k, v) for k, v in sessions.items() if v.get("pinned")],
        key=lambda x: x[1].get("created_at", "")
    )
    others = sorted(
        [(k, v) for k, v in sessions.items() if not v.get("pinned")],
        key=lambda x: x[1].get("created_at", ""), reverse=True
    )
    if pinned:
        st.caption(t("pinned"))
    all_sessions = pinned + others

    for idx, (sid, sdata) in enumerate(all_sessions):
        if pinned and idx == len(pinned):
            st.caption(t("others"))

        baslik = sdata.get("title", "Sohbet")
        aktif = sid == st.session_state.current_session_id
        sabitli = sdata.get("pinned", False)

        if st.session_state.get("renaming_sid") == sid:
            yeni_ad = st.text_input("", value=baslik, key="ri_" + sid,
                                    label_visibility="collapsed")
            if st.button(t("save"), key="rok_" + sid, use_container_width=True):
                sessions[sid]["title"] = yeni_ad.strip() or baslik
                sessions_kaydet(sessions)
                del st.session_state["renaming_sid"]
                st.rerun()
            if st.button(t("cancel"), key="rcan_" + sid, use_container_width=True):
                del st.session_state["renaming_sid"]
                st.rerun()
            continue

        col_isim, col_menu = st.columns([0.88, 0.12])
        with col_isim:
            label = ("▶ " if aktif else "") + ("📌 " if sabitli else "") + baslik
            if st.button(label, key="sess_" + sid, use_container_width=True,
                         type="primary" if aktif else "secondary"):
                if sid != st.session_state.current_session_id:
                    if (sdata.get("lang", st.session_state.lang) != st.session_state.lang
                            and sdata.get("messages")):
                        st.session_state["ceviri_gerekli"] = True
                    st.session_state.current_session_id = sid
                st.rerun()
        with col_menu:
            with st.popover("⋮", use_container_width=True):
                pin_lbl = t("unpin") if sabitli else t("pin")
                if st.button(pin_lbl, key="pin_" + sid, use_container_width=True):
                    sessions[sid]["pinned"] = not sabitli
                    sessions_kaydet(sessions)
                    st.rerun()
                if st.button(t("rename"), key="ren_" + sid, use_container_width=True):
                    st.session_state["renaming_sid"] = sid
                    st.rerun()
                if st.button(t("print"), key="prt_" + sid, use_container_width=True):
                    st.session_state["print_sid"] = sid
                st.divider()
                if st.button(t("delete"), key="del_" + sid, use_container_width=True):
                    del sessions[sid]
                    sessions_kaydet(sessions)
                    if st.session_state.current_session_id == sid:
                        kalan = list(sessions.keys())
                        st.session_state.current_session_id = (
                            kalan[-1] if kalan else yeni_oturum_olustur(st.session_state.lang))
                    st.rerun()

if "print_sid" in st.session_state:
    sohbeti_yazdir(st.session_state.pop("print_sid"))

# ── Ana alan: baslik + dil + ayarlar ─────────────────────────────────────────
col_title, col_gap, col_lang, col_settings = st.columns([5, 2, 1, 1])

with col_title:
    st.markdown("### " + t("title"))
    st.caption(t("subtitle"))

with col_lang:
    lang_options = ["🇹🇷 TR", "🇬🇧 EN"]
    current_idx = 0 if st.session_state.lang == "TR" else 1
    secim = st.selectbox(
        t("lang_label"),
        lang_options,
        index=current_idx,
        key="lang_selectbox",
        label_visibility="collapsed",
    )
    yeni_lang = "TR" if secim == "🇹🇷 TR" else "EN"
    if yeni_lang != st.session_state.lang:
        st.session_state.lang = yeni_lang
        st.session_state["ceviri_gerekli"] = True
        st.rerun()

with col_settings:
    with st.popover(t("settings"), use_container_width=True):
        st.markdown("#### " + t("s_colors"))
        new_btn_bg    = st.color_picker(t("s_btn_bg"),     st.session_state.settings["btn_bg"],     key="cp_btn_bg")
        new_btn_txt   = st.color_picker(t("s_btn_txt"),    st.session_state.settings["btn_txt"],    key="cp_btn_txt")
        new_app_bg    = st.color_picker(t("s_app_bg"),     st.session_state.settings["app_bg"],     key="cp_app_bg")
        new_sidebar_bg= st.color_picker(t("s_sidebar_bg"), st.session_state.settings["sidebar_bg"],key="cp_sidebar_bg")
        new_text      = st.color_picker(t("s_text"),       st.session_state.settings["text_color"], key="cp_text")

        st.markdown("#### " + t("s_fonts"))
        font_options = list(FONT_MAP.keys())
        cur_font_idx = font_options.index(st.session_state.settings["font_family"]) \
                       if st.session_state.settings["font_family"] in font_options else 0
        new_font = st.selectbox(t("s_family"), font_options, index=cur_font_idx, key="sel_font")
        new_size = st.slider(t("s_size"), 12, 24, st.session_state.settings["font_size"], key="sl_size")

        new_settings = {
            "btn_bg": new_btn_bg, "btn_txt": new_btn_txt,
            "app_bg": new_app_bg, "sidebar_bg": new_sidebar_bg,
            "text_color": new_text, "font_family": new_font, "font_size": new_size,
        }
        if new_settings != st.session_state.settings:
            st.session_state.settings = new_settings
            st.rerun()
        st.divider()
        if st.button(t("s_reset"), use_container_width=True):
            st.session_state.settings = DEFAULT_SETTINGS.copy()
            st.rerun()

# ── Mevcut oturum mesajlari ──────────────────────────────────────────────────
sessions = sessions_yukle()
messages = sessions.get(st.session_state.current_session_id, {}).get("messages", [])

# ── Ornek sorular ────────────────────────────────────────────────────────────
with st.expander(t("examples")):
    for kategori, ornekler in t("examples_list").items():
        st.markdown("**" + kategori + "**")
        cols = st.columns(2)
        for i, o in enumerate(ornekler):
            with cols[i % 2]:
                if st.button(o, key="o_" + o):
                    st.session_state["hazir_soru"] = o

# ── Mesajlari goster ─────────────────────────────────────────────────────────
for mesaj in messages:
    avatar = "icons/user.png" if mesaj["role"] == "user" else "icons/robot.png"
    with st.chat_message(mesaj["role"], avatar=avatar):
        st.markdown(mesaj["content"])
        if mesaj["role"] == "assistant" and mesaj.get("sources"):
            with st.expander(t("sources")):
                for tag in mesaj["sources"]:
                    st.markdown("- `" + tag + "`")

# ── Model seçici + Kullanici girisi ─────────────────────────────────────────
# Model seçiciyi chat_input'un hemen üstüne yerleştir
st.markdown("""
<style>
/* Model seçici satırı - gönder butonuyla aynı hizada görünmesi için */
div[data-testid="stHorizontalBlock"].model-row {
    position: fixed;
    bottom: 68px;
    right: 1.5rem;
    width: auto;
    z-index: 999;
    background: transparent;
}
div[data-testid="stHorizontalBlock"].model-row select {
    font-size: 13px !important;
    padding: 2px 6px !important;
    height: 32px !important;
}
</style>
""", unsafe_allow_html=True)

_model_keys = list(MODELS.keys())
_model_labels = [MODELS[k]["label"] for k in _model_keys]
_current_idx = _model_keys.index(st.session_state.selected_model)

col_gap, col_model = st.columns([4, 1])
with col_model:
    _secim_label = st.selectbox(
        t("model_label"),
        _model_labels,
        index=_current_idx,
        key="model_selectbox",
        label_visibility="collapsed",
    )
    _secim_key = _model_keys[_model_labels.index(_secim_label)]
    if _secim_key != st.session_state.selected_model:
        st.session_state.selected_model = _secim_key
        if MODELS[_secim_key]["provider"] == "ollama":
            st.info(t("model_local_warn"))
        st.rerun()

hazir = st.session_state.pop("hazir_soru", None)
girdi = st.chat_input(t("placeholder"))
soru = hazir or girdi

if soru:
    sessions = sessions_yukle()
    oturum = sessions.get(st.session_state.current_session_id,
                          {"messages": [], "title": "Yeni Sohbet"})
    messages = oturum.get("messages", [])
    messages.append({"role": "user", "content": soru})
    with st.chat_message("user", avatar="icons/user.png"):
        st.markdown(soru)

    if len(messages) == 1:
        sessions[st.session_state.current_session_id]["title"] = (
            soru[:45] + ("..." if len(soru) > 45 else ""))

    with st.chat_message("assistant", avatar="icons/robot.png"):
        with st.spinner(t("searching")):
            yanit, docs = yanit_uret(
                soru, messages[:-1], retriever, llm,
                t("sys_prompt"), t("rewrite_sys"), st.session_state.lang,
            )
            st.markdown(yanit)
            not_found = ("yonetmelikte yer almiyor" in yanit.lower() or
                         "not in the regulation" in yanit.lower() or
                         yanit.startswith("⚠️"))
            tags = kaynak_etiketleri(docs) if (docs and not not_found) else []
            if tags:
                with st.expander(t("sources")):
                    for tag in tags:
                        st.markdown("- `" + tag + "`")

    asistan_mesaj = {"role": "assistant", "content": yanit}
    if tags:
        asistan_mesaj["sources"] = tags
    messages.append(asistan_mesaj)
    sessions[st.session_state.current_session_id]["messages"] = messages
    sessions[st.session_state.current_session_id]["lang"] = st.session_state.lang
    sessions_kaydet(sessions)

"""
rag.py  -  RAG motoru: yukleme, sorgulama, cevap uretme, ceviri
LangChain + Google Gemini / Ollama. Streamlit bagimliligi yok.
"""

import json
from datetime import datetime, timezone, timedelta as td
from functools import lru_cache

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

load_dotenv()


# Retriever her zaman Gemini embedding kullanır (DB bu embedding ile oluşturuldu)
@lru_cache(maxsize=1)
def _retriever_yukle():
    emb = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    vdb = Chroma(persist_directory="./chroma_db", embedding_function=emb)
    return vdb.as_retriever(search_type="similarity", search_kwargs={"k": 5})


def _llm_olustur(provider: str, model_name: str):
    """Seçilen sağlayıcıya göre LLM nesnesi döner."""
    if provider == "gemini":
        return ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
    elif provider == "ollama":
        try:
            from langchain_ollama import ChatOllama
        except ImportError:
            raise ImportError(
                "langchain-ollama kurulu değil. "
                "Yüklemek için: pip install langchain-ollama"
            )
        return ChatOllama(model=model_name, temperature=0.2)
    else:
        raise ValueError(f"Bilinmeyen provider: {provider}")


def sistemi_yukle(provider: str = "gemini", model_name: str = "gemini-2.5-flash"):
    """Retriever + LLM döner. Retriever cache'li, LLM her seferinde oluşturulur."""
    ret = _retriever_yukle()
    llm = _llm_olustur(provider, model_name)
    return ret, llm


def soruyu_yeniden_yaz(soru: str, gecmis: list, llm, rewrite_sys: str) -> str:
    """Geçmiş bağlamını kullanarak soruyu bağımsız bir forma dönüştürür."""
    if not gecmis:
        return soru
    gecmis_metni = "".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}\n"
        for m in gecmis[-6:]
    )
    p = ChatPromptTemplate.from_messages([
        ("system", rewrite_sys + gecmis_metni),
        ("human", "{soru}"),
    ])
    try:
        return (p | llm | StrOutputParser()).invoke({"soru": soru})
    except Exception:
        return soru


def quota_mesaji(lang: str) -> str:
    """Günlük kota aşıldığında yenilenme saatini içeren uyarı mesajı döner."""
    pt = timezone(td(hours=-8))
    tr = timezone(td(hours=3))
    now_pt = datetime.now(pt)
    yarin_gece = (now_pt + td(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    yenileme = yarin_gece.astimezone(tr)
    tarih = yenileme.strftime("%d.%m.%Y %H:%M")
    if lang == "EN":
        return f"⚠️ Daily API limit reached. Quota resets on **{tarih}** (Turkey time)."
    return f"⚠️ Günlük API limitine ulaşıldı. Kota **{tarih}** itibarıyla yenilenecek."


def yanit_uret(soru: str, gecmis: list, ret, llm,
               sys_prompt: str, rewrite_sys: str, lang: str):
    """RAG zincirini çalıştırır; (yanit, docs) döner."""
    try:
        arama = soruyu_yeniden_yaz(soru, gecmis, llm, rewrite_sys)
    except Exception:
        arama = soru
    try:
        docs = ret.invoke(arama)
    except Exception:
        docs = ret.invoke(soru)

    ctx_parts = []
    for d in docs:
        kaynak = d.metadata.get("kaynak", "")
        header = f"[Belge: {kaynak}]" if kaynak else ""
        ctx_parts.append((header + "\n" + d.page_content).strip())
    ctx = "\n\n---\n\n".join(ctx_parts)

    gecmis_metni = "".join(
        f"{'User' if m['role'] == 'user' else 'Assistant'}: {m['content']}\n"
        for m in gecmis[-6:]
    ) if gecmis else ""
    gecmis_bl = f"Previous conversation:\n{gecmis_metni}\n" if gecmis_metni else ""

    full_sys = sys_prompt + gecmis_bl + "Context:\n{context}"
    p = ChatPromptTemplate.from_messages([("system", full_sys), ("human", "{input}")])
    try:
        yanit = (p | llm | StrOutputParser()).invoke({"context": ctx, "input": soru})
    except Exception as e:
        err = str(e)
        if "429" in err or "RESOURCE_EXHAUSTED" in err:
            yanit = quota_mesaji(lang)
        else:
            yanit = f"⚠️ Hata: {err}" if lang == "TR" else f"⚠️ Error: {err}"
    return yanit, docs


def kaynak_etiketleri(docs) -> list:
    """Docs listesinden tekrarsız kaynak etiketleri döndürür."""
    seen = set()
    tags = []
    for doc in docs:
        m = doc.metadata
        tag = " | ".join(filter(None, [
            m.get("madde", ""), m.get("bolum", ""), m.get("kaynak", "yonetmelik")
        ]))
        if tag and tag not in seen:
            tags.append(tag)
            seen.add(tag)
    return tags


def mesajlari_cevir(messages: list, hedef_dil: str, llm) -> list:
    """Oturumdaki tüm mesajları tek LLM çağrısıyla hedef dile çevirir."""
    if not messages:
        return messages
    hedef_ad = "English" if hedef_dil == "EN" else "Turkish"
    icerikler = [{"i": i, "c": m["content"]} for i, m in enumerate(messages)]
    icerik_json = json.dumps(icerikler, ensure_ascii=False)
    prompt = (
        f"Translate each 'c' field in this JSON array to {hedef_ad}. "
        f"Keep the JSON structure exactly the same, only translate 'c' values. "
        f"Return ONLY valid JSON, no extra text.\n\n{icerik_json}"
    )
    try:
        sonuc = llm.invoke([HumanMessage(content=prompt)])
        metin = sonuc.content.strip()
        if "```" in metin:
            metin = metin.split("```")[1]
            if metin.startswith("json"):
                metin = metin[4:]
        cevrilmis = json.loads(metin.strip())
        yeni = [dict(m) for m in messages]
        for item in cevrilmis:
            idx = item["i"]
            if 0 <= idx < len(yeni):
                yeni[idx]["content"] = item["c"]
        return yeni
    except Exception:
        return messages

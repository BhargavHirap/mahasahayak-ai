"""
मराठी एआय — Streamlit chatbot
General Marathi/English AI assistant + optional lookup in your schemes.csv
"""

import csv
import io
import json
import os
import re
from pathlib import Path

import anthropic
import streamlit as st

# ---------------- Config ----------------
MODEL = "claude-3-5-sonnet-20241022"
SCHEMES_FILE = Path("schemes.csv")  # optional, put it next to app.py
MAX_MESSAGES_SENT = 20
TOP_SCHEMES = 5

SYSTEM_PROMPT = """तू 'मराठी एआय' आहेस — वापरकर्त्याचा वैयक्तिक सहाय्यक.
- वापरकर्ता ज्या भाषेत लिहितो त्याच भाषेत उत्तर दे. डिफॉल्ट भाषा: सोपी, स्पष्ट मराठी.
- कोणताही विषय चालेल: अभ्यास, विज्ञान, कोडिंग, गप्पा, सल्ला, लेखन, इत्यादी.
- उत्तरे लहान आणि समजायला सोपी ठेव; गरज असेल तेव्हाच सविस्तर सांग.
- तुला माहीत नसेल तर तसे प्रामाणिकपणे सांग, अंदाजे माहिती खरी म्हणून सांगू नकोस.
- जर संदर्भात [योजना माहिती] दिली असेल आणि प्रश्न योजनांबद्दल असेल, तरच ती वापर.
  प्रश्न योजनांचा नसेल तर ती माहिती दुर्लक्षित करून सामान्यपणे उत्तर दे.
- योजनेचे नियम/तारखा बदलू शकतात, त्यामुळे अर्ज करण्यापूर्वी अधिकृत वेबसाइट तपासायला सांग.
"""

st.set_page_config(page_title="मराठी एआय", page_icon="🙏", layout="centered")


# ---------------- Helpers ----------------
def get_secret(name: str):
    try:
        return st.secrets[name]
    except Exception:
        return os.environ.get(name)


def tokenize(text: str) -> set:
    return set(re.findall(r"[\w\u0900-\u097F]+", text.lower()))


def parse_schemes(raw: bytes) -> list:
    rows = []
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    for row in reader:
        text = " | ".join(f"{k}: {v}" for k, v in row.items() if v)
        if text:
            rows.append((tokenize(text), text))
    return rows


@st.cache_data(show_spinner=False)
def load_repo_schemes() -> list:
    if SCHEMES_FILE.exists():
        return parse_schemes(SCHEMES_FILE.read_bytes())
    return []


def find_schemes(schemes: list, question: str) -> str:
    q = tokenize(question)
    if not q or not schemes:
        return ""
    scored = []
    for tokens, text in schemes:
        score = len(q & tokens)
        if score >= 2:
            scored.append((score, text))
    if not scored:
        return ""
    scored.sort(key=lambda x: x[0], reverse=True)
    best = "\n".join(f"- {t[:700]}" for _, t in scored[:TOP_SCHEMES])
    return f"[योजना माहिती]\n{best}\n[/योजना माहिती]\n\n"


def stream_reply(client, messages):
    with client.messages.stream(
        model=MODEL,
        max_tokens=1500,
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        for chunk in stream.text_stream:
            yield chunk


# ---------------- Optional password gate ----------------
app_password = get_secret("APP_PASSWORD")
if app_password and not st.session_state.get("authed"):
    st.title("🙏 मराठी एआय")
    pw = st.text_input("पासवर्ड", type="password")
    if pw:
        if pw == app_password:
            st.session_state.authed = True
            st.rerun()
        else:
            st.error("चुकीचा पासवर्ड")
    st.stop()

# ---------------- API key ----------------
api_key = get_secret("ANTHROPIC_API_KEY")
if not api_key:
    st.error("ANTHROPIC_API_KEY सेट केलेली नाही. README मधील सूचना पहा.")
    st.stop()
client = anthropic.Anthropic(api_key=api_key)

# ---------------- Sidebar ----------------
schemes = load_repo_schemes()
with st.sidebar:
    st.header("⚙️ सेटिंग्ज")

    uploaded = st.file_uploader("योजनांची CSV (ऐच्छिक)", type="csv")
    if uploaded is not None:
        try:
            schemes = parse_schemes(uploaded.getvalue())
        except Exception:
            st.error("CSV वाचता आली नाही (UTF-8 असावी).")
    use_schemes = st.toggle("योजना माहिती वापरा", value=bool(schemes), disabled=not schemes)
    if schemes:
        st.caption(f"{len(schemes)} योजना लोड झाल्या.")
    else:
        st.caption("योजना फाइल नाही — फक्त सामान्य चॅट चालेल.")

    st.divider()
    if st.button("🆕 नवीन चॅट", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        st.download_button(
            "⬇️ चॅट डाउनलोड करा",
            data=json.dumps(st.session_state.messages, ensure_ascii=False, indent=1),
            file_name="marathi_ai_chat.json",
            mime="application/json",
            use_container_width=True,
        )

# ---------------- Chat UI ----------------
st.title("🙏 मराठी एआय")
st.caption("तुमचा वैयक्तिक सहाय्यक — काहीही विचारा.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("तुमचा प्रश्न येथे लिहा..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build messages for API (scheme context only for this turn)
    history = st.session_state.messages[-MAX_MESSAGES_SENT:]
    while history and history[0]["role"] != "user":
        history = history[1:]
    context = find_schemes(schemes, prompt) if (schemes and use_schemes) else ""
    api_messages = [dict(m) for m in history]
    api_messages[-1]["content"] = context + prompt

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(stream_reply(client, api_messages))
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except anthropic.APIError as e:
            st.error(f"त्रुटी: {e}")
            st.session_state.messages.pop()

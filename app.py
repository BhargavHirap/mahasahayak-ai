"""
मराठी एआय — FREE VERSION - No credits needed
Uses Google Gemini - Lifetime Free
"""

import csv
import io
import json
import os
import re
from pathlib import Path

import streamlit as st
import google.generativeai as genai

# ---------------- Config ----------------
# ---------------- Config ----------------
# MODEL auto-detect hoga, tension nahi
SCHEMES_FILE = Path("schemes.csv")
MAX_MESSAGES_SENT = 20
TOP_SCHEMES = 5

SYSTEM_PROMPT = """तू 'मराठी एआय' आहेस — वापरकर्त्याचा वैयक्तिक सहाय्यक. Bhargav ने तुला बनवले आहे मुंबई मध्ये.
- वापरकर्ता ज्या भाषेत लिहितो त्याच भाषेत उत्तर दे. डिफॉल्ट भाषा: सोपी, स्पष्ट मराठी.
- कोणताही विषय चालेल: अभ्यास, विज्ञान, कोडिंग, गप्पा, सल्ला, लेखन, इत्यादी.
- उत्तरे लहान आणि समजायला सोपी ठेव.
- जर संदर्भात [योजना माहिती] दिली असेल आणि प्रश्न योजनांबद्दल असेल, तरच ती वापर.
"""

st.set_page_config(page_title="मराठी एआय", page_icon="🙏", layout="centered")

# ---------------- Helpers ----------------
def get_secret(name: str):
    try:
        val = st.secrets[name]
        if isinstance(val, str):
            return val.strip().strip('"').strip("'").strip()
        return val
    except Exception:
        return os.environ.get(name, "").strip() if os.environ.get(name) else None

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

# ---------------- Password gate ----------------
app_password = get_secret("APP_PASSWORD")
if app_password and not st.session_state.get("authed"):
    st.title("🙏 मराठी एआय")
    pw = st.text_input("पासवर्ड", type="password")
    if st.button("Login"):
        if pw == app_password:
            st.session_state.authed = True
            st.rerun()
        else:
            st.error("चुकीचा पासवर्ड")
    st.stop()

# ---------------- FREE API key ----------------
api_key = get_secret("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY सेट केलेली नाही.")
    st.info("""
    **FREE Key कशी मिळवायची (1 min):**
    1. जा: aistudio.google.com/app/apikey
    2. Login with Google > Create API Key > Copy
    3. Streamlit > Manage app > Settings > Secrets मध्ये टाका:
    
    GEMINI_API_KEY = "tumhari_key"
    """)
    st.stop()

genai.configure(api_key=api_key)

# Auto-find best free model
try:
    available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # Flash models ko priority de
    flash_models = [m for m in available if 'flash' in m.lower()]
    model_name = flash_models[0] if flash_models else available[0]
    # 'models/' hata de
    model_name = model_name.replace("models/", "")
except:
    model_name = "gemini-2.5-flash"  # fallback

model = genai.GenerativeModel(model_name, system_instruction=SYSTEM_PROMPT)

# ---------------- Sidebar ----------------
schemes = load_repo_schemes()
with st.sidebar:
    st.header("⚙️ सेटिंग्ज")
    st.success("✅ FREE Gemini Mode - No Credits!")
st.caption(f"Model: {model_name}")

    uploaded = st.file_uploader("योजनांची CSV (ऐच्छिक)", type="csv")
    if uploaded is not None:
        try:
            schemes = parse_schemes(uploaded.getvalue())
        except Exception:
            st.error("CSV वाचता आली नाही.")

    use_schemes = st.toggle("योजना माहिती वापरा", value=bool(schemes), disabled=not schemes)
    if schemes:
        st.caption(f"{len(schemes)} योजना लोड झाल्या.")
    else:
        st.caption("योजना फाइल नाही — फक्त सामान्य चॅट चालेल.")

    st.divider()
    if st.button("🆕 नवीन चॅट", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------- Chat UI ----------------
st.title("🙏 मराठी एआय")
st.caption("तुमचा वैयक्तिक सहाय्यक — काहीही विचारा. (FREE)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("तुमचा प्रश्न येथे लिहा..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    history = st.session_state.messages[-MAX_MESSAGES_SENT:]
    while history and history[0]["role"] != "user":
        history = history[1:]
    
    context = find_schemes(schemes, prompt) if (schemes and use_schemes) else ""
    final_prompt = context + prompt
    
    # Build Gemini chat history
    gemini_history = []
    for msg in history[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    with st.chat_message("assistant"):
        try:
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(final_prompt, stream=True)
            full_text = ""
            placeholder = st.empty()
            for chunk in response:
                if chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
        except Exception as e:
            st.error(f"त्रुटी: {e}")
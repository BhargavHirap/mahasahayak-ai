import csv
import io
import os
import re
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types

# ---------------- Config ----------------
SCHEMES_FILE = Path("schemes.csv")
MAX_MESSAGES_SENT = 20
TOP_SCHEMES = 5
# Google ne bola ye naya model use karne ko
MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """तू 'मराठी एआय' आहेस — वापरकर्त्याचा वैयक्तिक सहाय्यक. Bhargav ने तुला बनवले आहे मुंबई मध्ये.
- वापरकर्ता ज्या भाषेत लिहितो त्याच भाषेत उत्तर दे. डिफॉल्ट भाषा: सोपी, स्पष्ट मराठी.
- उत्तरे लहान आणि समजायला सोपी ठेव.
"""

st.set_page_config(page_title="मराठी एआय", page_icon="🙏", layout="centered")

def get_secret(name: str):
    try:
        val = st.secrets[name]
        if isinstance(val, str):
            return val.strip().strip('"').strip("'").strip()
        return val
    except Exception:
        v = os.environ.get(name)
        return v.strip() if v else None

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

# Password gate
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

# API Key
api_key = get_secret("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY सेट केलेली नाही.")
    st.stop()

client = genai.Client(api_key=api_key)
schemes = load_repo_schemes()

with st.sidebar:
    st.header("⚙️ सेटिंग्ज")
    st.success("✅ NEW API - FREE")
    st.caption(f"Model: {MODEL}")

with st.sidebar:
    if st.button("🆕 नवीन चॅट", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Chat UI
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

    try:
        # Naya API call
        contents = []
        for msg in st.session_state.messages[-MAX_MESSAGES_SENT:]:
            role = "user" if msg["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_text = ""
            stream = client.models.generate_content_stream(
                model=MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                )
            )
            for chunk in stream:
                if chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
            st.session_state.messages.append({"role": "assistant", "content": full_text})
    except Exception as e:
        st.error(f"त्रुटी: {e}")
        st.info("Agar model error aaye toh MODEL ko 'gemini-3.8-flash' ya 'gemini-2.0-flash-lite' karke try karo")
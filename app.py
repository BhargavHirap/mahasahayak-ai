"""
मराठी एआय — Streamlit Chatbot
Gemini AI + Marathi/English + Optional Schemes CSV
FIXED - Auto Fallback Model
"""

import csv
import io
import json
import os
import re
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types

# ---------------- CONFIG - FIXED ----------------

MODELS_TO_TRY = [
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-8b",
    "gemini-2.0-flash",
    "gemini-flash-latest",
]
SCHEMES_FILE = Path("schemes.csv")
MAX_MESSAGES_SENT = 20
TOP_SCHEMES = 5

SYSTEM_PROMPT = """
तू 'मराठी एआय' आहेस — वापरकर्त्याचा वैयक्तिक AI सहाय्यक.
- वापरकर्ता ज्या भाषेत लिहितो त्याच भाषेत उत्तर दे.
- डिफॉल्ट भाषा सोपी आणि स्पष्ट मराठी आहे.
- उत्तरे सोपी, अचूक आणि समजण्यासारखी ठेव.
"""

st.set_page_config(page_title="मराठी एआय", page_icon="🙏", layout="centered")

def get_secret(name):
    try:
        value = st.secrets.get(name)
        if value:
            return str(value).strip()
    except Exception:
        pass
    return os.environ.get(name)

def tokenize(text):
    return set(re.findall(r"[\w\u0900-\u097F]+", text.lower()))

def parse_schemes(raw):
    rows = []
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    for row in reader:
        text = " | ".join(f"{k}: {v}" for k, v in row.items() if k and v)
        if text:
            rows.append((tokenize(text), text))
    return rows

@st.cache_data(show_spinner=False)
def load_repo_schemes():
    if SCHEMES_FILE.exists():
        return parse_schemes(SCHEMES_FILE.read_bytes())
    return []

def find_schemes(schemes, question):
    q = tokenize(question)
    if not q or not schemes:
        return ""
    scored = []
    for tokens, text in schemes:
        score = len(q & tokens)
        if score >= 2:
            scored.append((score, text))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored:
        return ""
    best = "\n".join(f"- {text[:700]}" for _, text in scored[:TOP_SCHEMES])
    return "[योजना माहिती]\n" + best + "\n[/योजना माहिती]\n\n"

def generate_reply(client, messages, context=""):
    api_messages = []
    for index, message in enumerate(messages):
        content = message["content"]
        if index == len(messages) - 1:
            content = context + content
        role = "user" if message["role"] == "user" else "model"
        api_messages.append({"role": role, "parts": [{"text": content}]})

    last_error = None
    for model_name in MODELS_TO_TRY:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=api_messages,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=1500,
                    temperature=0.7
                )
            )
            if response.text:
                return response.text
        except Exception as e:
            last_error = e
            continue
    raise last_error

# ---------------- PASSWORD ----------------
app_password = get_secret("APP_PASSWORD")
if app_password and not st.session_state.get("authed"):
    st.title("🙏 मराठी एआय")
    password = st.text_input("पासवर्ड", type="password")
    if password:
        if password == app_password:
            st.session_state.authed = True
            st.rerun()
        else:
            st.error("चुकीचा पासवर्ड")
    st.stop()

# ---------------- API KEY ----------------
api_key = get_secret("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY सापडली नाही.")
    st.stop()
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"API Client Error: {e}")
    st.stop()

# ---------------- SIDEBAR ----------------
schemes = load_repo_schemes()
with st.sidebar:
    st.header("⚙️ सेटिंग्ज")
    uploaded = st.file_uploader("योजनांची CSV अपलोड करा", type=["csv"])
    if uploaded is not None:
        try:
            schemes = parse_schemes(uploaded.getvalue())
            st.success("CSV लोड झाली!")
        except Exception:
            st.error("CSV वाचता आली नाही.")
    use_schemes = st.toggle("योजना माहिती वापरा", value=bool(schemes), disabled=not schemes)
    if schemes:
        st.caption(f"{len(schemes)} योजना लोड झाल्या.")
    else:
        st.caption("सामान्य AI चॅट सुरू आहे.")
    st.divider()
    if st.button("🆕 नवीन चॅट", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ---------------- CHAT UI ----------------
st.title("🙏 मराठी एआय")
st.caption("तुमचा वैयक्तिक AI सहाय्यक — काहीही विचारा.")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("तुमचा प्रश्न येथे लिहा..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    history = st.session_state.messages[-MAX_MESSAGES_SENT:]
    while history and history[0]["role"] != "user":
        history = history[1:]
    context = find_schemes(schemes, prompt) if schemes and use_schemes else ""
    with st.chat_message("assistant"):
        try:
            with st.spinner("उत्तर तयार होत आहे..."):
                reply = import time

def generate_reply(client, messages, context=""):
    api_messages = []
    for index, message in enumerate(messages):
        content = message["content"]
        if index == len(messages) - 1:
            content = context + content
        role = "user" if message["role"] == "user" else "model"
        api_messages.append({"role": role, "parts": [{"text": content}]})

    last_error = None
    for model_name in MODELS_TO_TRY:
        for attempt in range(3): # pratyek model 3 vela try
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=api_messages,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        max_output_tokens=1500,
                        temperature=0.7
                    )
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                last_error = e
                err_str = str(e)
                if "503" in err_str or "UNAVAILABLE" in err_str:
                    time.sleep(2 * (attempt + 1)) # 2, 4, 6 sec wait
                    continue
                else:
                    break # 404 asel tar pudhchya model var ja
        # pudhcha model try
    
    # Jar ithparyant ala tar sagle busy
    raise Exception(f"Google servers busy ahet (503). 2-3 minute ni parat try kara. Last error: {last_error}") st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"AI Error: {e}")
            if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                st.session_state.messages.pop()
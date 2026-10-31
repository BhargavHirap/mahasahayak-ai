"""
मराठी एआय — Streamlit Chatbot - FINAL FIXED
"""

import csv
import io
import json
import os
import re
import time
from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types

# ---------------- CONFIG ----------------
MODELS_TO_TRY = [
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash-8b",
    "gemini-flash-latest",
]
SCHEMES_FILE = Path("schemes.csv")
MAX_MESSAGES_SENT = 20
TOP_SCHEMES = 5

SYSTEM_PROMPT = "तू 'मराठी एआय' आहेस — वापरकर्त्याचा वैयक्तिक AI सहाय्यक. वापरकर्ता ज्या भाषेत लिहितो त्याच भाषेत उत्तर दे. डिफॉल्ट सोपी मराठी."

st.set_page_config(page_title="मराठी एआय", page_icon="🙏", layout="centered")

def get_secret(name):
    try:
        v = st.secrets.get(name)
        if v: return str(v).strip()
    except: pass
    return os.environ.get(name)

def tokenize(text):
    return set(re.findall(r"[\w\u0900-\u097F]+", text.lower()))

def parse_schemes(raw):
    rows=[]
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    for row in reader:
        text=" | ".join(f"{k}: {v}" for k,v in row.items() if k and v)
        if text: rows.append((tokenize(text), text))
    return rows

@st.cache_data(show_spinner=False)
def load_repo_schemes():
    if SCHEMES_FILE.exists(): return parse_schemes(SCHEMES_FILE.read_bytes())
    return []

def find_schemes(schemes, question):
    q=tokenize(question)
    if not q or not schemes: return ""
    scored=[]
    for tokens, text in schemes:
        score=len(q & tokens)
        if score>=2: scored.append((score, text))
    scored.sort(key=lambda x: x[0], reverse=True)
    if not scored: return ""
    best="\n".join(f"- {text[:700]}" for _, text in scored[:TOP_SCHEMES])
    return "[योजना माहिती]\n"+best+"\n[/योजना माहिती]\n\n"

def generate_reply(client, messages, context=""):
    api_messages=[]
    for idx, m in enumerate(messages):
        content=m["content"]
        if idx==len(messages)-1: content=context+content
        role="user" if m["role"]=="user" else "model"
        api_messages.append({"role": role, "parts": [{"text": content}]})
    
    last_error=None
    for model_name in MODELS_TO_TRY:
        for attempt in range(3):
            try:
                response=client.models.generate_content(
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
                last_error=e
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(2*(attempt+1))
                    continue
                break
    raise Exception(f"Google busy (503). 2 min ni try kara. {last_error}")

# PASSWORD
app_password=get_secret("APP_PASSWORD")
if app_password and not st.session_state.get("authed"):
    st.title("🙏 मराठी एआय")
    pwd=st.text_input("पासवर्ड", type="password")
    if pwd:
        if pwd==app_password:
            st.session_state.authed=True
            st.rerun()
        else: st.error("चुकीचा पासवर्ड")
    st.stop()

# API KEY
api_key=get_secret("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY nahi")
    st.stop()
client=genai.Client(api_key=api_key)

# SIDEBAR
schemes=load_repo_schemes()
with st.sidebar:
    st.header("⚙️ सेटिंग्ज")
    up=st.file_uploader("CSV", type=["csv"])
    if up is not None:
        try:
            schemes=parse_schemes(up.getvalue())
            st.success("CSV load!")
        except: st.error("CSV error")
    use_schemes=st.toggle("योजना वापरा", value=bool(schemes), disabled=not schemes)
    if st.button("🆕 नवीन चॅट", use_container_width=True):
        st.session_state.messages=[]
        st.rerun()

# CHAT
st.title("🙏 मराठी एआय")
if "messages" not in st.session_state: st.session_state.messages=[]
for m in st.session_state.messages:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt:=st.chat_input("प्रश्न लिहा..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    history=st.session_state.messages[-MAX_MESSAGES_SENT:]
    while history and history[0]["role"]!="user": history=history[1:]
    context=find_schemes(schemes, prompt) if schemes and use_schemes else ""
    with st.chat_message("assistant"):
        try:
            with st.spinner("उत्तर..."):
                reply=generate_reply(client, history, context)
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(str(e))
            if st.session_state.messages and st.session_state.messages[-1]["role"]=="user":
                st.session_state.messages.pop()
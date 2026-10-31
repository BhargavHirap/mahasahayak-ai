import streamlit as st
from google import genai

st.set_page_config(page_title="मराठी एआय", page_icon="🙏")

# --- API KEY ---
try:
    api_key = str(st.secrets["GEMINI_API_KEY"]).strip().strip('"').strip("'")
except:
    st.error("GEMINI_API_KEY Secrets me nahi mili")
    st.stop()

client = genai.Client(api_key=api_key)

# --- UI ---
st.title("🙏 मराठी एआय")
st.caption("तुमचा सहाय्यक")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "नमस्कार! मी तुमचा मराठी सहाय्यक आहे. विचारा! 🙏"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT ---
if prompt := st.chat_input("इथे लिहा..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("विचार करतोय..."):
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash-lite",
                    contents=f"You are Marathi AI. Reply in Marathi/English mix. User: {prompt}"
                )
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("1 minute baad try karo. Agar bar-bar aaye toh naya API Key banao: aistudio.google.com")
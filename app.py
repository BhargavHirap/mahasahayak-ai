import streamlit as st
from google import genai
import time

st.set_page_config(page_title="मराठी एआय")

api_key = str(st.secrets["GEMINI_API_KEY"]).strip().strip('"').strip("'")
client = genai.Client(api_key=api_key)

st.title("🙏 मराठी एआय")
st.caption("तुमचा वैयक्तिक सहाय्यक – काहीही विचारा. (FREE)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Sabse latest se purane tak try karenge
MODELS_TO_TRY = [
    "gemini-3.8-flash",
]

if prompt := st.chat_input("तुमचा प्रश्न येथे लिहा..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""
        success = False
        
        for model_name in MODELS_TO_TRY:
            try:
                placeholder.markdown(f"_{model_name} try kar raha hu..._")
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                full_text = response.text
                placeholder.markdown(full_text)
                st.session_state.messages.append({"role": "assistant", "content": full_text})
                success = True
                st.caption(f"✅ Model: {model_name}")
                break
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    time.sleep(1)
                    continue  # Agla model try karo
                else:
                    continue
        
        if not success:
            st.error("Sabhi models busy hai, 1 minute baad fir se try karo 🙏")
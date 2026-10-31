import streamlit as st
from google import genai

st.set_page_config(page_title="मराठी एआय")
api_key = str(st.secrets["GEMINI_API_KEY"]).strip().strip('"').strip("'")
client = genai.Client(api_key=api_key)

st.title("🙏 मराठी एआय")

prompt = st.chat_input("Kuch likho...")
if prompt:
    st.chat_message("user").write(prompt)
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
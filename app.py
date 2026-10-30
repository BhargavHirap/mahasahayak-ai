import streamlit as st
from google import genai

st.set_page_config(page_title="मराठी एआय")

def get_secret(name):
    try:
        return str(st.secrets[name]).strip().strip('"').strip("'")
    except:
        return None

api_key = get_secret("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY nahi mili")
    st.stop()

st.title("🙏 मराठी एआय - Test Mode")
st.success("App chal raha hai!")

client = genai.Client(api_key=api_key)

prompt = st.chat_input("Kuch likho...")
if prompt:
    st.chat_message("user").write(prompt)
    try:
        # Sabse stable model
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        st.chat_message("assistant").write(response.text)
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Model name badal ke 'gemini-2.5-flash' ya 'gemini-2.0-flash-lite' try karo")
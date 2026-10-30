import streamlit as st
import requests
from gtts import gTTS
import base64
from urllib.parse import quote

st.set_page_config(page_title="महासहायक AI PRO", page_icon="🇮🇳", layout="wide")

# --- DESIGN - ChatGPT jaisa ---
st.markdown("""
<style>
.stChatMessage {border-radius: 20px; padding: 10px;}
</style>
""", unsafe_allow_html=True)

st.title("महासहायक AI PRO 🇮🇳")
st.caption("ChatGPT + Gemini jaisa | Bolta bhi hai | Websites kholta hai")

# --- SESSION FOR CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "नमस्कार! मी महासहायक PRO आहे. तुम्हाला काय हवे आहे? \n\nमी शिष्यवृत्ती, सरकारी योजना, कोणतीही माहिती देऊ शकतो आणि बोलू पण शकतो. विचारा!"}]

# --- FUNCTIONS ---
def search_web(query):
    try:
        # Free DuckDuckGo search
        url = f"https://api.duckduckgo.com/?q={quote(query)}&format=json&pretty=1"
        r = requests.get(url, timeout=5).json()
        if r.get("AbstractText"):
            return r["AbstractText"] + f"\n\nSource: {r.get('AbstractURL','duckduckgo.com')}"
        if r.get("RelatedTopics"):
            return r["RelatedTopics"][0].get("Text","") if isinstance(r["RelatedTopics"][0], dict) else ""
    except:
        pass
    return None

def speak_text(text, lang='mr'):
    try:
        tts = gTTS(text=text[:500], lang=lang, slow=False) # 500 char limit
        tts.save("/tmp/speech.mp3")
        with open("/tmp/speech.mp3", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>"""
            st.markdown(md, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Voice error: {e}")

# --- SIDEBAR - Like ChatGPT ---
with st.sidebar:
    st.header("⚙️ Settings")
    lang = st.selectbox("भाषा / Language", ["Marathi (mr)", "Hindi (hi)", "English (en)"])
    lang_code = lang.split("(")[1].replace(")","")
    
    voice_on = st.toggle("🔊 Bolke Uttar De (Speak Answer)", value=True)
    
    st.divider()
    st.subheader("🌐 Quick Open")
    if st.button("MahaDBT Portal"): st.link_button("Open MahaDBT", "https://mahadbt.maharashtra.gov.in")
    if st.button("Aaple Sarkar"): st.link_button("Open Aaple Sarkar", "https://aaplesarkar.mahaonline.gov.in")
    if st.button("Google Search"): st.link_button("Open Google", "https://google.com")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- SHOW CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- CHAT INPUT - Like ChatGPT ---
if prompt := st.chat_input("Tumcha prashna liha... e.g. Ladki Bahin Yojana kay ahe?"):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot thinking
    with st.chat_message("assistant"):
        with st.spinner("Shodhat ahe... Google + Sarkari sites check kartoy..."):
            # 1. Check Govt Schemes first
            SCHEMES = {
                "शिष्यवृत्ती": "MahaDBT Scholarship - mahadbt.maharashtra.gov.in वर अर्ज करा. आधार, मार्कशीट, उत्पन्न दाखला लागतो.",
                "लाडकी": "Majhi Ladki Bahin Yojana: ₹1500/month. Aadhar, Bank Passbook. Portal: ladakibahin.maharashtra.gov.in",
                "शेतकरी": "Shetkari Karj Mafi: 7/12, Aadhar, Bank. mahadbt.maharashtra.gov.in",
                "प्रमाणपत्र": "Jaat Pramanpatra: aaplesarkar.mahaonline.gov.in"
            }
            answer = None
            for k,v in SCHEMES.items():
                if k in prompt or k.lower() in prompt.lower():
                    answer = f"✅ **{k} Yojana**\n\n{v}\n\n🔗 [Official Link Open Kara](https://mahadbt.maharashtra.gov.in)"
                    break
            
            # 2. If not in schemes, search web
            if not answer:
                web_result = search_web(prompt)
                if web_result:
                    answer = f"{web_result}\n\n🌐 Source: Internet Search"
                else:
                    answer = f"Tumhi vicharle: '{prompt}'\n\nMala ya baddal mahiti milat ahe. Krupa karun thoda specific vichara - udaa: 'Shishyavrutti form kasa bharaycha?' \n\nMe tumhala MahaDBT, Aaple Sarkar, Google varun mahiti deu shakto."

            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            # 3. Speak
            if voice_on:
                speak_text(answer, lang=lang_code if lang_code in ['mr','hi','en'] else 'mr')

st.divider()
st.caption("PRO Version | FYBSc IT | Made like ChatGPT | Voice + Web + Govt Sites")
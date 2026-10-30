
import streamlit as st
import requests, base64
from gtts import gTTS
from urllib.parse import quote

st.set_page_config(page_title="महासहायक AI PRO", page_icon="🇮🇳", layout="wide")
st.title("महासहायक AI PRO 🇮🇳")
st.caption("ChatGPT + Gemini jaisa | 10 Official Schemes | Bolta bhi hai")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "नमस्कार! मी महासहायक PRO आहे. माझ्याकडे 10 verified सरकारी योजनांची माहिती आहे. विचारा - उदा. Ladki Bahin, Scholarship, PM Kisan"}]

# 10 VERIFIED SCHEMES - OFFICIAL DATA
SCHEMES = {
    "ladki": "✅ **Majhi Ladki Bahin Yojana**\n\n- **Eligibility:** MH resident, Woman 21-65yr, Income <2.5 Lakh\n- **Benefit:** ₹1500/month\n- **Docs:** Aadhaar, Bank (DBT), Domicile, Income, Ration Card\n- **Portal:** ladakibahin.maharashtra.gov.in\n- **Note:** eKYC mandatory every year. [Official Link](https://ladakibahin.maharashtra.gov.in)",
    "bahin": "✅ **Majhi Ladki Bahin Yojana**\n\n- **Eligibility:** MH resident, Woman 21-65yr, Income <2.5 Lakh\n- **Benefit:** ₹1500/month\n- **Docs:** Aadhaar, Bank (DBT), Domicile, Income\n- **Portal:** ladakibahin.maharashtra.gov.in",
    "scholarship": "✅ **MahaDBT Scholarship 2026-27**\n\n- **Portal:** mahadbt2.maharashtra.gov.in (New)\n- **Eligibility:** MH domicile, SC/ST/OBC/EBC/Minority, CAP admission\n- **Income:** SC upto 2.5L, OBC 1.5L, EBC upto 8L\n- **Docs:** Domicile, Caste Validity, Income, Marksheet, Fee Receipt, Aadhaar\n- **Deadline:** 30 Sept 2026 [Apply](https://mahadbt2.maharashtra.gov.in)",
    "shahu": "✅ **Rajarshi Shahu Shikshan Shulkh Yojana (EBC)**\n\n- **Eligibility:** Open category, Income ≤8 Lakh, CAP admission, 2 child limit\n- **Benefit:** 50% Tuition Fee + Exam Fee refund\n- **Docs:** Domicile, Income (8L), CAP letter\n- **Portal:** mahadbt2.maharashtra.gov.in",
    "hostel": "✅ **Dr. Panjabrao Deshmukh Vasatigruh Bhatta**\n\n- **Eligibility:** EBC/SEBC, Professional course hostel student\n- **Benefit:** Hostel maintenance allowance\n- **Docs:** Hostel Receipt, Fee Receipt\n- **Portal:** mahadbt2.maharashtra.gov.in",
    "minority": "✅ **Minority Scholarship (DHE)**\n\n- **Eligibility:** Muslim/Christian/Sikh/Buddhist/Jain, Income ≤8 Lakh, Graduation/PG\n- **Benefit:** Scholarship for 2000 students\n- **Docs:** Marksheet, Domicile, Income + Affidavit on ₹100 stamp\n- **Portal:** mahadbt.maharashtra.gov.in",
    "pm kisan": "✅ **PM Kisan Samman Nidhi**\n\n- **Eligibility:** Land-owning farmers\n- **Benefit:** ₹6000/year (₹2000 x 3)\n- **Docs:** Aadhaar, 7/12, Bank\n- **Portal:** pmkisan.gov.in",
    "kisan": "✅ **PM Kisan + MahaDBT Farmer**\n\n- **PM Kisan:** ₹6000/yr, pmkisan.gov.in\n- **Micro-irrigation:** Drip ₹97k, Sprinkler ₹47k subsidy\n- **New Well:** Upto ₹4 Lakh\n- **Docs:** Aadhaar, 7/12, Bank",
    "ayushman": "✅ **Ayushman Bharat PM-JAY**\n\n- **Eligibility:** SECC families + All 70+ senior citizens\n- **Benefit:** ₹5 Lakh free treatment/year\n- **Docs:** Aadhaar, Ration Card\n- **Portal:** pmjay.gov.in",
    "awas": "✅ **PM Awas Yojana 2.0**\n\n- **Eligibility:** No pucca house, EWS <3Lakh income\n- **Benefit:** 4% interest subsidy upto ₹8 Lakh loan\n- **Portal:** pmaymis.gov.in\n- **Extended till March 2029**"
}

def search_web(q):
    try:
        url = f"https://api.duckduckgo.com/?q={quote(q)}&format=json"
        r = requests.get(url, timeout=4).json()
        return r.get("AbstractText") or ""
    except: return ""

def speak(text, lang='mr'):
    try:
        tts = gTTS(text=text[:400], lang=lang, slow=False)
        tts.save("/tmp/s.mp3")
        with open("/tmp/s.mp3","rb") as f:
            b64=base64.b64encode(f.read()).decode()
            st.markdown(f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    except: pass

# Sidebar
with st.sidebar:
    st.header("⚙️ 10 Schemes")
    st.write("Ladki Bahin | Scholarship | Shahu | Hostel | Minority | PM Kisan | Ayushman | Awas")
    voice = st.toggle("🔊 Voice", True)
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages=[]
        st.rerun()

# Show history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Chat
if prompt := st.chat_input("Prashna liha... e.g. Ladki Bahin eligibility"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        ans=None
        for k,v in SCHEMES.items():
            if k.lower() in prompt.lower():
                ans=v
                break
        if not ans:
            web=search_web(prompt)
            ans = web if web else f"**Tumcha prashna:** {prompt}\n\nMazyakade 10 yojana ahet. Try kara: `Ladki Bahin`, `Scholarship`, `PM Kisan`, `Ayushman`, `Awas Yojana`"
        
        st.markdown(ans)
        st.session_state.messages.append({"role":"assistant","content":ans})
        if voice: speak(ans, 'mr')
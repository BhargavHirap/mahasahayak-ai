import streamlit as st
from deep_translator import GoogleTranslator

# --- PAGE SETUP - PROFESSIONAL LOOK ---
st.set_page_config(
    page_title="MahaSahayak AI - Professional",
    page_icon="🙏",
    layout="wide"
)

# Custom CSS for professional look
st.markdown("""
<style>
.main-header { background: linear-gradient(90deg, #FF6F00 0%, #FF8F00 100%); padding:20px; border-radius:15px; color:white; text-align:center; }
.scheme-card { background:white; padding:15px; border-radius:10px; border-left:5px solid #FF6F00; box-shadow:0 2px 5px #ddd; margin:10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>🙏 MahaSahayak AI | महासहायक AI</h1><p>Professional Government Scheme Assistant - English | हिंदी | मराठी</p></div>', unsafe_allow_html=True)

# --- MULTILINGUAL DATABASE ---
# Key in English, Hindi, Marathi - so it works in all languages
schemes_db = {
    "scholarship": {
        "keywords": ["scholarship", "शिष्यवृत्ती", "छात्रवृत्ति", "shishyavrutti", "students"],
        "mr": "महाडीबीटी https://mahadbt.maharashtra.gov.in वर शिष्यवृत्तीसाठी अर्ज करा. आवश्यक: आधार, उत्पन्न दाखला, जातीचा दाखला.",
        "en": "Apply for scholarship on MahaDBT: https://mahadbt.maharashtra.gov.in. Docs: Aadhaar, Income certificate.",
        "hi": "छात्रवृत्ति के लिए महाडीबीटी https://mahadbt.maharashtra.gov.in पर आवेदन करें।"
    },
    "farmer": {
        "keywords": ["farmer", "शेतकरी", "किसान", "shetkari", "pm kisan", "kisan"],
        "mr": "पीएम किसान सन्मान निधी - वर्षाला 6000 रु. pmkisan.gov.in वर अर्ज करा.",
        "en": "PM Kisan Samman Nidhi - Rs. 6000 per year. Apply on pmkisan.gov.in",
        "hi": "पीएम किसान योजना - सालाना 6000 रु. pmkisan.gov.in पर आवेदन करें।"
    },
    "ration": {
        "keywords": ["ration", "रेशन", "राशन", "ration card"],
        "mr": "रेशन कार्डसाठी mahafood.gov.in वर अर्ज करा. सेतू केंद्रातही अर्ज होतो.",
        "en": "For Ration Card, apply on mahafood.gov.in or visit Setu Kendra.",
        "hi": "राशन कार्ड के लिए mahafood.gov.in पर आवेदन करें।"
    },
    "sanjay gandhi": {
        "keywords": ["sanjay gandhi", "संजय गांधी", "निराधार", "niradhar"],
        "mr": "संजय गांधी निराधार योजना - दरमहा 1000 रु. तहसील कार्यालयात अर्ज करा.",
        "en": "Sanjay Gandhi Niradhar Scheme - Rs.1000 per month. Apply at Tahsil office.",
        "hi": "संजय गांधी निराधार योजना - हर महीने 1000 रु. तहसील में आवेदन करें।"
    }
}

def translate_to_marathi(text):
    try:
        return GoogleTranslator(source='auto', target='mr').translate(text)
    except:
        return text

def detect_and_answer(user_input, output_lang):
    user_input_lower = user_input.lower()
    
    # Search in all keywords
    for scheme, data in schemes_db.items():
        for kw in data["keywords"]:
            if kw in user_input_lower:
                if output_lang == "मराठी": return data["mr"]
                elif output_lang == "हिंदी": return data["hi"]
                else: return data["en"]
    
    # If no keyword match, translate question to Marathi for display
    translated = translate_to_marathi(user_input)
    return f"**Translated to Marathi:** {translated}\n\n" + "या प्रश्नाची माहिती लवकरच जोडत आहोत. कृपया महाडीबीटी पोर्टल तपासा: https://mahadbt.maharashtra.gov.in"

# --- UI ---
col1, col2 = st.columns([3, 1])

with col1:
    st.write("### 💬 Ask anything / काहीही विचारा")
    user_lang = st.radio("Answer Language / उत्तराची भाषा:", ["मराठी", "English", "हिंदी"], horizontal=True)
    
    question = st.text_input("Type here (English, Hindi or Marathi):", 
                             placeholder="Ex: I need scholarship info / मला शिष्यवृत्ती हवी आहे / मुझे छात्रवृत्ति चाहिए")

    if st.button("🔍 Get Information / माहिती मिळवा", type="primary", use_container_width=True):
        if question:
            with st.spinner("Searching..."):
                answer = detect_and_answer(question, user_lang)
                st.markdown(f'<div class="scheme-card"><h3>✅ Answer:</h3><p style="font-size:18px">{answer}</p></div>', unsafe_allow_html=True)
                
                # Show translation
                if user_lang != "मराठी":
                    marathi_version = translate_to_marathi(answer)
                    st.info(f"**मराठीत:** {marathi_version}")
        else:
            st.warning("Please enter your question / कृपया प्रश्न लिहा")

with col2:
    st.markdown("### 📋 Available Topics")
    st.write("Try typing:")
    st.code("scholarship\nfarmer scheme\nration card\nSanjay Gandhi Yojana\nशिष्यवृत्ती\nशेतकरी")
    
    st.markdown("### 🌐 Professional Features")
    st.markdown("""
    - ✅ English → Marathi Translation
    - ✅ Hindi → Marathi Translation  
    - ✅ Hinglish Support
    - ✅ Professional UI
    - ✅ Mobile Friendly
    - ✅ Free & Open Source
    """)

st.markdown("---")
st.caption("© 2025 MahaSahayak AI - Built for Maharashtra | Professional Version")

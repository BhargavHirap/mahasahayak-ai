import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(
    page_title="महासहायक AI",
    page_icon="🙏",
    layout="centered"
)

# --- YOUR AI LOGIC HERE ---
# For now, simple Marathi scheme database
# Later we will connect your real AI file

schemes = {
    "शिष्यवृत्ती": "महाडीबीटी https://mahadbt.maharashtra.gov.in वर अर्ज करा. उत्पन्न दाखला लागतो.",
    "शेतकरी": "पीएम किसान - वर्षाला 6000 रु. pmkisan.gov.in",
    "संजय गांधी": "निराधार योजना - दरमहा 1000 रु. सेतू केंद्रात अर्ज करा.",
    "महाडीबीटी": "सर्व योजनांसाठी एकच पोर्टल: mahadbt.maharashtra.gov.in",
    "रेशन": "रेशन कार्डसाठी mahafood.gov.in वर अर्ज करा.",
    "शिष्यवृत्तीची": "महाडीबीटी https://mahadbt.maharashtra.gov.in वर अर्ज करा. उत्पन्न दाखला लागतो."
}

def mahasahayak_ai(question):
    if not question:
        return "कृपया प्रश्न लिहा"
    for key, ans in schemes.items():
        if key in question:
            return ans
    return f"तुम्ही विचारले: {question}\n\nयाची माहिती लवकरच जोडत आहोत. तुम्ही महाडीबीटी तपासू शकता."

# --- WEBSITE UI ---
st.markdown("# 🙏 नमस्कार! मी महासहायक AI")
st.markdown("### महाराष्ट्र शासनाच्या योजनांची माहिती मराठीत")
st.write("---")

question = st.text_input("तुमचा प्रश्न मराठीत लिहा", placeholder="उदा. मला शिष्यवृत्तीची माहिती हवी आहे")

col1, col2 = st.columns([1, 1])
with col1:
    search_btn = st.button("माहिती मिळवा", use_container_width=True, type="primary")

if search_btn:
    if question:
        answer = mahasahayak_ai(question)
        st.success(answer)
    else:
        st.warning("कृपया आधी प्रश्न लिहा")

st.markdown("---")
st.caption("ही तुमची स्वतःची वेबसाइट आहे. लिंक शेअर करू शकता.")

# --- SIDEBAR WITH MORE INFO ---
with st.sidebar:
    st.header("उपलब्ध योजना")
    st.write("खालील शब्द वापरून प्रश्न विचारा:")
    for key in schemes.keys():
        st.write(f"• {key}")
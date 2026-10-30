import streamlit as st

SCHEMES = {
    "शिष्यवृत्ती": "✅ MahaDBT Scholarship\n\nपात्रता: 12वी पास, महाराष्ट्र रहिवासी\nकागदपत्रे: आधार, मार्कशीट, उत्पन्न दाखला\nअर्ज: mahadbt.maharashtra.gov.in वर",
    "शेतकरी": "✅ शेतकरी कर्जमुक्ती योजना\n\nपात्रता: महाराष्ट्रातील शेतकरी\nकागदपत्रे: 7/12, आधार, बँक पासबुक\nअर्ज: mahadbt.maharashtra.gov.in वर",
    "लाडकी": "✅ लेक लाडकी योजना\n\nपात्रता: मुलगी असलेल्या कुटुंबासाठी\nअर्ज: womenchild.maharashtra.gov.in वर",
    "प्रमाणपत्र": "✅ जात प्रमाणपत्र\n\nकागदपत्रे: आधार, रहिवासी दाखला, शाळा सोडल्याचा दाखला\nअर्ज: aaplesarkar.mahaonline.gov.in वर"
}

st.set_page_config(page_title="महासहायक AI", page_icon="🇮🇳", layout="centered")
st.title("महासहायक AI 🇮🇳")
st.subheader("तुमचा मराठी सहाय्यक")
st.divider()

q = st.text_input("तुमचा प्रश्न येथे लिहा:", placeholder="उदा: मला शिष्यवृत्तीची माहिती हवी आहे...")

col1, col2 = st.columns(2)
with col1:
    ask_btn = st.button("उत्तर मिळवा", use_container_width=True)
with col2:
    voice_btn = st.button("🎤 बोला (लवकरच)", use_container_width=True)

if ask_btn and q:
    found = False
    for key in SCHEMES:
        if key in q:
            st.success(SCHEMES[key])
            st.link_button("🔗 अधिकृत वेबसाइट उघडा", "https://mahadbt.maharashtra.gov.in")
            st.caption("Source: maharashtra.gov.in | Verified: Oct 2026")
            found = True
            break
    if not found:
        st.warning("माफ करा, या बद्दल माहिती अजून जोडत आहोत.\n\nकृपया हे शब्द वापरा: शिष्यवृत्ती, शेतकरी, लाडकी, प्रमाणपत्र")
        st.info("उदाहरण: 'मला शिष्यवृत्ती हवी आहे' असे लिहा.")
else:
    st.info("👆 वर प्रश्न लिहा आणि 'उत्तर मिळवा' दाबा")

st.divider()
st.caption("FYBSc IT Project | Team MahaSahayak | Made on Phone 📱")
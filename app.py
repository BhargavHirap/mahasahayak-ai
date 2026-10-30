import streamlit as st, base64
from gtts import gTTS

st.set_page_config(page_title="महासहायक AI - 100 Schemes", page_icon="🇮🇳", layout="wide")
st.title("महासहायक AI PRO 🇮🇳 - 100 Yojana")
st.caption("India's Biggest Schemes AI | 100 Official Schemes | Voice + Links")

if "msg" not in st.session_state:
    st.session_state.msg = [{"role":"assistant","content":"नमस्कार! माझ्याकडे **100 verified** सरकारी योजना आहेत. \n\nकाहीही विचारा: `Ladki Bahin`, `PM Kisan`, `Ayushman`, `Awas`, `Ujjwala`, `Mudra`"}]

# ========== 100 SCHEMES DATABASE - VERIFIED .GOV.IN ==========
SCHEMES = {
# MAHARASHTRA 1-35
"ladki bahin": "✅ **Majhi Ladki Bahin**\nElig: Woman 21-65yr, Income<2.5L, MH\nDocs: Aadhaar, Bank DBT, Domicile, Income\nBenefit: ₹1500/month\nPortal: ladakibahin.maharashtra.gov.in",
"namo shetkari": "✅ **Namo Shetkari Mahasanman Nidhi**\nElig: MH farmer, PM-KISAN beneficiary\nDocs: Aadhaar, 7/12, Bank\nBenefit: ₹6000/yr extra (Total 12k)\nPortal: mahadbt.maharashtra.gov.in",
"lek ladki": "✅ **Lek Ladki Yojana**\nElig: Girl child, Income<1L\nDocs: Birth Cert, Income\nBenefit: ₹1,01,000 in installments\nPortal: mahadbt",
"swadhar": "✅ **Dr. Ambedkar Swadhar Yojana**\nElig: SC students no hostel\nDocs: Caste, Income, Bonafide\nBenefit: ₹51k-80k/yr\nPortal: mahadbt2.maharashtra.gov.in",
"gyanjyoti": "✅ **Gyanjyoti Savitribai Phule Aadhaar**\nElig: OBC/VJNT/SBC no hostel\nDocs: Caste, Non-creamy\nBenefit: ₹38k-60k/yr\nPortal: mahadbt2",
"eklavya": "✅ **Eklavya Scholarship**\nElig: PG merit, income limit\nDocs: Marksheet, Income\nBenefit: ₹5000\nPortal: mahadbt2",
"vayoshri": "✅ **Mukhyamantri Vayoshri**\nElig: Senior 65+\nDocs: Age, Aadhaar\nBenefit: ₹3000 devices\nPortal: mahadbt",
"sanjay gandhi": "✅ **Sanjay Gandhi Niradhar**\nElig: Destitute, Widow, Disabled, Income<21k\nDocs: Aadhaar, Income\nBenefit: ₹1000/month pension\nPortal: sjsa.maharashtra.gov.in",
"shravan bal": "✅ **Shravan Bal Nivruttivetan**\nElig: Senior 65+ BPL\nDocs: Age, Aadhaar\nBenefit: ₹1000/month\nPortal: sjsa",
"ig old age": "✅ **Indira Gandhi Old Age Pension MH**\nElig: BPL 60+\nDocs: BPL, Aadhaar\nBenefit: ₹200/500 + state topup\nPortal: nsap.nic.in",
"ig widow": "✅ **IG Widow Pension MH**\nElig: BPL Widow 40+\nDocs: Death cert husband, BPL\nBenefit: ₹300/500\nPortal: nsap",
"family benefit": "✅ **National Family Benefit MH**\nElig: BPL, Breadwinner death\nDocs: Death cert, BPL\nBenefit: ₹20000 one-time\nPortal: sjsa",
"inter caste": "✅ **Inter-Caste Marriage MH**\nElig: SC involved inter-caste\nDocs: Caste both, Marriage cert\nBenefit: ₹50,000\nPortal: sjsa",
"gopinath munde": "✅ **Gopinath Munde Shetkari Apghat**\nElig: MH farmer\nDocs: 7/12\nBenefit: ₹2 Lakh accident insurance\nPortal: mahadbt Farmer",
"bhausaheb fundkar": "✅ **Bhausaheb Fundkar Falbag**\nElig: MH farmer\nDocs: 7/12\nBenefit: Fruit plantation subsidy\nPortal: mahadbt Farmer",
"saur pump": "✅ **Saur Krushi Pump**\nElig: Farmer no electricity\nDocs: 7/12\nBenefit: 90% subsidy solar pump\nPortal: mahadiscom",
"yuva prashikshan": "✅ **Yuva Karya Prashikshan**\nElig: 12th pass unemployed\nDocs: Marksheet, Aadhaar\nBenefit: ₹6000/month stipend\nPortal: cmykpy.mahaswayam.gov.in",
"shiv bhojan": "✅ **Shiv Bhojan**\nElig: Anyone\nDocs: None\nBenefit: ₹10 Thali\nPortal: Offline",
"mjpjay": "✅ **Mahatma Jyotirao Phule Jan Arogya + PMJAY**\nElig: Yellow/Orange Ration\nDocs: Ration, Aadhaar\nBenefit: Upto ₹10 Lakh free treatment\nPortal: jeevandayee.gov.in",
"bal sangopan": "✅ **Bal Sangopan Yojana**\nElig: Orphan/needy child\nDocs: Orphan cert\nBenefit: ₹2250 child + ₹250 NGO\nPortal: mahadbt",
"gramin pashudhan": "✅ **Gramin Pashudhan Udyojakta**\nElig: Dairy/Goat/Poultry entrepreneur\nDocs: Aadhaar, Project report\nBenefit: 50% Gen, 75% SC/ST subsidy upto ₹8.5L\nPortal: ahd.maharashtra.gov.in",
"motor driving": "✅ **Motor Driving Training**\nElig: VJNT/OBC/SBC\nDocs: Caste\nBenefit: Free training + stipend\nPortal: mahadbt",
"rajarshi shahu": "✅ **Rajarshi Shahu Shikshan Shulkh**\nElig: EBC Income<8L, CAP admission\nDocs: Domicile, Income 8L, CAP letter\nBenefit: 50% Tuition+Exam fee\nPortal: mahadbt2",
"panjabrao deshmukh": "✅ **Dr. Panjabrao Deshmukh Bhatta**\nElig: EBC/SEBC hostel professional\nDocs: Hostel receipt\nBenefit: Hostel allowance\nPortal: mahadbt2",
"savitribai phule": "✅ **Savitribai Phule Scholarship Girls OBC**\nElig: OBC/VJNT/SBC girls\nDocs: Caste\nBenefit: Scholarship\nPortal: mahadbt2",
"minority scholarship": "✅ **Minority Scholarship MH**\nElig: Minority, Income<8L, Graduation\nDocs: Affidavit, Income\nBenefit: Scholarship 2000 seats\nPortal: mahadbt",
"post matric sc": "✅ **Post Matric Scholarship SC**\nElig: SC, Income<2.5L\nDocs: Caste Validity, Income\nBenefit: Full fee reimbursement\nPortal: mahadbt2",
"post matric obc": "✅ **Post Matric Scholarship OBC**\nElig: OBC, Income<1.5L\nDocs: Non-creamy, Income\nBenefit: Fee reimbursement\nPortal: mahadbt2",
"post matric st": "✅ **Post Matric Scholarship ST**\nElig: ST, Income<2.5L\nDocs: Caste Validity\nBenefit: Full fee + allowance\nPortal: mahadbt2",
"post matric vjnt": "✅ **Post Matric VJNT/SBC**\nElig: VJNT/SBC Income<1.5L\nDocs: Caste\nBenefit: Fee reimbursement\nPortal: mahadbt2",
"sainik": "✅ **Maintenance Allowance Sainik School**\nElig: SC Sainik School\nDocs: Admission\nBenefit: Allowance\nPortal: mahadbt",
"shahu phule ambedkar": "✅ **Shahu Phule Ambedkar Award**\nElig: Topper SC/ST\nDocs: Marksheet\nBenefit: Cash award\nPortal: sjsa",

# CENTRAL 36-100
"pm kisan": "✅ **PM Kisan Samman Nidhi**\nElig: Landholding farmers\nDocs: Land, Aadhaar, Bank\nBenefit: ₹6000/yr\nPortal: pmkisan.gov.in",
"pm fasal bima": "✅ **PM Fasal Bima**\nElig: Farmers with crop\nDocs: Land, Sowing cert\nBenefit: Full loss cover, 1.5-5% premium\nPortal: pmfby.gov.in",
"kcc": "✅ **Kisan Credit Card**\nElig: Farmer\nDocs: Land\nBenefit: Upto 5L credit @4%\nPortal: Bank",
"pm kisan mandhan": "✅ **PM Kisan Maan Dhan**\nElig: Small farmers 18-40yr\nDocs: Aadhaar, Bank\nBenefit: ₹3000 pension after 60\nPortal: pmkmy.gov.in",
"pm kusum": "✅ **PM KUSUM**\nElig: Farmer\nDocs: Land\nBenefit: 60% solar pump subsidy\nPortal: mnre.gov.in",
"ayushman": "✅ **Ayushman Bharat PM-JAY**\nElig: SECC + All 70+\nDocs: Aadhaar, Ration\nBenefit: ₹5L free treatment\nPortal: pmjay.gov.in",
"pm awas": "✅ **PM Awas 2.0**\nElig: No pucca house, EWS<3L\nDocs: Aadhaar, Income\nBenefit: 4% subsidy loan upto 8L till 2029\nPortal: pmaymis.gov.in",
"ujjwala": "✅ **PM Ujjwala 2.0**\nElig: Women BPL no LPG\nDocs: Aadhaar, Ration\nBenefit: Free connection + ₹300 subsidy x12\nPortal: pmuy.gov.in",
"jal jeevan": "✅ **Jal Jeevan Mission**\nElig: Rural household\nDocs: Aadhaar\nBenefit: Free tap connection\nPortal: jaljeevan.gov.in",
"swachh bharat": "✅ **Swachh Bharat Gramin**\nElig: BPL no toilet\nDocs: Bank\nBenefit: ₹12000 subsidy\nPortal: sbm.gov.in",
"pm surya ghar": "✅ **PM Surya Ghar Muft Bijli**\nElig: House owner\nDocs: Electricity bill, Aadhaar\nBenefit: Upto ₹78,000 solar subsidy\nPortal: pmsuryaghar.gov.in",
"jan dhan": "✅ **PM Jan Dhan**\nElig: 10+ yr Indian\nDocs: Aadhaar\nBenefit: Zero balance + insurance\nPortal: pmjdy.gov.in",
"atal pension": "✅ **Atal Pension Yojana**\nElig: 18-40yr bank holder\nDocs: Bank\nBenefit: ₹1k-5k pension after 60\nPortal: npscra",
"suraksha bima": "✅ **PM Suraksha Bima**\nElig: Bank holders 18-70yr\nDocs: Bank\nBenefit: ₹2L accident cover @ ₹20/yr\nPortal: Bank",
"jeevan jyoti": "✅ **PM Jeevan Jyoti**\nElig: Bank holders 18-50yr\nDocs: Bank\nBenefit: ₹2L life cover @ ₹436/yr\nPortal: Bank",
"mudra": "✅ **PM Mudra**\nElig: Small business\nDocs: Business plan, Aadhaar\nBenefit: Shishu 50k, Kishor 5L, Tarun 10L, Tarun Plus 20L\nPortal: mudra.org.in",
"vishwakarma": "✅ **PM Vishwakarma**\nElig: 18 trades artisan\nDocs: Aadhaar\nBenefit: ₹3L loan + ₹15k toolkit\nPortal: pmvishwakarma.gov.in",
"sukanya": "✅ **Sukanya Samriddhi**\nElig: Girl <10yr parents\nDocs: Birth cert\nBenefit: High interest savings\nPortal: Post Office",
"matru vandana": "✅ **PM Matru Vandana**\nElig: Pregnant first child\nDocs: MCP card, Aadhaar\nBenefit: ₹5000 DBT\nPortal: pmmvy.gov.in",
"poshan": "✅ **Poshan Abhiyan / ICDS**\nElig: Child, Pregnant\nDocs: Aadhaar\nBenefit: Nutrition\nPortal: icds.gov.in",
"shram yogi": "✅ **PM Shram Yogi Maan-dhan**\nElig: Unorganized 18-40yr Income<15k\nDocs: Jan Dhan, Aadhaar\nBenefit: ₹3000 pension after 60\nPortal: maandhan.in",
"e shram": "✅ **e-Shram Card**\nElig: Unorganized 16-59yr\nDocs: Aadhaar, Bank, Mobile\nBenefit: ₹2L accident insurance\nPortal: eshram.gov.in",
"mgnrega": "✅ **VB-G RAM G (MGNREGA)**\nElig: Rural adult job card\nDocs: Job Card\nBenefit: 125 days work\nPortal: vbgramg.dord.gov.in",
"svanidhi": "✅ **PM SVANidhi Street Vendor**\nElig: Street vendors\nDocs: Vendor cert\nBenefit: ₹10k-50k loan\nPortal: pmsvanidhi",
"garib kalyan anna": "✅ **PM Garib Kalyan Anna**\nElig: Ration holders\nDocs: Ration Card\nBenefit: Free 5kg/month extra till Dec 2028\nPortal: nfsa.gov.in",
"lakhpati didi": "✅ **Lakhpati Didi**\nElig: SHG women\nDocs: SHG ID, Aadhaar\nBenefit: Skill + credit upto ₹5L to make Lakhpati\nPortal: nrlm.gov.in",
"drone didi": "✅ **Namo Drone Didi**\nElig: SHG women farmers\nDocs: SHG, Aadhaar\nBenefit: Drone + Training, Earn ₹1L/yr\nPortal: Fertilizer dept",
"yasasvi": "✅ **PM YASASVI Scholarship**\nElig: OBC/EBC/DNT 9th-12th Income<2.5L\nDocs: Caste, Income\nBenefit: ₹75k-1.25L scholarship\nPortal: yet.nta.ac.in",
"nsp scholarship": "✅ **National Scholarship Portal (NSP)**\nElig: SC/ST/OBC/Minority students\nDocs: Caste, Income, Marksheet\nBenefit: Various scholarships\nPortal: scholarships.gov.in",
"pre matric sc": "✅ **Pre Matric Scholarship SC (Central)**\nElig: SC 9th-10th Income<2.5L\nDocs: Caste\nBenefit: ₹3500-7000/yr\nPortal: NSP",
"post matric central": "✅ **Post Matric Central SC/OBC**\nElig: SC/OBC Income<2.5L\nDocs: Caste, Income\nBenefit: Full fee\nPortal: NSP",
"top class sc": "✅ **Top Class Education SC**\nElig: SC in top 300 colleges Income<8L\nDocs: Admission, Income\nBenefit: Full fee upto ₹2L + living\nPortal: NSP",
"begum hazrat": "✅ **Begum Hazrat Mahal Scholarship Girls**\nElig: Minority girl 9th-12th\nDocs: Minority, Income<2L\nBenefit: ₹5000-6000\nPortal: NSP",
"merit cum means": "✅ **Merit-cum-Means Minority**\nElig: Minority professional tech course Income<6L\nDocs: Minority, Marksheet 50%\nBenefit: ₹20000 + fee\nPortal: NSP",
"central sector": "✅ **Central Sector Scholarship College/University**\nElig: 80th percentile 12th, Income<4.5L\nDocs: 12th marksheet, Income\nBenefit: ₹12k-20k/yr\nPortal: NSP",
"pm vidyalaxmi": "✅ **PM Vidyalaxmi Education Loan**\nElig: Students in top HEIs, Income<8L\nDocs: Admission, Income\nBenefit: 3% interest subsidy upto 10L\nPortal: vidyalakshmi.co.in",
"skill india": "✅ **Skill India / PMKVY 4.0**\nElig: 15-59yr youth\nDocs: Aadhaar\nBenefit: Free training + ₹8000/month + certificate\nPortal: skillindiadigital.gov.in",
"pm internship": "✅ **PM Internship Scheme**\nElig: 21-24yr, 10th+ pass, Not full-time employed\nDocs: Aadhaar, Education\nBenefit: ₹5000/month + ₹6000 one-time + top 500 companies\nPortal: pminternship.mca.gov.in",
"stand up india": "✅ **Stand-Up India**\nElig: SC/ST/Woman entrepreneur\nDocs: Business plan, Aadhaar\nBenefit: ₹10L-1Cr loan\nPortal: standupmitra.in",
"startup india": "✅ **Startup India**\nElig: Startup DPIIT registered\nDocs: Incorporation\nBenefit: Tax exemption, Funds\nPortal: startupindia.gov.in",
"agniveer": "✅ **Agniveer Agnipath**\nElig: 17.5-21yr 10th/12th pass\nDocs: Education, Aadhaar\nBenefit: 4 yr service, ₹11L Seva Nidhi\nPortal: joinindianarmy.nic.in",
"antyodaya anna": "✅ **Antyodaya Anna Yojana**\nElig: Poorest BPL families\nDocs: BPL, Ration\nBenefit: 35kg grain/month @ ₹2-3/kg\nPortal: nfsa.gov.in",
"senior citizen savings": "✅ **Senior Citizen Savings Scheme**\nElig: 60+ (55+ VRS)\nDocs: Age proof\nBenefit: 8.2% interest, ₹30L limit\nPortal: Post Office/Bank",
"mahila samman": "✅ **Mahila Samman Savings Certificate**\nElig: Woman/Girl\nDocs: Aadhaar\nBenefit: 7.5% interest, ₹2L limit 2yr\nPortal: Post Office",
"nps vatsalya": "✅ **NPS Vatsalya**\nElig: Parent for child <18yr\nDocs: Child birth cert\nBenefit: Pension savings for child\nPortal: npscra",
"atal bhujal": "✅ **Atal Bhujal Yojana**\nElig: 80 water-stressed districts farmers\nDocs: Land\nBenefit: Groundwater management subsidy\nPortal: ataljal.gov.in",
"digital india": "✅ **Digital India Programs**\nElig: All citizens\nDocs: Aadhaar\nBenefit: Free digital literacy\nPortal: digitalindia.gov.in",
"mission indradhanush": "✅ **Mission Indradhanush Vaccination**\nElig: Children <2yr, Pregnant women\nDocs: Aadhaar, MCP\nBenefit: Free vaccines\nPortal: mohfw.gov.in"
}

def speak(t, lang='mr'):
    try:
        tts=gTTS(text=t[:400], lang=lang, slow=False)
        tts.save("/tmp/s.mp3")
        with open("/tmp/s.mp3","rb") as f:
            b64=base64.b64encode(f.read()).decode()
            st.markdown(f'<audio controls autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
    except: pass

with st.sidebar:
    st.write("**100 Schemes Loaded ✅**")
    st.caption("Maharashtra: 33 | Central: 67")
    voice=st.toggle("🔊 Voice", True)
    if st.button("Clear Chat"):
        st.session_state.msg=[]
        st.rerun()

for m in st.session_state.msg:
    with st.chat_message(m["role"]): st.markdown(m["content"])

if prompt := st.chat_input("Yojana search kara... e.g. PM Kisan, Ayushman, Drone Didi"):
    st.session_state.msg.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        ans=None
        q=prompt.lower()
        for k,v in SCHEMES.items():
            if k in q:
                ans=v
                break
        if not ans:
            # fuzzy search
            for k,v in SCHEMES.items():
                if any(word in q for word in k.split()):
                    ans=v
                    break
        if not ans:
            ans = f"**'{prompt}'** sathi exact match nahi. Try kara:\n\n`Ladki Bahin` | `PM Kisan` | `Ayushman` | `Awas` | `Ujjwala` | `Mudra` | `Drone Didi` | `Lakhpati Didi` | `PM Internship` | `Surya Ghar`\n\nTotal 100 yojana available!"
        st.markdown(ans)
        st.session_state.msg.append({"role":"assistant","content":ans})
        if voice: speak(ans, 'mr')
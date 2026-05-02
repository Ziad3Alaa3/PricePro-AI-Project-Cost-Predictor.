import streamlit as st
import pandas as pd
import joblib
import time
from streamlit_lottie import st_lottie
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="PricePro AI | Luxury Edition", page_icon="💎", layout="centered")

# جلب الأيقونات المتحركة
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_ai = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json") # أيقونة ذكاء اصطناعي متفاعلة

# 2. تصميم CSS 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Roboto:wght@300;400;700&display=swap');

    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
        color: #e9ecef;
    }

    /* كارت المدخلات  */
    [data-testid="stVerticalBlock"] > div:nth-child(2) {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* زرار الحساب  */
    div.stButton > button {
        background: linear-gradient(45deg, #00d2ff 0%, #3a7bd5 100%);
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        transition: all 0.4s ease;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.4);
        width: 100%;
    }

    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0, 210, 255, 0.7);
        color: #fff;
    }

    /* كارت النتيجة  */
    .price-card {
        background: rgba(0, 210, 255, 0.1);
        border-radius: 20px;
        border-left: 5px solid #00d2ff;
        padding: 20px;
        margin-top: 30px;
        animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# 3. محتوى الصفحة الرئيسي
if lottie_ai:
    st_lottie(lottie_ai, height=200, key="initial")

st.markdown("<h1 style='text-align: center; font-family: Orbitron; color: #00d2ff;'>PRICEPRO AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.7;'>Precision Machine Learning for Tech Valuations</p>", unsafe_allow_html=True)

# 4. تحميل الموديل
@st.cache_resource
def load_model():
    try:
        return joblib.load('project_cost_model.pkl')
    except:
        return None

model = load_model()

if model:
    # تقسيم المدخلات بشكل مريح 
    with st.container():
        st.markdown("###  Project Configuration")
        c1, c2 = st.columns(2)
        with c1:
            p_type = st.selectbox("Category", ['Web Development', 'Mobile App', 'Data Science', 'UI/UX Design', 'SEO'])
            hours = st.select_slider("Workload (Hours)", options=list(range(10, 1010, 10)), value=150)
        with c2:
            c_size = st.selectbox("Market Tier", ['Startup', 'Mid-Market', 'Enterprise'])
            exp = st.selectbox("Seniority Level", ['Junior', 'Mid-Level', 'Senior'])
        
        team = st.slider("Deployment Team Size", 1, 20, 3)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("GENERATE ESTIMATE"):
        with st.spinner('Analyzing market data...'):
            time.sleep(1.5) 
            
            input_df = pd.DataFrame({
                'Project_Type': [p_type], 'Hours_Estimated': [hours],
                'Team_Size': [team], 'Company_Size': [c_size], 'Experience_Required': [exp]
            })
            
            res = model.predict(input_df)[0]
            
            st.markdown(f"""
                <div class="price-card">
                    <h3 style='margin:0; color:#00d2ff;'>Analysis Complete </h3>
                    <p style='margin:5px 0; opacity:0.8;'>Based on current market trends and project complexity, the fair valuation is:</p>
                    <h1 style='margin:0; font-size:50px; color:white;'>${res:,.2f}</h1>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()

# 5. Sidebar Branding
with st.sidebar:
    st.markdown("<h2 style='color: #00d2ff;'>Ziad.AI</h2>", unsafe_allow_html=True)
    st.write("---")
    st.write("🚀 **Project:** Price Prediction")
    st.write("📊 **Model:** Random Forest Regressor")
    st.write("✅ **Accuracy:** 96%")
    st.write("---")
    st.markdown("[LinkedIn](https://linkedin.com) | [GitHub](https://github.com)")
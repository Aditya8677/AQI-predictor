import json
import requests
import streamlit as st
from streamlit_lottie import st_lottie
import numpy as np

# ------------------------------
# Lottie Loader
# ------------------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ------------------------------
# Health Message Function
# ------------------------------
def health_message(aqi):
    if 0 <= aqi <= 50:
        return (
            "🟢 *Good (0-50)*\n\nMinimal impact on health.\n"
            "Enjoy all activities freely.\n\n"
            "*Yoga Tips:* Tadasana (Mountain Pose), Vrikshasana (Tree Pose)\n"
            "*Food Tips:* Include tulsi tea, fresh fruits like apples, and omega-3 rich foods like flaxseeds.\n"
            "*Health Routine:* Daily morning walk, 10-minute deep breathing."
        )
    elif 51 <= aqi <= 100:
        return (
            "🟡 *Satisfactory (51-100)*\n\nMinor discomfort to sensitive individuals.\n"
            "Avoid long outdoor activities if you have asthma or other issues.\n\n"
            "*Yoga Tips:* Anulom Vilom, Bhramari Pranayama\n"
            "*Food Tips:* Turmeric milk, steamed vegetables, antioxidant-rich fruits like berries.\n"
            "*Health Routine:* Hydrate well and keep indoor plants for air purification."
        )
    elif 101 <= aqi <= 200:
        return (
            "🟠 *Moderate (101-200)*\n\nCan cause discomfort in lungs and throat.\n"
            "Sensitive groups should minimize outdoor exertion.\n\n"
            "*Yoga Tips:* Sheetali Pranayama, gentle Surya Namaskar indoors\n"
            "*Food Tips:* Use ginger, garlic, and honey; drink warm water with lemon.\n"
            "*Health Routine:* Use air-purifying masks and avoid morning jogs."
        )
    elif 201 <= aqi <= 300:
        return (
            "🔴 *Poor (201-300)*\n\nNoticeable discomfort. Avoid outdoor activities.\n"
            "People with heart/lung conditions must stay indoors.\n\n"
            "*Yoga Tips:* Practice Bhramari and deep belly breathing indoors.\n"
            "*Food Tips:* Avoid fried/spicy food; eat light meals; include green tea and citrus fruits.\n"
            "*Health Routine:* Use HEPA air purifiers; avoid heavy workouts."
        )
    elif 301 <= aqi <= 400:
        return (
            "🟤 *Very Poor (301-400)*\n\nHigh risk of respiratory illness.\n"
            "Stay indoors with clean air and rest.\n\n"
            "*Yoga Tips:* Meditation, Nadi Shodhana, and alternate nostril breathing.\n"
            "*Food Tips:* Steam inhalation with tulsi/eucalyptus, eat warm soups and organic veggies.\n"
            "*Health Routine:* Limit screen time, monitor oxygen levels if needed."
        )
    else:
        return (
            "⚫ *Severe (401+)*\n\nSevere health impacts. Even healthy people may experience symptoms.\n"
            "Emergency protocols should be followed.\n\n"
            "*Yoga Tips:* Avoid physical strain. Just practice slow, conscious breathing indoors.\n"
            "*Food Tips:* Consume herbal teas, jaggery, pomegranate, and avoid dairy temporarily.\n"
            "*Health Routine:* Stay indoors, wear N95 if needed, visit a doctor if symptoms persist."
        )

# ------------------------------
# Predict Page
# ------------------------------
def show_predict_page():
    st_lottie(load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_q5qeoo3q.json"), height=250, key="predict")
    st.title("Air Quality Prediction and Health Advisory")
    st.write("🔎 Enter air pollutant values to predict AQI and receive health advice.")

    co = st.slider("CO Level (mg/m³)", 0.0, 10.0, 1.0)
    no2 = st.slider("NO2 Level (µg/m³)", 0.0, 200.0, 50.0)
    pm2_5 = st.slider("PM2.5 Level (µg/m³)", 0.0, 500.0, 100.0)
    so2 = st.slider("SO2 Level (µg/m³)", 0.0, 50.0, 10.0)
    o3 = st.slider("O3 Level (µg/m³)", 0.0, 100.0, 30.0)

    if st.button("📈 Predict AQI"):
        aqi = (co * 5 + no2 * 0.5 + pm2_5 * 0.8 + so2 * 1.2 + o3 * 0.6)
        aqi = round(aqi, 2)
        with st.container():
            st.success(f"✅ Predicted AQI: *{aqi}*")
            st.info(health_message(aqi))

# ------------------------------
# Explore Page
# ------------------------------
def show_explore_page():
    st_lottie(load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_zlrpnoxz.json"), height=250, key="explore")
    st.title("Explore Air Quality Data")
    st.write("🧪 Explore how pollutant levels affect AQI. Use sliders to simulate different conditions.")

    co = st.slider("CO Level (mg/m³)", 0.0, 10.0, 1.0)
    no2 = st.slider("NO2 Level (µg/m³)", 0.0, 200.0, 50.0)
    pm2_5 = st.slider("PM2.5 Level (µg/m³)", 0.0, 500.0, 100.0)
    so2 = st.slider("SO2 Level (µg/m³)", 0.0, 50.0, 10.0)
    o3 = st.slider("O3 Level (µg/m³)", 0.0, 100.0, 30.0)

    if st.button("📊 View AQI Based on Pollutants"):
        aqi = (co * 5 + no2 * 0.5 + pm2_5 * 0.8 + so2 * 1.2 + o3 * 0.6)
        aqi = round(aqi, 2)
        st.subheader(f"Predicted AQI: {aqi}")
        st.info(health_message(aqi))

    aqi_values = [co, no2, pm2_5, so2, o3]
    pollutant_names = ["CO", "NO2", "PM2.5", "SO2", "O3"]

    st.write("📊 AQI Influence from Pollutants:")
    st.bar_chart(dict(zip(pollutant_names, aqi_values)))

# ------------------------------
# Landing Page
# ------------------------------
def show_landing_page():
    st_lottie(load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ydo1amjm.json"), height=300, key="landing")
    st.title("🌍 Welcome to the Air Quality Dashboard")
    st.write("Curious about the air you're breathing? Use our AQI Calculator to check air quality based on common pollutants.")
    if st.button("🌫️ Enter Dashboard"):
        st.session_state.landing_shown = True

# ------------------------------
# Main App
# ------------------------------
if "landing_shown" not in st.session_state:
    st.session_state.landing_shown = False

if not st.session_state.landing_shown:
    show_landing_page()
else:
    page = st.sidebar.selectbox("🔍 Navigation", ("Predict", "Explore"))
    if page == "Predict":
        show_predict_page()
    elif page == "Explore":
        show_explore_page()

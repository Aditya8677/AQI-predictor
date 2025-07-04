import streamlit as st
import numpy as np

def health_message(aqi):
    if 0 <= aqi <= 50:
        return "🌿 *Air Quality: Good* - Minimal impact on health. Maintain a healthy lifestyle with regular walks, hydration, and deep breathing exercises like Anulom-Vilom and Bhramari Pranayama."
    elif 51 <= aqi <= 100:
        return "🌤 *Satisfactory* - Minor discomfort for sensitive people. Consider light yoga such as Tadasana and gentle walking outdoors."
    elif 101 <= aqi <= 200:
        return "🌫 *Moderate* - People with lungs/heart problems may experience discomfort. Do indoor yoga like Sukhasana, and avoid outdoor cardio."
    elif 201 <= aqi <= 300:
        return "😷 *Poor* - Breathing discomfort with prolonged exposure. Stay indoors. Try breathing exercises and keep windows closed."
    elif 301 <= aqi <= 400:
        return "🚫 *Very Poor* - May cause illness even for healthy people. Do not exercise outdoors. Use air purifiers and do meditation and Pranayama indoors."
    else:
        return "☠ *Severe* - Serious health effects. Avoid all physical activity outside. Drink turmeric milk, use steam therapy, and consult a doctor if breathing worsens."

def show_predict_page():
    st.title("AQI Prediction and Health Advisory")
    st.write("🔎 Enter air pollutant values to predict AQI and receive personalized health tips.")

    PM2_5 = st.number_input("PM2.5 (0.1 - 120 µg/m³)", min_value=0.0, max_value=950.0, step=0.01, format="%.2f")
    NO2 = st.number_input("NO2 (0.01 - 60 ppb)", min_value=0.0, max_value=362.0, step=0.01, format="%.2f")
    CO = st.number_input("CO (0 - 3 ppm)", min_value=0.0, max_value=1756.0, step=0.01, format="%.2f")
    SO2 = st.number_input("SO2 (0.01 - 25 ppb)", min_value=0.0, max_value=194.0, step=0.01, format="%.2f")
    O3 = st.number_input("O3 (0.01 - 65 ppb)", min_value=0.0, max_value=258.0, step=0.01, format="%.2f")

    from predict import regressor  # make sure this import is correct!

    if st.button("📈 Calculate AQI"):
        X = np.array([[PM2_5, NO2, CO, SO2, O3]])
        X = X.astype(float)
        AQI = round(regressor.predict(X)[0], 2)

        st.markdown(
            f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
                <h3>✅ Estimated AQI: {AQI}</h3>
                <p style='font-size:18px'>{health_message(AQI)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown('[📁 GitHub Source Code](https://github.com/evon0101/Air-Quality-index-Prediction)', unsafe_allow_html=True)

    st.write("### 👨‍💻 Contributors")
    st.write("[Nooruddin](https://www.linkedin.com/in/nooruddin-shaikh)")
    st.write("[Karthik](https://www.linkedin.com/in/kartik-bhargav-93a3aa1b0/)")
    st.write("[Saurabh](https://www.linkedin.com/in/saurabh-jejurkar-b80042195)")
    st.write("[Milind](https://www.linkedin.com/in/milind-sai-2017/)")

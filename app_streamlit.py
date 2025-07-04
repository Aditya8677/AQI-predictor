import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64
import io
import time

# Set page configuration
st.set_page_config(
    page_title="Air Quality Index Predictor",
    page_icon="🌬️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and styling
def local_css():
    st.markdown("""
    <style>
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(66, 153, 225, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(66, 153, 225, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(66, 153, 225, 0);
        }
    }
    
    .stButton > button {
        border-radius: 20px;
        padding: 12px 24px;
        background-color: #4299e1;
        color: white;
        font-weight: bold;
        transition: all 0.3s ease;
        animation: pulse 2s infinite;
    }
    
    .stButton > button:hover {
        background-color: #3182ce;
        transform: translateY(-2px);
    }
    
    .css-1d391kg, .css-12oz5g7 {
        background-color: #f9fafc;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    h1, h2, h3 {
        color: #2d3748;
    }

    .fade-in {
        animation: fadeIn 1.5s;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    
    .slide-up {
        animation: slideUp 1s;
    }
    
    @keyframes slideUp {
        0% { 
            opacity: 0;
            transform: translateY(20px);
        }
        100% { 
            opacity: 1;
            transform: translateY(0);
        }
    }

    .aqi-scale {
        display: flex;
        justify-content: space-between;
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
    }
    
    .aqi-category {
        text-align: center;
        padding: 10px;
        border-radius: 5px;
        width: 18%;
    }
    
    .aqi-good {
        background-color: rgba(0, 228, 0, 0.7);
    }
    
    .aqi-moderate {
        background-color: rgba(255, 255, 0, 0.7);
        color: #333;
    }
    
    .aqi-sensitive {
        background-color: rgba(255, 126, 0, 0.7);
    }
    
    .aqi-unhealthy {
        background-color: rgba(255, 0, 0, 0.7);
        color: white;
    }
    
    .aqi-hazardous {
        background-color: rgba(143, 63, 151, 0.7);
        color: white;
    }

    .highlight-box {
        background-color: #EDF2F7;
        border-left: 5px solid #4299e1;
        padding: 15px;
        border-radius: 5px;
        margin: 20px 0;
    }

    .recommendation-item {
        background-color: white;
        padding: 10px 15px;
        border-radius: 5px;
        margin-bottom: 10px;
        border-left: 4px solid #4299e1;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# Create animated background for the header
def create_animated_header():
    st.markdown("""
    <div class="fade-in" style="text-align: center; padding: 30px 0;">
        <h1 style="font-size: 3rem; margin-bottom: 20px;">Air Quality Index Predictor</h1>
        <p class="slide-up" style="font-size: 1.2rem; max-width: 800px; margin: 0 auto 30px auto; color: #4A5568;">
            Assess air quality based on weather parameters and understand potential health impacts. 
            Make informed decisions about outdoor activities and protect your health with personalized recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Create AQI scale visualization
def create_aqi_scale():
    st.markdown("""
    <div class="aqi-scale fade-in">
        <div class="aqi-category aqi-good">
            <h3>Good</h3>
            <p>0-50</p>
        </div>
        <div class="aqi-category aqi-moderate">
            <h3>Moderate</h3>
            <p>51-100</p>
        </div>
        <div class="aqi-category aqi-sensitive">
            <h3>Sensitive</h3>
            <p>101-150</p>
        </div>
        <div class="aqi-category aqi-unhealthy">
            <h3>Unhealthy</h3>
            <p>151-200</p>
        </div>
        <div class="aqi-category aqi-hazardous">
            <h3>Hazardous</h3>
            <p>201+</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Function to visualize AQI with a gauge
def create_aqi_gauge(aqi_value):
    if aqi_value <= 50:
        color = "green"
        level = "Good"
    elif aqi_value <= 100:
        color = "yellow"
        level = "Moderate"
    elif aqi_value <= 150:
        color = "orange"
        level = "Unhealthy for Sensitive Groups"
    elif aqi_value <= 200:
        color = "red"
        level = "Unhealthy"
    else:
        color = "purple"
        level = "Very Unhealthy to Hazardous"
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = aqi_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Air Quality Index: {level}", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [None, 300], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(0, 228, 0, 0.7)'},
                {'range': [50, 100], 'color': 'rgba(255, 255, 0, 0.7)'},
                {'range': [100, 150], 'color': 'rgba(255, 126, 0, 0.7)'},
                {'range': [150, 200], 'color': 'rgba(255, 0, 0, 0.7)'},
                {'range': [200, 300], 'color': 'rgba(143, 63, 151, 0.7)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': aqi_value
            }
        }
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

# Main application
def main():
    # Session state initialization for multi-page flow
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    if 'aqi_value' not in st.session_state:
        st.session_state.aqi_value = None
    if 'impact_assessment' not in st.session_state:
        st.session_state.impact_assessment = None
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/air-quality.png", width=100)
        st.title("Navigation")
        
        if st.button("Home"):
            st.session_state.page = "home"
            
        if st.button("Check AQI"):
            st.session_state.page = "check_aqi"
            
        if st.session_state.aqi_value is not None:
            if st.button("Health Impact"):
                st.session_state.page = "health_impact"
                
        st.markdown("---")
        st.markdown("#### About AQI")
        st.markdown("""
        The Air Quality Index (AQI) is a measure used to communicate how polluted the air is and what associated health effects might be of concern.
        
        This app helps you:
        - Predict AQI based on weather parameters
        - Assess potential health impacts
        - Get personalized recommendations
        """)

    # Main content based on current page
    if st.session_state.page == "home":
        create_animated_header()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="slide-up">', unsafe_allow_html=True)
            if st.button("Check Air Quality Index", key="main_button"):
                st.session_state.page = "check_aqi"
            st.markdown('</div>', unsafe_allow_html=True)
            
        create_aqi_scale()
        
        # Adding some informative content
        st.markdown("---")
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        st.subheader("Why Monitor Air Quality?")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="highlight-box">
                <h3>Health Impact</h3>
                <p>Poor air quality can lead to respiratory issues, cardiovascular problems, and worsen existing health conditions.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="highlight-box">
                <h3>Daily Activities</h3>
                <p>Making informed decisions about outdoor activities, especially for sensitive groups like children, elderly, and those with respiratory conditions.</p>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
            
    elif st.session_state.page == "check_aqi":
        st.markdown('<h2 class="fade-in">Enter Weather Parameters</h2>', unsafe_allow_html=True)
        
        # Animated loading effect
        with st.container():
            st.markdown('<div class="slide-up">', unsafe_allow_html=True)
            
            # Create a form for input parameters
            with st.form("aqi_prediction_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    T = st.number_input("Temperature (°C)", format="%.1f", step=0.1)
                    TM = st.number_input("Maximum Temperature (°C)", format="%.1f", step=0.1)
                    Tm = st.number_input("Minimum Temperature (°C)", format="%.1f", step=0.1)
                    SLP = st.number_input("Sea Level Pressure (hPa)", value=1013.2, format="%.1f", step=0.1)
                    
                with col2:
                    H = st.number_input("Humidity (%)", value=50.0, min_value=0.0, max_value=100.0, format="%.1f", step=0.1)
                    VV = st.number_input("Visibility (km)", value=10.0, format="%.1f", step=0.1)
                    V = st.number_input("Wind Speed (km/h)", value=10.0, format="%.1f", step=0.1)
                    VM = st.number_input("Maximum Wind Speed (km/h)", value=15.0, format="%.1f", step=0.1)
                
                submitted = st.form_submit_button("Predict AQI")
                
                if submitted:
                    # Show loading animation
                    with st.spinner("Calculating AQI..."):
                        time.sleep(1)  # Simulate processing time
                        
                        # Prepare data for prediction
                        input_data = {
                            'T': T,
                            'TM': TM,
                            'Tm': Tm,
                            'SLP': SLP,
                            'H': H,
                            'VV': VV,
                            'V': V,
                            'VM': VM
                        }
                        
                        try:
                            # Make prediction using Flask backend
                            response = requests.post('http://localhost:5000/predict', data=input_data)
                            result = response.json()
                            
                            # Store AQI value in session state
                            st.session_state.aqi_value = result['aqi']
                            
                            # Redirect to result display
                            st.session_state.page = "aqi_result"
                            st.experimental_rerun()
                        except Exception as e:
                            st.error(f"Error making prediction: {str(e)}")
                            st.info("Make sure your Flask backend is running on localhost:5000")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Back to Home", key="back_to_home"):
                st.session_state.page = "home"
                st.experimental_rerun()
                
    elif st.session_state.page == "aqi_result":
        st.markdown('<h2 class="fade-in">AQI Prediction Result</h2>', unsafe_allow_html=True)
        
        aqi_value = st.session_state.aqi_value
        
        # Display AQI gauge
        st.plotly_chart(create_aqi_gauge(aqi_value), use_container_width=True)
        
        # Add explanation based on AQI value
        if aqi_value <= 50:
            explanation = "Air quality is considered satisfactory, and air pollution poses little or no risk."
        elif aqi_value <= 100:
            explanation = "Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people."
        elif aqi_value <= 150:
            explanation = "Members of sensitive groups may experience health effects. The general public is not likely to be affected."
        elif aqi_value <= 200:
            explanation = "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."
        else:
            explanation = "Health warnings of emergency conditions. The entire population is more likely to be affected."
            
        st.markdown(f"""
        <div class="highlight-box fade-in">
            <p>{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("Check Health Impact", key="check_health_impact"):
                st.session_state.page = "health_impact"
                st.experimental_rerun()
                
            if st.button("Return to Home", key="return_home"):
                st.session_state.page = "home"
                st.experimental_rerun()
                
    elif st.session_state.page == "health_impact":
        st.markdown('<h2 class="fade-in">Assess Health Impact</h2>', unsafe_allow_html=True)
        
        st.markdown('<div class="slide-up">', unsafe_allow_html=True)
        
        with st.form("health_assessment_form"):
            aqi_value = st.session_state.aqi_value
            st.info(f"Current AQI: {aqi_value:.1f}")
            
            exposure_time = st.slider("Exposure Time (hours)", 1, 24, 8)
            age = st.number_input("Age", min_value=1, max_value=120, value=35)
            health_condition = st.selectbox(
                "Pre-existing Health Condition",
                ["none", "respiratory", "cardiovascular", "allergies", "other"]
            )
            
            submitted = st.form_submit_button("Get Health Assessment")
            
            if submitted:
                with st.spinner("Analyzing health impact..."):
                    time.sleep(1)  # Simulate processing time
                    
                    # Prepare data for health assessment
                    input_data = {
                        'aqi_value': aqi_value,
                        'exposure_time': exposure_time,
                        'age': age,
                        'health_condition': health_condition
                    }
                    
                    try:
                        # Make prediction using Flask backend
                        response = requests.post('http://localhost:5000/predict_health', data=input_data)
                        result = response.json()
                        
                        # Store result in session state
                        st.session_state.impact_assessment = result
                        
                        # Redirect to health result display
                        st.session_state.page = "health_result"
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Error getting health assessment: {str(e)}")
                        st.info("Make sure your Flask backend is running on localhost:5000")
                        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("Back to AQI Result", key="back_to_aqi"):
            st.session_state.page = "aqi_result"
            st.experimental_rerun()
            
    elif st.session_state.page == "health_result":
        assessment = st.session_state.impact_assessment
        
        # Color mapping for impact levels
        color_map = {
            "Low Health Risk": "green",
            "Moderate Health Risk": "yellow",
            "Unhealthy for Sensitive Groups": "orange",
            "Unhealthy": "red",
            "Very Unhealthy to Hazardous": "purple"
        }
        
        impact_color = color_map.get(assessment['impact_level'], "gray")
        
        st.markdown(f"""
        <h2 class="fade-in">Health Impact Assessment</h2>
        <div style="background-color: white; padding: 20px; border-radius: 10px; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h3 style="color: {impact_color}; font-size: 24px; text-align: center;">{assessment['impact_level']}</h3>
            <p style="margin: 15px 0; font-size: 16px;">{assessment['risk_description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h3 class="fade-in">Recommendations:</h3>', unsafe_allow_html=True)
        
        for i, recommendation in enumerate(assessment['recommendations']):
            st.markdown(f"""
            <div class="recommendation-item slide-up" style="animation-delay: {i*0.2}s">
                {recommendation}
            </div>
            """, unsafe_allow_html=True)
            
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Start Over", key="start_over"):
                st.session_state.page = "home"
                st.session_state.aqi_value = None
                st.session_state.impact_assessment = None
                st.experimental_rerun()
                
        with col2:
            if st.button("Check Another AQI", key="another_aqi"):
                st.session_state.page = "check_aqi"
                st.experimental_rerun()

if __name__ == "__main__":
    main()
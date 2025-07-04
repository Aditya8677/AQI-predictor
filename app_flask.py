from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes to allow Streamlit to access the API

# Load the trained model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/predict', methods=['POST'])
def predict():
    # Get form data
    features = [float(request.form[x]) for x in ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM']]
    
    # Convert to numpy array
    final_features = np.array(features).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(final_features)[0]
    
    # Return prediction as JSON
    return jsonify({
        'aqi': float(prediction)
    })

@app.route('/predict_health', methods=['POST'])
def predict_health():
    # Get form data
    aqi_value = float(request.form['aqi_value'])
    exposure_time = int(request.form['exposure_time'])
    age = int(request.form['age'])
    health_condition = request.form['health_condition']
    
    # Logic for health impact (this is a simplified example)
    impact_level = ''
    risk_description = ''
    recommendations = []
    
    # Determine impact based on AQI value
    if aqi_value <= 50:
        impact_level = 'Low Health Risk'
        risk_description = 'Air quality is good and poses little or no risk.'
        recommendations = [
            'Continue with normal outdoor activities',
            'No special precautions needed',
            'Enjoy the clean air'
        ]
    elif aqi_value <= 100:
        impact_level = 'Moderate Health Risk'
        risk_description = 'Air quality is acceptable, but there may be moderate health concerns for sensitive individuals.'
        
        if health_condition in ['respiratory', 'cardiovascular', 'allergies'] or age > 65 or age < 10:
            recommendations = [
                'Consider reducing prolonged outdoor exertion',
                'Monitor your symptoms',
                'Keep any necessary medication accessible'
            ]
        else:
            recommendations = [
                'Most people can continue outdoor activities',
                'Watch for unusual symptoms like coughing or throat irritation',
                'Stay hydrated'
            ]
    elif aqi_value <= 150:
        impact_level = 'Unhealthy for Sensitive Groups'
        risk_description = 'Members of sensitive groups may experience health effects. The general public is less likely to be affected.'
        
        if health_condition in ['respiratory', 'cardiovascular', 'allergies']:
            recommendations = [
                'Reduce prolonged or heavy outdoor exertion',
                'Take more breaks during outdoor activities',
                'Consider moving longer or more intense activities indoors',
                'Have relief medication readily available'
            ]
        elif age > 65 or age < 10:
            recommendations = [
                'Limit prolonged outdoor activities',
                'Take frequent breaks when outdoors',
                'Monitor for respiratory symptoms'
            ]
        else:
            recommendations = [
                'Unusually sensitive people should consider reducing prolonged exertion',
                'Watch for symptoms such as coughing or shortness of breath',
                'Reduce prolonged outdoor activities if experiencing symptoms'
            ]
    elif aqi_value <= 200:
        impact_level = 'Unhealthy'
        risk_description = 'Everyone may begin to experience health effects. Sensitive groups may experience more serious effects.'
        
        if exposure_time > 3:
            risk_description += ' Extended exposure increases health risks.'
            
        if health_condition in ['respiratory', 'cardiovascular']:
            recommendations = [
                'Avoid prolonged outdoor exertion',
                'Consider rescheduling outdoor activities',
                'Stay indoors with air purification if possible',
                'Have emergency medication readily available',
                'Monitor symptoms closely'
            ]
        else:
            recommendations = [
                'Reduce prolonged or heavy outdoor exertion',
                'Take frequent breaks during outdoor activities',
                'Consider rescheduling strenuous outdoor activities',
                'Use a mask designed for air pollution when outdoors'
            ]
    else:
        impact_level = 'Very Unhealthy to Hazardous'
        risk_description = 'Health alert: everyone may experience more serious health effects.'
        
        if exposure_time > 1:
            risk_description += ' Even short-term exposure can lead to significant health effects.'
            
        recommendations = [
            'Avoid all outdoor physical activities',
            'Stay indoors with windows closed',
            'Use air purifiers if available',
            'Wear a proper mask if you must go outside',
            'Seek medical attention if experiencing difficulty breathing or other severe symptoms'
        ]
        
        if health_condition in ['respiratory', 'cardiovascular'] or age > 65 or age < 10:
            recommendations.append('Consider temporarily relocating to an area with better air quality if possible')
    
    # Return assessment as JSON
    return jsonify({
        'impact_level': impact_level,
        'risk_description': risk_description,
        'recommendations': recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
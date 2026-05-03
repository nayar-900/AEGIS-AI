import streamlit as st
import pandas as pd
import numpy as np
import joblib
import leafmap.foliumap as leafmap
import folium
import os
from geopy.geocoders import Nominatim

st.set_page_config(page_title="AEGIS: Resource Allocation", layout="wide")

st.title("Resource Allocation & Impact Intelligence")

MODEL_PATH = os.path.join('models', 'earthquake_model.pkl')

@st.cache_resource
def load_ai_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

model = load_ai_model()

if model is None:
    st.warning("No AI model found. Please train the model first.")
    st.stop()

# --- SIDEBAR: LOCATION SEARCH ---
st.sidebar.header("Find Location")
place_name = st.sidebar.text_input("Enter Place Name", "")

default_lat, default_lon = 31.5204, 74.3587

if place_name:
    try:
        geolocator = Nominatim(user_agent="disaster_response_app")
        location = geolocator.geocode(place_name)
        if location:
            default_lat, default_lon = location.latitude, location.longitude
            st.sidebar.success(f"Found: {location.address[:30]}...")
    except:
        st.sidebar.error("Geocoding service busy.")

st.sidebar.write("---")
st.sidebar.header("Precise Coordinates")
lat = st.sidebar.number_input("Latitude", value=default_lat, format="%.4f")
lon = st.sidebar.number_input("Longitude", value=default_lon, format="%.4f")
depth = st.sidebar.slider("Depth (km)", 0, 700, 10)

# --- COMMUNITY CONTEXT ---
st.sidebar.write("---")
st.sidebar.header("Community Context")
pop_density = st.sidebar.selectbox(
    "Area Population Type",
    ["Sparsely Populated (Rural)", "Moderately Populated (Suburban)", "Densely Populated (Urban City)"]
)

pop_multiplier = 1.0
if pop_density == "Moderately Populated (Suburban)":
    pop_multiplier = 4.0
elif pop_density == "Densely Populated (Urban City)":
    pop_multiplier = 12.0

# --- SATELLITE SETTINGS ---
st.sidebar.header("Satellite View")
basemap_type = st.sidebar.selectbox("Select Source", ["SATELLITE", "HYBRID", "TERRAIN", "ROADMAP"])

# --- AI PREDICTION & ADVANCED IMPACT LOGIC ---
input_data = pd.DataFrame([[depth, lat, lon]], columns=['depth', 'latitude', 'longitude'])
predicted_mag = model.predict(input_data)[0]

def calculate_advanced_impact(mag, d, multiplier):
    """
    Semester 5 Logic: Impact is proportional to Magnitude and Density,
    but inversely proportional to the log of Depth (Shallow = More Dangerous).
    """
    safe_depth = max(d, 1) # Avoid log(0)
    # Scientific Formula: Mag * Pop / log(Depth)
    score = (mag * multiplier) / (np.log1p(safe_depth))
    return round(score, 2)

impact_score = calculate_advanced_impact(predicted_mag, depth, pop_multiplier)

def get_plan(mag, multiplier):
    if mag >= 7.0:
        res = {"L": "💀 CRITICAL", "M": int(50 * multiplier), "S": "National Guard + Heavy SAR"}
    elif mag >= 6.0:
        res = {"L": "🔴 STRONG", "M": int(25 * multiplier), "S": "Full Regional SAR Teams"}
    elif mag >= 5.0:
        res = {"L": "🟠 MODERATE", "M": int(10 * multiplier), "S": "Local SAR + Fire Dept"}
    elif mag >= 3.0:
        res = {"L": "🟡 LIGHT", "M": int(3 * multiplier), "S": "Standby Monitoring"}
    else:
        res = {"L": "🟢 MINOR", "M": int(1 * multiplier), "S": "None Required"}
    return res

plan = get_plan(predicted_mag, pop_multiplier)

# --- DASHBOARD DISPLAY ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("AI Risk Assessment")
    st.metric("Predicted Magnitude", f"{predicted_mag:.2f}")
    
    # NEW: Advanced Impact Metric
    st.metric("Calculated Impact Score", impact_score)
    # Impact progress bar
    progress_val = min(impact_score / 100, 1.0)
    st.progress(progress_val)
    st.caption("AI-Calculated Impact (Factors in Depth & Density)")
    
    if "CRITICAL" in plan['L'] or "STRONG" in plan['L']:
        st.error(f"Response Level: {plan['L']}")
    elif "MODERATE" in plan['L']:
        st.warning(f"Response Level: {plan['L']}")
    else:
        st.success(f"Response Level: {plan['L']}")
    
    st.write("---")
    st.subheader("Dispatch Orders")
    st.write(f"**Medical Units:** {plan['M']}")
    st.write(f"**Search & Rescue:** {plan['S']}")
    
    report_text = f"Location: {lat}, {lon}\nMag: {predicted_mag:.2f}\nImpact: {impact_score}\nMedics: {plan['M']}"
    st.download_button("Download Dispatch Plan", report_text, file_name="dispatch.txt")

with col2:
    st.subheader("Satellite Intelligence")
    m = leafmap.Map(center=[lat, lon], zoom=12)
    m.add_basemap(basemap_type)
    
    # Visualizing the impact zone based on calculated impact score
    folium.Circle(
        location=[lat, lon], 
        radius=int(impact_score * 100), # Radius grows with impact score
        color="red", fill=True, fill_opacity=0.3,
        popup=f"Impact Radius: {impact_score} units"
    ).add_to(m)
    
    folium.Marker(
        location=[lat, lon], 
        icon=folium.Icon(color="red", icon="warning", prefix='fa'),
        popup=f"Epicenter: {lat}, {lon}"
    ).add_to(m)

    m.to_streamlit(height=600)
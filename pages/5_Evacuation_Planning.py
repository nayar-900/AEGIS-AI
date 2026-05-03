import streamlit as st
import leafmap.foliumap as leafmap
import folium
import pandas as pd
import requests
import joblib
import os
import numpy as np
from geopy.distance import geodesic

st.set_page_config(page_title="Real-World Evacuation Planning", layout="wide")

st.title("Evacuation and Safe Zone Routing")

# --- LOAD AI MODEL FOR PREDICTION ---
MODEL_PATH = os.path.join('models', 'earthquake_model.pkl')

@st.cache_resource
def load_ai_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

model = load_ai_model()

# --- 1. SIDEBAR CONTROLS ---
st.sidebar.header("Disaster Epicenter")
lat = st.sidebar.number_input("Latitude", value=33.6996, format="%.4f")
lon = st.sidebar.number_input("Longitude", value=73.0362, format="%.4f")
radius_km = st.sidebar.slider("Evacuation Radius (km)", 2, 20, 5)
depth = st.sidebar.slider("Simulated Depth (km)", 0, 700, 10)

st.sidebar.header("Map Settings")
basemap_type = st.sidebar.selectbox("Satellite View", ["HYBRID", "SATELLITE", "TERRAIN", "ROADMAP"])

# --- 2. RESOURCE GAP LOGIC FUNCTION ---
def analyze_resource_gap(required_units, available_facilities):
    """
    Calculates infrastructure resilience. 
    Assumes each facility has a capacity of 5 units.
    """
    total_capacity = available_facilities * 5
    gap = required_units - total_capacity
    
    if gap <= 0:
        return "Sufficient", gap, "green"
    elif gap < (required_units * 0.5):
        return "Moderate Strain", gap, "orange"
    else:
        return "Critical Shortfall", gap, "red"

# --- 3. DATA FETCHING (OpenStreetMap) ---
@st.cache_data(ttl=3600)
def fetch_real_safe_zones(lat, lon, radius=10000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
      node["amenity"="community_centre"](around:{radius},{lat},{lon});
    );
    out body;
    """
    try:
        response = requests.get(overpass_url, params={'data': overpass_query}, timeout=10)
        data = response.json()
        places = []
        for element in data['elements']:
            places.append({
                "Name": element['tags'].get('name', 'Unnamed Facility'),
                "lat": element['lat'],
                "lon": element['lon'],
                "Type": element['tags'].get('amenity', 'Safe Zone').title()
            })
        return pd.DataFrame(places)
    except:
        return pd.DataFrame()

with st.spinner("Searching real-world infrastructure database..."):
    safe_zones = fetch_real_safe_zones(lat, lon, radius=15000)

# --- 4. AI PREDICTION FOR ANALYSIS ---
if model:
    input_data = pd.DataFrame([[depth, lat, lon]], columns=['depth', 'latitude', 'longitude'])
    predicted_mag = model.predict(input_data)[0]
    # Required units calculation (Magnitude based)
    required_med_units = int(predicted_mag * 8) 
else:
    predicted_mag = 0
    required_med_units = 0

# --- 5. DASHBOARD LAYOUT ---
col_map, col_info = st.columns([2, 1])

with col_map:
    st.subheader("Live Infrastructure Map")
    m = leafmap.Map(center=[lat, lon], zoom=13)
    m.add_basemap(basemap_type)

    folium.Circle(
        location=[lat, lon],
        radius=radius_km * 1000,
        color="red", weight=2, fill=True, fill_opacity=0.3,
        popup="DANGER ZONE"
    ).add_to(m)

    folium.Marker([lat, lon], icon=folium.Icon(color='darkred', icon='bolt', prefix='fa')).add_to(m)

    valid_zones_count = 0
    if not safe_zones.empty:
        for _, zone in safe_zones.iterrows():
            dist = geodesic((lat, lon), (zone['lat'], zone['lon'])).km
            if dist > radius_km:
                valid_zones_count += 1
                icon_color = "green" if "Hospital" in zone['Type'] else "blue"
                folium.Marker(
                    [zone['lat'], zone['lon']],
                    popup=f"{zone['Name']} ({dist:.1f}km away)",
                    icon=folium.Icon(color=icon_color, icon='plus' if icon_color=="green" else 'shield-halved', prefix='fa')
                ).add_to(m)
                folium.PolyLine(
                    locations=[[lat, lon], [zone['lat'], zone['lon']]],
                    color="yellow", weight=2, dash_array='5'
                ).add_to(m)
    else:
        st.warning("No medical facilities found via OpenStreetMap.")

    m.to_streamlit(height=600)

with col_info:
    st.subheader("Infrastructure Resilience")
    
    if model:
        status, gap, color = analyze_resource_gap(required_med_units, valid_zones_count)
        
        st.metric("Predicted Magnitude", f"{predicted_mag:.2f}")
        st.write(f"**Required Capacity:** {required_med_units} Units")
        st.write(f"**Available Safe Facilities:** {valid_zones_count}")
        
        if color == "red":
            st.error(f"Status: {status}")
            st.write(f"Critical Shortfall: {abs(gap)} units")
        elif color == "orange":
            st.warning(f"Status: {status}")
        else:
            st.success(f"Status: {status}")
    else:
        st.info("Train AI model to enable Gap Analysis.")

    st.write("---")
    st.subheader("Evacuation Targets")
    if not safe_zones.empty:
        # Filter only safe zones outside danger radius
        safe_zones['dist'] = safe_zones.apply(lambda x: geodesic((lat, lon), (x['lat'], x['lon'])).km, axis=1)
        targets = safe_zones[safe_zones['dist'] > radius_km].sort_values('dist')
        
        if not targets.empty:
            for _, zone in targets.head(5).iterrows():
                with st.expander(f"{zone['Name']} ({zone['dist']:.1f}km)"):
                    st.write(f"Type: {zone['Type']}")
                    st.button(f"Deploy to {zone['Name'][:10]}", key=zone['Name'])
        else:
            st.write("All nearby facilities are within the danger zone.")
    else:
        st.write("No infrastructure data available.")
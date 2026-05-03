import os
os.environ["PYTHONUTF8"] = "1"

import streamlit as st
import folium
import pandas as pd
import joblib
import datetime
from streamlit.components.v1 import html
from utils.data_processor import fetch_latest_earthquakes, purify_data

st.set_page_config(page_title="Live Global Monitoring", layout="wide")

# --- CSS ---
st.markdown("""
    <style>
    @keyframes flash {
        0% { background-color: #ff4b4b; }
        50% { background-color: #1e1e1e; }
        100% { background-color: #ff4b4b; }
    }
    .flash-alert {
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-weight: bold;
        animation: flash 1s infinite;
        margin-bottom: 10px;
        border: 2px solid white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Live Global Monitoring and Intelligent Alerts")

# --- MODEL ---
@st.cache_resource
def load_model():
    path = os.path.join('models', 'earthquake_model.pkl')
    return joblib.load(path) if os.path.exists(path) else None

model = load_model()

# --- SIDEBAR ---
st.sidebar.header("Map Controls")
basemap_type = st.sidebar.selectbox(
    "Select View", ["Default", "Terrain", "Dark"]
)
min_mag = st.sidebar.slider("Minimum Magnitude", 0.0, 9.0, 3.0)

# --- BROADCAST ---
def simulate_emergency_broadcast(event_data):
    st.sidebar.write("---")
    st.sidebar.subheader("Automated Broadcast System")
    
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.sidebar.error(f"BROADCAST SENT AT {timestamp}")
    
    safe_location = str(event_data['location']).encode('utf-8', 'ignore').decode('utf-8')
    
    alert_msg = f"CRITICAL: {event_data['magnitude']} Mag quake at {safe_location}"
    st.sidebar.info(alert_msg)
    
    if 'broadcast_log' not in st.session_state:
        st.session_state['broadcast_log'] = []
    
    log = f"[{timestamp}] {safe_location} ({event_data['magnitude']})"
    if log not in st.session_state['broadcast_log']:
        st.session_state['broadcast_log'].append(log)

# --- DATA ---
raw_data = fetch_latest_earthquakes()

if raw_data is not None:
    df = purify_data(raw_data)

    # 🔥 CLEAN DATA
    df['location'] = df['location'].astype(str).apply(
        lambda x: x.encode('utf-8', 'ignore').decode('utf-8')
    )
    df = df.dropna(subset=['latitude', 'longitude', 'magnitude'])

    # --- ALERTS ---
    high_risk = df[df['magnitude'] >= 6.0]

    if not high_risk.empty:
        for i, alert in high_risk.iterrows():
            loc = alert['location']
            st.markdown(f"""
            <div class="flash-alert">
            🚨 {alert['magnitude']} Mag Earthquake at {loc}
            </div>
            """, unsafe_allow_html=True)

            if i == high_risk.index[0]:
                simulate_emergency_broadcast(alert)

        st.components.v1.html(
            """<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>""",
            height=0
        )

    # --- FILTER ---
    filtered_df = df[df['magnitude'] >= min_mag].copy()

    if model:
        filtered_df['ai_risk_score'] = model.predict(
            filtered_df[['depth', 'latitude', 'longitude']]
        )

    # --- LAYOUT ---
    col_map, col_log = st.columns([2, 1])

    # --- MAP ---
    with col_map:
        m = folium.Map(location=[20, 0], zoom_start=2)

        # Basemap options
        if basemap_type == "Terrain":
            folium.TileLayer('Stamen Terrain').add_to(m)
        elif basemap_type == "Dark":
            folium.TileLayer('CartoDB dark_matter').add_to(m)

        for _, row in filtered_df.iterrows():
            color = "red" if row['magnitude'] > 6 else "orange" if row['magnitude'] > 4.5 else "blue"

            popup = f"""
            Mag: {row['magnitude']}<br>
            Loc: {row['location']}<br>
            Depth: {row['depth']} km
            """

            folium.Circle(
                location=[row['latitude'], row['longitude']],
                radius=row['magnitude'] * 15000,
                color=color,
                fill=True,
                fill_opacity=0.6,
                popup=popup
            ).add_to(m)

        # ✅ SAFE RENDER
        html(m._repr_html_(), height=600)

    # --- LOG ---
    with col_log:
        st.subheader("Broadcast Log")
        logs = st.session_state.get('broadcast_log', [])
        if logs:
            for l in reversed(logs):
                st.info(l)
        else:
            st.write("No alerts yet.")

    # --- TABLE ---
    st.write("---")
    st.subheader("All Data")
    st.dataframe(filtered_df.sort_values(by='magnitude', ascending=False))

else:
    st.error("Failed to fetch live data.")
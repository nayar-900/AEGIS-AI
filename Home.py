import os
os.environ["PYTHONUTF8"] = "1"
import streamlit as st
import leafmap.foliumap as leafmap
from utils.data_processor import fetch_latest_earthquakes, purify_data

st.set_page_config(page_title="AEGIS-AI", layout="wide")

st.title("AEGIS-AI")

st.markdown("""
### Welcome to the Automated Earthquake Locate & Response Management Portal
This system integrates **Real-time USGS Seismic Data** with **Machine Learning** to provide:
1. **Live Monitoring** of global earthquake events.
2. **AI-Driven Risk Prediction** based on historical patterns.
3. **Automated Resource Allocation** for emergency responders.
""")

# Quick Global Snapshot
raw_data = fetch_latest_earthquakes()
if raw_data is not None:
    data = purify_data(raw_data)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Recent Events", len(data))
    m2.metric("Max Magnitude", f"{data['magnitude'].max():.1f}")
    m3.metric("Avg Depth", f"{data['depth'].mean():.1f} km")

    st.subheader("Global Seismic Heatmap")
    m = leafmap.Map(center=[20, 0], zoom=2)
    m.add_heatmap(data, latitude="latitude", longitude="longitude", value="magnitude", name="Heatmap")
    m.to_streamlit(height=500)
else:
    st.error("Unable to connect to live data feed.")
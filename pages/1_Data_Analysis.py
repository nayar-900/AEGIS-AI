import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_processor import fetch_latest_earthquakes, purify_data

st.set_page_config(page_title="Data Analysis", layout="wide")

st.title("Geospatial Data Analysis & Purification")

# Fetch Data
with st.spinner("Fetching live USGS data..."):
    raw_df = fetch_latest_earthquakes()
    if raw_df is not None:
        df = purify_data(raw_df)
        
        # 1. Statistical Summary
        st.subheader("1. Data Purification Summary")
        col1, col2, col3 = st.columns(3)
        col1.write("**Raw Columns Found:**")
        col1.write(list(raw_df.columns)[:5]) # Show first 5 raw cols
        col2.write("**Purified Features:**")
        col2.write(['magnitude', 'depth', 'latitude', 'longitude'])
        col3.metric("Cleaned Rows", len(df))

        st.divider()

        # 2. Correlation Analysis (Requirement #2)
        st.subheader("2. Magnitude vs. Depth Correlation")
        fig = px.scatter(df, x="depth", y="magnitude", 
                         color="magnitude", 
                         title="Seismic Correlation: How Depth affects Magnitude",
                         labels={"depth": "Depth (km)", "magnitude": "Magnitude (Mw)"},
                         template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # 3. Data Distribution
        st.subheader("3. Magnitude Distribution")
        fig_hist = px.histogram(df, x="magnitude", nbins=20, 
                                title="Frequency of Earthquake Magnitudes",
                                color_discrete_sequence=['#F63366'])
        st.plotly_chart(fig_hist, use_container_width=True)

    else:
        st.error("Failed to load data. Please check USGS connection.")
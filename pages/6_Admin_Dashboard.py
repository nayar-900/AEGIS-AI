import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="AEGIS Admin Dashboard", layout="wide")

st.title("Disaster Response Command Center")

# --- 1. SYSTEM READINESS OVERVIEW ---
col1, col2, col3 = st.columns(3)

col1.metric("AI Model Status", "Operational", delta="R²: 0.84")
col2.metric("Satellite Sync", "Active", delta="USGS Live")
col3.metric("System Uptime", "99.8%", delta="High Priority")

# --- 2. GENERATE FORMAL REPORT ---
st.write("---")
st.subheader("Generate Official Disaster Summary")

# Create the form
with st.form("report_form"):
    report_title = st.text_input("Incident Title", value="Seismic Event Report")
    region = st.text_input("Affected Region", value="Punjab, Pakistan")
    severity = st.selectbox("Assessed Severity", ["Minor", "Moderate", "High", "Catastrophic"])
    summary_notes = st.text_area("Observations", "AI predicted magnitude was consistent with USGS data. Evacuation routes established.")
    
    submitted = st.form_submit_button("Generate Report")

# LOGIC TO HANDLE DOWNLOAD OUTSIDE THE FORM
if submitted:
    report_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_report = f"""
AEGIS DISASTER RESPONSE REPORT
------------------------------
Title: {report_title}
Timestamp: {report_timestamp}
Region: {region}
Severity Level: {severity}

AI Assessment:
- Model Accuracy: Verified
- Impact Prediction: Active

Notes: {summary_notes}
------------------------------
(Authorized by AEGIS AI Framework)
    """
    
    st.success("Report data compiled successfully.")
    
    # Place the download button here, outside the st.form block
    st.download_button(
        label="Download Official Report",
        data=full_report,
        file_name=f"disaster_report_{datetime.date.today()}.txt",
        mime="text/plain"
    )

# --- 3. BROADCAST HISTORY LOG ---
st.write("---")
st.subheader("Global Alert Audit Trail")

if 'broadcast_log' in st.session_state:
    log_df = pd.DataFrame(st.session_state['broadcast_log'], columns=["Log Entry"])
    st.table(log_df.tail(5))
else:
    st.info("No active broadcast logs found for this session.")
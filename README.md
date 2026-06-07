<div align="center">

<img width="100%" src="https://svg-banners.vercel.app/api?type=glitch&text1=AEGIS%20AI&width=900&height=160&textColor1=58a6ff&textColor2=ffa657" />

<h3>Automated Earthquake Geospatial Intelligence System</h3>

<p><i>From raw seismic signal to actionable rescue plan — fully automated, zero human bottleneck.</i></p>

<br/>

![Python](https://img.shields.io/badge/Python_3.10+-0d1f3c?style=flat-square&logo=python&logoColor=58A6FF)
![Streamlit](https://img.shields.io/badge/Streamlit-0d1f3c?style=flat-square&logo=streamlit&logoColor=58A6FF)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-0d1f3c?style=flat-square&logo=scikitlearn&logoColor=58A6FF)
![Pandas](https://img.shields.io/badge/Pandas-0d1f3c?style=flat-square&logo=pandas&logoColor=58A6FF)
![Plotly](https://img.shields.io/badge/Plotly-0d1f3c?style=flat-square&logo=plotly&logoColor=58A6FF)

![USGS API](https://img.shields.io/badge/USGS_API-Live-0a1a0a?style=flat-square&logoColor=22c55e)
![OpenStreetMap](https://img.shields.io/badge/OpenStreetMap-0a1a0a?style=flat-square&logo=openstreetmap&logoColor=22c55e)
![License](https://img.shields.io/badge/License-MIT-1a0000?style=flat-square&logoColor=cc3333)

<br/>

<a href="#overview">Overview</a> &nbsp;·&nbsp;
<a href="#architecture">Architecture</a> &nbsp;·&nbsp;
<a href="#modules">Modules</a> &nbsp;·&nbsp;
<a href="#ml-model">ML Model</a> &nbsp;·&nbsp;
<a href="#installation">Installation</a> &nbsp;·&nbsp;
<a href="#usage">Usage</a>

</div>

---

## Overview

**AEGIS AI** eliminates the critical gap between seismic detection and emergency rescue deployment. Instead of relying on slow, manual interpretation of geological data across fragmented tools, AEGIS automatically predicts earthquake impact, identifies safe medical facilities, filters danger zones, and generates dispatch orders — all within **1.5 seconds**.

Current systems create dangerous data silos: seismologists use geological software while emergency services use separate logistics databases. During the golden hour, this fragmentation costs lives. AEGIS solves this with a unified, automated intelligence pipeline.

```text
Detection Speed     →  Raw seismic signal to dispatch order in 1.5 seconds
ML Accuracy         →  Random Forest R² = 0.835, CV Accuracy = 83.5%
Data Source         →  Live USGS GeoJSON API (60-second poll interval)
Geospatial Engine   →  OpenStreetMap Overpass API + 5km Danger Zone Filtering
Alert Threshold     →  Automated flashing alerts for M ≥ 6.0 events
```

---

## Architecture

```
USGS Live API (60s poll)
        │
        ▼
┌─────────────────────┐
│  Data Ingestion     │  ← fetch_latest_earthquakes() + purify_data()
│  & Preprocessing    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  AI Intelligence    │  ← Random Forest Regressor (Scikit-Learn)
│  Layer              │  ← Impact Score = (Mag × Pop Density) / log(Depth+1)
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Geospatial Engine  │  ← OpenStreetMap Overpass API
│                     │  ← 5km Danger Zone Filter + Safe Route Mapping
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Presentation Layer │  ← Streamlit + Folium + Leafmap
│  (Dashboard)        │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Admin Control      │  ← Dispatch Orders + Report Generation + Audit Log
└─────────────────────┘
```

**Impact Score Formula:**
```
Impact Score = (Magnitude × Population Density) / log(Depth + 1)
```

**Engineering decisions worth noting:**
- USGS API feeds normalized in real time before hitting the prediction pipeline — no stale batch processing
- Geospatial routing triggers only on filtered high-magnitude events, preventing alert fatigue in field use
- QoS-style traffic class applied to event severity: minor, moderate, major, critical — each routing to a different dispatch protocol
- Offline model served from `earthquake_model.pkl` via Joblib; no network dependency at prediction time
- Streamlit dashboard designed for minimal-click operation: data ingestion to actionable output in under 3 interactions

---

## Project Structure

```
DISASTER_RESPONSE_SYSTEM/
│
├── Home.py                           # Entry point — Global Seismic Heatmap
│
├── pages/
│   ├── 1_Data_Analysis.py            # Data purification & geospatial visualization
│   ├── 2_AI_Training.py              # Model training, comparison & persistence
│   ├── 3_Live_Monitoring.py          # Real-time global monitoring & flash alerts
│   ├── 4_Resource_Allocation.py      # Risk assessment & dispatch order generation
│   ├── 5_Evacuation_Planning.py      # Safe zone routing via OpenStreetMap
│   └── 6_Admin_Dashboard.py          # Command center & official report generation
│
├── utils/
│   ├── __init__.py
│   └── data_processor.py             # USGS API fetch + data purification logic
│
├── models/
│   └── earthquake_model.pkl          # Saved trained Random Forest model (Joblib)
│
├── data/                             # Local data cache
├── .streamlit/config.toml            # Theme & config settings
├── requirements.txt
└── pages.txt
```

---

## Modules

### `utils/data_processor.py`

| Function | Description |
|:--|:--|
| `fetch_latest_earthquakes()` | Calls USGS GeoJSON API, returns raw DataFrame |
| `purify_data(df)` | Extracts magnitude, depth, lat, lon, location from raw feed |

### Page Breakdown

| Page | Responsibility |
|:--|:--|
| `1_Data_Analysis.py` | Fetches and purifies 10,853+ seismic records · Magnitude vs Depth scatter · Frequency histogram |
| `2_AI_Training.py` | Trains RF, Decision Tree, Linear Regression · 5-Fold CV · Saves best model via Joblib |
| `3_Live_Monitoring.py` | Real-time Folium map · Flashing CSS alerts for M ≥ 6.0 · Timestamped broadcast audit log |
| `4_Resource_Allocation.py` | Geocodes place names · Predicts magnitude · Calculates impact score · Auto-generates dispatch orders |
| `5_Evacuation_Planning.py` | Queries OSM Overpass API · Filters 5km danger zone · Plots safe routing · Resilience gap analysis |
| `6_Admin_Dashboard.py` | System status metrics · Formal report form with `.txt` download · Global alert audit trail |

---

## ML Model

### Model Comparison — 80/20 Split, 100 Trees

<div align="center">

| Model | R² Score | RMSE | CV Accuracy |
|:--|:-:|:-:|:-:|
| **Random Forest** | **0.835** | **0.4962** | **83.5%** |
| Decision Tree | 0.740 | 0.6725 | 74.0% |
| Linear Regression | 0.620 | 0.8355 | 62.0% |

</div>

**Input Features:**
```python
X = ['depth', 'latitude', 'longitude']
y = ['magnitude']
```

**Why Random Forest?**
- Handles non-linear relationships between depth and surface magnitude
- Ensemble of 100 trees significantly reduces overfitting on real-world seismic outliers
- Highest R² and CV accuracy across all three compared models
- Model serialized via Joblib for zero-latency offline prediction at runtime

---

## Installation

**Prerequisites:** Python 3.10+, pip, internet connection (USGS API + OpenStreetMap)

```bash
# Clone the repository
git clone https://github.com/nayar-900/AEGIS-AI.git
cd AEGIS-AI

# Create virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

**Key dependencies:**
```
streamlit · pandas · numpy · scikit-learn · joblib
folium · leafmap · plotly · requests · geopy · geopandas
```

---

## Usage

```bash
streamlit run Home.py
```

Opens at `http://localhost:8501`. Follow this sequence on first launch:

| Step | Page | Action |
|:--|:--|:--|
| 1 | Data Analysis | Fetch and purify live USGS data |
| 2 | AI Training | Train and save the Random Forest model |
| 3 | Live Monitoring | View real-time global seismic activity |
| 4 | Resource Allocation | Test AI risk assessment for any location |
| 5 | Evacuation Planning | Get safe zone routing via OpenStreetMap |
| 6 | Admin Dashboard | Generate official disaster reports |

---

## Tech Stack

<div align="center">

| Category | Technology |
|:--|:--|
| Frontend / UI | Streamlit |
| ML / AI | Scikit-Learn — Random Forest · Decision Tree · Linear Regression |
| Data Processing | Pandas · NumPy |
| Visualization | Plotly · Folium · Leafmap |
| Geospatial | OpenStreetMap Overpass API · GeoPy · GeoPandas |
| Live Data | USGS Earthquake Hazards API (GeoJSON) |
| Model Persistence | Joblib (.pkl) |
| Language | Python 3.10+ |

</div>

---

## Future Work

```text
[ ]  Multi-disaster support — wildfire, flood, and tsunami live data feeds
[ ]  Database integration — PostgreSQL for historical event storage and trend analysis
[ ]  WebSocket alerts — replace 60s polling with true real-time push notifications
[ ]  Mobile application — field-level access for first responders
[ ]  Live census data — replace static population density with real-time figures
[ ]  REST API endpoint — expose AEGIS predictions as an external API for third-party integration
```

---

## Author

**Muhammad Rayan Badar** — BS Computer Science, Namal University Mianwali

<a href="https://www.linkedin.com/in/rayan-badar-b64542367/"><img src="https://img.shields.io/badge/LinkedIn-0a1628?style=flat-square&logo=linkedin&logoColor=58A6FF" /></a>
&nbsp;
<a href="mailto:rayanbadar900@gmail.com"><img src="https://img.shields.io/badge/Email-0a1628?style=flat-square&logo=gmail&logoColor=cc3333" /></a>
&nbsp;
<a href="https://github.com/nayar-900"><img src="https://img.shields.io/badge/GitHub-0a1628?style=flat-square&logo=github&logoColor=ffffff" /></a>

---

<div align="center">

![footer](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)

<sub>AEGIS AI &nbsp;·&nbsp; Namal University 2025 &nbsp;·&nbsp; MIT License</sub>

</div>

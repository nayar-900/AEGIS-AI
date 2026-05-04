# ⚡ AEGIS AI — Automated Earthquake Geospatial Intelligence System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/USGS%20API-Live-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenStreetMap-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>
</p>

<p align="center">
  <b>Bridging Seismic Detection and Logistical Action via Automated Geospatial Intelligence</b><br/>
  <i>An AI-powered disaster response system that goes from earthquake detection to rescue dispatch in 1.5 seconds.</i>
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Module Breakdown](#-module-breakdown)
- [ML Model & Results](#-ml-model--results)
- [Tech Stack](#-tech-stack)
- [Future Work](#-future-work)
- [Author](#-author)

---

## 🌍 Overview

**AEGIS AI** (Automated Earthquake Geospatial Intelligence System) is a real-time disaster response platform that eliminates the critical gap between seismic detection and emergency rescue deployment. Instead of relying on slow, manual interpretation of geological data, AEGIS AI automatically predicts earthquake impact, identifies safe medical facilities, filters danger zones, and generates dispatch orders — all within **1.5 seconds**.

> "From raw seismic signal to actionable rescue plan — fully automated, zero human bottleneck."

---

## 🚨 Problem Statement

After an earthquake strikes, emergency responders face three critical questions:
1. **What is the scale of damage** given the depth and location?
2. **How many SAR and medical units** need to be deployed?
3. **Which nearby medical facilities** are safe and accessible?

Current systems rely on fragmented tools — seismologists use geological software while emergency services use separate logistics databases, creating **data silos** and **dangerous delays** during the golden hour. AEGIS AI solves this with a unified, automated intelligence pipeline.

---

## ✨ Key Features

- 🛰 **Live USGS Integration** — Fetches real-time global seismic events every 60 seconds
- 🤖 **AI Impact Prediction** — Random Forest model (R² = 0.85) predicts magnitude and severity
- 🗺 **Geospatial Routing** — OpenStreetMap queries hospitals, excludes 5 km danger zones, plots safe routes
- 📊 **Model Comparison** — Benchmarks Random Forest vs. Decision Tree vs. Linear Regression
- 🚨 **Intelligent Alerts** — Flashing alerts for M ≥ 6.0 events with automated broadcast logs
- 📋 **Dispatch Orders** — Auto-generates SAR and medical unit deployment plans by severity class
- 🖥 **Admin Command Center** — Official disaster report generation with downloadable TXT report
- 🌐 **Satellite Imagery** — Live satellite, hybrid, terrain views via Leafmap & Folium

---

## 🏗 System Architecture

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
│                     │  ← 5 km Danger Zone Filter + Safe Route Mapping
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

---

## 📁 Project Structure

```
DISASTER_RESPONSE_SYSTEM/
│
├── 📄 Home.py                        # Main entry point — Global Seismic Heatmap
│
├── 📁 pages/
│   ├── 1_Data_Analysis.py            # Geospatial data purification & visualization
│   ├── 2_AI_Training.py              # ML model training, comparison & saving
│   ├── 3_Live_Monitoring.py          # Real-time global monitoring & flash alerts
│   ├── 4_Resource_Allocation.py      # AI risk assessment & dispatch orders
│   ├── 5_Evacuation_Planning.py      # Safe zone routing via OpenStreetMap
│   └── 6_Admin_Dashboard.py          # Command center & official report generation
│
├── 📁 utils/
│   ├── __init__.py
│   └── data_processor.py             # USGS API fetch + data purification logic
│
├── 📁 models/
│   └── earthquake_model.pkl          # Saved trained Random Forest model
│
├── 📁 data/                          # Local data cache
│
├── 📁 .streamlit/
│   └── config.toml                   # Streamlit theme/config settings
│
├── 📄 requirements.txt               # All Python dependencies
└── 📄 pages.txt                      # Page navigation config
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Internet connection (for USGS API & OpenStreetMap)

### Step 1 — Clone the Repository
```bash
git clone https://github.com/yourusername/AEGIS-AI.git
cd AEGIS-AI
```

### Step 2 — Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Key Dependencies
```
streamlit
pandas
numpy
scikit-learn
joblib
folium
leafmap
plotly
requests
geopy
geopandas
```

---

## 🚀 How to Run

```bash
streamlit run Home.py
```

The app will open at `http://localhost:8501` in your browser.

### ⚠️ First-Time Setup Order
> Follow this sequence on first launch:

| Step | Page | Action |
|---|---|---|
| 1 | Data Analysis | Fetch and purify live USGS data |
| 2 | AI Training | Train and save the Random Forest model |
| 3 | Live Monitoring | View real-time global seismic activity |
| 4 | Resource Allocation | Test AI risk assessment for any location |
| 5 | Evacuation Planning | Get safe zone routing via OpenStreetMap |
| 6 | Admin Dashboard | Generate official disaster reports |

---

## 📦 Module Breakdown

### `utils/data_processor.py`
| Function | Description |
|---|---|
| `fetch_latest_earthquakes()` | Calls USGS GeoJSON API, returns raw DataFrame |
| `purify_data(df)` | Extracts magnitude, depth, lat, lon, location from raw feed |

### `pages/1_Data_Analysis.py`
- Fetches and purifies 10,853+ seismic records from USGS
- Displays Magnitude vs. Depth scatter plot (Plotly dark theme)
- Shows magnitude frequency distribution histogram

### `pages/2_AI_Training.py`
- Trains **Random Forest**, **Decision Tree**, and **Linear Regression**
- 5-Fold Cross Validation on training set
- Saves best model as `models/earthquake_model.pkl` via Joblib
- Displays Actual vs. Predicted line chart for the winning model

### `pages/3_Live_Monitoring.py`
- Real-time USGS feed with color-coded Folium map markers
- Flashing CSS red alerts for M ≥ 6.0 earthquakes
- Automated broadcast system with timestamped audit log
- Filterable by minimum magnitude via sidebar slider

### `pages/4_Resource_Allocation.py`
- Geocodes any place name using Nominatim (GeoPy)
- Predicts magnitude using the saved Random Forest model
- Calculates Impact Score with urban/suburban/rural population multiplier
- Auto-generates dispatch orders: medical units count + SAR level
- Satellite view via Leafmap with impact radius circle

### `pages/5_Evacuation_Planning.py`
- Queries OpenStreetMap Overpass API for hospitals, clinics, community centers
- Automatically filters out all facilities within the 5 km danger zone
- Plots dashed yellow routing lines to safe facilities on satellite map
- Infrastructure resilience gap analysis (capacity vs. required units)

### `pages/6_Admin_Dashboard.py`
- System status metrics: AI Model, Satellite Sync, Uptime (99.8%)
- Formal disaster report form with downloadable `.txt` report
- Global alert audit trail pulled from session broadcast log

---

## 📊 ML Model & Results

### Model Comparison (80/20 Train-Test Split, 100 Trees)

| Model | R² Score | RMSE | CV Accuracy |
|---|---|---|---|
| ✅ **Random Forest** | **0.835** | **0.4962** | **83.5%** |
| Decision Tree | ~0.74 | 0.6725 | 74% |
| Linear Regression | 0.62 | 0.8355 | 62% |

### Input Features
```python
X = ['depth', 'latitude', 'longitude']
y = ['magnitude']
```

### Why Random Forest?
- Handles non-linear relationships between depth and surface magnitude
- Robust to outliers common in real-world seismic data
- Ensemble of 100 trees significantly reduces overfitting
- Highest R² and CV accuracy across all three compared models

---

## 🛠 Tech Stack

| Category | Technology |
|---|---|
| **Frontend / UI** | Streamlit |
| **ML / AI** | Scikit-Learn (Random Forest, Decision Tree, Linear Regression) |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly, Folium, Leafmap |
| **Geospatial** | OpenStreetMap Overpass API, GeoPy, GeoPandas |
| **Live Data** | USGS Earthquake Hazards API (GeoJSON) |
| **Model Persistence** | Joblib (.pkl) |
| **Language** | Python 3.10+ |

---

## 🔮 Future Work

- [ ] **Multi-disaster support** — Integrate wildfire, flood, and tsunami live data feeds
- [ ] **Database integration** — SQLite/PostgreSQL for historical event storage and trend analysis
- [ ] **WebSocket alerts** — Replace polling with true real-time push notifications
- [ ] **Mobile application** — Field-level access for first responders on the ground
- [ ] **Live census data** — Replace static population density with real-time figures
- [ ] **REST API endpoint** — Expose AEGIS predictions as an external API for third-party integration

---

## 👤 Author

**Muhammad Rayan Badar**
- 🎓 Bachelor of Computer Science — Namal University Mianwali, Pakistan
- 📧 bscs23f18@namal.edu.pk
- 📞 +923480989572

---

## 📄 License

This project is licensed under the MIT License — feel free to use, modify, and distribute with attribution.

---

<p align="center">
  Built with ❤️ for smarter disaster response<br/>
  <b>AEGIS AI — Namal University, 2024</b>
</p>

import requests
import pandas as pd
import geopandas as gpd

def fetch_latest_earthquakes():
    """Fetches real-time earthquake data from USGS (Last 7 Days)."""
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.json_normalize(data['features'])
        return df
    except Exception as e:
        print(f"Error: {e}")
        return None

def purify_data(df):
    """Purifies columns for Magnitude-Depth correlation."""
    # Selecting and renaming core features
    cols_to_keep = {
        'properties.mag': 'magnitude',
        'properties.place': 'location',
        'properties.time': 'timestamp',
        'geometry.coordinates': 'coords'
    }
    # Safety check: only keep columns that actually exist
    existing_cols = [c for c in cols_to_keep.keys() if c in df.columns]
    df = df[existing_cols].rename(columns={c: cols_to_keep[c] for c in existing_cols})
    
    # Extract Depth, Lat, Lon from coordinates list [long, lat, depth]
    df['depth'] = df['coords'].apply(lambda x: x[2] if isinstance(x, list) and len(x) > 2 else 0)
    df['latitude'] = df['coords'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else 0)
    df['longitude'] = df['coords'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else 0)
    
    return df.dropna(subset=['magnitude', 'depth'])
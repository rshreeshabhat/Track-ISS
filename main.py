import requests
import streamlit as st
import pandas as pd
import pydeck as pdk

# Set the title of the app
st.title("ISRO Satellite Tracker")

# Satellite data with IDs and names
satellites = {
    "Cartosat-2A": 32783,
    "Cartosat-2B": 36839,
    "Cartosat-2C": 41599,
    "Cartosat-2D": 42063,
    "Cartosat-2E": 42747,
    "Cartosat-2F": 43111,
    "INSAT-3A": 27714,
    "INSAT-3C": 27298,
    "INSAT-4A": 28911,
    "INSAT-4B": 30793,
    "INSAT-4CR": 32050,
    "GSAT-6A": 43241,
    "GSAT-7": 39234,
    "GSAT-10": 38778,
    "GSAT-12": 37746,
    "GSAT-16": 40332,
    "GSAT-18": 41793,
    "RISAT-1": 38337,
    "RISAT-2": 34807,
    "IRNSS-1A": 39199,
    "IRNSS-1B": 39635,
    "IRNSS-1C": 40269,
    "IRNSS-1D": 40547,
    "IRNSS-1E": 41384,
    "IRNSS-1F": 41469,
    "IRNSS-1G": 41589,
    "Chandrayaan-2 Orbiter": 44426
}

# Assign unique colors for each satellite
satellite_colors = {
    "Cartosat-2A": [255, 0, 0],  # Red
    "Cartosat-2B": [0, 255, 0],  # Green
    "Cartosat-2C": [0, 0, 255],  # Blue
    "Cartosat-2D": [255, 255, 0],  # Yellow
    "Cartosat-2E": [255, 0, 255],  # Magenta
    "Cartosat-2F": [0, 255, 255],  # Cyan
    "INSAT-3A": [255, 165, 0],  # Orange
    "INSAT-3C": [128, 0, 128],  # Purple
    "INSAT-4A": [0, 128, 128],  # Teal
    "INSAT-4B": [128, 128, 0],  # Olive
    "INSAT-4CR": [0, 0, 128],  # Navy
    "GSAT-6A": [192, 192, 192],  # Silver
    "GSAT-7": [128, 128, 128],  # Gray
    "GSAT-10": [0, 255, 127],  # Spring Green
    "GSAT-12": [255, 20, 147],  # Deep Pink
    "GSAT-16": [123, 104, 238],  # Medium Slate Blue
    "GSAT-18": [65, 105, 225],  # Royal Blue
    "RISAT-1": [106, 90, 205],  # Slate Blue
    "RISAT-2": [220, 20, 60],  # Crimson
    "IRNSS-1A": [255, 99, 71],  # Tomato
    "IRNSS-1B": [32, 178, 170],  # Light Sea Green
    "IRNSS-1C": [107, 142, 35],  # Olive Drab
    "IRNSS-1D": [255, 215, 0],  # Gold
    "IRNSS-1E": [154, 205, 50],  # Yellow Green
    "IRNSS-1F": [255, 140, 0],  # Dark Orange
    "IRNSS-1G": [233, 150, 122],  # Dark Salmon
    "Chandrayaan-2 Orbiter": [72, 61, 139]  # Dark Slate Blue
}

# Function to fetch data for selected satellites
def fetch_satellite_data(satellite_ids):
    satellite_data = []
    
    for sat_name, sat_id in satellite_ids.items():
        url = f"https://api.n2yo.com/rest/v1/satellite/positions/{sat_id}/41.702/-76.014/0/2/&apiKey=56C4JJ-JGEVZ3-KZSEXW-5BKR"
        response = requests.get(url).json()
        
        if 'positions' in response:
            position = response['positions'][0]
            satellite_data.append({
                'name': sat_name,
                'latitude': position.get('satlatitude', 'N/A'),
                'longitude': position.get('satlongitude', 'N/A'),
                'color': satellite_colors[sat_name]
            })
        else:
           

import requests
import streamlit as st
import pandas as pd
import pydeck as pdk

# Set the title of the app
st.title("ISRO Satellite Tracker")

# Satellite data with IDs and names categorized
satellite_categories = {
    "Cartosat Series": {
        "Cartosat-2A": 32783,
        "Cartosat-2B": 36839,
        "Cartosat-2C": 41599,
        "Cartosat-2D": 42063,
        "Cartosat-2E": 42747,
        "Cartosat-2F": 43111,
    },
    "INSAT Series": {
        "INSAT-3A": 27714,
        "INSAT-3C": 27298,
        "INSAT-4A": 28911,
        "INSAT-4B": 30793,
        "INSAT-4CR": 32050,
    },
    "GSAT Series": {
        "GSAT-6A": 43241,
        "GSAT-7": 39234,
        "GSAT-10": 38778,
        "GSAT-12": 37746,
        "GSAT-16": 40332,
        "GSAT-18": 41793,
    },
    "RISAT Series": {
        "RISAT-1": 38337,
        "RISAT-2": 34807,
    },
    "IRNSS Series": {
        "IRNSS-1A": 39199,
        "IRNSS-1B": 39635,
        "IRNSS-1C": 40269,
        "IRNSS-1D": 40547,
        "IRNSS-1E": 41384,
        "IRNSS-1F": 41469,
        "IRNSS-1G": 41589,
    },
    "Other": {
        "Chandrayaan-2 Orbiter": 44426
    }
}

# Assign unique colors for each satellite
satellite_colors = {
    "Cartosat-2A": "#FF0000",  # Red
    "Cartosat-2B": "#00FF00",  # Green
    "Cartosat-2C": "#0000FF",  # Blue
    "Cartosat-2D": "#FFFF00",  # Yellow
    "Cartosat-2E": "#FF00FF",  # Magenta
    "Cartosat-2F": "#00FFFF",  # Cyan
    "INSAT-3A": "#FFA500",  # Orange
    "INSAT-3C": "#800080",  # Purple
    "INSAT-4A": "#008080",  # Teal
    "INSAT-4B": "#808000",  # Olive
    "INSAT-4CR": "#000080",  # Navy
    "GSAT-6A": "#C0C0C0",  # Silver
    "GSAT-7": "#808080",  # Gray
    "GSAT-10": "#00FF7F",  # Spring Green
    "GSAT-12": "#FF1493",  # Deep Pink
    "GSAT-16": "#7B68EE",  # Medium Slate Blue
    "GSAT-18": "#4169E1",  # Royal Blue
    "RISAT-1": "#6A5ACD",  # Slate Blue
    "RISAT-2": "#DC143C",  # Crimson
    "IRNSS-1A": "#FF6347",  # Tomato
    "IRNSS-1B": "#20B2AA",  # Light Sea Green
    "IRNSS-1C": "#6B8E23",  # Olive Drab
    "IRNSS-1D": "#FFD700",  # Gold
    "IRNSS-1E": "#9ACD32",  # Yellow Green
    "IRNSS-1F": "#FF8C00",  # Dark Orange
    "IRNSS-1G": "#E9967A",  # Dark Salmon
    "Chandrayaan-2 Orbiter": "#483D8B"  # Dark Slate Blue
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
            st.error(f"Error: 'positions' not found for satellite {sat_name}.")
    
    return satellite_data

# Grouped checkboxes for satellite selection with color labels
st.subheader("Select Satellites to Display on the Map:")
selected_satellites = {}

for category, sats in satellite_categories.items():
    with st.expander(f"{category}"):
        cols = st.columns(4)  # Creating 4 columns for the grid
        for idx, (sat_name, sat_id) in enumerate(sats.items()):
            col = cols[idx % 4]  # Determine which column to place the checkbox in
            color_hex = satellite_colors[sat_name]  # Get the hex color for the satellite
            color_label = f'<span style="color:{color_hex};">&#11044;</span> '  # Create a colored dot label
            if col.checkbox(f"{color_label}{sat_name}", value=True):
                selected_satellites[sat_name] = sat_id

# Fetch data for the selected satellites
satellite_data = fetch_satellite_data(selected_satellites)

# Display Satellite Location and Map
if satellite_data:
    st.header("Current Location of ISRO Satellites")
    
    # Prepare data for map and display details
    map_data = []
    for sat in satellite_data:
       
        map_data.append({
            'lat': sat['latitude'],
            'lon': sat['longitude'],
            'name': sat['name'],
            'color': sat['color']
        })
    
    # Convert map data to DataFrame
    df = pd.DataFrame(map_data)

    # Define the pydeck layer
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[lon, lat]',
        get_fill_color='color',  # Use 'get_fill_color' to assign color
        get_radius=50000,  # Same size for all
        pickable=True
    )

    # Define the view state of the map
    view_state = pdk.ViewState(
        latitude=df['lat'].mean(),
        longitude=df['lon'].mean(),
        zoom=3,
        pitch=0
    )

    # Render the pydeck map
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}"}
    )

    st.pydeck_chart(r)
else:
    st.write("No satellite selected or failed to fetch satellite data.")

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

# Sidebar checkboxes for satellite selection
selected_satellites = [sat_name for sat_name in satellites if st.sidebar.checkbox(sat_name, value=True)]

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
            })
        else:
            st.error(f"Error: 'positions' not found for satellite {sat_name}.")
    
    return satellite_data

# Fetch data for the selected satellites
satellite_data = fetch_satellite_data({name: satellites[name] for name in selected_satellites})

# Display Satellite Location and Map
if satellite_data:
    st.header("Current Location of Selected ISRO Satellites")
    
    # Prepare data for map and display details
    map_data = []
    for sat in satellite_data:
        st.subheader(f"Satellite: {sat['name']}")
        st.write(f"**Latitude:** {sat['latitude']}")
        st.write(f"**Longitude:** {sat['longitude']}")
        
        map_data.append({
            'lat': sat['latitude'],
            'lon': sat['longitude'],
            'name': sat['name']
        })
    
    # Convert map data to DataFrame
    df = pd.DataFrame(map_data)

    # Define the pydeck layer
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[lon, lat]',
        get_color='[255,0,255]',  # Cyan color
        get_radius=50000,
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

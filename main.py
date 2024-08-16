import requests
import streamlit as st
import pandas as pd
import pydeck as pdk

# Set the title of the app
st.title("International Space Station Tracker")

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.write("Home")

# ISS Data Fetching
def fetch_iss_data():
    url = "https://api.n2yo.com/rest/v1/satellite/positions/25544/41.702/-76.014/0/2/&apiKey=56C4JJ-JGEVZ3-KZSEXW-5BKR"
    response = requests.get(url).json()
    
    if 'positions' in response:
        position = response['positions'][0]
        return {
            'latitude': position.get('satlatitude', 'N/A'),
            'longitude': position.get('satlongitude', 'N/A'),
        }
    else:
        st.error("Error: 'positions' not found in API response.")
        return None

# Display ISS Location and Map
st.header("Current Location of the ISS")

iss_data = fetch_iss_data()
if iss_data:
    latitude = iss_data['latitude']
    longitude = iss_data['longitude']
    
    # Display ISS details
    st.subheader("Details")
    st.write(f"**Latitude:** {latitude}")
    st.write(f"**Longitude:** {longitude}")

    # Create DataFrame for map
    df = pd.DataFrame({
        'lat': [latitude],
        'lon': [longitude],
        'name': ['International Space Station']
    })

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
        latitude=latitude,
        longitude=longitude,
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
    st.write("Failed to fetch ISS data.")


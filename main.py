import requests
import streamlit as st
import pandas as pd
import pydeck as pdk

# Set the title of the app
st.title("International Space Station Tracker")

# Sidebar navigation
st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ["Home", "ISS Location"])

# ISS Data Fetching
def fetch_iss_data():
    url = "https://api.n2yo.com/rest/v1/satellite/positions/25544/41.702/-76.014/0/2/&apiKey=56C4JJ-JGEVZ3-KZSEXW-5BKR"
    response = requests.get(url).json()
    position = response['positions'][0]
    return {
        'latitude': position['satlatitude'],
        'longitude': position['satlongitude'],
        'altitude': position['sataltitude'],
        'velocity': position['satvelocity'],
    }

# Display ISS Location page
if option == "ISS Location":
    st.header("Current Location of the ISS")

    iss_data = fetch_iss_data()
    latitude = iss_data['latitude']
    longitude = iss_data['longitude']
    
    # Display ISS details
    st.subheader("Details")
    st.write(f"**Latitude:** {latitude}")
    st.write(f"**Longitude:** {longitude}")
    st.write(f"**Altitude:** {iss_data['altitude']} km")
    st.write(f"**Velocity:** {iss_data['velocity']} km/h")

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

# Home page
else:
    st.header("Welcome to the ISS Tracker")
    st.write("""
        This application tracks the current location of the International Space Station (ISS).
        Use the navigation on the left to explore the app.
    """)

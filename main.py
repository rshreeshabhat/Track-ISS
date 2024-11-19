import requests
import streamlit as st
import pandas as pd
import pydeck as pdk

# Set the title of the app
st.title("ISS Real-Time Tracker")

# ISS NORAD ID
ISS_ID = 25544

# Function to fetch ISS data
@st.cache_data(ttl=30)  # Cache data for 30 seconds
def fetch_iss_data():
    # Replace 'YOUR_API_KEY' with your N2YO API key
    url = f"https://api.n2yo.com/rest/v1/satellite/positions/{ISS_ID}/0/0/0/1/&apiKey=56C4JJ-JGEVZ3-KZSEXW-5BKR"
    response = requests.get(url).json()

    if "positions" in response:
        position = response["positions"][0]
        return {
            "latitude": position.get("satlatitude", 0),
            "longitude": position.get("satlongitude", 0),
        }
    else:
        st.error("Failed to fetch ISS data. Please check your API key or try again later.")
        return None

# Fetch ISS position
iss_position = fetch_iss_data()

# Display ISS location and map
if iss_position:
    st.header("Current Location of the ISS")
    st.write(f"**Latitude:** {iss_position['latitude']}")
    st.write(f"**Longitude:** {iss_position['longitude']}")

    # Prepare data for the map
    map_data = pd.DataFrame([{
        "lat": iss_position["latitude"],
        "lon": iss_position["longitude"]
    }])

    # Define the pydeck layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position="[lon, lat]",
        get_fill_color="[255, 0, 0]",  # Red color for ISS
        get_radius=50000,  # Radius of the marker
        pickable=True,
    )

    # Define the view state of the map
    view_state = pdk.ViewState(
        latitude=iss_position["latitude"],
        longitude=iss_position["longitude"],
        zoom=3,
        pitch=0,
    )

    # Render the pydeck map
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "ISS Current Position"}
    )

    st.pydeck_chart(r)
else:
    st.write("Unable to display ISS location. Please try again later.")

import requests
import streamlit as st
import pandas as pd
import pydeck as pdk

# Your API URL
url = "https://api.n2yo.com/rest/v1/satellite/positions/25544/41.702/-76.014/0/2/&apiKey=56C4JJ-JGEVZ3-KZSEXW-5BKR"
responses = requests.get(url)
response = responses.json()
res = response.get('positions')

# Extract latitude and longitude
latitude = res[0].get('satlatitude')
longitude = res[0].get('satlongitude')

# Create a DataFrame with the ISS position
df = pd.DataFrame({
    'lat': [latitude],
    'lon': [longitude],
    'name': ['International Space Station']  # Add a column for the tooltip
})

# Define a layer for pydeck
layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[lon, lat]',
    get_color='[0, 255, 255]',  # Cyan color
    get_radius=50000,
    pickable=True,
    tooltip=True
)

# Define the view of the map
view_state = pdk.ViewState(
    latitude=latitude,
    longitude=longitude,
    zoom=3,
    pitch=0
)

# Render the map
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{name}"}
)

st.pydeck_chart(r)

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
    'name': ['International Space Station'],
    'icon_data': [{
        'url': 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',  # Use the local file path for the image
        'width': 3000,  # Original width
        'height': 1569,  # Original height
        'anchorY': 1569 # Adjust anchor based on the image
    }]
})

# Define an IconLayer
icon_layer = pdk.Layer(
    'IconLayer',
    data=df,
    get_icon='icon_data',
    get_size=4,  # Adjust as needed
    size_scale=1,  # Scale down significantly due to large original size
    get_position='[lon, lat]',
    pickable=True,
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
    layers=[icon_layer],
    initial_view_state=view_state,
    tooltip={"text": "{name}"}
)

st.pydeck_chart(r)

import requests
import streamlit as st
import pandas as pd
import numpy as np

url = "https://api.n2yo.com/rest/v1/satellite/positions/25544/41.702/-76.014/0/2/&apiKey=56C4JJ-JGEVZ3-KZSEXW-5BKR"
responses = requests.get(url)
response = responses.json()
res = response.get('positions')

data = [{'lat': res[0].get('satlatitude'), 'lon': res[0].get('satlongitude')}]  

df = pd.DataFrame(data) 
st.map(df)

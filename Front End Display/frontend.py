import pandas as pd
import streamlit as st
import pydeck as pdk
import numpy as np
from streamlit_folium import folium_static
import folium

st.title("RetroPark")
st.header("EE/CPE 2021 Senior Design Team 5")
col1, col2 = st.columns(2)

col1.metric(label="Training Accuracy", value="98.1%", delta="-0.1%")
col2.metric(label="Validation Accuracy", value="96.2%", delta="0.2%")

col1.metric(label="Training Loss", value="0.21%", delta="1.3%")
col2.metric(label="Validation Loss", value="0.14%", delta="-0.8%")

# read in data`
# df = pd.read_csv('spotdata.csv', sep=',')
df = pd.DataFrame(
    np.random.randn(1000, 2) / [2, 2] + [29.582064, -98.619715],
    columns=['lat', 'lon'])

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/satellite-v9',
    initial_view_state=pdk.ViewState(
        latitude=29.582064,
        longitude=-98.619715,
        zoom=19.3,
        pitch=45,
        bearing=59
    ),
    layers=[
        pdk.Layer(
            'GridCellLayer',
            data=df,
            get_position='[lon, lat]',
            pickable=False,
            extruded=True,
            cellSize=2,
            get_elevation='Value'
        ),
    ],
))
# test

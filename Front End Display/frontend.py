import streamlit as st
from streamlit_folium import folium_static
import folium

st.title("RetroPark")
st.header("EE/CPE 2021 Senior Design Team 5")
col1, col2 = st.columns(2)

col1.metric(label="Training Accuracy", value="98.1%", delta="-0.1%")
col2.metric(label="Validation Accuracy", value="96.2%", delta="0.2%")

col1.metric(label="Training Loss", value="0.21%", delta="1.3%")
col2.metric(label="Validation Loss", value="0.14%", delta="-0.8%")

m = folium.Map(location=[29.581953, -98.619457], zoom_start=20)
tile = folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = False,
        control = True
       ).add_to(m)


# call to render Folium map in Streamlit
folium_static(m)

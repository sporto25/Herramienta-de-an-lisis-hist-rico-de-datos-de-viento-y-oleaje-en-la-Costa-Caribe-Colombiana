# app.py
import streamlit as st
from Waves.wind_utils import *
from Waves.visualizacion import *

st.title("🌬️ Viento histórico – Caribe colombiano")

ds = load_dataset("data/ERA5_viento_caribe.nc")
ds = subset_caribe_dimar(ds)
ds = compute_wind_speed(ds)
ds = compute_wind_direction(ds)

year = st.slider("Año", 1990, 2020, 2010)
plot_mean_wind(ds, year)

lat = st.slider("Latitud", 8.5, 13.0, 11.0)
lon = st.slider("Longitud", -81.5, -71.5, -75.0)
plot_time_series(ds, lat, lon)

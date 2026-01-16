import streamlit as st
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------
# CONFIG STREAMLIT
# ----------------------------------
st.set_page_config(
    page_title="Climatología de Olas - Caribe Colombiano",
    layout="wide"
)

st.title("🌊 Análisis de Olas - Caribe Colombiano (ERA5)")
st.markdown("Promedios históricos, series temporales y análisis mensual")

# ----------------------------------
# CARGA DE DATOS
# ----------------------------------
@st.cache_data
def cargar_datos():
    archivos = [
        r"data/TIME0.nc",
        r"data/TIME6.nc",
        r"data/TIME12.nc",
        r"data/TIME18.nc"
    ]

    datasets = [
        xr.open_dataset(f, engine="netcdf4", cache=False)
        for f in archivos
    ]

    ds = xr.concat(datasets, dim="time")
    ds_flat = ds.mean(dim="time", skipna=True)

    return ds_flat

ds = cargar_datos()

# ----------------------------------
# SIDEBAR - CONTROLES
# ----------------------------------
st.sidebar.header("⚙️ Configuración")

lat_sel = st.sidebar.selectbox(
    "Latitud",
    ds.latitude.values
)

lon_sel = st.sidebar.selectbox(
    "Longitud",
    ds.longitude.values
)

variable = st.sidebar.selectbox(
    "Variable",
    ["swh", "mwd", "mwp"]
)

# ----------------------------------
# MAPA PROMEDIO HISTÓRICO
# ----------------------------------
st.header("🗺️ Promedio histórico espacial")

campo_mean = ds[variable].mean(dim="valid_time")

fig, ax = plt.subplots()
pcm = ax.pcolormesh(
    ds.longitude,
    ds.latitude,
    campo_mean,
    shading="auto"
)
plt.colorbar(pcm, ax=ax, label=variable.upper())
ax.set_xlabel("Longitud")
ax.set_ylabel("Latitud")
ax.set_title(f"Promedio histórico de {variable.upper()}")

st.pyplot(fig)

# ----------------------------------
# SERIE TEMPORAL EN UN PUNTO
# ----------------------------------
st.header("📈 Serie temporal en un punto")

pt = ds[variable].sel(
    latitude=lat_sel,
    longitude=lon_sel,
    method="nearest"
)

fig, ax = plt.subplots()
pt.plot(ax=ax)
ax.set_title(
    f"{variable.upper()} en ({lat_sel:.2f}, {lon_sel:.2f})"
)
ax.set_ylabel(variable.upper())

st.pyplot(fig)

# ----------------------------------
# CICLO MENSUAL
# ----------------------------------
st.header("📊 Climatología mensual")

pt_month = pt.groupby("valid_time.month").mean()

fig, ax = plt.subplots()
ax.plot(
    pt_month.month,
    pt_month,
    marker="o"
)
ax.set_xlabel("Mes")
ax.set_ylabel(variable.upper())
ax.set_title("Ciclo mensual promedio")

st.pyplot(fig)

# ----------------------------------
# FOOTER
# ----------------------------------
st.markdown("---")
st.markdown(
    "📌 **Fuente:** ERA5 / ECMWF  \n"
    "🛠️ Herramienta desarrollada para análisis costero y offshore"
)



import streamlit as st
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Rosa de Olas – Caribe Colombiano",
    layout="centered"
)

st.title("🌊 Rosa de Olas – Caribe Colombiano (ERA5)")
st.markdown("Herramienta offline para análisis histórico en zona DIMAR")

# =========================
# CARGA DE DATOS
# =========================
@st.cache_data
def cargar_datos():
    rutas = [
        r"C:\Users\Santiago Elias Porto\Downloads\data\TIME0.nc",
        r"C:\Users\Santiago Elias Porto\Downloads\data\TIME6.nc",
        r"C:\Users\Santiago Elias Porto\Downloads\data\TIME12.nc",
        r"C:\Users\Santiago Elias Porto\Downloads\data\TIME18.nc",
    ]

    datasets = []
    for ruta in rutas:
        ds = xr.open_dataset(
            ruta,
            engine="netcdf4"
        )
        return ds
        datasets.append(ds)

    ds_final = xr.concat(datasets, dim="valid_time")

    return ds_final


ds = cargar_datos()

# =========================
# CONTROLES
# =========================
st.sidebar.header("📍 Selección de punto")

lat = st.sidebar.selectbox("Latitud", ds.latitude.values)
lon = st.sidebar.selectbox("Longitud", ds.longitude.values)

# =========================
# SELECCIÓN DEL PUNTO
# =========================
pt = ds.sel(latitude=lat, longitude=lon)

Hs = pt["swh"].values
Dir = pt["mwd"].values

mask = np.isfinite(Hs) & np.isfinite(Dir)
Hs = Hs[mask]
Dir = Dir[mask]

# =========================
# ROSA DE OLAS
# =========================
dir_bins = np.arange(0, 361, 30)
hs_bins = [0, 1, 2, 3, 4, 5, 10]

hist, _, _ = np.histogram2d(
    Dir,
    Hs,
    bins=[dir_bins, hs_bins]
)

hist = hist / hist.sum() * 100

theta = np.deg2rad((dir_bins[:-1] + dir_bins[1:]) / 2)

fig = plt.figure(figsize=(7, 7))
ax = plt.subplot(111, polar=True)

bottom = np.zeros(len(theta))

for i in range(len(hs_bins) - 1):
    values = hist[:, i]
    ax.bar(
        theta,
        values,
        width=np.deg2rad(30),
        bottom=bottom,
        label=f"{hs_bins[i]}–{hs_bins[i+1]} m"
    )
    bottom += values

ax.set_theta_zero_location("N")
ax.set_theta_direction(-1)
ax.set_title(
    f"Rosa de olas\nLat: {lat} | Lon: {lon}",
    pad=20
)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

st.pyplot(fig)

# =========================
# MÉTRICAS
# =========================
st.subheader("📊 Estadísticos básicos")

col1, col2, col3 = st.columns(3)
col1.metric("Hs media [m]", f"{np.mean(Hs):.2f}")
col2.metric("Hs máx [m]", f"{np.max(Hs):.2f}")
col3.metric("Registros", len(Hs))

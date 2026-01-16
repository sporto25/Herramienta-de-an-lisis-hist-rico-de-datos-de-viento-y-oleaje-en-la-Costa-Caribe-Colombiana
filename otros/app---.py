import streamlit as st
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# =========================
# CONFIGURACIÓN DE LA APP
# =========================
st.set_page_config(
    page_title="Rosa de Olas – Caribe Colombiano",
    layout="wide"
)

# =========================
# REGISTRO DE USUARIO
# =========================
st.sidebar.header("👤 Registro de usuario")
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Iniciar sesión"):
        # Aquí podrías validar contra una base de datos real
        if username and password:
            st.session_state.logged_in = True
            st.session_state.username = username
        else:
            st.sidebar.error("Ingresa usuario y contraseña")
else:
    st.sidebar.success(f"Bienvenido, {st.session_state.username}")

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
        ds = xr.open_dataset(ruta, engine="netcdf4")
        datasets.append(ds)

    ds_final = xr.concat(datasets, dim="valid_time")
    return ds_final

if st.session_state.logged_in:
    ds = cargar_datos()

    # =========================
    # PUNTOS DISPONIBLES
    # =========================
    st.sidebar.header("📍 Selección de punto")
    df_coords = pd.DataFrame({
        "lat": ds.latitude.values,
        "lon": ds.longitude.values
    })

    # =========================
    # MAPA INTERACTIVO
    # =========================
    st.subheader("🗺️ Mapa de puntos disponibles")
    m = folium.Map(location=[10.0, -75.5], zoom_start=6)  # Ajustar al Caribe colombiano

    for idx, row in df_coords.iterrows():
        folium.Marker(
            location=[row.lat, row.lon],
            popup=f"Lat: {row.lat}, Lon: {row.lon}",
            tooltip="Click para seleccionar"
        ).add_to(m)

    map_data = st_folium(m, width=700, height=500)

    # =========================
    # SELECCIÓN DE PUNTO DEL MAPA
    # =========================
    selected_point = None
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        selected_point = ds.sel(latitude=lat, longitude=lon, method="nearest")
        st.success(f"Punto seleccionado: Lat {lat:.2f}, Lon {lon:.2f}")

    # =========================
    # SELECCIÓN DE PARÁMETRO
    # =========================
    st.sidebar.header("🌡️ Selección de parámetro")
    parametro = st.sidebar.selectbox(
        "Elige un parámetro",
        options=["swh", "mwd", "u100", "v100"]  # Oleaje, dirección, viento u/v 100m
    )

    if selected_point:
        data = selected_point[parametro].values
        # Filtrar datos válidos
        mask = np.isfinite(data)
        data = data[mask]

        if parametro in ["swh", "mwd"]:
            # =========================
            # ROSA DE OLAS
            # =========================
            Hs = selected_point["swh"].values
            Dir = selected_point["mwd"].values

            mask = np.isfinite(Hs) & np.isfinite(Dir)
            Hs = Hs[mask]
            Dir = Dir[mask]

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
                f"Rosa de olas\nLat: {lat:.2f} | Lon: {lon:.2f}",
                pad=20
            )
            ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

            st.pyplot(fig)

        else:
            # =========================
            # GRÁFICO DE VIENTO U/V 100m
            # =========================
            st.subheader(f"📈 Serie temporal de {parametro}")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(data)
            ax.set_xlabel("Tiempo")
            ax.set_ylabel(parametro)
            st.pyplot(fig)

        # =========================
        # MÉTRICAS
        # =========================
        st.subheader("📊 Estadísticos básicos")
        col1, col2, col3 = st.columns(3)
        col1.metric(f"{parametro} media", f"{np.mean(data):.2f}")
        col2.metric(f"{parametro} máximo", f"{np.max(data):.2f}")
        col3.metric("Registros", len(data))

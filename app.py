import streamlit as st
import importlib
import streamlit as st
import xarray as xr
from pathlib import Path
from core.zones import ZONES

# =========================
# CONFIG STREAMLIT
# =========================
st.set_page_config(
    page_title="Herramienta online Costa Caribe Colombiano",
    layout="wide"
)

# =========================
# SESSION STATE INIT (CRÍTICO)
# =========================
for key, value in {
    "logged_in": False,
    "user": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================
# LOGIN
# =========================
from core.auth.db import init_db
from core.auth.ui import login_ui

init_db()

if not st.session_state["logged_in"]:
    login_ui()
    st.stop()

# =========================
# SIDEBAR USUARIO
# =========================
st.sidebar.success(f"👤 Usuario: {st.session_state['user']}")

if st.sidebar.button("Cerrar sesión"):
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.rerun()

st.title("Herramienta online para evaluacion de condiciones historicas de viento y Oleaje en el caribe colombiano. 🌊")

DATA_DIR = Path("data")

# =========================
# ZONAS Y PARÁMETROS
# =========================


st.sidebar.header("🗺️ Zona de estudio")

zone_name = st.sidebar.selectbox(
    "Seleccione zona",
    list(ZONES.keys())
)

zone = ZONES[zone_name]

st.sidebar.header("📊 Parámetro")

param_name = st.sidebar.selectbox(
    "Seleccione parámetro",
    list(zone["parameters"].keys())
)

param = zone["parameters"][param_name]

# =========================
# INFO GENERAL
# =========================
st.title("🌊 Herramienta Metoceánica – Caribe Colombiano")

st.info(f"""
**Zona:** {zone_name}  
**Parámetro:** {param_name}
""")

# =========================
# CARGA DINÁMICA DEL SERVICIO
# =========================
try:
    service = importlib.import_module(
        f"services.{param['service']}"
    )
except ModuleNotFoundError:
    st.error("Servicio no encontrado")
    st.stop()

# =========================
# PROCESAMIENTO
# =========================
with st.spinner("Cargando datos..."):
    ds = service.load_data(param["path"])

with st.spinner("Procesando información..."):
    stats = service.process(ds)

with st.spinner("Generando visualización..."):
    fig = service.plot(ds)

# =========================
# VISUALIZACIÓN
# =========================
st.subheader("📈 Resultados")
st.pyplot(fig)

st.subheader("📊 Estadísticas")
st.json(stats)

# =========================
# EXPORT (BASE)
# =========================
st.download_button(
    label="📥 Descargar estadísticas (JSON)",
    data=str(stats),
    file_name=f"{zone_name}_{param_name}_stats.json",
    mime="application/json"
)

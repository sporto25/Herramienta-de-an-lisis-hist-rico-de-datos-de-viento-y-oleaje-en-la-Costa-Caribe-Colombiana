import numpy as np
import streamlit as st

def calculate(data, config):
    # AQUÍ modificas la lógica física
    ws = data["wind_speed"]
    return {
        "mean": np.mean(ws),
        "p95": np.percentile(ws, 95)
    }

def render(results):
    st.subheader("🌬️ Resultados de Viento")
    st.metric("Velocidad media", f"{results['mean']:.2f} m/s")
    st.metric("P95", f"{results['p95']:.2f} m/s")

WIND_PARAM = {
    "key": "wind",
    "name": "Viento",
    "inputs": {
        "height": {
            "label": "Altura (m)",
            "default": 100,
            "type": "number"
        }
    },
    "calculate": calculate,
    "render": render
}

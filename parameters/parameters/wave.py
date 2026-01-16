import numpy as np
import streamlit as st

def calculate(data, config):
    hs = data["significant_wave_height"]
    return {
        "Hs_mean": np.mean(hs),
        "Hs_max": np.max(hs)
    }

def render(results):
    st.subheader("🌊 Oleaje")
    st.metric("Hs media", f"{results['Hs_mean']:.2f} m")
    st.metric("Hs máxima", f"{results['Hs_max']:.2f} m")

WAVE_PARAM = {
    "key": "wave",
    "name": "Oleaje",
    "inputs": {},
    "calculate": calculate,
    "render": render
}

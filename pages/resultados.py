import streamlit as st
from parameters import PARAMETERS
from core.state import init_state, save_result

def render(data):
    init_state()

    st.title("Resultados")

    for name, param in PARAMETERS.items():
        st.divider()

        # Inputs dinámicos
        config = {}
        for k, meta in param["inputs"].items():
            config[k] = st.number_input(
                meta["label"],
                value=meta["default"]
            )

        # Cálculo
        result = param["calculate"](data, config)
        save_result(param["key"], result)

        # Render
        param["render"](result)

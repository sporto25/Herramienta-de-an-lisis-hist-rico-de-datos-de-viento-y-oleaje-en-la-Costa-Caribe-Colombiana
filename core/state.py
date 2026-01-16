import streamlit as st

def init_state():
    if "results" not in st.session_state:
        st.session_state.results = {}

def save_result(param_key, value):
    st.session_state.results[param_key] = value



import streamlit as st
from core.auth.db import login_user, register_user

def login_ui():
    st.title("🔐 Acceso a la plataforma")

    tab1, tab2 = st.tabs(["Login", "Registro"])

    with tab1:
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            if login_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["user"] = username
                st.success("Acceso concedido")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")

    with tab2:
        new_user = st.text_input("Nuevo usuario")
        new_pass = st.text_input("Nueva contraseña", type="password")

        if st.button("Registrar"):
            if register_user(new_user, new_pass):
                st.success("Usuario registrado correctamente")
            else:
                st.error("El usuario ya existe")

import streamlit as st
from views import dashboard, carga

# Configuración inicial de la página
st.set_page_config(page_title="Inversiones Modulares", layout="wide", page_icon="💰")

# Menú lateral de navegación
menu = st.sidebar.radio("Navegación:", ["📈 Dashboard", "📥 Cargar Datos"])
st.sidebar.write("---")

# Enrutamiento dinámico
if menu == "📈 Dashboard":
    dashboard.render_page()
elif menu == "📥 Cargar Datos":
    carga.render_page()
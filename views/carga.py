import streamlit as st
from datetime import datetime
import pandas as pd
import data_manager

def render_page():
    st.header("📥 Registro de nueva actualización")
    
    try:
        nombres_hojas = pd.ExcelFile(data_manager.PATH_EXCEL, engine="openpyxl").sheet_names
    except:
        nombres_hojas = ["iol-mm"]

    with st.form("form_carga", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            inversion_destino = st.selectbox("Seleccionar Inversión (Hoja):", nombres_hojas)
            fecha_input = st.date_input("Fecha de actualización:", datetime.now())
        with col_f2:
            nominales_input = st.number_input("Cantidad de Nominales:", min_value=0.0, step=0.01)
            saldo_input = st.number_input("Saldo Total ($):", min_value=0.0, step=0.01)
        
        btn_guardar = st.form_submit_button("Guardar en Excel")

        if btn_guardar:
            if saldo_input > 0:
                exito, mensaje = data_manager.guardar_registro(inversion_destino, fecha_input, nominales_input, saldo_input)
                if exito:
                    st.success(f"✅ {mensaje}")
                    st.cache_data.clear()  # Limpia caché para actualizar el dashboard
                else:
                    st.error(mensaje)
            else:
                st.warning("El saldo debe ser mayor a 0.")
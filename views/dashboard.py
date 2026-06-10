import streamlit as st
import plotly.express as px
import data_manager

def render_page():
    df_total = data_manager.cargar_todo()
    
    if df_total.empty:
        st.warning("No hay datos para mostrar. Cargá algo en la pestaña 'Cargar Datos'.")
        return

    st.header("📈 Rendimiento de Cartera")
    
    opciones = ["Todos"] + list(df_total['Inversion'].unique())
    seleccion = st.sidebar.selectbox("Filtrar Inversión:", opciones)
    df_f = df_total if seleccion == "Todos" else df_total[df_total['Inversion'] == seleccion]
    
    # Lógica de procesamiento de líneas de tiempo y deltas
    df_lt = df_f.groupby('Fecha')['Saldo'].sum().reset_index().sort_values('Fecha')
    actual = df_lt['Saldo'].iloc[-1]
    anterior = df_lt['Saldo'].iloc[-2] if len(df_lt) > 1 else actual
    delta_abs = actual - anterior
    delta_pct = (delta_abs / anterior) * 100 if anterior != 0 else 0

    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Saldo Actual", f"$ {actual:,.2f}")
    c2.metric("Evolución Diaria", f"{delta_pct:+.2f}%", f"$ {delta_abs:+,.2f}")
    c3.metric("Última Fecha", df_lt['Fecha'].max().strftime('%d/%m/%Y'))

    # Gráfico
    st.plotly_chart(px.line(df_lt, x='Fecha', y='Saldo', markers=True), use_container_width=True)
    
    if st.checkbox("Ver tabla"):
        st.dataframe(df_f.sort_values('Fecha', ascending=False))
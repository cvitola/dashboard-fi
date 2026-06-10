import streamlit as st
import plotly.express as px
import data_manager

def render_page():
    df_total = data_manager.cargar_todo()
    
    if df_total.empty:
        st.warning("No hay datos para mostrar. Cargá algo en la pestaña 'Cargar Datos'.")
        return

    st.header("📈 Rendimiento de Cartera")
    
    # --- FILTROS ---
    opciones = ["Todos"] + list(df_total['Inversion'].unique())
    seleccion = st.sidebar.selectbox("Filtrar Inversión:", opciones)
    
    df_f = df_total if seleccion == "Todos" else df_total[df_total['Inversion'] == seleccion]
    
    # --- PROCESAMIENTO DE LÍNEA DE TIEMPO ---
    df_lt = df_f.groupby('Fecha')['Saldo'].sum().reset_index().sort_values('Fecha')
    
    if not df_lt.empty:
        actual = df_lt['Saldo'].iloc[-1]
        anterior = df_lt['Saldo'].iloc[-2] if len(df_lt) > 1 else actual
        delta_abs = actual - anterior
        delta_pct = (delta_abs / anterior) * 100 if anterior != 0 else 0

        # KPIs superiores
        c1, c2, c3 = st.columns(3)
        titulo_kpi = "Saldo Actual" if seleccion == "Todos" else f"Saldo en {seleccion}"
        c1.metric(titulo_kpi, f"$ {actual:,.2f}")
        c2.metric("Evolución Diaria", f"{delta_pct:+.2f}%", f"$ {delta_abs:+,.2f}")
        c3.metric("Última Fecha", df_lt['Fecha'].max().strftime('%d/%m/%Y'))

    st.write("---")

    # --- GRÁFICOS ---
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("📊 Evolución Histórica")
        fig_linea = px.line(
            df_lt, x='Fecha', y='Saldo', markers=True,
            labels={'Fecha': 'Fecha', 'Saldo': 'Monto ($)'},
            template="plotly_white"
        )
        fig_linea.update_traces(line_color='#008080')
        st.plotly_chart(fig_linea, use_container_width=True)

    with col_graf2:
        if seleccion == "Todos":
            st.subheader("🍰 Distribución del Portafolio")
            df_actual = df_total.sort_values('Fecha').drop_duplicates('Inversion', keep='last')
            
            fig_torta = px.pie(
                df_actual, 
                values='Saldo', 
                names='Inversion', 
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig_torta, use_container_width=True)
        else:
            # ========================================================
            # NUEVO GRÁFICO: RENDIMIENTO PORCENTUAL PERÍODO A PERÍODO
            # ========================================================
            st.subheader(f"📊 Variación Porcentual de {seleccion}")
            
            # Calculamos el cambio porcentual registro a registro
            df_lt['Variación (%)'] = df_lt['Saldo'].pct_change() * 100
            
            # Eliminamos el primer registro porque no tiene contra qué compararse (daría NaN)
            df_rendimiento = df_lt.dropna(subset=['Variación (%)'])
            
            if df_rendimiento.empty:
                st.info("Aún no hay suficiente historial para calcular variaciones (se necesitan al menos 2 registros).")
            else:
                fig_barras = px.bar(
                    df_rendimiento, 
                    x='Fecha', 
                    y='Variación (%)',
                    labels={'Variación (%)': 'Rendimiento (%)', 'Fecha': 'Fecha'},
                    color='Variación (%)',
                    # Escala Divergente: Rojo para pérdidas, Blanco/Gris en el medio, Verde para ganancias
                    color_continuous_scale=[(0.0, '#ff4b4b'), (0.5, '#f4f4f4'), (1.0, '#238636')],
                    color_continuous_midpoint=0.0,
                    template="plotly_white"
                )
                
                # Ocultamos la barra de colores lateral para que el diseño quede bien limpio
                fig_barras.update_layout(coloraxis_showscale=False)
                
                # Formateamos los carteles flotantes para ver el "+" o "-" explícito
                fig_barras.update_traces(hovertemplate="Fecha: %{x}<br>Variación: %{y:+.2f}%")
                
                st.plotly_chart(fig_barras, use_container_width=True)
    
    # --- TABLA CRUDA ---
    st.write("---")
    if st.checkbox("Ver historial de datos filtrados"):
        st.dataframe(df_f.sort_values('Fecha', ascending=False), use_container_width=True)
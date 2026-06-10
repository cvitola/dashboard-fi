import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página web
st.set_page_config(
    page_title="Mis Inversiones - Evolución", 
    layout="wide", 
    page_icon="📈"
)

st.title("📊 Mi Panel de Control Financiero")
st.markdown("Seguimiento de saldos con cálculo de rendimiento diario y semanal.")
st.write("---")

PATH_EXCEL = "caja.xlsx"

# 2. Función para leer TODAS las hojas y unificarlas
@st.cache_data(ttl="5m")
def cargar_y_unificar_hojas(path):
    try:
        hojas = pd.read_excel(path, sheet_name=None, engine="openpyxl")
    except Exception as e:
        st.error(f"No se pudo abrir el archivo '{path}'. Error: {e}")
        st.stop()
        
    lista_df = []
    
    for nombre_hoja, df_hoja in hojas.items():
        df_hoja.columns = df_hoja.columns.str.strip()
        columnas_requeridas = ['Fecha actualizacion', 'nominales', 'saldo']
        if not all(col in df_hoja.columns for col in columnas_requeridas):
            continue 
            
        df_hoja = df_hoja.rename(columns={
            'Fecha actualizacion': 'Fecha',
            'nominales': 'Nominales',
            'saldo': 'Saldo'
        })
        
        # .dt.normalize() elimina la hora y deja solo la fecha (clave para agrupar diariamente)
        df_hoja['Fecha'] = pd.to_datetime(df_hoja['Fecha']).dt.normalize()
        df_hoja['Saldo'] = pd.to_numeric(df_hoja['Saldo'], errors='coerce')
        df_hoja['Nominales'] = pd.to_numeric(df_hoja['Nominales'], errors='coerce')
        df_hoja['Inversion'] = nombre_hoja
        df_hoja = df_hoja.dropna(subset=['Fecha', 'Saldo'])
        
        lista_df.append(df_hoja)
        
    if not lista_df:
        st.error("No se encontraron hojas con la estructura correcta.")
        st.stop()
        
    return pd.concat(lista_df, ignore_index=True)

# Cargar la data
df_total = cargar_y_unificar_hojas(PATH_EXCEL)

# 3. Filtro en la barra lateral
st.sidebar.header("Filtros")
opciones_inversion = ["Todos"] + list(df_total['Inversion'].unique())
seleccion = st.sidebar.selectbox("Seleccionar tipo de inversión:", opciones_inversion)

if seleccion == "Todos":
    df_filtrado = df_total.copy()
else:
    df_filtrado = df_total[df_total['Inversion'] == seleccion]

# ==========================================
# 4. CÁLCULO MÁGICO DE EVOLUCIÓN (DIARIA Y SEMANAL)
# ==========================================

# Creamos una línea de tiempo unificada sumando los saldos por día
df_linea_tiempo = df_filtrado.groupby('Fecha')['Saldo'].sum().reset_index().sort_values('Fecha')

# Valores por defecto por si no hay suficiente historial
saldo_actual = 0
var_diaria_abs, var_diaria_pct = 0, 0
var_semanal_abs, var_semanal_pct = 0, 0

if not df_linea_tiempo.empty:
    saldo_actual = df_linea_tiempo['Saldo'].iloc[-1]
    ultima_fecha = df_linea_tiempo['Fecha'].iloc[-1]
    
    # --- EVOLUCIÓN DIARIA (Último registro vs el anterior disponible) ---
    if len(df_linea_tiempo) >= 2:
        saldo_anterior_diario = df_linea_tiempo['Saldo'].iloc[-2]
        var_diaria_abs = saldo_actual - saldo_anterior_diario
        var_diaria_pct = (var_diaria_abs / saldo_anterior_diario) * 100 if saldo_anterior_diario != 0 else 0

    # --- EVOLUCIÓN SEMANAL (Último registro vs hace 7 días o el más cercano) ---
    fecha_7_dias_atras = ultima_fecha - pd.Timedelta(days=7)
    # Buscamos los registros que sean de hace 7 días o menos
    df_pasado_semanal = df_linea_tiempo[df_linea_tiempo['Fecha'] <= fecha_7_dias_atras]
    
    if not df_pasado_semanal.empty:
        # Si encontramos un registro de hace una semana (o más viejo), tomamos el último de ellos
        saldo_anterior_semanal = df_pasado_semanal['Saldo'].iloc[-1]
        var_semanal_abs = saldo_actual - saldo_anterior_semanal
        var_semanal_pct = (var_semanal_abs / saldo_anterior_semanal) * 100 if saldo_anterior_semanal != 0 else 0
    elif len(df_linea_tiempo) >= 2:
        # Si no hay 7 días de historial pero hay más de un registro, usamos el primero que exista como base
        saldo_anterior_semanal = df_linea_tiempo['Saldo'].iloc[0]
        var_semanal_abs = saldo_actual - saldo_anterior_semanal
        var_semanal_pct = (var_semanal_abs / saldo_anterior_semanal) * 100 if saldo_anterior_semanal != 0 else 0

# ==========================================
# 5. BLOQUE DE MÉTRICAS CON DELTAS
# ==========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    titulo_saldo = "Capital Total" if seleccion == "Todos" else f"Saldo {seleccion}"
    st.metric(label=titulo_saldo, value=f"$ {saldo_actual:,.2f}")

with col2:
    # Muestra cuánto subió/bajó de un día para el otro
    st.metric(
        label="Variación Diaria", 
        value=f"{var_diaria_pct:+.2f}%", 
        delta=f"$ {var_diaria_abs:+,.2f} (vs ayer/reg. anterior)",
        delta_color="normal" # Verde si es +, Rojo si es -
    )

with col3:
    # Muestra el comportamiento semanal
    st.metric(
        label="Variación Semanal", 
        value=f"{var_semanal_pct:+.2f}%", 
        delta=f"$ {var_semanal_abs:+,.2f} (vs hace ~7 días)",
        delta_color="normal"
    )

with col4:
    ultima_fecha_str = df_linea_tiempo['Fecha'].max().strftime('%d/%m/%Y') if not df_linea_tiempo.empty else "N/A"
    st.metric(label="Última Actualización", value=ultima_fecha_str)

st.write("---")

# ==========================================
# 6. GRÁFICOS INTERACTIVOS
# ==========================================
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("📈 Evolución del Saldo en el Tiempo")
    fig_linea = px.line(
        df_linea_tiempo, 
        x='Fecha', 
        y='Saldo', 
        markers=True,
        labels={'Fecha': 'Fecha', 'Saldo': 'Monto Total ($)'}
    )
    # Le ponemos un color lindo a la línea principal
    fig_linea.update_traces(line_color='#008080')
    st.plotly_chart(fig_linea, use_container_width=True)

with col_graf2:
    if seleccion == "Todos":
        st.subheader("🍰 Distribución Actual del Capital")
        # Conseguimos la foto del último día por cada hoja
        idx_ultimos = df_filtrado.groupby('Inversion')['Fecha'].idxmax()
        df_actual = df_filtrado.loc[idx_ultimos]
        
        fig_torta = px.pie(
            df_actual, 
            values='Saldo', 
            names='Inversion', 
            hole=0.4
        )
        st.plotly_chart(fig_torta, use_container_width=True)
    else:
        st.subheader("📊 Historial de Variaciones Diarias (%)")
        # Calculamos el porcentaje diario histórico para graficarlo en barras
        df_linea_tiempo['Rendimiento Diario (%)'] = df_linea_tiempo['Saldo'].pct_change() * 100
        df_barras = df_linea_tiempo.dropna(subset=['Rendimiento Diario (%)'])
        
        fig_var_diaria = px.bar(
            df_barras,
            x='Fecha',
            y='Rendimiento Diario (%)',
            labels={'Rendimiento Diario (%)': 'Variación (%)'},
            color='Rendimiento Diario (%)',
            color_continuous_scale=['#FF4B4B', '#238636'] # Rojo a Verde
        )
        st.plotly_chart(fig_var_diaria, use_container_width=True)

# 7. Tabla de datos crudos
st.write("---")
if st.checkbox("Mostrar planilla de datos crudos filtrados"):
    st.subheader("Registros históricos")
    st.dataframe(df_filtrado.sort_values(by='Fecha', ascending=False), use_container_width=True)
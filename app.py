import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página web
st.set_page_config(
    page_title="Mis Inversiones - OneDrive", 
    layout="wide", 
    page_icon="📈"
)

st.title("📈 Mi Panel de Inversiones Personales")
st.markdown("Datos sincronizados en tiempo real desde Microsoft OneDrive.")
st.write("---")

# URL DE DESCARGA DIRECTA RECIÉN DETECTADA
URL_ONEDRIVE = "https://onedrive.live.com/download?resid=FEED71FD4ED1FF87!s20d3ec0ed72f4137bed9fe65810c7c78"

# 2. Función para leer los datos (con caché de 5 minutos)
@st.cache_data(ttl="5m")
def cargar_datos(url):
    # Ahora sí descarga el .xlsx directo
    data = pd.read_excel(url, engine="openpyxl")
    
    # Limpieza preventiva de nombres de columnas
    data.columns = data.columns.str.strip()
    
    # Convertir formatos de forma segura
    data['Fecha actualizacion'] = pd.to_datetime(data['Fecha actualizacion'])
    data['Saldo'] = pd.to_numeric(data['Saldo'], errors='coerce')
    data['Nominales'] = pd.to_numeric(data['Nominales'], errors='coerce')
    
    return data

# 3. Levantar la data
try:
    df = cargar_datos(URL_ONEDRIVE)
except Exception as e:
    st.error(f"Error al conectar con OneDrive: {e}")
    st.stop()

# 4. Procesamiento: Obtener la foto del día (último saldo por fondo)
try:
    idx_ultimos = df.groupby('Fondo')['Fecha actualizacion'].idxmax()
    df_actual = df.loc[idx_ultimos]
    saldo_total = df_actual['Saldo'].sum()
except Exception as e:
    st.warning("Revisá que los nombres de las columnas en tu Excel coincidan exactamente con: 'Fecha actualizacion', 'Nominales', 'Fondo', 'Saldo'.")
    st.stop()

# 5. Bloque de Métricas (KPIs)
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Capital Total Actual", value=f"$ {saldo_total:,.2f}")
with col2:
    st.metric(label="Fondos Activos", value=int(df_actual['Fondo'].nunique()))
with col3:
    ultima_fecha = df['Fecha actualizacion'].max().strftime('%d/%m/%Y')
    st.metric(label="Última Actualización", value=ultima_fecha)

st.write("---")

# 6. Gráficos Interactivos (Plotly)
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Evolución Histórica de los Saldos")
    fig_linea = px.line(
        df.sort_values('Fecha actualizacion'), 
        x='Fecha actualizacion', 
        y='Saldo', 
        color='Fondo',
        markers=True,
        labels={'Fecha actualizacion': 'Fecha', 'Saldo': 'Monto ($)'}
    )
    st.plotly_chart(fig_linea, use_container_width=True)

with col_graf2:
    st.subheader("Distribución Actual del Portafolio")
    fig_torta = px.pie(
        df_actual, 
        values='Saldo', 
        names='Fondo', 
        hole=0.4,
        labels={'Saldo': 'Monto ($)'}
    )
    st.plotly_chart(fig_torta, use_container_width=True)

# 7. Tabla de auditoría
st.write("---")
if st.checkbox("Mostrar tabla con el historial de datos completos"):
    st.subheader("Registros históricos en crudo")
    st.dataframe(df.sort_values(by='Fecha actualizacion', ascending=False), use_container_width=True)
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Mis Finanzas", layout="wide")
st.title("📊 Mi Panel de Inversiones (Local)")

# 2. LEER EL EXCEL DIRECTO (Una sola línea de código transparente)
try:
    df = pd.read_excel("caja.xlsx")
except Exception as e:
    st.error(f"No se pudo leer el archivo 'inversiones.xlsx'. Asegurate de que esté en la misma carpeta. Error: {e}")
    st.stop()

# 3. Limpieza estándar de datos
df['Fecha actualizacion'] = pd.to_datetime(df['Fecha actualizacion'])

# 4. Métricas rápidas
saldo_total = df.groupby('Fondo').last()['Saldo'].sum() # Suma del último saldo de cada fondo
st.metric(label="Capital Total Actual", value=f"$ {saldo_total:,.2f}")

st.write("---")

# 5. Gráfico de evolución
fig = px.line(df, x='Fecha actualizacion', y='Saldo', color='Fondo', markers=True)
st.plotly_chart(fig, use_container_width=True)

# 6. Ver la tabla
st.subheader("Datos cargados:")
st.dataframe(df)
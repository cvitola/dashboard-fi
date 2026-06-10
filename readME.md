# 📈 Dashboard de Inversiones Personales

Mini aplicación web desarrollada en Python con **Streamlit** para el control, seguimiento y visualización de inversiones personales. Utiliza **Google Sheets** como base de datos (backend serverless) para facilitar la carga de datos desde cualquier dispositivo.

---

## 🛠️ Requisitos Previos

* Python 3.9 o superior.
* Una cuenta de Google Cloud (para la conexión segura con la API de Sheets).

---

## 🚀 Configuración del Entorno (Paso 0)

Para mantener las dependencias aisladas y evitar conflictos, se recomienda usar un entorno virtual de Python (`venv`).

### 1. Clonar el repositorio
```bash
git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
cd TU_REPOSITORIO

### 2. Instalar ambiente aislado venv
python -m venv venv
### 3. Instalar las siguientes librerias python
streamlit > pagina web local.
pandas > para manejar los datos
openpyxl > leer y entender archivos .xlsx
pltly > grafica y esteticas
pip install streamlit pandas openpyxl plotly
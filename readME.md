# 📈 Dashboard de Inversiones Personales

Aplicación web modular desarrollada en Python con **Streamlit** para el control, seguimiento y visualización de finanzas e inversiones. El sistema funciona como una interfaz CRUD ágil que lee y escribe de forma directa en un archivo Excel local, evitando la carga manual propensa a errores.

---

## 🚀 Características Clave

* **Separación de Conceptos:** Arquitectura modular (Vistas independientes de la lógica de datos).
* **Evolución Histórica:** Gráfico de líneas dinámico que trackea el crecimiento del capital total o por fondo.
* **Distribución del Portafolio:** Gráfico de torta automatizado que calcula la foto del día de tus activos.
* **Métricas de Rendimiento:** Historial de variación porcentual período a período con alertas visuales (Verde/Rojo) para ganancias y pérdidas.
* **Carga Atómica:** Formulario de registro inteligente que detecta y escribe en la última fila real del Excel sin generar registros huérfanos.

---

## 📂 Estructura del Proyecto

El proyecto está organizado bajo una arquitectura limpia y escalable:

```text
mi_proyecto/
│
├── app.py                 # Orquestador principal (Manejo de menú y ruteo)
├── data_manager.py        # Cerebro de datos (Lectura, escritura y tipado en Excel)
├── caja.xlsx              # Base de datos local (Tablas por tipo de inversión)
└── views/                 # Pantallas de la interfaz de usuario
    ├── __init__.py        # Inicializador de módulo de Python
    ├── dashboard.py       # Panel visual de analítica, KPIs y gráficos Plotly
    └── carga.py           # Formulario de entrada de nuevos registros

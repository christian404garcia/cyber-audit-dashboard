import streamlit as st
import psutil
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Diagnóstico de Hardware Local", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# Estilo visual Cyber/Matrix
st.markdown("""
<style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    .stApp {
        background-color: #030712;
        color: #e2e8f0;
    }
    div.stButton > button, div[data-testid="metric-container"] {
        background-color: rgba(11, 15, 25, 0.90) !important;
        border: 1px solid #0284c7 !important;
        color: #38bdf8 !important;
        border-radius: 8px;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ Panel de Diagnóstico de Hardware en Tiempo Real")
st.markdown("Esta interfaz extrae métricas reales y directas del sistema operativo y los componentes físicos del equipo donde se está ejecutando el script.")

st.info("💡 **Nota:** Si ejecutas este código en tu PC de forma local, analizará tu computadora. Si se ejecuta en un servidor web en la nube, analizará los recursos de ese servidor.")

# --- OBTENCIÓN DE DATOS REALES CON PSUTIL ---
cpu_percent = psutil.cpu_percent(interval=0.5)
cpu_count_logical = psutil.cpu_count(logical=True)
cpu_count_physical = psutil.cpu_count(logical=False)

ram = psutil.virtual_memory()
ram_total_gb = round(ram.total / (1024**3), 2)
ram_used_gb = round(ram.used / (1024**3), 2)
ram_percent = ram.percent

disk = psutil.disk_usage('/')
disk_total_gb = round(disk.total / (1024**3), 2)
disk_used_gb = round(disk.used / (1024**3), 2)
disk_percent = disk.percent

# --- SECCIÓN DE MÉTRICAS PRINCIPALES ---
st.subheader("💻 Métricas del Sistema Físico")

col1, col2, col3 = st.columns(3)
col1.metric("Uso Actual de CPU", f"{cpu_percent}%", f"{cpu_count_physical} Cores / {cpu_count_logical} Hilos")
col2.metric("Memoria RAM Usada", f"{ram_used_gb} GB / {ram_total_gb} GB", f"{ram_percent}% en uso")
col3.metric("Almacenamiento Principal (Disco)", f"{disk_used_gb} GB / {disk_total_gb} GB", f"{disk_percent}% en uso")

st.divider()

# --- GRÁFICO DE RENDIMIENTO ---
st.subheader("📊 Distribución y Carga de Recursos")

df_recursos = pd.DataFrame({
    "Componente": ["CPU (Procesador)", "Memoria RAM", "Almacenamiento (Disco)"],
    "Porcentaje de Uso (%)": [cpu_percent, ram_percent, disk_percent]
})

fig = px.bar(
    df_recursos, 
    x="Componente", 
    y="Porcentaje de Uso (%)", 
    text="Porcentaje de Uso (%)",
    title="Carga de Componentes en Vivo",
    color="Componente",
    color_discrete_sequence=['#38bdf8', '#34d399', '#f43f5e']
)
fig.update_traces(texttemplate='%{text}%', textposition='outside')
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", 
    plot_bgcolor="rgba(0,0,0,0)", 
    font_color="#38bdf8",
    height=420,
    showlegend=False
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Botón para refrescar métricas
if st.button("🔄 Actualizar Diagnóstico en Vivo"):
    st.rerun()

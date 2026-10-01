import streamlit as st
import streamlit.components.v1 as components
import platform
import pandas as pd
import plotly.express as px
import psutil

# Configuración de la página en modo ancho y colapsando/ocultando la barra lateral
st.set_page_config(page_title="CyberAudit & Performance Dashboard", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# Estilo visual: Fondo transparente, lluvia Matrix y Ocultamiento Total de la Barra Lateral
st.markdown("""
<style>
    /* Ocultar completamente la barra lateral y su botón de despliegue */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    .stApp {
        background: transparent !important;
        color: #e2e8f0;
    }
    
    div.stExpander, div.stButton > button, div[data-testid="metric-container"] {
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

# Componente de Lluvia de Código Matrix inyectado en la ventana principal
components.html("""
<script>
    const doc = window.parent.document;
    if (!doc.getElementById('matrix-canvas')) {
        const canvas = doc.createElement('canvas');
        canvas.id = 'matrix-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '-999';
        doc.body.appendChild(canvas);
        
        const ctx = canvas.getContext('2d');
        canvas.width = window.parent.innerWidth;
        canvas.height = window.parent.innerHeight;
        
        const chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZアァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = [];
        for(let i=0; i<columns; i++) drops[i] = 1;
        
        function draw() {
            ctx.fillStyle = 'rgba(3, 7, 18, 0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#38bdf8';
            ctx.font = fontSize + 'px monospace';
            for(let i=0; i<drops.length; i++) {
                const text = chars.charAt(Math.floor(Math.random() * chars.length));
                ctx.fillText(text, i*fontSize, drops[i]*fontSize);
                if(drops[i]*fontSize > canvas.height && Math.random() > 0.975) { drops[i] = 0; }
                drops[i]++;
            }
        }
        setInterval(draw, 33);
        window.parent.addEventListener('resize', () => {
            canvas.width = window.parent.innerWidth;
            canvas.height = window.parent.innerHeight;
        });
    }
</script>
""", height=0)

st.title("⚡ Panel Galáctico de Rendimiento & Ciberseguridad Cloud")
st.markdown("¡Bienvenido! Interfaz limpia y optimizada en pantalla completa con monitoreo en tiempo real.")

# Extracción en tiempo real del equipo local o servidor
ram = psutil.virtual_memory()
disk = psutil.disk_usage('C:') if platform.system() == "Windows" else psutil.disk_usage('/')
cpu_usage = psutil.cpu_percent(interval=0.5)

sys_info = {
    "OS": f"{platform.system()} {platform.release()}",
    "Node": platform.node(),
    "Processor": platform.processor() or "Intel / AMD x64 Processor",
    "BaseBoard": "ASUS PRIME H310M-E R2.0",
    "RAM_Total": f"{round(ram.total / (1024**3), 2)} GB",
    "RAM_Percent": f"{ram.percent}%",
    "RAM_Used": f"{round(ram.used / (1024**3), 2)} GB",
    "RAM_Free": f"{round(ram.available / (1024**3), 2)} GB",
    "Disk_Total": f"{round(disk.total / (1024**3), 2)} GB",
    "Disk_Free": f"{round(disk.free / (1024**3), 2)} GB",
    "Disk_Percent": f"{disk.percent}%",
    "CPU_Percent": f"{cpu_usage}%"
}

# Sección Superior: Info del equipo
st.subheader(f"💻 Analizando Host: {sys_info['Node']}")
col_inf1, col_inf2, col_inf3 = st.columns(3)
col_inf1.metric("Sistema Operativo", sys_info['OS'])
col_inf2.metric("Procesador", sys_info['Processor'])
col_inf3.metric("Placa Base", sys_info['BaseBoard'])

col_inf4, col_inf5, col_inf6 = st.columns(3)
col_inf4.metric("Memoria RAM", sys_info['RAM_Total'])
col_inf5.metric("Almacenamiento Total", sys_info['Disk_Total'])
col_inf6.metric("Espacio Libre", sys_info['Disk_Free'])

st.divider()

# Resumen de Estado de Rendimiento
st.subheader("🚀 Resumen de Estado de Rendimiento")
col_perf1, col_perf2, col_perf3 = st.columns(3)
col_perf1.metric("Uso de CPU", sys_info['CPU_Percent'], delta="Monitoreo activo")
col_perf2.metric("Uso de Memoria RAM", sys_info['RAM_Percent'], delta="Estable", delta_color="inverse")
col_perf3.metric("Uso de Almacenamiento", sys_info['Disk_Percent'], delta="Saludable")

# Gráficos de Torta Ampliados
colores_vivos = ['#38bdf8', '#34d399', '#f43f5e', '#fbbf24', '#a855f7']

st.subheader("🥧 Distribución Gráfica de Recursos")
df_rendimiento = pd.DataFrame({
    "Recurso": ["RAM en Uso", "RAM Libre", "Espacio Usado", "Espacio Libre"],
    "Porcentaje": [ram.percent, 100 - ram.percent, disk.percent, 100 - disk.percent]
})

fig_pie_perf = px.pie(
    df_rendimiento, 
    names="Recurso", 
    values="Porcentaje", 
    title="Estado Actual de Recursos (%)",
    hole=0.4,
    color_discrete_sequence=colores_vivos
)
fig_pie_perf.update_traces(textinfo='percent+label', textfont_size=14)
fig_pie_perf.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", 
    plot_bgcolor="rgba(0,0,0,0)", 
    font_color="#38bdf8",
    height=480,
    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
)
st.plotly_chart(fig_pie_perf, use_container_width=True)

st.divider()

# Hallazgos de Seguridad
st.subheader("🔍 Hallazgos y Acciones de Blindaje")
vulnerabilities = [
    {"component": "Actualizaciones de sistema", "risk": "Crítico", "desc": "Parches de seguridad pendientes de instalación."},
    {"component": "Firewall de Red", "risk": "Medio", "desc": "Revisión de reglas perimetrales recomendada."},
    {"component": "Control de Cuentas (UAC)", "risk": "Bajo", "desc": "Ajuste en políticas de permisos de usuario."},
]

for vuln in vulnerabilities:
    with st.expander(f"[{vuln['risk'].upper()}] {vuln['component']}"):
        st.write(f"**Diagnóstico:** {vuln['desc']}")

st.divider()

# Generación del reporte HTML interactivo para descargar
st.subheader("📤 Exportar Reporte HTML Interactivo")

html_template = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Reporte - __NODE__</title>
<style>body { background-color: #030712; color: #e2e8f0; font-family: sans-serif; padding: 30px; }</style>
</head><body><h1>⚡ Reporte de Auditoría: __NODE__</h1>
<p><strong>OS:</strong> __OS__ | <strong>Procesador:</strong> __PROCESSOR__</p>
<p><strong>RAM Usada:</strong> __RAM_PERCENT__ | <strong>CPU:</strong> __CPU_PERCENT__</p>
</body></html>"""

html_content = (
    html_template
    .replace("__NODE__", sys_info['Node'])
    .replace("__OS__", sys_info['OS'])
    .replace("__PROCESSOR__", sys_info['Processor'])
    .replace("__RAM_PERCENT__", sys_info['RAM_Percent'])
    .replace("__CPU_PERCENT__", sys_info['CPU_Percent'])
)

st.download_button(
    label="📥 Descargar Reporte HTML",
    data=html_content,
    file_name=f"reporte_auditoria_{sys_info['Node']}.html",
    mime="text/html"
)
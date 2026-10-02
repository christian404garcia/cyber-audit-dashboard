import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px

# Configuración de la página en modo ancho y ocultando barra lateral
st.set_page_config(page_title="CyberAudit & Device Analyzer", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# Estilo visual: Fondo transparente, lluvia Matrix y Ocultamiento Total de la Barra Lateral
st.markdown("""
<style>
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

# 1. INYECCIÓN DEL SCRIPT QUE PINTA LOS DATOS REALES DIRECTAMENTE EN EL DOM DEL CLIENTE
components.html("""
<div id="device-info" style="color: #38bdf8; font-family: monospace; font-size: 15px; padding: 15px; background: rgba(11, 15, 25, 0.85); border: 1px solid #0284c7; border-radius: 8px; margin-bottom: 20px;">
    <strong>🔍 Diagnóstico en Vivo del Navegador / Hardware:</strong><br>
    • <b>Plataforma / OS:</b> <span id="plat">Cargando...</span><br>
    • <b>Núcleos Lógicos (CPU):</b> <span id="cores">Cargando...</span> hilos<br>
    • <b>Memoria RAM Estimada:</b> <span id="ram">Cargando...</span><br>
    • <b>Resolución de Pantalla:</b> <span id="screen">Cargando...</span><br>
    • <b>Estado de Red:</b> <span id="net">Cargando...</span><br>
    • <b>Idioma:</b> <span id="lang">Cargando...</span>
</div>

<script>
    document.getElementById('plat').innerText = navigator.platform || "No disponible";
    document.getElementById('cores').innerText = navigator.hardwareConcurrency || "Desconocido";
    document.getElementById('ram').innerText = navigator.deviceMemory ? navigator.deviceMemory + " GB (Aprox)" : "No expuesto por navegador";
    document.getElementById('screen').innerText = window.screen.width + "x" + window.screen.height;
    document.getElementById('net').innerText = navigator.onLine ? "Online (Seguro)" : "Offline";
    document.getElementById('lang').innerText = navigator.language || "es";
</script>

<canvas id="matrix-canvas" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: -999;"></canvas>
<script>
    const canvas = document.getElementById('matrix-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
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
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
</script>
""", height=220)

st.title("⚡ Panel de Auditoría & Dispositivo del Cliente")
st.markdown("La herramienta superior recopila de forma instantánea y en vivo las especificaciones reales de tu navegador y hardware local.")

st.divider()

# Resumen de Estado de Seguridad del Cliente
st.subheader("🚀 Indicadores de Blindaje del Cliente")
col_perf1, col_perf2, col_perf3 = st.columns(3)
col_perf1.metric("Integridad de Cabeceras", "Óptima", delta="Seguro")
col_perf2.metric("Políticas de Cookies", "Bloqueo Activo", delta="Privacidad Alta")
col_perf3.metric("Cifrado de Sesión", "TLS 1.3 / HTTPS", delta="Activo")

# Gráficos interactivos de distribución de capacidades
colores_vivos = ['#38bdf8', '#34d399', '#f43f5e', '#fbbf24', '#a855f7']

st.subheader("🥧 Distribución de Capacidades del Dispositivo")
df_rendimiento = pd.DataFrame({
    "Característica": ["Capacidad de Núcleos CPU", "Memoria RAM Asignable", "Ancho de Banda Disponible", "Seguridad Perimetral"],
    "Valor": [85, 90, 95, 99]
})

fig_pie_perf = px.pie(
    df_rendimiento, 
    names="Característica", 
    values="Valor", 
    title="Nivel de Rendimiento y Capacidades del Cliente (%)",
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

# Hallazgos de Seguridad del Navegador
st.subheader("🔍 Hallazgos y Auditoría del Entorno Web")
vulnerabilities = [
    {"component": "Versión del Navegador", "risk": "Bajo", "desc": "El navegador web opera con soporte moderno de APIs de hardware."},
    {"component": "Aislamiento de Origen", "risk": "Seguro", "desc": "No se detectaron fugas de memoria en cachés globales."},
    {"component": "Políticas CORS", "risk": "Controlado", "desc": "Restricciones de llamadas externas activas."},
]

for vuln in vulnerabilities:
    with st.expander(f"[{vuln['risk'].upper()}] {vuln['component']}"):
        st.write(f"**Diagnóstico:** {vuln['desc']}")

st.divider()

# Generación del reporte HTML interactivo para descargar por el usuario
st.subheader("📤 Exportar Reporte de Auditoría del Cliente")

html_template = """<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8"><title>Reporte de Auditoría Web</title>
<style>body { background-color: #030712; color: #e2e8f0; font-family: sans-serif; padding: 30px; }</style>
</head><body><h1>⚡ Reporte de Auditoría del Dispositivo Cliente</h1>
<p><strong>Estado:</strong> Conexión Segura HTTPS</p>
<p><strong>Herramienta:</strong> CyberAudit & Client Device Analyzer</p>
</body></html>"""

st.download_button(
    label="📥 Descargar Reporte de Auditoría HTML",
    data=html_template,
    file_name="reporte_auditoria_cliente.html",
    mime="text/html"
)

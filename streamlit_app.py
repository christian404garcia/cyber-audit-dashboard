import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from urllib.parse import urlparse
import socket
import ssl

# Configuración de la página
st.set_page_config(page_title="CyberSec Web Vulnerability Scanner", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# Estilo visual Cyber / SOC Dark Mode
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
        background-color: rgba(11, 15, 25, 0.95) !important;
        border: 1px solid #0284c7 !important;
        color: #38bdf8 !important;
        border-radius: 8px;
    }
    div.stTextInput input {
        background-color: #0b0f19;
        color: #38bdf8;
        border: 1px solid #0284c7;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        text-shadow: 0 0 12px rgba(56, 189, 248, 0.35);
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️️ CyberSec Web Vulnerability Scanner")
st.markdown("Plataforma de auditoría ofensiva/defensiva para evaluar la postura de seguridad, cabeceras HTTP y riesgos de exposición de sitios web.")

# Barra de entrada de objetivo
target_url = st.text_input("Introduce el Dominio o URL a Auditar (ej: https://example.com)", "https://google.com")

if st.button("🚀 Iniciar Escaneo de Vulnerabilidades"):
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    parsed_url = urlparse(target_url)
    domain = parsed_url.netloc or parsed_url.path

    with st.spinner(f"Analizando vectores de ataque y cabeceras para: {domain}..."):
        try:
            # Realizar petición HTTP para analizar cabeceras
            response = requests.get(target_url, timeout=5, verify=True)
            headers = response.headers
            status_code = response.status_code
            
            # Auditoría de Cabeceras de Seguridad Clave
            security_headers = {
                "Strict-Transport-Security (HSTS)": "Strict-Transport-Security" in headers,
                "Content-Security-Policy (CSP)": "Content-Security-Policy" in headers,
                "X-Frame-Options (Clickjacking)": "X-Frame-Options" in headers,
                "X-Content-Type-Options": "X-Content-Type-Options" in headers,
                "X-XSS-Protection": "X-XSS-Protection" in headers,
            }
            
            score_headers = sum(1 for val in security_headers.values() if val)
            security_score = int((score_headers / len(security_headers)) * 100)

            st.success(f"¡Análisis completado con éxito para {domain}!")

            # --- MÉTRICAS GENERALES ---
            st.subheader("📊 Resumen del Perfil de Riesgo")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Código de Estado HTTP", status_code, "Normal" if status_code == 200 else "Revisar")
            col2.metric("Índice de Blindaje", f"{security_score}%", "Alto" if security_score > 60 else "Vulnerable")
            col3.metric("Protocolo de Transporte", parsed_url.scheme.upper(), "Cifrado SSL/TLS" if parsed_url.scheme == "https" else "Inseguro (HTTP)")
            col4.metric("Cabeceras Evaluadas", f"{score_headers}/{len(security_headers)}", "Protecciones activas")

            st.divider()

            # --- DETALLE DE CABECERAS ---
            st.subheader("🔍 Auditoría de Cabeceras de Seguridad (HTTP Headers)")
            
            header_data = []
            for header_name, status in security_headers.items():
                header_data.append({
                    "Cabecera de Seguridad": header_name,
                    "Estado": "✅ Implementada" if status else "❌ Ausente (Riesgo)",
                    "Nivel de Impacto": "Alto" if "HSTS" in header_name or "CSP" in header_name else "Medio"
                })
            
            df_headers = pd.DataFrame(header_data)
            st.dataframe(df_headers, use_container_width=True)

            st.divider()

            # --- GRÁFICO DE DISTRIBUCIÓN DE RIESGOS ---
            st.subheader("📈 Distribución de Controles de Seguridad")
            
            fig_bar = px.bar(
                df_headers, 
                x="Cabecera de Seguridad", 
                y=[100 if "✅" in x else 30 for x in df_headers["Estado"]],
                color="Estado",
                title="Puntuación de Controles Activos por Cabecera",
                color_discrete_map={"✅ Implementada": "#34d399", "❌ Ausente (Riesgo)": "#f43f5e"}
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)", 
                font_color="#38bdf8",
                height=400,
                yaxis_title="Nivel de Cumplimiento (%)"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            st.divider()

            # --- RECOMENDACIONES TÉCNICAS ---
            st.subheader("🛠️ Recomendaciones de Mitigación")
            if security_score < 80:
                st.warning("⚠️ **Alerta SOC:** Se detectaron carencias en las políticas de cabeceras. Se recomienda implementar cabeceras como `Content-Security-Policy` y `Strict-Transport-Security` para mitigar ataques de Cross-Site Scripting (XSS) y Man-in-the-Middle.")
            else:
                st.info("💡 **Estado Óptimo:** El sitio cumple con los estándares principales de endurecimiento de cabeceras web.")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error al conectar con el objetivo: No se pudo resolver o acceder a {target_url}. Verifica que la URL sea correcta y esté online.")

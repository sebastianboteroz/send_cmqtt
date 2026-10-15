import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y UI IoT CYBER
# ==========================================
st.set_page_config(
    page_title="IoT Command Center | Control MQTT",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS de Alto Contraste para Telemetría y Actuadores IoT
st.markdown("""
<style>
    /* Estructura Global Oscura Cyber/Industrial */
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }

    /* Header Principal */
    .iot-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F766E 100%);
        padding: 2.2rem;
        border-radius: 20px;
        color: #FFFFFF;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 25px rgba(15, 118, 110, 0.25);
        border: 1px solid #14B8A6;
    }

    .iot-header h1 {
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 0.4rem;
    }

    .iot-header p {
        color: #99F6E4;
        font-size: 1.05rem;
        margin: 0;
    }

    /* Badge de Estado Activo */
    .status-badge {
        display: inline-flex;
        align-items: center;
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 0.5rem 1rem;
        border-radius: 30px;
        color: #2DD4BF;
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    .status-dot {
        height: 10px;
        width: 10px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 8px #10B981;
    }

    /* Estilos personalizados para botones ON / OFF */
    div.stButton > button:first-child {
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: 0.6rem 1.5rem !important;
    }

    /* Botón Analógico Principal */
    .stButton>button {
        background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        padding: 0.65rem 1.5rem;
        width: 100%;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
        transition: all 0.2s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #0F766E 0%, #115E59 100%);
        box-shadow: 0 6px 16px rgba(13, 148, 136, 0.5);
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# FUNCIONES Y CONFIGURACIÓN MQTT ORIGINAL
# ==========================================
values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("clientesebasboteroz")
client1.on_message = on_message

# ==========================================
# BARRA LATERAL (DATOS DE CONEXIÓN)
# ==========================================
with st.sidebar:
    st.markdown("## ⚙️ Panel de Telemetría")
    st.caption("Configuración del Cliente MQTT")
    
    st.markdown("---")
    
    st.subheader("🌐 Servidor & Parámetros")
    st.code(f"Broker: {broker}\nPuerto: {port}\nID Cliente: clientesebasboteroz", language="yaml")
    
    st.markdown("---")
    st.caption(f"Versión de Python: {platform.python_version()}")

# ==========================================
# CUERPO PRINCIPAL
# ==========================================
st.markdown("""
<div class="iot-header">
    <h1>MQTT Command Center ⚡</h1>
    <p>Panel de control para actuadores digitales y emisión de señales analógicas en tiempo real.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="status-badge">
    <span class="status-dot"></span> Broker MQTT Online | Tópicos cmqtt_sebasttt / cmqtt_sebastianboteroz
</div>
""", unsafe_allow_html=True)

# Layout de dos columnas para separar actuadores digitales de señal analógica
col_digital, col_analog = st.columns([1, 1], gap="large")

# ------------------------------------------
# COLUMNA 1: ACTUADOR DIGITAL (ON / OFF)
# ------------------------------------------
with col_digital:
    with st.container(border=True):
        st.subheader("🔌 Control Digital (Actuador 1)")
        st.write("Emisión de comandos discretos al tópico `cmqtt_sebasttt`:")
        
        btn_col1, btn_col2 = st.columns(2)
        
        with btn_col1:
            if st.button('🟢 ENCENDER (ON)', use_container_width=True):
                act1 = "ON"
                client1 = paho.Client("clientesebasboteroz")                           
                client1.on_publish = on_publish                          
                client1.connect(broker, port)  
                message = json.dumps({"Act1": act1})
                ret = client1.publish("cmqtt_sebasttt", message)
                st.success("Comando ON publicado correctamente")
            else:
                st.write('')

        with btn_col2:
            if st.button('🔴 APAGAR (OFF)', use_container_width=True):
                act1 = "OFF"
                client1 = paho.Client("clientesebasboteroz")                           
                client1.on_publish = on_publish                          
                client1.connect(broker, port)  
                message = json.dumps({"Act1": act1})
                ret = client1.publish("cmqtt_sebasttt", message)
                st.error("Comando OFF publicado correctamente")
            else:
                st.write('')

# ------------------------------------------
# COLUMNA 2: CONTROL ANALÓGICO (SLIDER)
# ------------------------------------------
with col_analog:
    with st.container(border=True):
        st.subheader("🎛️ Modulación Analógica (PWM / Valor)")
        st.write("Selecciona el valor continuo para el tópico `cmqtt_sebastianboteroz`:")
        
        values = st.slider('Selecciona el rango de valores', 0.0, 100.0, 50.0)
        st.info(f"📊 Valor Seleccionado: **{values:.1f}**")

        if st.button('🚀 Enviar valor analógico'):
            client1 = paho.Client("clientesebasboteroz")                           
            client1.on_publish = on_publish                          
            client1.connect(broker, port)   
            message = json.dumps({"Analog": float(values)})
            ret = client1.publish("cmqtt_sebastianboteroz", message)
            st.success(f"Señalk analógica {values} publicada con éxito")
        else:
            st.write('')

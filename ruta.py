import streamlit as st
import folium
from folium import plugins
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Optimización de Rutas y Consumo de Gasolina", page_icon="🚗", layout="wide")

# Estilo CSS para mejorar la interfaz visual
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            color: #1E88E5;
            font-weight: bold;
            text-align: center;
            padding: 20px;
        }
        .section-header {
            font-size: 30px;
            color: #1976D2;
            font-weight: bold;
            padding-top: 20px;
        }
        .stButton>button {
            background-color: #0288D1;
            color: white;
            font-size: 18px;
            border-radius: 5px;
            width: 300px;
            height: 60px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #01579B;
        }
        .stSlider>div {
            color: #1976D2;
            font-size: 18px;
        }
        .stTextInput>div {
            font-size: 18px;
        }
        .stMarkdown {
            font-size: 18px;
        }
        .stDataFrame {
            font-size: 18px;
            margin-top: 20px;
        }
        .stBarChart>div {
            background-color: #0288D1;
        }
    </style>
""", unsafe_allow_html=True)

# Título de la aplicación
st.markdown('<div class="title">Optimización de Rutas y Consumo de Gasolina 🚗</div>', unsafe_allow_html=True)

# Configuración de la optimización
st.sidebar.header("Parámetros del Vehículo y Ruta")
velocidad_promedio = st.sidebar.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 80)
capacidad_tanque = st.sidebar.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
consumo_gasolina = st.sidebar.slider('Consumo de gasolina (litros/km)', 0.05, 0.2, 0.1)

# Inicializar lista de puntos (coordenadas)
puntos_seleccionados = []

# Crear mapa interactivo donde el usuario puede marcar puntos
mapa = folium.Map(location=[-12.0464, -77.0428], zoom_start=6)  # Coordenadas de inicio (ejemplo de Perú)

# Usar el plugin Draw de Folium para permitir que el usuario dibuje en el mapa
draw = plugins.Draw(export=True)
draw.add_to(mapa)

# Convertir el mapa a HTML y mostrar en Streamlit
mapa_html = mapa._repr_html_()
components.html(mapa_html, height=600)

# Mostrar mensaje sobre cómo interactuar
st.markdown("Haz clic en el mapa para agregar puntos. Luego, selecciona el botón para calcular la ruta optimizada.")

# Aquí es donde se manejarían las coordenadas marcadas por el usuario
# Esto debería ser procesado en el backend una vez que el usuario termine de dibujar los puntos.
# Para obtener las coordenadas de los puntos, Folium genera un archivo GeoJSON cuando el usuario dibuja.

if st.sidebar.button("Ejecutar Optimización"):
    if len(puntos_seleccionados) < 2:
        st.warning("Por favor, agrega al menos dos puntos en el mapa para optimizar la ruta.")
    else:
        # Aquí se implementaría la lógica para calcular la ruta con base en los puntos seleccionados
        st.write("Calculando la mejor ruta...")
        # Mostrar detalles de la ruta calculada (esto debería llamarse a la lógica que ya tenías de optimización de rutas)
        # Ejemplo:
        # ruta, tiempo, consumo, distancia = calcular_ruta_optima(...)

# Añadir lógica para extraer las coordenadas de los puntos seleccionados después de interactuar

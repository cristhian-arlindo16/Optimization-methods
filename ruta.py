import streamlit as st
import folium
from folium import plugins
import networkx as nx
import numpy as np
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
puntos_seleccionados = []
num_puntos = st.sidebar.number_input('Número de puntos a seleccionar', min_value=1, max_value=5, value=2)

# Recolectar las coordenadas de los puntos
for i in range(num_puntos):
    nombre_punto = st.sidebar.text_input(f'Nombre del punto {i+1}', f'Ciudad {i+1}')
    latitud = st.sidebar.number_input(f'Latitud del punto {i+1}', -90.0, 90.0, 0.0)
    longitud = st.sidebar.number_input(f'Longitud del punto {i+1}', -180.0, 180.0, 0.0)
    if nombre_punto and latitud and longitud:
        puntos_seleccionados.append((nombre_punto, [latitud, longitud]))

# Definir el grafo de rutas (distancia en km y tiempo estimado en horas)
grafo = nx.Graph()

# Función para calcular la mejor ruta optimizada
def calcular_ruta_optima(grafo, inicio, destino, velocidad, consumo_gasolina):
    # Calcular la mejor ruta usando Dijkstra (considerando distancia como métrica)
    ruta = nx.dijkstra_path(grafo, source=inicio, target=destino, weight='distance')
    
    # Calcular el tiempo total y el consumo de gasolina total de la ruta
    distancia_total = 0
    tiempo_total = 0
    consumo_total = 0

    for i in range(len(ruta) - 1):
        distancia = grafo[ruta[i]][ruta[i + 1]]['distance']
        tiempo = grafo[ruta[i]][ruta[i + 1]]['time']
        
        # Acumulamos los resultados
        distancia_total += distancia
        tiempo_total += tiempo
        consumo_total += distancia * consumo_gasolina  # Litros por km
    
    tiempo_llegada = tiempo_total  # Tiempo total de la ruta
    consumo_total_gasolina = consumo_total  # Consumo total de gasolina

    return ruta, tiempo_llegada, consumo_total_gasolina, distancia_total

# Función para crear el mapa con las rutas
def mostrar_mapa(ruta, coordenadas):
    # Crear el mapa centrado en el primer punto seleccionado
    mapa = folium.Map(location=coordenadas[0][1], zoom_start=6)

    # Agregar los puntos de las ciudades
    for ciudad, coord in coordenadas:
        folium.Marker(location=coord, popup=ciudad, icon=folium.Icon(color="blue")).add_to(mapa)
    
    # Trazar las rutas entre las ciudades
    for i in range(len(ruta) - 1):
        ciudad_inicio = ruta[i]
        ciudad_fin = ruta[i + 1]
        folium.PolyLine(locations=[coordenadas[ciudad_inicio], coordenadas[ciudad_fin]],
                        color='blue', weight=3, opacity=0.7).add_to(mapa)
    
    return mapa

# Botón para ejecutar la optimización de la ruta
if st.sidebar.button("Ejecutar Optimización"):
    # Calcular la mejor ruta
    ruta, tiempo, consumo, distancia = calcular_ruta_optima(grafo, inicio, destino, velocidad_promedio, consumo_gasolina)
    
    # Mostrar los resultados
    st.subheader(f"Ruta más eficiente desde {inicio} hasta {destino}:")
    st.write(f"Ruta: {' -> '.join(ruta)}")
    st.write(f"Distancia total: {distancia} km")
    st.write(f"Tiempo estimado de llegada: {tiempo} horas")
    st.write(f"Consumo total de gasolina: {consumo:.2f} litros")
    
    # Mostrar el mapa interactivo
    mapa_ruta = mostrar_mapa(ruta, puntos_seleccionados)
    
    # Convertir el mapa a HTML y mostrar en Streamlit
    mapa_html = mapa_ruta._repr_html_()  # Convertir el mapa en HTML
    components.html(mapa_html, height=600)  # Incrustar el mapa en la app

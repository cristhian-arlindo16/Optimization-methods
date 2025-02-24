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
inicio = st.sidebar.selectbox('Selecciona el punto de inicio', ['Ciudad A', 'Ciudad B', 'Ciudad C', 'Ciudad D'])
destino = st.sidebar.selectbox('Selecciona el destino', ['Ciudad A', 'Ciudad B', 'Ciudad C', 'Ciudad D'])
velocidad_promedio = st.sidebar.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 80)
capacidad_tanque = st.sidebar.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
consumo_gasolina = st.sidebar.slider('Consumo de gasolina (litros/km)', 0.05, 0.2, 0.1)

# Definir las coordenadas geográficas de las ciudades (latitud, longitud)
coordenadas = {
    'Ciudad A': [19.4326, -99.1332],  # Ejemplo: Ciudad A (CDMX)
    'Ciudad B': [19.0810, -98.1980],  # Ejemplo: Ciudad B
    'Ciudad C': [19.5047, -98.7073],  # Ejemplo: Ciudad C
    'Ciudad D': [19.3202, -99.7111],  # Ejemplo: Ciudad D
}

# Definir el grafo de rutas (distancia en km y tiempo estimado en horas)
grafo = nx.Graph()

# Agregar las rutas y distancias entre las ciudades (en km y horas)
grafo.add_edge('Ciudad A', 'Ciudad B', distance=150, time=2)  
grafo.add_edge('Ciudad A', 'Ciudad C', distance=200, time=3)  
grafo.add_edge('Ciudad B', 'Ciudad D', distance=120, time=1.5)  
grafo.add_edge('Ciudad C', 'Ciudad D', distance=180, time=2.5)  

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
    # Crear el mapa centrado en la primera ciudad (inicio)
    mapa = folium.Map(location=coordenadas[ruta[0]], zoom_start=6)

    # Agregar los puntos de las ciudades
    for ciudad, coord in coordenadas.items():
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
    mapa_ruta = mostrar_mapa(ruta, coordenadas)
    
    # Convertir el mapa a HTML y mostrar en Streamlit
    mapa_html = mapa_ruta._repr_html_()  # Convertir el mapa en HTML
    components.html(mapa_html, height=600)  # Incrustar el mapa en la app

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
velocidad_promedio = st.sidebar.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 80)
capacidad_tanque = st.sidebar.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
consumo_gasolina = st.sidebar.slider('Consumo de gasolina (litros/km)', 0.05, 0.2, 0.1)

# Crear el mapa interactivo
mapa = folium.Map(location=[-13.5310, -69.1910], zoom_start=10)  # Centrado en una ubicación ejemplo

# Habilitar el plugin Draw para agregar puntos al mapa
draw = plugins.Draw(export=True)
draw.add_to(mapa)

# Convertir el mapa a HTML y mostrarlo en Streamlit
mapa_html = mapa._repr_html_()
components.html(mapa_html, height=600)

# Recibir el GeoJSON generado por el plugin Draw
geojson_dibujado = st.text_area("Pega el GeoJSON aquí", "")

if geojson_dibujado:
    st.write("Puntos dibujados en el mapa:")
    st.json(geojson_dibujado)

    # Procesar el GeoJSON para obtener las coordenadas
    import json
    geojson_data = json.loads(geojson_dibujado)
    puntos = []
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'Point':
            puntos.append(feature['geometry']['coordinates'])
    
    # Calcular la mejor ruta entre los puntos
    if len(puntos) > 1:
        # Aquí implementas la lógica de optimización de ruta
        # Definir el grafo de rutas con distancias entre las ciudades
        grafo = nx.Graph()
        
        # Añadir nodos (puntos) al grafo
        for i, punto in enumerate(puntos):
            grafo.add_node(i, location=punto)
        
        # Conectar todos los puntos entre sí para simplificar el cálculo
        for i in range(len(puntos)):
            for j in range(i + 1, len(puntos)):
                lat1, lon1 = puntos[i]
                lat2, lon2 = puntos[j]
                # Calcular la distancia entre los puntos (usando distancia de Haversine)
                from geopy.distance import geodesic
                distancia = geodesic((lat1, lon1), (lat2, lon2)).km
                grafo.add_edge(i, j, weight=distancia)

        # Calcular la ruta más corta usando Dijkstra
        ruta_optima = nx.approximation.traveling_salesman_problem(grafo, cycle=False)
        coordenadas_ruta = [grafo.nodes[i]['location'] for i in ruta_optima]

        # Mostrar la ruta
        st.write("Ruta óptima:")
        for idx, coord in enumerate(coordenadas_ruta):
            st.write(f"Paso {idx + 1}: {coord}")
        
        # Mostrar el mapa con la ruta óptima
        mapa_optimo = folium.Map(location=coordenadas_ruta[0], zoom_start=10)
        for coord in coordenadas_ruta:
            folium.Marker(location=coord, icon=folium.Icon(color="blue")).add_to(mapa_optimo)
        
        for i in range(len(coordenadas_ruta) - 1):
            folium.PolyLine(locations=[coordenadas_ruta[i], coordenadas_ruta[i + 1]], color="red").add_to(mapa_optimo)

        mapa_html_optimo = mapa_optimo._repr_html_()
        components.html(mapa_html_optimo, height=600)


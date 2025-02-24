import streamlit as st
import folium
import networkx as nx
import streamlit.components.v1 as components

# Configuración de la página
st.set_page_config(page_title="Optimización de Rutas y Consumo de Gasolina", page_icon="🚗", layout="wide")

# Título de la aplicación
st.markdown('<div style="font-size: 40px; color: #1E88E5; font-weight: bold; text-align: center;">Optimización de Rutas y Consumo de Gasolina 🚗</div>', unsafe_allow_html=True)

# Configuración de la optimización
st.sidebar.header("Parámetros del Vehículo y Ruta")
inicio = st.sidebar.selectbox('Selecciona el punto de inicio', ['Ciudad A', 'Ciudad B', 'Ciudad C', 'Ciudad D'])
destino = st.sidebar.selectbox('Selecciona el destino', ['Ciudad A', 'Ciudad B', 'Ciudad C', 'Ciudad D'])
velocidad_promedio = st.sidebar.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 80)
capacidad_tanque = st.sidebar.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
consumo_gasolina = st.sidebar.slider('Consumo de gasolina (litros/km)', 0.05, 0.2, 0.1)

# Coordenadas de las ciudades (latitud, longitud)
coordenadas = {
    'Ciudad A': [19.4326, -99.1332],  # Ciudad A
    'Ciudad B': [19.0810, -98.1980],  # Ciudad B
    'Ciudad C': [19.5047, -98.7073],  # Ciudad C
    'Ciudad D': [19.3202, -99.7111],  # Ciudad D
}

# Grafo de rutas (distancia en km y tiempo estimado en horas)
grafo = nx.Graph()
grafo.add_edge('Ciudad A', 'Ciudad B', distance=150, time=2)
grafo.add_edge('Ciudad A', 'Ciudad C', distance=200, time=3)
grafo.add_edge('Ciudad B', 'Ciudad D', distance=120, time=1.5)
grafo.add_edge('Ciudad C', 'Ciudad D', distance=180, time=2.5)

# Función para calcular la ruta optimizada
def calcular_ruta_optima(grafo, inicio, destino, velocidad, consumo_gasolina):
    ruta = nx.dijkstra_path(grafo, source=inicio, target=destino, weight='distance')
    distancia_total = 0
    tiempo_total = 0
    consumo_total = 0

    for i in range(len(ruta) - 1):
        distancia = grafo[ruta[i]][ruta[i + 1]]['distance']
        tiempo = grafo[ruta[i]][ruta[i + 1]]['time']
        distancia_total += distancia
        tiempo_total += tiempo
        consumo_total += distancia * consumo_gasolina

    return ruta, tiempo_total, consumo_total, distancia_total

# Función para mostrar el mapa con la ruta
def mostrar_mapa(ruta, coordenadas):
    mapa = folium.Map(location=coordenadas[ruta[0]], zoom_start=6)
    for ciudad, coord in coordenadas.items():
        folium.Marker(location=coord, popup=ciudad).add_to(mapa)
    
    for i in range(len(ruta) - 1):
        folium.PolyLine(locations=[coordenadas[ruta[i]], coordenadas[ruta[i + 1]]], color='blue', weight=3, opacity=0.7).add_to(mapa)
    
    return mapa

# Ejecutar la optimización
if st.sidebar.button("Ejecutar Optimización"):
    ruta, tiempo, consumo, distancia = calcular_ruta_optima(grafo, inicio, destino, velocidad_promedio, consumo_gasolina)
    st.subheader(f"Ruta más eficiente desde {inicio} hasta {destino}:")
    st.write(f"Ruta: {' -> '.join(ruta)}")
    st.write(f"Distancia total: {distancia} km")
    st.write(f"Tiempo estimado de llegada: {tiempo} horas")
    st.write(f"Consumo total de gasolina: {consumo:.2f} litros")
    
    mapa_ruta = mostrar_mapa(ruta, coordenadas)
    mapa_html = mapa_ruta._repr_html_()
    components.html(mapa_html, height=600)

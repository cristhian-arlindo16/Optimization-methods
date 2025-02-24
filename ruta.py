import streamlit as st
import folium
import streamlit.components.v1 as components
from folium.plugins import Draw
import networkx as nx

# Configuración de la página
st.set_page_config(page_title="Optimización de Rutas y Consumo de Gasolina", page_icon="🚗", layout="wide")

# Título de la aplicación
st.markdown('<div style="font-size: 40px; color: #1E88E5; font-weight: bold; text-align: center;">Optimización de Rutas y Consumo de Gasolina 🚗</div>', unsafe_allow_html=True)

# Configuración de la optimización
st.sidebar.header("Parámetros del Vehículo y Ruta")
velocidad_promedio = st.sidebar.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 80)
capacidad_tanque = st.sidebar.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
consumo_gasolina = st.sidebar.slider('Consumo de gasolina (litros/km)', 0.05, 0.2, 0.1)

# Grafo de rutas (distancia en km y tiempo estimado en horas) - Deberías agregar más rutas
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
def mostrar_mapa(puntos):
    mapa = folium.Map(location=[19.4326, -99.1332], zoom_start=6)
    
    # Dibujar los puntos en el mapa
    for punto in puntos:
        folium.Marker(location=punto['coordinates'], popup=punto['name']).add_to(mapa)
    
    # Dibujar la ruta entre los puntos seleccionados
    if len(puntos) > 1:
        for i in range(len(puntos) - 1):
            folium.PolyLine(locations=[puntos[i]['coordinates'], puntos[i + 1]['coordinates']], color='blue', weight=3, opacity=0.7).add_to(mapa)

    return mapa

# Función para añadir puntos al mapa
def add_point(event):
    coords = event['latlng']
    st.session_state['puntos'].append({'name': f'Punto {len(st.session_state["puntos"]) + 1}', 'coordinates': [coords[0], coords[1]]})

# Inicializar los puntos en la sesión de Streamlit si no existen
if 'puntos' not in st.session_state:
    st.session_state['puntos'] = []

# Crear el mapa interactivo con folium
mapa = folium.Map(location=[19.4326, -99.1332], zoom_start=6)

# Habilitar la opción para dibujar puntos en el mapa
draw = Draw(
    draw_options={
        'polyline': False,
        'polygon': False,
        'circle': False,
        'rectangle': False,
        'marker': True
    },
    edit_options={'edit': True}
)
draw.add_to(mapa)

# Agregar los puntos y líneas
if len(st.session_state['puntos']) > 0:
    mapa_ruta = mostrar_mapa(st.session_state['puntos'])
    mapa_html = mapa_ruta._repr_html_()
    components.html(mapa_html, height=600)

# Agregar un botón para optimizar
if st.button('Optimizar Ruta'):
    if len(st.session_state['puntos']) < 2:
        st.error("Por favor, agregue al menos dos puntos en el mapa para calcular la ruta.")
    else:
        # Puedes ajustar esto a la lógica que desees para las ciudades
        ruta, tiempo, consumo, distancia = calcular_ruta_optima(grafo, 'Ciudad A', 'Ciudad B', velocidad_promedio, consumo_gasolina)
        st.subheader(f"Ruta más eficiente:")
        st.write(f"Ruta: {' -> '.join(ruta)}")
        st.write(f"Distancia total: {distancia} km")
        st.write(f"Tiempo estimado de llegada: {tiempo} horas")
        st.write(f"Consumo total de gasolina: {consumo:.2f} litros")
        
        mapa_ruta = mostrar_mapa(st.session_state['puntos'])
        mapa_html = mapa_ruta._repr_html_()
        components.html(mapa_html, height=600)

import streamlit as st
import folium
from folium.plugins import MarkerCluster
import geopy.distance  # Para calcular la distancia entre dos puntos

# Título de la aplicación
st.title('Optimización de Rutas y Consumo de Gasolina 🚗⛽')

# Parámetros de entrada
st.sidebar.header('Parámetros del Vehículo y Ruta')

# Selección de puntos de inicio y destino
ciudad_a = st.sidebar.selectbox('Selecciona el punto de inicio', ['Ciudad A', 'Ciudad B'])
ciudad_b = st.sidebar.selectbox('Selecciona el destino', ['Ciudad A', 'Ciudad B'])

# Coordenadas de las ciudades (Ejemplo, puedes cambiarlas con las coordenadas reales)
coordenadas = {
    'Ciudad A': [19.4326, -99.1332],  # Coordenadas de Ciudad A
    'Ciudad B': [20.6597, -103.3496]   # Coordenadas de Ciudad B
}

# Velocidad y capacidad del vehículo
velocidad = st.sidebar.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 100)
capacidad_tanque = st.sidebar.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
consumo_gasolina = st.sidebar.slider('Consumo de gasolina (litros/km)', 0.05, 0.20, 0.10)

# Calcular distancia entre las dos ciudades
start_coords = coordenadas[ciudad_a]
end_coords = coordenadas[ciudad_b]
distance = geopy.distance.geodesic(start_coords, end_coords).km

# Calcular tiempo estimado de viaje
tiempo_estimado = distance / velocidad  # Tiempo en horas

# Calcular el consumo de gasolina
consumo_estimado = distance * consumo_gasolina  # Litros de gasolina

# Crear el mapa centrado en el punto de inicio
mapa = folium.Map(location=start_coords, zoom_start=7)

# Agregar marcadores para las ciudades de inicio y destino
folium.Marker(start_coords, popup=f"{ciudad_a} (Inicio)", icon=folium.Icon(color='green')).add_to(mapa)
folium.Marker(end_coords, popup=f"{ciudad_b} (Destino)", icon=folium.Icon(color='red')).add_to(mapa)

# Dibuja la ruta entre las dos ciudades
folium.PolyLine([start_coords, end_coords], color="blue", weight=2.5, opacity=1).add_to(mapa)

# Agregar la funcionalidad de "MarkerCluster" para hacer el mapa más dinámico y limpio
marker_cluster = MarkerCluster().add_to(mapa)
folium.Marker(start_coords, popup=f"{ciudad_a} (Inicio)").add_to(marker_cluster)
folium.Marker(end_coords, popup=f"{ciudad_b} (Destino)").add_to(marker_cluster)

# Mostrar el mapa
st.write(mapa)

# Mostrar los resultados
st.subheader('Resultados del Viaje')

st.write(f'Distancia entre {ciudad_a} y {ciudad_b}: {distance:.2f} km')
st.write(f'Tiempo estimado de viaje: {tiempo_estimado:.2f} horas')
st.write(f'Consumo estimado de gasolina: {consumo_estimado:.2f} litros')

# Botón para ejecutar la optimización
if st.sidebar.button("Ejecutar Optimización"):
    st.subheader("Ruta Optima Calculada")
    st.write(f"La distancia es de {distance:.2f} km, el tiempo estimado es de {tiempo_estimado:.2f} horas y el consumo estimado de gasolina es de {consumo_estimado:.2f} litros.")

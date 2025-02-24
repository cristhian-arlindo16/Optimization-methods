import streamlit as st
import folium
from streamlit_folium import st_folium

# Título
st.title('Optimización de Rutas y Consumo de Gasolina 🚗')

# Parámetros del vehículo y ruta
velocidad_promedio = st.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 60)
capacidad_tanque = st.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
consumo_gasolina = st.slider('Consumo de gasolina (litros/km)', 0.05, 0.20, 0.10)

# Mapa interactivo inicial (coordenadas para el centro de Perú)
m = folium.Map(location=[-13.1631, -71.8129], zoom_start=6)

# Función para agregar puntos
def agregar_punto(lat, lon):
    folium.Marker([lat, lon], popup=f"Lat: {lat}, Lon: {lon}").add_to(m)

# Muestra el mapa interactivo y permite al usuario agregar puntos
st.subheader('Haz clic en el mapa para agregar puntos')

# Mostrar el mapa interactivo de Folium
mapa_interactivo = st_folium(m, width=700, height=500)

# Si el mapa tiene puntos, se mostrarán las coordenadas
if mapa_interactivo:
    # Obtener la coordenada del clic
    lat = mapa_interactivo.get("last_click", {}).get("lat")
    lon = mapa_interactivo.get("last_click", {}).get("lon")
    
    if lat and lon:
        agregar_punto(lat, lon)
        st.write(f"Se ha agregado un punto en: Lat: {lat}, Lon: {lon}")

# Mostrar los parámetros de la ruta
st.write(f"Velocidad promedio del vehículo: {velocidad_promedio} km/h")
st.write(f"Capacidad del tanque de gasolina: {capacidad_tanque} litros")
st.write(f"Consumo de gasolina: {consumo_gasolina} litros/km")

# Lógica para optimizar la ruta (puedes agregar tu lógica aquí)
if st.button('Optimizar Ruta'):
    st.write('Optimización en proceso...')
    # Agregar aquí el código para calcular la ruta optimizada, si es necesario
    st.write('Ruta optimizada con éxito!')

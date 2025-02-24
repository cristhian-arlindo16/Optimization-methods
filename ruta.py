import streamlit as st
import folium
from geopy.distance import geodesic
from streamlit_folium import st_folium

# Título y descripción de la aplicación
st.title("Optimización de Rutas y Consumo de Gasolina 🚗")
st.markdown("""
    Esta aplicación muestra la ruta más eficiente entre dos puntos en un mapa, 
    calcula la distancia y estima el tiempo de llegada dependiendo de los parámetros del vehículo.
""")

# Parámetros del vehículo y ruta
start_city = st.selectbox('Selecciona el punto de inicio', ['Ciudad A', 'Ciudad B'])
end_city = st.selectbox('Selecciona el destino', ['Ciudad A', 'Ciudad B'])

# Coordenadas de las ciudades
if start_city == 'Ciudad A' and end_city == 'Ciudad B':
    start_coords = [19.432608, -99.133209]  # Ciudad de México
    end_coords = [20.659698, -103.349609]  # Guadalajara
elif start_city == 'Ciudad B' and end_city == 'Ciudad A':
    start_coords = [20.659698, -103.349609]  # Guadalajara
    end_coords = [19.432608, -99.133209]  # Ciudad de México

# Parámetros del vehículo
vehicle_speed = st.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 100)
tank_capacity = st.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
fuel_consumption = st.slider('Consumo de gasolina (litros/km)', 0.05, 0.20, 0.10)

# Función para crear el mapa con folium
def create_map(start_coords, end_coords):
    m = folium.Map(location=start_coords, zoom_start=6)
    folium.Marker(location=start_coords, popup="Punto de inicio").add_to(m)
    folium.Marker(location=end_coords, popup="Punto de destino").add_to(m)
    folium.PolyLine([start_coords, end_coords], color="blue", weight=2.5, opacity=1).add_to(m)
    return m

# Crear el mapa
m = create_map(start_coords, end_coords)

# Mostrar el mapa en Streamlit usando st_folium
st_folium(m, width=700)

# Calcular la distancia entre los puntos
distance = geodesic(start_coords, end_coords).km
st.write(f"**Distancia entre los puntos:** {distance:.2f} km")

# Estimar el tiempo de llegada
travel_time = distance / vehicle_speed
st.write(f"**Tiempo estimado de llegada:** {travel_time:.2f} horas")

# Calcular el consumo de gasolina
total_fuel = distance * fuel_consumption
st.write(f"**Consumo estimado de gasolina:** {total_fuel:.2f} litros")

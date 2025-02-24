import streamlit as st
import googlemaps
from datetime import datetime

# Tu clave API de Google Maps
gmaps = googlemaps.Client(key="TU_CLAVE_API")

# Título de la aplicación
st.title('Optimización de Rutas en Puno')

# Coordenadas aproximadas del centro de Puno
puno_lat = -15.8402
puno_lon = -69.0188

# Ingreso de varias coordenadas
n = st.number_input("Número de destinos:", min_value=2, value=3)  # Al menos 2 puntos

# Entrada de coordenadas (origen + destinos)
coordinates = []
for i in range(n):
    st.subheader(f"Destino {i + 1}")
    lat = st.number_input(f"Latitud del destino {i + 1}", value=puno_lat)
    lon = st.number_input(f"Longitud del destino {i + 1}", value=puno_lon)
    coordinates.append((lat, lon))

# Botón para calcular la mejor ruta
if st.button('Calcular Mejor Ruta'):
    # Origen: primero se asume que el origen es el primer destino
    origin = coordinates[0]
    destinations = coordinates[1:]  # Los demás destinos

    # Solicitar la optimización de la ruta (instrucciones de dirección)
    directions_result = gmaps.directions(
        origin,
        destinations,
        mode="driving",  # Modo de transporte: conduciendo
        waypoints=destinations,  # Los puntos intermedios
        departure_time=datetime.now(),  # Hora de salida
        optimize_waypoints=True  # Optimiza los puntos intermedios
    )

    # Mostrar resultados
    if directions_result:
        # La mejor ruta optimizada
        best_route = directions_result[0]

        st.write("### Mejor Ruta Optimizada:")
        st.write(f"Distancia total: {best_route['legs'][0]['distance']['text']}")
        st.write(f"Tiempo estimado: {best_route['legs'][0]['duration']['text']}")

        st.write("### Instrucciones:")
        for step in best_route['legs'][0]['steps']:
            st.write(f"- {step['html_instructions']}")

    else:
        st.error("Error al calcular la ruta. Verifica las coordenadas y la clave API.")

import streamlit as st
import requests

# Título de la aplicación
st.title('Optimización de Rutas')

# Ingreso de coordenadas de origen y destino
origen_lat = st.number_input('Latitud de origen', value=40.712776)  # Nueva York por defecto
origen_lon = st.number_input('Longitud de origen', value=-74.005974)  # Nueva York por defecto
destino_lat = st.number_input('Latitud de destino', value=34.052235)  # Los Ángeles por defecto
destino_lon = st.number_input('Longitud de destino', value=-118.243683)  # Los Ángeles por defecto

# Botón para calcular la ruta
if st.button('Calcular Ruta'):
    # URL del servidor público de OSRM para calcular la ruta
    url = f'http://router.project-osrm.org/route/v1/driving/{origen_lon},{origen_lat};{destino_lon},{destino_lat}?overview=false'

    # Realizar la solicitud GET al servidor de OSRM
    response = requests.get(url)

    # Obtener los resultados en formato JSON
    data = response.json()

    # Verificar si la ruta fue calculada exitosamente
    if 'routes' in data:
        # Obtener la distancia y el tiempo estimado de la ruta
        distance = data['routes'][0]['legs'][0]['distance'] / 1000  # km
        duration = data['routes'][0]['legs'][0]['duration'] / 60  # minutos
        st.success(f'Distancia: {distance:.2f} km')
        st.success(f'Tiempo estimado: {duration:.2f} minutos')
    else:
        st.error("Error al calcular la ruta. Verifica las coordenadas o el servidor.")

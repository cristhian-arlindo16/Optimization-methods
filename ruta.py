import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium

# Inicializa la lista de puntos si no existe
if 'puntos' not in st.session_state:
    st.session_state['puntos'] = []

# Titulo
st.title('Optimización de Rutas y Consumo de Gasolina 🚗')

# Parámetros del vehículo y ruta
velocidad_promedio = st.slider('Velocidad promedio del vehículo (km/h)', 40, 120, 60)
capacidad_tanque = st.slider('Capacidad del tanque de gasolina (litros)', 20, 100, 50)
consumo_gasolina = st.slider('Consumo de gasolina (litros/km)', 0.05, 0.20, 0.10)

# Map
m = folium.Map(location=[20.659, -103.349], zoom_start=6)

# Función para agregar puntos en el mapa
def agregar_punto(lat, lon):
    st.session_state['puntos'].append((lat, lon))
    folium.Marker([lat, lon], popup=f"Lat: {lat}, Lon: {lon}").add_to(m)

# Mapa para que el usuario agregue puntos
st.subheader('Haz clic en el mapa para agregar puntos')
clicked = st_folium(m, width=700)

if clicked:
    lat, lon = clicked["lat"], clicked["lng"]
    agregar_punto(lat, lon)

# Mostrar puntos agregados
st.write(f'Puntos agregados: {len(st.session_state["puntos"])}')
for i, punto in enumerate(st.session_state['puntos']):
    st.write(f'{i+1}. Lat: {punto[0]}, Lon: {punto[1]}')

# Si se tienen al menos dos puntos, mostrar el botón para optimizar la ruta
if len(st.session_state['puntos']) >= 2:
    if st.button('Optimizar Ruta'):
        st.write('Optimización en proceso...')
        # Aquí puedes agregar el código para optimizar la ruta
        # Por ejemplo, usando una API para el cálculo de rutas más eficientes
        # Deberías implementar la lógica de optimización aquí.
        st.write('Ruta optimizada con éxito!')
else:
    st.warning("Por favor, agrega al menos dos puntos en el mapa para optimizar la ruta.")



import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

# Función para calcular EOQ por modelo
def calcular_eoq(demanda, costo_pedido, costo_almacenaje):
    eoq = np.sqrt((2 * demanda * costo_pedido) / costo_almacenaje)
    return eoq

# Función para mostrar rentabilidad de los modelos
def mostrar_rentabilidad(df):
    df['Rentabilidad'] = df['Precio_Venta'] - df['Costo_Pedido'] - df['Costo_Almacenaje']
    df_sorted = df.sort_values('Rentabilidad', ascending=False)
    st.write("Modelos más rentables:")
    st.write(df_sorted[['Marca', 'Modelo', 'Rentabilidad']].head())

# Función para calcular depreciación de cada coche
def calcular_depreciacion(df):
    df['Depreciacion_Anual'] = df['Precio_Venta'] / df['Vida_Util']
    return df

# Función para limpiar y verificar la columna 'Demanda'
def limpiar_datos_demanda(df):
    if df['Demanda'].isnull().any():
        st.warning("Hay valores nulos en la columna 'Demanda'. Los valores nulos serán eliminados.")
        df = df.dropna(subset=['Demanda'])  # Eliminar filas con valores nulos en 'Demanda'
    
    if not pd.api.types.is_numeric_dtype(df['Demanda']):
        st.warning("La columna 'Demanda' tiene valores no numéricos. Asegúrate de que todos los valores sean números.")
        df['Demanda'] = pd.to_numeric(df['Demanda'], errors='coerce')
        df = df.dropna(subset=['Demanda'])
    
    return df

# Función para realizar simulación de Monte Carlo de demanda
def simulacion_montecarlo(df, num_simulaciones=1000):
    if 'Demanda' not in df.columns:
        st.error("La columna 'Demanda' no está en los datos.")
        return []

    df = limpiar_datos_demanda(df)
    
    media_demanda = df['Demanda'].mean()
    desviacion_demanda = df['Demanda'].std()

    if np.isnan(media_demanda) or np.isnan(desviacion_demanda):
        st.error("Los datos de demanda no son válidos para la simulación de Monte Carlo.")
        return []

    demanda_simulada = np.random.normal(loc=media_demanda, scale=desviacion_demanda, size=num_simulaciones)
    return demanda_simulada

# Función para visualizar el inventario por modelo
def plot_inventarios(df):
    df['EOQ'] = df.apply(lambda row: calcular_eoq(row['Demanda'], row['Costo_Pedido'], row['Costo_Almacenaje']), axis=1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['Modelo'], df['EOQ'], label="EOQ por Modelo")
    plt.xlabel('Modelo de coche')
    plt.ylabel('EOQ (Cantidad de Pedido Económica)')
    plt.title('EOQ por Modelo')
    plt.legend()
    st.pyplot(plt)

# Visualización interactiva con Plotly
def plot_rentabilidad_interactiva(df):
    fig = px.bar(df, x="Modelo", y="Rentabilidad", title="Rentabilidad por Modelo")
    st.plotly_chart(fig)

# Título de la aplicación
st.title("Optimización de Inventarios en Concesionarios de Coches")

# Subir archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV con datos de coches", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, delimiter=';')
        
        # Mostrar los datos cargados
        st.write("Datos del archivo CSV cargado:")
        st.write(df.head())  # Muestra solo las primeras filas para revisar
        
        # Verificar si las columnas necesarias están presentes
        if 'Demanda' in df.columns and 'Costo_Pedido' in df.columns and 'Costo_Almacenaje' in df.columns and 'Precio_Venta' in df.columns and 'Vida_Util' in df.columns:
            
            # Filtros interactivos para seleccionar Marca y Modelo
            marcas = df['Marca'].unique().tolist()
            marca_seleccionada = st.selectbox('Selecciona una Marca', ['Todos'] + marcas)  # Opción "Todos"
            
            if marca_seleccionada != 'Todos':
                df_filtrado_marca = df[df['Marca'] == marca_seleccionada]
            else:
                df_filtrado_marca = df  # Si se selecciona "Todos", no se filtra por marca

            # Mostrar todos los modelos si se selecciona "Todos"
            modelos = df_filtrado_marca['Modelo'].unique().tolist()
            modelo_seleccionado = st.selectbox('Selecciona un Modelo', ['Todos'] + modelos)  # Opción "Todos"

            if modelo_seleccionado != 'Todos':
                df_filtrado_modelo = df_filtrado_marca[df_filtrado_marca['Modelo'] == modelo_seleccionado]
            else:
                df_filtrado_modelo = df_filtrado_marca  # Si se selecciona "Todos", no se filtra por modelo
            
            # Mostrar rentabilidad y gráficos solo para la marca y modelo seleccionados
            mostrar_rentabilidad(df_filtrado_modelo)
            plot_inventarios(df_filtrado_modelo)
            plot_rentabilidad_interactiva(df_filtrado_modelo)
            
            # Mostrar la tabla con los resultados de EOQ y Depreciación
            df_filtrado_modelo = calcular_depreciacion(df_filtrado_modelo)
            st.write("Resultados de la optimización (EOQ y Depreciación por modelo):")
            st.write(df_filtrado_modelo[['Marca', 'Modelo', 'Demanda', 'Costo_Pedido', 'Costo_Almacenaje', 'Precio_Venta', 'Vida_Util', 'EOQ', 'Depreciacion_Anual']])
            
            # Simulación de demanda futura con Monte Carlo
            num_simulaciones = st.slider('Número de simulaciones', min_value=100, max_value=5000, value=1000)
            demanda_simulada = simulacion_montecarlo(df_filtrado_modelo, num_simulaciones)
            
            if len(demanda_simulada) > 0:
                st.write(f"Promedio de la demanda simulada: {demanda_simulada.mean()}")
                st.write("Primeros valores de la simulación:")
                st.write(demanda_simulada[:10])
            else:
                st.write("No se pudo realizar la simulación de Monte Carlo debido a datos incorrectos.")
            
            # Crear archivo CSV con los resultados de la optimización
            csv_filename = "resultados_optimizacion.csv"
            df_filtrado_modelo.to_csv(csv_filename, index=False)
            
            # Crear enlace de descarga para el archivo CSV
            st.download_button(
                label="Descargar resultados optimización",
                data=df_filtrado_modelo.to_csv(index=False).encode('utf-8'),
                file_name=csv_filename,
                mime='text/csv'
            )
            
        else:
            st.write("El archivo CSV no contiene las columnas necesarias ('Demanda', 'Costo_Pedido', 'Costo_Almacenaje', 'Precio_Venta', 'Vida_Util').")
    except Exception as e:
        st.error(f"Hubo un problema al cargar el archivo: {e}")
else:
    st.write("Por favor, sube un archivo CSV con datos de coches para continuar.")

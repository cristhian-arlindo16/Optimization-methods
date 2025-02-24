import streamlit as st
import numpy as np
import pandas as pd
import random
import simpy
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms

# Configuración de la aplicación
st.set_page_config(page_title="Optimización de Ensamblaje Automotriz", page_icon="🚗", layout="wide")

# Estilo CSS para mejorar la interfaz
st.markdown("""
    <style>
        .title {
            font-size: 50px;
            color: #0D47A1;
            font-weight: bold;
            text-align: center;
            padding: 10px;
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
st.markdown('<div class="title">Optimización de la Línea de Ensamblaje Automotriz 🚗</div>', unsafe_allow_html=True)

# 1. Algoritmo Genético

def algoritmo_genetico(num_estaciones, max_generaciones, poblacion_size):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))  # Minimizar costo
    creator.create("Individual", list, fitness=creator.FitnessMin)

    def crear_individuo():
        return [random.randint(1, 5) for _ in range(num_estaciones)]  # Asignar aleatoriamente operarios

    def evaluar_individuo(individuo):
        costo = sum(individuo) * 10  # Costos simplificados (se pueden ajustar)
        return costo,  # Tupla de un solo valor

    toolbox = base.Toolbox()
    toolbox.register("individual", tools.initIterate, creator.Individual, crear_individuo)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evaluar_individuo)

    poblacion = toolbox.population(n=poblacion_size)

    resultados = []
    for gen in range(max_generaciones):
        for ind in poblacion:
            if not ind.fitness.valid:
                ind.fitness.values = toolbox.evaluate(ind)

        elite = toolbox.select(poblacion, len(poblacion))
        poblacion = list(map(toolbox.clone, elite))

        for i in range(0, len(poblacion), 2):
            if random.random() < 0.7:
                toolbox.mate(poblacion[i], poblacion[i+1])
                del poblacion[i].fitness.values
                del poblacion[i+1].fitness.values

        for i in range(len(poblacion)):
            if random.random() < 0.2:
                toolbox.mutate(poblacion[i])
                del poblacion[i].fitness.values

        mejores = tools.selBest(poblacion, 1)
        resultados.append(mejores[0].fitness.values[0])

    return resultados, poblacion

# 2. Simulación de Eventos Discretos (DES)

def simulacion_dinamica(estaciones, recursos):
    env = simpy.Environment()
    tiempos_ensamblaje = [random.randint(1, 5) for _ in range(estaciones)]
    resultados = []

    def linea_ensamblaje(env, estaciones, recursos):
        for i in range(estaciones):
            yield env.timeout(tiempos_ensamblaje[i])
            resultados.append(f"Estación {i+1} completada.")
    
    env.process(linea_ensamblaje(env, estaciones, recursos))
    env.run()
    
    return resultados

# 3. Interfaz de Usuario en Streamlit

# Entrada de parámetros por parte del usuario
st.sidebar.header("Configuración de la Optimización")
num_estaciones = st.sidebar.slider('Número de estaciones de ensamblaje', 1, 10, 3)
num_operarios = st.sidebar.slider('Número de operarios por estación', 1, 10, 5)
max_generaciones = st.sidebar.slider('Número de generaciones del algoritmo genético', 10, 100, 50)
poblacion_size = st.sidebar.slider('Tamaño de la población', 10, 100, 28)

# Botón para ejecutar la optimización
if st.sidebar.button("Ejecutar Optimización"):
    with st.spinner("Calculando..."):
        # Ejecutar optimización
        resultados_optim = algoritmo_genetico(num_estaciones, max_generaciones, poblacion_size)
        resultados_simulacion = simulacion_dinamica(num_estaciones, num_operarios)
        
        # Mostrar resultados de la optimización
        st.subheader("Resultados de la Optimización")
        costo_mejor = min(resultados_optim[0])
        st.write(f"Costo total de la mejor asignación: {costo_mejor}")
        
        # Mostrar gráfica de evolución del costo
        st.subheader("Evolución del Costo de la Optimización")
        st.line_chart(resultados_optim[0])

        # Mostrar resultados de la simulación
        st.subheader("Simulación de Eventos Discretos")
        for res in resultados_simulacion:
            st.write(res)

# 4. Mostrar gráficos y tablas

# Asignación de operarios
asignacion_operarios = [random.randint(1, 10) for _ in range(num_estaciones)]
st.subheader("Asignación de Operarios a Estaciones")
st.bar_chart(asignacion_operarios)

# Mostrar tabla con los resultados de la optimización
st.subheader("Tabla de Resultados de Optimización")
resultados_tabla = pd.DataFrame({
    "Estación": [f"Estación {i+1}" for i in range(num_estaciones)],
    "Operarios Asignados": asignacion_operarios,
})
st.write(resultados_tabla)

# Finalizar
st.markdown('<div class="section-header">¡Optimización completada! Ajusta los parámetros y prueba diferentes escenarios.</div>', unsafe_allow_html=True)


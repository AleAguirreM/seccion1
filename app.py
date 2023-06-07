# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 21:50:56 2023

@author: Usuario
"""

import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Utilizar la página completa en lugar de una columna central estrecha
st.set_page_config(layout="wide")

# Título principal
st.markdown("<h1 style='text-align: center; color: #4A148C;'>Enfermedades que han afectado gravemente a Nueva York 🗽</h1>", unsafe_allow_html=True)

# Cargar datos

df0 = pd.read_csv('covid.csv')  # base historico
df1 = pd.read_csv('vih.csv')  # base actual
df2 = pd.read_csv('causas_muertes.csv')  # base actual

# Tratamiento de datos 
df0['fecha_muestra'] = df0['fecha_muestra'].apply(
    pd.to_datetime, format='%Y/%m/%d')
df0['año'] = df0['fecha_muestra'].dt.year
df1.columns = ['año', 'distritos', 'genero', 'edad', 'raza/etnia', 'diagnosticos_vih', 'tasa_diagnostico_vih',
               'diagnosticos_sida', 'tasa_diagnostico_sida', 'muertes']
df2.columns = ['año', 'causa_de_muerte', 'genero', 'raza/etnia',
               'muertes']
df2['raza/etnia'] = df2['raza/etnia'].replace(['Non-Hispanic White', 'Non-Hispanic Black','Asian and Pacific Islander','Other Race/ Ethnicity','Not Stated/Unknown' ], ['White Non-Hispanic', 'Black Non-Hispanic','Asian/Pacific Islander','Other/Unknown','Other/Unknown'])
a = df0.groupby(['año'])[['muertes']].sum().reset_index()
a.rename(columns={'muertes': 'muertes_covid'}, inplace=True)
b = df1.groupby(['año'])[['muertes']].sum().reset_index()
b.rename(columns={'muertes': 'muertes_VIH'}, inplace=True)
c = df2.groupby(['año'])[['muertes']].sum().reset_index()
c.rename(columns={'muertes': 'muertes_otras'}, inplace=True)
df = pd.merge(b, c, how='outer', on='año').merge(a, how='outer', on='año')

# Dividir el ancho en 3 columnas de igual tamaño
c1, c2, c3 = st.columns((1, 1, 1))

# --------------- Top sexo
c1.markdown("<h3 style='text-align: left; color: #000000;'> Top Muertes por Sexo </h3>",
            unsafe_allow_html=True)
base5 = df1.query('genero != "All"').groupby(df1['genero'])['muertes'].sum().reset_index()
base6 = df2.query('genero != "All"').groupby(df2['genero'])['muertes'].sum().reset_index()
df4 = pd.concat([base5, base6])

df5 = df4.groupby(df4['genero'])['muertes'].sum().reset_index().sort_values('muertes', ascending=False)
top_perp_name = (df5['genero'].value_counts().index[0])
top_perp_num = (round(df5['muertes'][1]/(df5['muertes'].sum()), 4)*100)

c1.text('Genero: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

# --------------- Top raza
c2.markdown("<h3 style='text-align: left; color: #000000;'> Top Muertes por Raza </h3>", unsafe_allow_html=True)
base7 = df1.groupby(df1['raza/etnia'])['muertes'].sum().reset_index().sort_values('muertes', ascending=False)
base8 = df2.groupby(df2['raza/etnia'])['muertes'].sum().reset_index().sort_values('muertes', ascending=False)
df6 = pd.concat([base7, base8])
df7 = df6.groupby(df6['raza/etnia'])['muertes'].sum().reset_index().sort_values('muertes', ascending=False)
top_perp_name = (df7['raza/etnia'].value_counts().index[0])
top_perp_num = (round((df7['muertes'].max())/(df7['muertes'].sum()), 4)*100)

c2.text('Raza: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

# --------------- Top edad
c3.markdown("<h3 style='text-align: left; color: #000000;'> Top Muertes por Edad </h3>",
            unsafe_allow_html=True)
base9 = df1.query('edad != "All"').groupby(df1['edad'])['muertes'].sum().reset_index()

top_perp_name = (base9['edad'].value_counts().index[5])
top_perp_num =  (round((base9['muertes'].max())/(base9['muertes'].sum()), 4)*100)

c3.text('Edad: '+str(top_perp_name)+', '+str(top_perp_num)+'%')

#---------------------------------SECCION 2--------------------------------------------------------------------------------------------------------------------------
st.markdown("<h2 style='text-align: center; color: #4A148C;'>Como ha afectado el VIH/SIDA a Nueva York 🗽</h2>", unsafe_allow_html=True)
#----- DONA1
# Filtrar las filas sin la categoría "all" en la columna "genero"
df_filtrado = df1[df1['genero'] != 'All']

# Agrupar por género y calcular la suma de diagnósticos de VIH por género
diagnosticos_vih_por_genero = df_filtrado.groupby('genero')['diagnosticos_vih'].sum()

# Calcular el total de diagnósticos de VIH por género
total_diagnosticos_vih = diagnosticos_vih_por_genero.sum()

# Crear un nuevo DataFrame para almacenar los resultados
df_porcentaje_vih = pd.DataFrame(columns=['Genero', 'Porcentaje'])

# Calcular el porcentaje de mujeres y hombres diagnosticados con VIH
porcentaje_mujeres_vih = (diagnosticos_vih_por_genero['Female'] / total_diagnosticos_vih) * 100
porcentaje_hombres_vih = (diagnosticos_vih_por_genero['Male'] / total_diagnosticos_vih) * 100

# Agregar los valores al DataFrame
df_porcentaje_vih.loc[0] = ['Mujeres', porcentaje_mujeres_vih]
df_porcentaje_vih.loc[1] = ['Hombres', porcentaje_hombres_vih]

# Agrupar por género y calcular la suma de diagnósticos de SIDA por género
diagnosticos_sida_por_genero = df_filtrado.groupby('genero')['diagnosticos_sida'].sum()

# Calcular el total de diagnósticos de SIDA por género
total_diagnosticos_sida = diagnosticos_sida_por_genero.sum()

# Crear un nuevo DataFrame para almacenar los resultados
df_porcentaje_sida = pd.DataFrame(columns=['Genero', 'Porcentaje'])

# Calcular el porcentaje de mujeres y hombres diagnosticados con VIH
porcentaje_mujeres_sida = (diagnosticos_sida_por_genero['Female'] / total_diagnosticos_sida) * 100
porcentaje_hombres_sida = (diagnosticos_sida_por_genero['Male'] / total_diagnosticos_sida) * 100

# Agregar los valores al DataFrame
df_porcentaje_sida.loc[0] = ['Mujeres', porcentaje_mujeres_sida]
df_porcentaje_sida.loc[1] = ['Hombres', porcentaje_hombres_sida]

# Calcular la suma de diagnósticos de VIH por año
diagnosticos_vih_por_año = df1.groupby('año')['diagnosticos_vih'].sum()

# Calcular la suma de diagnósticos de SIDA por año
diagnosticos_sida_por_año = df1.groupby('año')['diagnosticos_sida'].sum()

# Dividir el ancho en 3 columnas de igual tamaño
col1, col2 = st.columns(2)

# gráfica 1
fig1 = px.pie(df_porcentaje_vih, values='Porcentaje', names='Genero', title='<b>% Diagnosticos de VIH por genero <b>', hole=0.6)
fig1.update_traces(marker=dict(colors=['#BA68C8', '#9C27B0']))
fig1.update_layout(
    template='simple_white',
    title_x=0.5,
    annotations=[dict(text=str(total_diagnosticos_vih), x=0.5, y=0.5, font_size=22, showarrow=False)])
col1.plotly_chart(fig1)

# gráfica 2
fig2 = px.pie(df_porcentaje_sida, values='Porcentaje', names='Genero', title='<b>% Diagnosticos de SIDA por genero <b>', hole=0.6)
fig2.update_traces(marker=dict(colors=['#BA68C8', '#9C27B0']))
fig2.update_layout(
    template='simple_white',
    legend_title='Genero',
    title_x=0.5,
    annotations=[dict(text=str(total_diagnosticos_sida), x=0.5, y=0.5, font_size=22, showarrow=False)])
col1.plotly_chart(fig2)

# grafica 3
# debido a la cantidad de vatriables se resuekve crear dos gráficas una que muestre por año y la otra por genero

base2 = df1.groupby(['año'])[['diagnosticos_vih', 'diagnosticos_sida']].sum().reset_index()

d = base2[['año', 'diagnosticos_vih']].rename(columns={'diagnosticos_vih': 'valores'})
e = base2[['año', 'diagnosticos_sida']].rename(columns={'diagnosticos_sida': 'valores'})
d['categoria'] = 'VIH'
e['categoria'] = 'SIDA'
base2 = pd.concat([d, e])
base3 = base2.groupby(['categoria', 'año'])[['valores']].sum().reset_index()
# crear dataset
base1 = df1.query('genero != "All"').groupby(['genero'])[['diagnosticos_vih', 'diagnosticos_sida']].sum().reset_index()

# gráfica 4
fig = px.bar(base1, x='genero', y=['diagnosticos_vih', 'diagnosticos_sida'], barmode='group', color_discrete_map={
             'diagnosticos_vih': '#BA68C8', 'diagnosticos_sida': '#9C27B0'}, title='<b>Diagnosticos de VIH y SIDA por genero<b>')

# Agregar detalles a la gráfica
fig.update_layout(
    xaxis_title='Diagnóstico',
    yaxis_title='Diagnosticos',
    template='simple_white',
    title_x=0.5,
    legend_title='<b>Genero<b>')

# Mostrar gráfica utilizando Streamlit
col2.plotly_chart(fig)

# --------GRAFICA 5
# crear dataset
# crear gráfica
fig = px.bar(base3,  x='año', y='valores', color='categoria', barmode='group', color_discrete_map={
             'SIDA': '#BA68C8', 'VIH': '#9C27B0'}, title='<b>Diagnósticos de VIH y SIDA por año<b>')

# agregar detalles a la gráfica
fig.update_layout(
    xaxis_title='Año',
    yaxis_title='Diagnosticos',
    template='seaborn',
    title_x=0.5,
    legend_title='<b>Diagnóstico<b>')

col2.plotly_chart(fig)

col1, col2 = st.columns((1, 2))
# ----------------------------------------------------PREGUNTA 6------------------------------------------------------------
# ¿Como es la distribución en los diagnosticos de SIDA y los de VIH según la raza/etnia?
raza_etnia_sida = df1[df1['raza/etnia'] != 'Other/Unknown'].groupby('raza/etnia')['diagnosticos_sida'].sum()
raza_etnia_vih = df1[df1['raza/etnia'] != 'Other/Unknown'].groupby('raza/etnia')['diagnosticos_vih'].sum()

tabla_datos = pd.DataFrame({
    'raza/etnia': raza_etnia_sida.index,
    'diagnosticos_sida': raza_etnia_sida.values,
    'diagnosticos_vih': raza_etnia_vih.values
})

aids_diagnoses = tabla_datos['diagnosticos_sida'].values
labels = tabla_datos['raza/etnia'].values

# Crear la figura y los ejes
fig = px.pie(tabla_datos, values='diagnosticos_sida', names='raza/etnia', title='Distribución de diagnósticos de SIDA por raza')

# Graficar la torta de "AIDS diagnoses"
fig.update_traces(marker=dict(colors=['#7B1FA2', '#E1BEE7', '#CE93D8', '#AB47BC', '#8E24AA']))

# Mostrar las gráficas en Streamlit
col1.plotly_chart(fig)

hiv_diagnoses = tabla_datos['diagnosticos_vih'].values
labels = tabla_datos['raza/etnia'].values

# Crear la figura y los ejes
fig = px.pie(tabla_datos, values='diagnosticos_vih', names='raza/etnia', title='Distribución de diagnósticos de SIDA por raza')

# Graficar la torta de "AIDS diagnoses"
fig.update_traces(marker=dict(colors=['#7B1FA2', '#E1BEE7', '#CE93D8', '#AB47BC', '#8E24AA']))

# Mostrar las gráficas en Streamlit
col1.plotly_chart(fig)

# --------GRAFICA 6
# Crear dataset
estadisticas = df1.query('edad != "All"').groupby(['edad'])['diagnosticos_vih', 'diagnosticos_sida'].mean().reset_index()

# Crear la figura y ejes para el gráfico de líneas
fig = px.line(estadisticas, x='edad', y=['diagnosticos_vih', 'diagnosticos_sida'], title='Promedio SIDA y VIH por rango de edad')

# Cambiar los colores de las líneas
fig.update_traces(line=dict(color='#BA68C8'), name='VIH')
fig.update_traces(line=dict(color='#9C27B0'), name='SIDA')

# Configurar los ejes y la leyenda
fig.update_xaxes(title='Edad')
fig.update_yaxes(title='Promedio')

# Mostrar el gráfico en Streamlit
col2.plotly_chart(fig)

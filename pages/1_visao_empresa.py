
#importando bibliotecas
import pandas as pd
import plotly.express as px
import numpy as np
from haversine import haversine
import folium
import streamlit as st
from datetime import datetime
from PIL import Image
import folium
from folium import *
from streamlit_folium import folium_static
from utils.clean import Clean
from utils.sidebar import Side_Bar

# Definir cor de fundo
st.set_page_config(page_title='Visão Empresa'
                   ,page_icon="🏢"
                   ,layout="wide")

#=========
# Funções
#=========

def order_metric(df1):
    """
    Calcula e retorna um gráfico de barras mostrando a métrica de pedidos por data.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    plotly.graph_objects.Figure
        Gráfico de barras mostrando a métrica de pedidos por data.

    """
    cols = ['ID','Order_Date']
    df_aux = df1.loc[:,cols].groupby('Order_Date').count().reset_index()

    # Desenhar Grafico
    bar = px.bar(df_aux,'Order_Date','ID')
    return bar

def trafic_order(df1,cols,groupby,graph):
    """
    Cria um gráfico com base nos dados de tráfego de pedidos.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.
    cols : list
        Lista das colunas a serem consideradas no agrupamento.
    groupby : str
        Lista das colunas (ou coluna) a serem usada para agrupar os dados.
    graph : str
        Tipo de gráfico a ser criado ('pie' para pizza, 'scatter' para dispersão).

    Retorna
    -------
    plotly.graph_objects.Figure
        Gráfico de pizza ou de dispersão com base nos dados de tráfego de pedidos.

    """
    df_aux = df1.loc[:,cols].groupby(groupby).count().reset_index()
    df_aux['entregas_perc'] = df_aux['ID'] / df_aux['ID'].sum()
    if graph == 'pie':
        graph =  px.pie(df_aux, values='entregas_perc',names='Road_traffic_density')
    elif graph == 'scater':
        graph = px.scatter(df_aux, x='City', y='Road_traffic_density',size='ID',color='City')
    else:
        None
    return graph

def order_by_week(df1):
    """
    Calcula e retorna um gráfico de linhas mostrando a métrica de pedidos por semana.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    plotly.graph_objects.Figure
        Gráfico de linhas mostrando a métrica de pedidos por semana.

    """
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( '%U')
    df_aux = df1.loc[: ,['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    line1 = px.line(df_aux,'week_of_year','ID')
    return line1

def order_share_by_week(df1):
    """
    Calcula e retorna um gráfico de linhas mostrando a participação de pedidos por semana.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    plotly.graph_objects.Figure
        Gráfico de linhas mostrando a participação de pedidos por semana.

    """
    df_aux01 = df1.loc[ : , ['ID','week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux02 = df1.loc[ :, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()
    df_aux = pd.merge( df_aux01, df_aux02, how='inner')
    df_aux['order_by_deliver'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    line = px.line(df_aux, x='week_of_year', y='order_by_deliver')
    return line

def country_maps(df1):
    """
    Cria e mostra um mapa interativo com marcadores das cidades e densidades de tráfego.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados das cidades e densidades de tráfego.

    """
    df_aux =( df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
            .groupby(['City', 'Road_traffic_density'])
            .median()
            .reset_index()
            )
    df_aux = df_aux.loc[df_aux['City'] != 'NaN', :]
    df_aux = df_aux.loc[df_aux['Road_traffic_density'] != 'NaN', :]

    #Calulando distancias
    min_lat = df_aux['Delivery_location_latitude'].min()
    max_lat = df_aux['Delivery_location_latitude'].max()
    min_lon = df_aux['Delivery_location_longitude'].min()
    max_lon = df_aux['Delivery_location_longitude'].max()
    #passando distancias e zoom para centralizar a região correta
    map = folium.Map(location=[(min_lat + max_lat) / 2, (min_lon + max_lon) / 2],zoom_start=6)
    for index , location_info in df_aux.iterrows():
        folium.Marker(
                    [location_info.loc['Delivery_location_latitude',]
                    ,location_info.loc['Delivery_location_longitude']]
                    ,popup=location_info[['City','Road_traffic_density']]
                    ).add_to(map)

    folium_static(map,width=1024,height=600)

#=========
# Extract 
#=========

df = pd.read_csv('./dataset/train.csv',sep=',')

#============
# Transnform 
#============

clean = Clean()
df1 = clean.clean_code(df)

#=========================
# Barra Lateral Streamlit 
#=========================

st.header('Marketplace - Visão da Empresa')
image_path = './images/Logo.png'
image = Image.open( image_path )
st.sidebar.image(image,width=120)

#Chamando a classe e criando filtros na barra lateral
sidebar = Side_Bar()
date_slider, trafic_option, city_options, wheater_options = sidebar.sidebar(df1)

st.sidebar.markdown('___')
st.sidebar.markdown('## Powered by Thiago Vale')

# Ajustando o formato do date_slider
date_slider = date_slider.strftime('%Y-%m-%d')

# Filtrando o DataFrame
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

linhas_selecionada = df1['Road_traffic_density'].isin(trafic_option)
df1 = df1.loc[linhas_selecionada,:]

linhas_selecionada = df1['City'].isin(city_options)
df1 = df1.loc[linhas_selecionada,:]

linhas_selecionada = df1['Weatherconditions'].isin(wheater_options)
df1 = df1.loc[linhas_selecionada,:]


#==================
# Layout Streamlit 
#==================

tab1,tab2,tab3 = st.tabs(['Visão Gerencial','Visão Tatica','Visão Geografica'])

with tab1:
    #Criando Container dos graficos
    with st.container():
        st.markdown("# Orders by Day")
        bar = order_metric(df1)
        st.plotly_chart(bar, use_container_width=True)
        #Criando container aninhado
        with st.container():
            #Separando o container em colunas
            col1, col2 = st.columns(2)

            with col1:
                st.header('Trafic order share')
                pie = trafic_order(df1,['ID','Road_traffic_density'],'Road_traffic_density','pie')
                st.plotly_chart(pie,use_container_width=True)

            with col2:
                st.header('Trafic order City')
                buble = trafic_order(df1,['ID','City', 'Road_traffic_density'],['City', 'Road_traffic_density'],'scater')
                st.plotly_chart(buble,use_container_width=True)

with tab2:
    with st.container():
        st.markdown("# Order by week")

        line1 = order_by_week(df1)
        st.plotly_chart(line1,use_container_width=True)

    with st.container():    
        st.markdown("# Order Share by Week ")
        line2 = order_share_by_week(df1)
        st.plotly_chart(line2,use_container_width=True)


with tab3:
    st.markdown("# Country Maps")
    country_maps(df1)
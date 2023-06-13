
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
import sys
from utils.clean import Clean
from utils.sidebar import Side_Bar

# Definir cor de fundo
st.set_page_config(page_title='Visão Entregadores'
                   ,page_icon="🚚"
                   ,layout="wide")

#=========
# Funções
#=========
def df_ratings(df1):
    """
    Calcula as médias das avaliações dos entregadores e retorna um DataFrame com os resultados.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    pandas.DataFrame
        DataFrame com as médias das avaliações dos entregadores.

    """
    df_ratings =(
        df1.loc[: , ['Delivery_person_ID','Delivery_person_Ratings']]
                    .groupby('Delivery_person_ID')
                    .mean()
                    .reset_index()
                    )
    return df_ratings

def ratings(df1,columns,groupby,agg,kpis,new_columns):
    """
    Calcula as métricas de avaliação com base nos dados fornecidos e retorna um DataFrame com os resultados.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.
    columns : list
        Lista das colunas a serem consideradas para o cálculo das métricas.
    groupby : str
        Coluna a ser usada para agrupar os dados.
    agg : str or dict
        Função ou dicionário de funções de agregação a serem aplicadas aos dados agrupados.
    kpis : list
        Lista de métricas a serem calculadas.
    new_columns : list
        Lista dos novos nomes das colunas no DataFrame resultante.

    Retorna
    -------
    pandas.DataFrame
        DataFrame com as métricas de avaliação calculadas.

    """
    df_ratings = (
        df1.loc[ : , columns]
                    .groupby(groupby)
                    .agg({agg:kpis})
                    )
    df_ratings.columns = new_columns
    df_ratings = df_ratings.reset_index()
    return df_ratings

def df_top_fast_slow(df1,top_asc):
    """
    Retorna um DataFrame com os 10 principais entregadores mais rápidos ou mais lentos em cada tipo de cidade.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.
    top_asc : bool
        Indicador para classificar os resultados em ordem ascendente (True) ou descendente (False).

    Retorna
    -------
    pandas.DataFrame
        DataFrame com os 10 principais entregadores mais rápidos ou mais lentos em cada tipo de cidade.

    """
    df2 = (
        df1.loc[:, ['Delivery_person_ID','City','Time_taken(min)']]
                    .groupby(['Delivery_person_ID','City'])
                    .min()
                    .sort_values(['City','Time_taken(min)'], ascending=top_asc)
                    .reset_index()
            )

    dfa1 =df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    dfa2 = df2.loc[df2['City'] == 'Urban', :].head(10)
    dfa3 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df = pd.concat([dfa1,dfa2,dfa3]).reset_index(drop=True)
    return df


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

st.header('Marketplace - Visão dos Entregadores')
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

tab1,tab2,tab3 = st.tabs(['Visão Gerencial',' ',' '])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        
        col1,col2,col3,col4 = st.columns(4,gap='large')
        with col1:
            maior_idade =  df1.loc[:,'Delivery_person_Age'].max()
            col1.metric('Maior Idade',maior_idade)

        with col2:
            menor_idade = df1.loc[:,'Delivery_person_Age'].min()
            col2.metric('Menor Idade',menor_idade)

        with col3:
            melhor_condicao = df1.loc[:,'Vehicle_condition'].max()
            col3.metric('Melhor Condição de Veiculos',melhor_condicao)

        with col4:
            pior_condicao = df1.loc[:,'Vehicle_condition'].min()
            col4.metric('Pior Condição de Veiculos',pior_condicao)

    with st.container():
        st.markdown("""---""")
        st.title('Avaliações')

        col1,col2 = st.columns( 2 )

        with col1:
            st.markdown('##### Avaliação Media Por Entregador')
            st.dataframe(df_ratings(df1))

        with col2:
            st.markdown('##### Avaliação Media Por Transito')
            df_ratings = (ratings(df1
                                      ,['Delivery_person_Ratings','Road_traffic_density']
                                      ,'Road_traffic_density'
                                      ,'Delivery_person_Ratings'
                                      ,['mean','std']
                                      ,['delivery_mean','delivery_std'])
                              )
            st.dataframe(df_ratings)

            st.markdown('##### Avaliação Media Por Cilma')
            df_ratings = (ratings(df1
                                  ,['Delivery_person_Ratings','Weatherconditions']
                                  ,'Weatherconditions'
                                  ,'Delivery_person_Ratings'
                                  ,['mean','std']
                                  ,['delivery_mean','delivery_std'])
                          )
            st.dataframe(df_ratings)

    with st.container():
        st.markdown("""---""")
        st.title("Velocidade de Entrega")

        col1,col2 = st.columns( 2 )

        with col1:
            st.markdown('##### Top Entregadores mais rapidos')
            df_top = df_top_fast_slow(df1,True)
            st.dataframe(df_top.head(10))

        with col2:
            st.markdown('##### Top Entregadores mais lentos')

            df_tail = df_top_fast_slow(df1,False)
            st.dataframe(df_tail)
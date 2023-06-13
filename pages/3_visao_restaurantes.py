
#importando bibliotecas
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
st.set_page_config(page_title='Visão Restaurantes'
                   ,page_icon="🍽️"
                   ,layout="wide")

#=========
# Funções
#=========
def tempo_medio(df1):
    """
    Calcula o tempo médio de entrega por cidade e gera um gráfico de barras com a média e o desvio padrão.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    plotly.graph_objects.Figure
        Gráfico de barras com a média e o desvio padrão do tempo de entrega por cidade.

    """
    df_aux = df1.loc[:,['City', 'Time_taken(min)',]].groupby('City').agg({'Time_taken(min)':['mean','std']})

    df_aux.columns = ['avg_time','std_time']
    df_aux['coef_var'] = df_aux['avg_time']/df_aux['std_time']

    df_aux = df_aux.reset_index()

    fig = go.Figure()
    fig.add_trace( go.Bar(
                            name='Control',
                            x=df_aux['City'],
                            y=df_aux['avg_time'],
                            error_y=dict(type='data', array=df_aux['std_time'])))
    fig.update_layout(barmode='group')
    return fig

def tempo_medio_entrega(df1):
    """
    Calcula a média da distância de entrega por cidade e gera um gráfico de pizza.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    plotly.graph_objects.Figure
        Gráfico de pizza com a média da distância de entrega por cidade.

    """
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude','Restaurant_latitude', 'Restaurant_longitude']

    lat1 ='Delivery_location_latitude'
    long1 ='Delivery_location_longitude'
    lat2 ='Restaurant_latitude'
    long2 ='Restaurant_longitude'

    df1['distance'] = df1.loc[:, cols].apply(lambda x: haversine((x[lat1], x[long1]), (x[lat2], x[long2])), axis=1)
    avg_distance = df1.loc[:,['City','distance']].groupby('City').mean().reset_index()
    fig = go.Figure(data=[go.Pie(labels=avg_distance['City'],values=avg_distance['distance'],pull=[0,0.1,0])])
    return fig

def trafego_por_cidade(df1):
    """
    Calcula o tempo médio de entrega e o desvio padrão por cidade e densidade de tráfego,
    e gera um gráfico de sunburst.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    plotly.graph_objects.Figure
        Gráfico de sunburst com o tempo médio de entrega por cidade e densidade de tráfego.

    """
    df_aux = (df1.loc[:,['City', 'Time_taken(min)','Road_traffic_density']]
                .groupby(['City','Road_traffic_density'])
                .agg({'Time_taken(min)':['mean','std']})
            )

    df_aux.columns = ['avg_time','std_time']
    df_aux['coef_var'] = df_aux['avg_time']/df_aux['std_time']
    df_aux = df_aux.reset_index()

    fig = px.sunburst(df_aux,path=['City','Road_traffic_density'],values='avg_time',
                    color='std_time', color_continuous_scale='bluered',
                    color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig

def dist_distancia(df1):
    """
    Calcula a média e o desvio padrão do tempo de entrega por cidade e tipo de pedido,
    retornando um DataFrame com os resultados.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    pandas.DataFrame
        DataFrame com a média e o desvio padrão do tempo de entrega por cidade e tipo de pedido.

    """
    df_aux = (df1.loc[:,['City', 'Time_taken(min)','Type_of_order']]
                .groupby(['City','Type_of_order'])
                .agg({'Time_taken(min)':['mean','std']}))

    df_aux.columns = ['avg_time','std_time']
    df_aux['coef_var'] = df_aux['avg_time']/df_aux['std_time']
    df = df_aux.reset_index()
    return df

def distance(df1):
    """
    Calcula a média da distância de entrega e retorna o valor arredondado.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.

    Retorna
    -------
    float
        Média arredondada da distância de entrega.

    """
    cols = ['Delivery_location_latitude', 'Delivery_location_longitude','Restaurant_latitude', 'Restaurant_longitude']
    df1['distance'] = (
        df1.loc[:, cols]
                        .apply(lambda x: haversine((x['Delivery_location_latitude']
                                                    , x['Delivery_location_longitude'])
                                                    , (x['Restaurant_latitude']
                                                    , x['Restaurant_longitude'])), axis=1))
#calculando a media da coluna e aredondando com numpy
    df = np.round(df1['distance'].mean(),2)
    return df

def avg_std_time_delivery(df1,op,festival,column):
    """
    Calcula a média ou o desvio padrão do tempo de entrega agrupado por evento festival,
    retornando o valor arredondado.

    Parâmetros
    ----------
    df1 : pandas.DataFrame
        DataFrame contendo os dados dos pedidos.
    op : str
        Operação a ser aplicada para calcular a média ou o desvio padrão.
    column : str
        Nome da coluna no DataFrame resultante.

    Retorna
    -------
    float
        Valor arredondado da média ou do desvio padrão do tempo de entrega para eventos festival.

    """
    df_aux = (
        df1.loc[:,['Time_taken(min)','Festival']]
            .groupby('Festival')
            .agg({'Time_taken(min)':op})
            )

    df_aux.columns = [column]
    df_aux = df_aux.reset_index()

    df = np.round(df_aux.loc[df_aux['Festival'] == festival, column],2)
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

st.header('Marketplace - Visão dos Restaurantes')
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
        st.markdown("""---""")
        st.title('Overal Metrics')

        col1,col2,col3,col4,col5,col6 = st.columns(6)

        with col1:
            delivery_unique = len( df1.loc[:, 'Delivery_person_ID'].unique())
            col1.metric('Entregadores Unicos',delivery_unique)

        with col2:
            avg_distance = distance(df1)
            col2.metric('Distancia Média',avg_distance)

        with col3:
            df_mean = avg_std_time_delivery(df1,'mean','Yes','avg_time')
            col3.metric('Média',df_mean)
            
        with col4:
            df_std = avg_std_time_delivery(df1,'std','Yes','std_time')
            col4.metric('Desv Pad',df_std)
        with col5:
            df_mean = avg_std_time_delivery(df1,'mean','No','avg_time')
            col5.metric('Média',df_mean)
        with col6:
            df_std = avg_std_time_delivery(df1,'std','No','std_time')
            col6.metric('Desv Pad',df_mean)
    
    with st.container():
        st.markdown("""---""")
        st.markdown('Tempo Médio c/ Desv Pad')
        fig = tempo_medio(df1)
        st.plotly_chart(fig)
    
    with st.container():
        st.markdown("""---""")
        st.title('Distirbuição do tempo')

        col1,col2 = st.columns(2)
        with col1:

            st.markdown('Tempo Médio de Entrega por Cidade')

            fig = tempo_medio_entrega(df1)
            st.plotly_chart(fig)

        with col2:
            st.markdown('Distribuição de trafego por cidade') 
            fig = trafego_por_cidade(df1)
            st.plotly_chart(fig)
    
    with st.container():
        st.markdown("""---""")
        st.title('Distribuição da Distancia')
        df_aux = dist_distancia(df1)
        st.dataframe(df_aux)
    
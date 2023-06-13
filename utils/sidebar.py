import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class Side_Bar():
    """
    Classe que representa a barra lateral de seleção.

    ...

    Métodos
    -------
    sidebar(df1)
        Cria a barra lateral de seleção e retorna as opções selecionadas.

    """

    def sidebar(self,df1):

        """
        Cria a barra lateral de seleção e retorna as opções selecionadas.

        Parâmetros
        ----------
        df1 : pandas.DataFrame
            DataFrame contendo os dados a serem filtrados.

        Retorna
        -------
        tuple
            Uma tupla contendo as opções selecionadas na barra lateral.

        """
        
        st.sidebar.markdown('# Cury Company')
        st.sidebar.markdown('## Fastest Delivery in Town')
        st.sidebar.markdown('''___''')

        st.sidebar.markdown('## Selecione uma data limite')
        date_slider = st.sidebar.slider(
            'Até qual valor?',
            value=datetime(2022, 4, 13),
            min_value=datetime(2022, 2, 11),
            max_value=datetime(2022, 4, 6),
            format='DD-MM-YYYY'
        )

        st.sidebar.markdown('___')

        trafic_option = st.sidebar.multiselect(
            'Quais as condições de trânsito',
            ['Low', 'Medium', 'High', 'Jam'],
            default=['Low', 'Medium', 'High', 'Jam']
        )

        city_options = st.sidebar.multiselect(
            'Cidades',
        df1['City'].sort_values().unique(),
            default=df1['City'].sort_values().unique()
            )

        wheater_options = st.sidebar.multiselect(
            'Condições Climaticas',
        df1['Weatherconditions'].sort_values().unique(),
            default=df1['Weatherconditions'].sort_values().unique()
            )
        return date_slider,trafic_option,city_options, wheater_options
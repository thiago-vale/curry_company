import pandas as pd
import numpy as np


class Clean():
    """
    Classe responsável por realizar a limpeza de dados de um DataFrame.

    Métodos:
        clean_code(df1): Limpa e transforma os dados do DataFrame fornecido.

    """

    def clean_code(self,df1):
        """
        Limpa e transforma os dados do DataFrame fornecido.

        Parâmetros:
            df1 (pandas.DataFrame): O DataFrame a ser limpo.

        Retorna:
            pandas.DataFrame: O DataFrame limpo e transformado.

        Tipos de Limpeza:
            1. Remoção dos dados NaN
            2. Mudança dos tipos de coluns de dados
            3. Remoção dos espaços das variaveis de texto
            4. Formatação da data
            5. Limpeza da coluna de tempo
        """
        #Removendo dados nulos
        linhas_selcionadas = (df1['Delivery_person_Age'] != 'NaN ')
        df1 = df1.loc[linhas_selcionadas, :].copy()
        linhas_selcionadas = (df1['multiple_deliveries'] != 'NaN ')
        df1 = df1.loc[linhas_selcionadas, :].copy()
        linhas_selcionadas = (df1['Road_traffic_density'] != 'NaN ')
        df1 = df1.loc[linhas_selcionadas, :].copy()
        linhas_selcionadas = (df1['Time_taken(min)'] != 'NaN ')
        df1 = df1.loc[linhas_selcionadas, :].copy()
        linhas_selcionadas = (df1['City'] != 'NaN ')
        df1 = df1.loc[linhas_selcionadas, :].copy()
        linhas_selcionadas = (df1['Festival'] != 'NaN ')
        df1 = df1.loc[linhas_selcionadas, :].copy()

        #Removendo espaços da coluna time taken
        df1.replace("NaN", np.nan, inplace=True)
        df1.dropna(inplace=True)

        #Tratando coluna time taken
        df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split('(min) ')[1])

        #Mudando formato e tipagem dos dados
        df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

        df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

        df1['Order_Date'] = pd.to_datetime( df1['Order_Date'], format='%d-%m-%Y' )

        df1['multiple_deliveries'] = df1['multiple_deliveries'].astype( int )

        df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

        df1 = df1.reset_index(drop=True)

        #Removendo os espaços dentro
        df1.loc[ : , 'ID'] =  df1.loc[ : ,'ID'].str.strip()
        df1.loc[ : , 'Road_traffic_density'] =  df1.loc[ : ,'Road_traffic_density'].str.strip()
        df1.loc[ : , 'Type_of_order'] =  df1.loc[ : ,'Type_of_order'].str.strip()
        df1.loc[ : , 'Type_of_vehicle'] =  df1.loc[ : ,'Type_of_vehicle'].str.strip()
        df1.loc[ : , 'City'] =  df1.loc[ : ,'City'].str.strip()
        df1.loc[ : , 'Festival'] =  df1.loc[ : ,'Festival'].str.strip()
        return df1
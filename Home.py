import streamlit as st
from PIL import Image

st.set_page_config(page_title='Visão Empresa'
                   ,page_icon="🏠"
                   ,layout="wide")

image_path = './images/Logo.png'
image = Image.open(image_path)
st.sidebar.image(image,width=120)

st.sidebar.markdown('# Cury Company')
st.sidebar.markdown('## Fastest Delivery in Town')
st.sidebar.markdown('''___''')

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Grouth Dashboard foi constuido para acompanhar as métricas de crescimento dos Entregadores e Restaurantes
    ### Como Utilizar o Growth Dashboard
    - Visão da Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores seamanais de crescimento.
        - Visão Geográfica: Insights de geolocalização
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento
    - Visão Restaurantes:
        - Indocadores semanais de cresciemnto dos restaurantes
    """)

st.sidebar.markdown('''___''')
st.sidebar.markdown('## Powered by Thiago Vale')
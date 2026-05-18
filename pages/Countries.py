#=================================
# Bibliotecas
#=================================
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd
import streamlit as st
from PIL import Image
import folium
import inflection
from streamlit_folium import st_folium

st.set_page_config(
    page_title ='Countries'
)

#===================================
# Funções
#===================================

#renomeando as colunas

def rename_columns(df):
  title = lambda x: inflection.titleize(x)
  snakecase = lambda x: inflection.underscore(x)
  spaces = lambda x: x.replace(" ", "")
  cols_old = list(df.columns)
  cols_old = list(map(title, cols_old))
  cols_old = list(map(spaces, cols_old))
  cols_new = list(map(snakecase, cols_old))
  df.columns = cols_new

  return df

#===============================================================

#colocando de cores nos códigos de cores

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred"
}

def color_name(color_code):
  return COLORS[color_code]

#===============================================================

#categorizando os lugars por preço

def create_price_type(price_range):
  if price_range == 1:
    return "cheap"
  elif price_range == 2:
    return "normal"
  elif price_range == 3:
    return "expensive"
  else:
    return "gourmet"

#===============================================================

#trocando código dos páises pelo nome

COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
  return COUNTRIES[country_id]

#===============================================================

#FUNÇÕES PARA GRÁFICOS E RESPOSTAS

def num_rest_por_pais(df):    
    df_aux = df.groupby('country_name')['restaurant_id'].nunique().reset_index(name = 'numero_rest_por_pais')
    fig = px.bar(df_aux, x = 'country_name', y = 'numero_rest_por_pais')
    return fig


def qtd_city_por_pais(df):
    df_aux = df.groupby('country_name')['city'].nunique().reset_index(name = 'numero_cidades_por_pais')
    fig = px.bar(df_aux, x = 'country_name', y = 'numero_cidades_por_pais')
    return fig

def media_votos_por_pais(df):
    df_aux = df.groupby('country_name')['votes'] \
               .mean() \
               .reset_index(name = 'media_de_numero_de_votos')
    fig = px.bar(df_aux, x = 'country_name', y = 'media_de_numero_de_votos')
    return fig

def media_preco_para_dois(df):
    df_aux = df.groupby('country_name')['average_cost_for_two'] \
               .mean() \
               .reset_index(name = 'media_cost_for_two')
    fig = px.bar(df_aux, x = 'country_name', y = 'media_cost_for_two')
    return fig

#===================================
# Importando os dados
#===================================

df_raw = pd.read_csv('dataset/zomato.csv')

df = df_raw.copy()

#===================================
# Limpeza dos dados
#===================================

df = rename_columns(df)

df['color_name'] = df['rating_color'].apply(color_name)
df['price_type'] = df['price_range'].apply(create_price_type)
df['country_name'] = df['country_code'].apply(country_name)

#deixa apenas um tipo de especialização de cozinha no restaurante. Alguns restaurantes tinham mais de uma.
#df['cuisines'] = df.loc[:, 'cuisines'].apply(lambda x: x.split(',')[0])
df['cuisines'] = df['cuisines'].apply(lambda x: x.split(',')[0] if pd.notna(x) else x)


csv = df.to_csv(index=False).encode('utf-8')
#====================================================
# Barra Lateral
#====================================================
st.sidebar.markdown('''---''')

#criando o filtro países
st.sidebar.markdown('## Filtros')

paises = sorted(df['country_name'].unique().tolist())
paises_default = df.loc[df['country_name'] == 'Brazil', 'country_name'] \
                    .unique() \
                    .tolist()

country_options = st.sidebar.multiselect(
    'Escolha os país',
    paises,
    default = paises_default    
)

#criando um novo df para que ele seja condicionado ao filtro "Escolha os país"
linhas_selecionadas = df['country_name'].isin(country_options)
df = df.loc[linhas_selecionadas, :]


#====================================================
# Layout no Steamlit
#====================================================

with st.container():
    st.markdown('# Visão Países')
    
with st.container():
    st.markdown('#### Quantidade de Restaurantes Registrados por País')
    fig = num_rest_por_pais(df)
    st.plotly_chart(fig, use_container_width = True) 

with st.container():
    st.markdown('#### Quantidade de Cidades Registrados por País')
    fig = qtd_city_por_pais(df)
    st.plotly_chart(fig, use_container_width = True)

with st.container():
    #criando 2 colunas lado a lado
    col1, col2 = st.columns(2)

    #gráfico de barras com os países
    with col1:
        st.markdown('###### Média de avaliações feitas por país')
        fig = media_votos_por_pais(df)
        st.plotly_chart(fig, use_container_width = True)
        

    with col2:
        st.markdown('###### Média de preço de um prato para duas pessoas por país')
        fig = media_preco_para_dois(df)
        st.plotly_chart(fig, use_container_width = True)
    



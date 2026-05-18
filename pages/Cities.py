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

def top_10_cidades_mais_rest(df):
    df_aux = df.groupby(['country_name', 'city'])['restaurant_id'] \
               .nunique() \
               .sort_values(ascending=False) \
               .reset_index(name='qtd_rest_por_city') \
               .head(10)
    fig = px.bar(df_aux, x = 'city', y = 'qtd_rest_por_city', color = 'country_name')
    return fig

def top_7_nota_media_4_mais(df):
    df_aux = df.loc[df['aggregate_rating'] > 4, :] \
               .groupby(['country_name', 'city'])['restaurant_id'] \
               .nunique() \
               .sort_values(ascending = False) \
               .reset_index(name = 'n_de_rest_nota_acima_4') \
               .head(7)
    fig = px.bar(df_aux, x = 'city', y = 'n_de_rest_nota_acima_4', color = 'country_name')
    return fig

def top_7_nota_media_2_ponto_5_menos(df):
    df_aux = df.loc[df['aggregate_rating'] < 2.5, :] \
               .groupby(['country_name', 'city'])['restaurant_id'] \
               .nunique() \
               .sort_values(ascending = False) \
               .reset_index(name = 'n_de_rest_nota_abaixo_2.5') \
               .head(7)
    fig = px.bar(df_aux, x = 'city', y = 'n_de_rest_nota_abaixo_2.5', color = 'country_name')
    return fig

def top_10_qtd_cozinhas_distintas(df):
    df_aux = df.groupby(['country_name', 'city'])['cuisines'] \
               .nunique() \
               .sort_values(ascending = False) \
               .reset_index() \
               .head(10)
    fig = px.bar(df_aux, x = 'city', y = 'cuisines', color = 'country_name')
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
st.dataframe(df)

#====================================================
# Layout no Steamlit
#====================================================

with st.container():
    st.markdown('# Visão Cidades')

with st.container():
    st.markdown('#### Top 10 cidades com mais restaurantes na base de daddos')
    fig = top_10_cidades_mais_rest(df)
    st.plotly_chart(fig, use_container_width = True) 
    
    
with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('#### Top 7 cidades restaurantes com média de avaliação acima de 4')
        fig = top_7_nota_media_4_mais(df)
        st.plotly_chart(fig, use_container_width = True)
    
    with col2:
        st.markdown('#### Top 7 cidades restaurantes com média de avaliação abaixo de 2.5')
        fig = top_7_nota_media_2_ponto_5_menos(df)
        st.plotly_chart(fig, use_container_width = True)
        
with st.container():
    st.markdown('#### Top 10 cidades com mais restaurantes com tipos de culinária distintos')
    fig = top_10_qtd_cozinhas_distintas(df)
    st.plotly_chart(fig, use_container_width = True)

  
        

   
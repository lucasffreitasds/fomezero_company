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

def melhores_rest_italianos(df2):
    df_aux = df2.loc[df2['cuisines'] == 'Italian', ['restaurant_id', 'restaurant_name', 'aggregate_rating']] \
               .sort_values(by = ['aggregate_rating', 'restaurant_id'], ascending = [False, True]) \
               .reset_index() \
               .head(5)
    return df_aux

def top_restaurantes(df, quantidade):
    df_aux = df.loc[:, ['restaurant_id', 'restaurant_name', 'aggregate_rating']] \
               .sort_values(by=['aggregate_rating', 'restaurant_id'], ascending=[False, True]) \
               .drop_duplicates(subset='restaurant_id') \
               .reset_index(drop=True) \
               .head(quantidade)
    return df_aux

def top_melhores_cozinhas(df, quantidade):
    df_aux = df.groupby('cuisines')['aggregate_rating'] \
               .mean() \
               .reset_index(name='media_nota') \
               .sort_values(by='media_nota', ascending=False) \
               .head(quantidade)
    fig = px.bar(df_aux, x='cuisines', y='media_nota')
    return fig


def top_piores_cozinhas(df, quantidade):
    df_aux = df.groupby('cuisines')['aggregate_rating'] \
               .mean() \
               .reset_index(name='media_nota') \
               .sort_values(by='media_nota', ascending=True) \
               .head(quantidade)
    fig = px.bar(df_aux, x='cuisines', y='media_nota')
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

df2 = df.copy()
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

#criando filtro tipo de culinária
cozinhas = sorted(df['cuisines'].dropna().unique().tolist())
cozinhas_default = df.loc[df['cuisines'] == 'Pizza', 'cuisines'].unique().tolist()

cozinha_options = st.sidebar.multiselect(
    'Escolha o tipo de culinária',
    cozinhas,
    default = cozinhas_default
)

#criando o filtro de quantidade de restaurantes desejo visualizar
quantidade = st.sidebar.slider(
    'Selecione a quantidade de restaurantes que deseja visualizar',
    min_value=1,
    max_value=20,
    value=9,
    step=1
)

#criando um novo df para que ele seja condicionado ao filtro "Escolha os país e tipo de culinárias"
linhas_selecionadas = (df['country_name'].isin(country_options)) & (df['cuisines'].isin(cozinha_options))
df = df.loc[linhas_selecionadas, :]


#====================================================
# Layout no Steamlit
#====================================================

with st.container():
    st.markdown('# Visão Tipos de Cozinhas')

with st.container():
    st.markdown(f'### Melhores Restaurantes Italianos - Top 5')

    cols = st.columns(5)
    top5 = melhores_rest_italianos(df2)

    for i in range(len(top5)):
        linha = top5.iloc[i]
        with cols[i]:
            st.metric(linha['restaurant_name'], f"{linha['aggregate_rating']}/5.0")

with st.container():
    st.markdown(f'### Top {quantidade} Restaurantes')
    df1 = top_restaurantes(df, quantidade)
    st.dataframe(df1)
        
with st.container():

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f'#### Top {quantidade} melhores tipos de culinária')
        fig1 = top_melhores_cozinhas(df, quantidade)
        st.plotly_chart(fig1, use_container_width = True, key='grafico_melhores')

    with col2:
        st.markdown(f'#### Top {quantidade} piores tipos de culinária')
        fig2 = top_piores_cozinhas(df, quantidade)
        st.plotly_chart(fig2, use_container_width = True, key='grafico_piores')












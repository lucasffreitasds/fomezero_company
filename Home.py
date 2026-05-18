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
    page_title ='Main Page'
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

st.sidebar.markdown('# Fome Zero')
image = Image.open('imagem_fome_zero.jpg')
st.sidebar.image(image, width = 120)



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

#criando botão de download do dado tratado:
st.sidebar.markdown('## Dados Tratados')


st.sidebar.download_button(
    label = 'Download dados tratados .csv',
    data = csv,
    file_name = 'zomato_tratado.csv',
    mime = 'text/csv'
)

#====================================================
# Layout no Steamlit
#====================================================

with st.container():
    st.markdown('# Fome Zero!')
    st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')

with st.container():
    st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:')

    #criando 2 colunas lado a lado
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown('###### Restaurantes Cadastrados')
        rest_cad = df.loc[:, 'restaurant_id'].nunique()
        col1.metric('-', rest_cad)
        
    with col2:
        st.markdown('###### Países Cadastrados')
        pais_cad = df.loc[:, 'country_name'].nunique()
        col2.metric('-', pais_cad)

    with col3:
        st.markdown('###### Cidades Cadastradas')
        cid_cad = df.loc[:, 'city'].nunique()
        col3.metric('-', cid_cad)

    with col4:
        st.markdown('###### Avaliações Feitas na Plataforma')
        num_avl = df.loc[:, 'votes'].sum()
        col4.metric('-', num_avl)

    with col5:
        st.markdown('###### Tipos de Culinárias Oferecidas')
        cul_ofer = df.loc[:, 'cuisines'].nunique()
        col5.metric('-', cul_ofer)
            
with st.container():
    

    #centralizando o mapa
    centro_lat = df['latitude'].mean()
    centro_lon = df['longitude'].mean()
    
    #criando o mapa
    mapa = folium.Map(location = [centro_lat, centro_lon], zoom_start = 6)

    #adicionando os marcadores
    for _, linha in df.iterrows():
        folium.Marker(
            location = [linha['latitude'], linha['longitude']],
            popup = linha[['restaurant_name', 'cuisines']],
            tooltip = linha['restaurant_name'],
            icon = folium.Icon(icon = 'home', prefix = 'fa', color = 'red')
        ).add_to(mapa)

    #exibindo o mapa
    st_folium(mapa, width = 1000, height = 600)
    




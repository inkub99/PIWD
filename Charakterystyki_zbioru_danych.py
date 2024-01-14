import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme()
sns.set_theme(style="white")
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from streamlit_extras.app_logo import add_logo
import squarify
import os
st.set_option('deprecation.showPyplotGlobalUse', False)


add_logo("./na_paluchu.png", height=300)

page_bg_img = """
<style>
[data-testid="stSidebar"]{
    background-color: #5d2c80;
    
}
</style>
"""

with st.sidebar:
    st.markdown(page_bg_img, unsafe_allow_html=True)

df = pd.read_excel('schro_aplikacja.xlsx')

col1a, col2a = st.sidebar.columns([2,2])

with col1a:
    st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)
    st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)
    st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)
    typ = st.radio("", ["Wszystkie", "Psy", "Koty"])
    waga = st.slider('Waga', 1, 65, [1, 65])

rasowe = False

with col2a:
    wiek = st.slider('Wiek (lata)', 1, 20, [1, 20])
    samce = st.checkbox("Samce", value=True)
    samice = st.checkbox("Samice", value=True)
    if typ == 'Psy':
        rasowe = st.checkbox("Tylko rasowe", value=False)
    

col1, col2, col3 = st.columns([5.0, 0.1, 1.7])

with col1:
    st.markdown("<h2 style='margin-top: -75px; text-align: left;'>Charakterystyki zbioru danych</h2>", unsafe_allow_html=True)

with col3:
    wyk_typ = st.radio("", ['Rozkłady', 'Analiza w czasie'], horizontal=True, index=0)
    st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)

st.write("Dane potrzebne do przygotowania niniejszej wizualizacji zostały zescrapowane ze strony warszawskiego schroniska (https://napaluchu.waw.pl/zwierzeta/znalazly-dom/. Autor ograniczył zbiór danych do zwierząt, które trafiły do schroniska w latach 2015-2022.\n")
st.write("Zapraszam do ekspolarcji!")



df_cel = df.copy()

df_cel = df_cel[df_cel['Wiek'].between(wiek[0], wiek[1])]
df_cel = df_cel[df_cel['Waga'].between(waga[0], waga[1])]

if samce == False and samice == False:
    samce = True
    samice = True

elif samce == True and samice == False:
    df_cel = df_cel[df_cel['Płeć']=='samiec']

elif samce == False and samice == True:
    df_cel = df_cel[df_cel['Płeć']=='samica']

if typ == 'Psy':
    df_cel = df_cel[df_cel['typ']=='pies']

elif typ == 'Koty':
    df_cel = df_cel[df_cel['typ']=='kot']

if rasowe == True:
    df_cel = df_cel[df_cel['rasowy']==1]

if  wyk_typ == 'Analiza w czasie':
    col1b, col2b, col3b = st.columns([0.5,3,0.5])
    wiz = df.groupby('rok')['id'].count().reset_index()
    wiz['Grupa'] = 'Wszystkie zwierzęta'
    wiz_2 = df_cel.groupby('rok')['id'].count().reset_index()
    wiz_2['Grupa'] = 'Wybrana grupa'
    wiz = pd.concat([wiz, wiz_2])
    wiz.columns = ['rok', 'id', 'Grupa']
    plt.figure(figsize=(10, 6))
    sns.relplot(data=wiz, x='rok', y='id', palette='Purples', hue='Grupa', kind='line', style='Grupa', markers=True)
    plt.ylabel('Liczba przypadków')  
    plt.title('Liczba przypadków dla badanych lat')
    plt.ylim(0, 2600)
    with col2b:
        st.pyplot()

else:
    df['Grupa'] = 'Wszystkie zwierzęta'
    df_cel['Grupa'] = 'Wybrana grupa'
    wiz = pd.concat([df, df_cel])
    col1b, col2b = st.columns([1,1])
    
    colors = sns.color_palette("Purples", n_colors=3)

    try:
        n_1 = len(df_cel[df_cel['typ']=='kot'])
    except:
        n_1 = 0 

    try:
        n_2 = len(df_cel[(df_cel['typ']=='pies') & (df_cel['rasowy']==1)])
    except:
        n_2 = 0 

    try:
        n_3 = len(df_cel[(df_cel['typ']=='pies') & (df_cel['rasowy']==0)])
    except:
        n_3 = 0 

    df2 = pd.DataFrame({'N':[n_1, n_2, n_3], 'group':["Koty","Psy rasowe", "Psy nierasowe"] })
    squarify.plot(sizes=df2['N'], label=df2['group'], alpha=.8, color=colors)
    plt.title('Struktura badanego zbioru (wybrana grupa)')  
    with col1b:
        st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)
        st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)
        st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)
        st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)
        st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)
        st.pyplot()


    plt.figure(figsize=(10, 6))
    sns.kdeplot(data=wiz, x='Wiek', palette='Purples', fill=True, hue='Grupa', common_norm=True)
    plt.title('Wiek')     
    plt.xlabel('Wiek')
    plt.ylabel('-')
    plt.xlim(1, 20)
    with col2b:
        st.pyplot()
    sns.kdeplot(data=wiz, x='Waga', palette='Purples', fill=True, hue='Grupa', common_norm=True)
    plt.title('Waga')     
    plt.xlabel('Waga')
    plt.ylabel('-')
    with col2b:
        st.pyplot()    



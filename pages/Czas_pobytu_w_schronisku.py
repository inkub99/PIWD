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

st.set_option('deprecation.showPyplotGlobalUse', False)

add_logo("./na_paluchu.png", height=250)

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
    st.markdown("<h1 style='margin-top: -95px; text-align: left;'>Czas pobytu w schronisku</h1>", unsafe_allow_html=True)

with col3:
    wyk_typ = st.radio("", ['Rozkład', 'Analiza w czasie'], horizontal=True, index=0)
    st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)


df_cel = df.copy()

df_cel = df_cel[df_cel['Wiek']>=wiek[0]]
df_cel = df_cel[df_cel['Wiek']<=wiek[1]]
df_cel = df_cel[df_cel['Waga']>=waga[0]]
df_cel = df_cel[df_cel['Waga']<=waga[1]]

if samce == False and samice == False:
    samce = True
    samice = True

if samce == True and samice == False:
    df_cel = df_cel[df_cel['Płeć']=='samiec']

if samce == False and samice == True:
    df_cel = df_cel[df_cel['Płeć']=='samica']

if typ == 'Psy':
    df_cel = df_cel[df_cel['typ']=='pies']

if typ == 'Koty':
    df_cel = df_cel[df_cel['typ']=='kot']

if rasowe == True:
    df_cel = df_cel[df_cel['rasowy']==1]

if  wyk_typ == 'Analiza w czasie':
    wiz = df.groupby('rok')['l_dni'].median().reset_index()
    wiz['Grupa'] = 'Wszystkie zwierzęta'
    wiz_2 = df_cel.groupby('rok')['l_dni'].median().reset_index()
    wiz_2['Grupa'] = 'Wybrana grupa'
    wiz = pd.concat([wiz, wiz_2])
    wiz.columns = ['rok', 'Liczba dni', 'Grupa']

    plt.figure(figsize=(10, 6))
    sns.catplot(data=wiz, x='Liczba dni', y='rok', kind='bar', palette='Purples', orient='h', hue='Grupa')
    plt.title('Medianowy czas pobytu w schronisku (liczba dni)')
    st.pyplot()

else:
    col1b, col2b, col3b = st.columns([1.1,8,1.1])
    df['Grupa'] = 'Wszystkie zwierzęta'
    df_cel['Grupa'] = 'Wybrana grupa'
    df_cal = pd.concat([df,df_cel])
    plt.figure(figsize=(10, 6))  
    sns.catplot(data=df_cal, x='Grupa', y='l_dni', kind='box', palette='Purples', showfliers = False)
    plt.title('Rozkład czasu pobytu w schronisku (liczba dni)')
    plt.ylabel('Liczba dni')  
    with col2b:
        st.pyplot()





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

col1, col2, col3 = st.columns([4.0, 0.1, 1.7])

with col1:
    st.markdown("<h1 style='margin-top: -95px; text-align: left;'>P-stwo adopcji w czasie</h1>", unsafe_allow_html=True)

with col3:
    wyk_typ = st.radio("", ['Skumulowane p-stwa', 'Analiza w czasie'], horizontal=True, index=0)
    st.markdown("<style>div.row-widget.stRadio > div{margin-top: -95px;}</style>", unsafe_allow_html=True)


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
    wiz = pd.DataFrame()
    for rok in range(2015, 2023):
        for t in range(1,13):
            n_1 = len(df_cel[(df_cel['rok']==rok) & (df_cel['l_dni']>t*30) & (df_cel['l_dni']<t*30+30+1)])
            n_2 = len(df_cel[(df_cel['rok']==rok) & (df_cel['l_dni']>t*30)])
            try:
                wiz.loc[rok,t] = n_1/n_2 * 100
            except:
                wiz.loc[rok,t] = 100


    plt.figure(figsize=(10, 6))  
    sns.heatmap(wiz, annot=True, fmt='.0f', cmap='Purples', cbar_kws={'label': 'Procent'})
    plt.title('P-stwo adopcji (%) w okreśonym miesiącu')
    st.pyplot()



else:
    wiz = pd.DataFrame()
    wiz_2 = pd.DataFrame()

    for t in range(6,366):
        wiz.loc[t,'p-stwo']  = len(df[(df['l_dni']<=t)]) / len(df) * 100 
        wiz_2.loc[t,'p-stwo'] = len(df_cel[(df_cel['l_dni']<=t)]) / len(df_cel) * 100
    
    wiz['Grupa'] = 'Wszystkie zwierzęta'
    wiz_2['Grupa'] = 'Wybrana grupa'
    wiz = pd.concat([wiz, wiz_2])


    plt.figure(figsize=(10, 6))  
    sns.lineplot(data=wiz, x=wiz.index, y='p-stwo', hue='Grupa', drawstyle='steps-post', palette='Purples')
    plt.title('Skumulowane p-stwo adopcji (%) w czasie')
    plt.xlabel('Liczba dni')
    plt.ylabel('P-stwo')  

    st.pyplot()





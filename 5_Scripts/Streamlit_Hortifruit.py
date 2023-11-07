# importando as libraries

import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Nome da aplicação
st.write(
    """
    **MDC HORTIFRUIT**\n
    VENDAS DE FRUTAS
    
    """
)

# Criando uma side bar

st.sidebar.header('Escolha uma variável') # cabeçalho do sidebar


# Lendo arquivo de ações

def get_data():
    path = '../2_Bases_Tratadas/MDCHORTFRUIT.csv'
    return pd.read_csv(path, sep=';')

df = get_data()


# criando o tipo de variavel para o usuario escolher
tipo = ['categoricas', 'numericas', 'todas']
# criando o tipo de analise para o usuario escolher
tipo2 = ['univariado', 'bivariado']
# coletando as variáveis da minha base
variaveis = list(df.columns)
# conforme a escolha do usuario, ela vai ser atribuida ao objeto escolha do tipo
escolha_do_tipo = st.sidebar.selectbox("Escolha o tipo de variavel", tipo)

if escolha_do_tipo == 'categoricas':
    # a unica opcao de analise vai ser o univariado
    escolha_do_tipo2 = st.sidebar.selectbox("Escolha o tipo de variavel", ['univariado'])
    # a minha escolha vai ser a unica variavel categorica da base
    escolha = ['sexo']
    escolha_da_variavel = st.sidebar.selectbox("Escolha o indicador", escolha)
    
    #criando uma segunda coluna de sexo, igual o arquivo de analise exploratoria
    df2 = df.copy()
    df2['sexo2']='m'
    df2.loc[df2.sexo==0, 'sexo2']='f'
    # aqui, estamos criando um agrupamento para conseguir fazer o gráfico de pizza e barra a seguir
    dfaux = df2.groupby('sexo2')['sexo'].count().reset_index(drop=False)

    #criando o grfico de pizza para aparecer no streamlit
    figcateg = px.pie(dfaux, values='sexo', names='sexo2')
    st.plotly_chart(figcateg)

# se a escolha for numerica
elif escolha_do_tipo == 'numericas':
    # as opcoes de escolha serao univariada ou bivariada
    escolha_do_tipo2 = st.sidebar.selectbox("Escolha o tipo de variavel",tipo2)
    # se o usuario escolher univariado
    
    if escolha_do_tipo2=='univariado':
        # separando as variaveis numericas da base
        df2 = df[['renda', 'compras', 'idade']].copy()
        # jogando o nome das colunas numa lista
        escolha = list(df2.columns)
        # a escolha do usuario vai ser atribuida ao objeto escolha_da_variavel
        escolha_da_variavel = st.sidebar.selectbox("Escolha o indicador", escolha)
        # fazendo um histograma como univariado
        figuni = px.histogram(df, escolha_da_variavel,color = df.sexo)
        # plotando o grafico no streamlit
        st.plotly_chart(figuni)
    # se a escolha nao for univariada, vai ser bivariada
    
    else:
        df2 = df[['renda', 'compras', 'idade']].copy()
        escolha = list(df2.columns)
        
        #por ser bivariada, aqui estou dizendo quem fica no eixo x e quem fica no eixo y
        escolha_da_variavel1 = st.sidebar.selectbox("Escolha a variavel do eixo X", escolha)
        escolha_da_variavel2 = st.sidebar.selectbox("Escolha a variavel do eixo Y", escolha)
        
        # vou possibilitar do usuario escolher uma variavel para colocar na cor
        adicao_de_cor = st.sidebar.selectbox("Voce quer adicionar cor?", ['sim', 'nao'])

        # se ele quiser adicionar cor, vamos...
        if adicao_de_cor=='sim':
            # colocar as colunas numa lista
            variavel_da_cor = list(df.columns)
            # a escolha da lista ficará no objeto escolha_variavel_cor
            escolha_variavel_cor = st.sidebar.selectbox("Voce quer adicionar cor?", variavel_da_cor)
            #vamos plotar o grafico figbiv com os argumentos (base, eixo x, eixo y e a cor) tudo conforme a escolha do usuario
            figbiv = px.scatter(df, x=escolha_da_variavel1, y = escolha_da_variavel2, color=escolha_variavel_cor)
            st.plotly_chart(figbiv)
        else:
            # se ele nao quiser cor, vamos apenas comparar as variaveis x e y 
            figbiv = px.scatter(df, x=escolha_da_variavel1, y = escolha_da_variavel2)
            st.plotly_chart(figbiv)
else:
    # exemplo de como plotar o seaborn caso o usuario escolha todas!
    figtodas = sns.pairplot(df)
    st.pyplot(figtodas)


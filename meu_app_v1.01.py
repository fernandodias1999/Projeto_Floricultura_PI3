###########################################
#  Site de Floricultura Rosas & Espinhos
#  RA: 2102144  Fernando Dias
#  RA: 2009640  Felipe Sousa Chagas
#  PJI 310 - Turma 004 Grupo 005
#  Ultima atualização 14/04/2024 as 17:15 hs
#  #########################################

# import tkinter

import requests

import streamlit as st

import pandas as pd

from pandas import read_csv

import sqlite3

#  from tkinter import *  # não suportado pelo site

# ####################
# variaveis utilizadas
# ####################
janela = ""
tabela = ""
cliente = ""
banco = ""
erro = ""
# ####################

# ##############################################################################################
# Rotina não suportada pelo servidor da internet - desabilitado em 14/04/2024
#
# def janela_cadastro():
#    janela = Tk()
#    janela.title("Cadastro de Produtos")
#    label_descricao = Label(janela, text='Cadastro de Produtos')
#    label_descricao.grid(column=0, row=1)
#
#    botao_Cadastrar = Button(janela, text="Cadastrar") # command = True
#    botao_Cadastrar.grid(column=0, row=3)
#    botao_cancelar = Button(janela, text="Cancelar", command=janela.destroy)  # Destroi a janela
#    botao_cancelar.grid(column=0, row=5)
#
#    janela.mainloop()
#    return
# ##############################################################################################


# ##############################################################################################
# ##############################################################################################
# funcao pega_cotacoes está ok nao alterar
def pega_cotacoes():  #  Capturando as cotações de dolar euro e btc por uma api
    requisicao = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")
    requisicao_dic = requisicao.json()
    cotacao_dolar = requisicao_dic["USDBRL"]["bid"]
    cotacao_euro = requisicao_dic["EURBRL"]["bid"]
    cotacao_btc = requisicao_dic["BTCBRL"]["bid"]
    with st.container(border=True, height=150):
        st.write("Cotação Dolar R$", float(cotacao_dolar))
        st.write("Cotação Euro  R$", float(cotacao_euro))
        st.write("Cotação Btc   R$", float(cotacao_btc))
    return


# ########################################################################################
# ########################################################################################
# só p/ uso do programador e criacao do Banco de Dados
def conexao_db(): #  função para criação do Banco de Dados e tabelas, consultas, insercoes
    try:
        db = sqlite3.connect("floricultura.db")
        cursor = db.cursor()
        #  cursor.execute("CREATE TABLE dbclientes (nome text, email text)")
        #  cursor.execute("INSERT INTO dbclientes VALUES ('FERNANDO','fernando@gmail.com')")
        #  Exemplo com variaveis
        #  nome = "JULIANA"
        #  idade = 30
        #  email = "juliana@gmail.com"
        #  cursor.execute("INSERT INTO dbclientes VALUES ('"+nome+"',"+str(idade)+",'"+email+"')")
        #  cursor.execute("DELETE FROM dbcliente WHERE nome = 'nome da pessoa'")
        #  cursor.execute('UPDATE dbclientes SET nome = "Fabio" WHERE idade = 28')
        #  db.commit()  # Gravando no Banco de Dados
        #  db.close()   # Fechando o Banco de Dados
        st.write("Sucesso na operação no Banco de Dados !!!")
    except sqlite3.Error as erro:
        st.write("Erro ao manipular o Banco de Dados: ", erro )

    return


# ############################################################
# funcao inicial de configuracao da pagina está ok nao alterar
st.set_page_config(page_title="Floricultura Rosas & Espinhos",
        page_icon="🧊", layout="wide")
# ############################################################


# #############################################################
# funcao criacao do sidebar está ok nao alterar
with st.sidebar:
    # "Floricultura Rosas & Espinhos."   # Nome acima da imagem
    opcoes = st.sidebar.selectbox(
    "Escolha uma opção",
    ("        ", "Clientes", "Cotações Moedas", "Cadastrar Produtos", "Relatórios"),  # Menu de opções
    )


    if opcoes == "Cotações Moedas":
        pega_cotacoes()  # pega a cotação das moedas dolar, euro e bitcoin e exib


    if opcoes == "Clientes":
        db = sqlite3.connect("floricultura.db")     # conectando ao banco de dados
        cursor = db.cursor()
        cursor.execute("SELECT * FROM dbclientes")  # consultando o banco de dados
        with st.container(border=True, height=200):
            st.write(cursor.fetchall())             # apresenta os clientes na tela
            db.close()


    if opcoes == "Cadastrar Produtos":
        st.write("Em programação -> aguarde")
        # Cadastro dos Produtos da Floricultura


    if opcoes == "Relatórios":
        st.write("Em programação -> aguarde")


    st.image("flower.png", width=270)  # Imagem da Flor

# ########################################################################################
# nome da empresa e linha colorida rainbow - está ok não alterar
with st.container(border=True, height=170):
    st.subheader("Floricultura Rosas & Espinhos - 30 anos no mercado.", divider="rainbow")
    st.title("Tabela das Ultimas Vendas")

@st.cache_data  # não mexer
def carregar_vendas():
    tabela = pd.read_csv("resultados.csv")  # carrega a tabela resultados da vendas p/ dias
    return tabela

@st.cache_data  # não mexer
def carregar_produtos():
    produto  = read_csv("produtos.csv")
    return produto

# ##############################################################################
# relatorio de apresentacao de vendas está ok - não alterar
with st.container(border=True, height=420):
    qtde_dias = st.selectbox("Selecione o período de pesquisa", ["7D", "15D", "21D", "30D"])
    num_dias = int(qtde_dias.replace("D", ""))
    dados = carregar_vendas()
    dados = dados[-num_dias:]
    # apresenta na tela ass ultimas vendas
    st.area_chart(dados, x="Data", y="Vendas", width=180, height=300)


# ###############################################################
# Tabela de Produtos da floricultura está ok - não alterar
with st.container(border=True, height=400):  # Tabela de Produtos
    st.title("Produtos da Floricultura")
    pro = carregar_produtos()
    st.dataframe(pro)  # Tabela de Produtos


#  with st.container(border=True, height=400):  # Calendario
#      date = st.date_input("Escolha um dia", format="DD/MM/YYYY", label_visibility="visible")


# #############################################################
# Rodapé da página com informações importantes - não alterar
with st.container(border=True, height=200):  # Rodapé da Pagina
    st.write("Patrocinio [Clique aqui] (https://www.hashtagtreinamentos.com/curso-python)")
    st.write("Copyright(C) 2024 - Direitos Reservados - Versão 1.02")
    with st.container(border=True, height=100):  # Rodapé da Pagina (2)
        st.write("Desenvolvido pela Turma 004 Grupo 005")
        st.write("Linguagem utilizada Python 3.12.2 + Streamlit + Pandas")


# Fim deste Módulo
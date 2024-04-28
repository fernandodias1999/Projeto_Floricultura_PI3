###########################################
#  Site de Floricultura Rosas & Espinhos
#  RA: 2102144  Fernando Dias
#  RA: 2009640  Felipe Sousa Chagas
#  PJI 310 - Turma 004 Grupo 005
#  Ultima atualização 15/04/2024 as 21:30 hs
#  #########################################

import requests

import streamlit as st

import pandas as pd

from pandas import read_csv

import sqlite3

# ####################
# variaveis utilizadas
# ####################
janela = ""
tabela = ""
cliente = ""
banco = ""
erro = ""
# ####################

@st.cache_data  # não mexer
def carregar_vendas():
    tabela = pd.read_csv("resultados.csv")  # carrega a tabela resultados da vendas p/ dias
    return tabela

@st.cache_data  # não mexer
def carregar_produtos():
    produto  = read_csv("produtos.csv")
    return produto

# ##############################################################################################
# relatorio de apresentacao de vendas está ok - não alterar
# ##############################################################################################
def apresenta_vendas():
    with st.container(border=True, height=420):
        qtde_dias = st.selectbox("Selecione o período de pesquisa", ["7D", "15D", "21D", "30D"])
        num_dias = int(qtde_dias.replace("D", ""))
        dados = carregar_vendas()
        dados = dados[-num_dias:]
        # apresenta na tela ass ultimas vendas
        st.area_chart(dados, x="Data", y="Vendas", width=180, height=300)

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


# ############################################################
# funcao inicial de configuracao da pagina está ok nao alterar
st.set_page_config(page_title="Floricultura Rosas & Espinhos",
        page_icon="🧊", layout="wide")
# #########################################################################################
# funcao sidebar está ok nao alterar
with st.sidebar:
    opcoes = st.sidebar.selectbox(
    "Menu Principal",
    ("Relatório de Vendas", "Lista de Clientes", "Cotações de Moedas",
     "Lista de Produtos", "Incluir Clientes", "Incluir Produtos"),  # Menu de opções
    )

    st.image("flower.png", width=270)  # Imagem da Flor

# Fim do SideBar ###########################################################################

# #######################################################################################
# Bloco Principal - Bloco Principal - Bloco Principal - Bloco Principal - Bloco Principal
# nome da empresa e linha colorida rainbow - está ok não alterar
with st.container(border=True, height=600):
    st.subheader("Floricultura Rosas & Espinhos - 30 anos no mercado.", divider="rainbow")


    if opcoes == "Relatório de Vendas":
        st.title("Tabela das Ultimas Vendas")
        with st.container(border=True, height=420):
            qtde_dias = st.selectbox("Selecione o período de pesquisa", ["7D", "15D", "21D", "30D"])
            num_dias = int(qtde_dias.replace("D", ""))
            dados = carregar_vendas()
            dados = dados[-num_dias:]
            # apresenta na tela ass ultimas vendas
            st.area_chart(dados, x="Data", y="Vendas", width=180, height=300)


    if opcoes == "Lista de Produtos":
        # Tabela de Produtos da floricultura está ok - não alterar
        with st.container(border=True, height=400):  # Tabela de Produtos
            st.title("Produtos da Floricultura")
            pro = carregar_produtos()
            st.dataframe(pro)  # Tabela de Produtos


    if opcoes == "Cotações de Moedas":
        pega_cotacoes()  # pega a cotação das moedas dolar, euro e bitcoin e exib


    if opcoes == "Lista de Clientes":
        st.subheader("Listagem de Clientes")
        db = sqlite3.connect("floricultura.db")     # conectando ao banco de dados
        cursor = db.cursor()
        cursor.execute("SELECT * FROM dbclientes")  # consultando o banco de dados
        with st.container(border=True, height=300):
            st.table(cursor)
            db.close()


    if opcoes == "Incluir Clientes":  # Formulario para incluir Clientes no Sistema
        st.subheader("Cadastro de Clientes")
        with st.form(key="include_clientes"):
            name = st.text_input(label="Insira seu nome", max_chars=30)
            email = st.text_input(label="Insira seu e-mail", max_chars=60)
            button_submit = st.form_submit_button("Cadastrar")

        if button_submit:
            name = name.upper()     # nome em maisculo
            email = email.lower()   # email em minusculo
            try:
                db = sqlite3.connect("floricultura.db")  # conectando ao banco de dados
                cursor = db.cursor()
                cursor.execute("INSERT INTO dbclientes VALUES ('"+name+"','"+email+"') ")
                db.commit()  # Gravando no Banco de Dados
                db.close()   # Fechando o Banco de Dados
                st.write("Cadastro efetuado com sucesso !!!", name, email)
            except sqlite3.Error as erro:
                st.write("Erro no acesso ao Banco de Dados: ", erro)

    if opcoes == "Incluir Produtos":  # Formulario para incluir Produtos no Sistema
        st.subheader("Cadastro de Produtos")
        with st.form(key="include_produtos"):
            nome_produto = st.text_input(label="Insira o novo produto", max_chars=30)
            unidade_produto = st.text_input(label="Insira a unidade", max_chars=3)
            valor_produto = st.number_input(label="Insira o preço")
            button_submit = st.form_submit_button("Cadastrar")

        if button_submit:
            nome_produto = nome_produto.upper()        # nome do produto em maisculo
            unidade_produto = unidade_produto.upper()  # unidade do produto em maisculo


# #########################################################################################
# Rodapé da página com informações importantes - não alterar
with st.container(border=True, height=200):  # Rodapé da Pagina
    # st.write("Patrocinio [Clique aqui] (https://www.hashtagtreinamentos.com/curso-python)")
    st.write("Copyright(C) 2024 - Direitos Reservados - Versão 1.02")
    with st.container(border=True, height=100):  # Rodapé da Pagina (2)
        st.write("Desenvolvido pela Turma 004 Grupo 005")
        st.write("Linguagem utilizada Python 3.12.2 + Streamlit + Pandas")


#  Fim deste Módulo

#  Notas de uso de dados
#  name = st.text_input(label="Insira seu nome", max_chars=30)
#  email = st.text_input(label="insira seu e-mail", max_chars=60)
#  idade = st.number_input(label="insira a sua idade", format="%d", step=1) ou "%i"
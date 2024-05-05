###########################################
#  Site de Floricultura Rosas & Espinhos
#  RA: 2102144  Fernando Dias
#  RA: 2009640  Felipe Sousa Chagas
#  PJI 310 - Turma 004 Grupo 005
#  Ultima atualização 04/05/2024 as 15:00 hs
#  #########################################

import requests

import streamlit as st

import pandas as pd

# from pandas import read_csv

import sqlite3

# import numpy as np

from datetime import date

# ####################
# variaveis utilizadas
# ####################
janela = ""
tabela = ""
cliente = ""
banco = ""
erro = ""
# ####################

# ##### classes ######
class itempedido:
    def __init__(self, produto, preco, quantidade):
        self.produto = produto
        self.preco = preco
        self.quantidade = quantidade


class pedido:
    def __init__(self,numero, cliente, data):
        self.numero = numero
        self.cliente = cliente
        self.data = data
        self.itens = []

    def adicionar_itens(self, produto, preco, quantidade):
        item = itempedido(produto, preco, quantidade)
        self.itens.append(item)

    def exibir_informacoes(self):
        st.write(f'Número do Pedido: {self.numero}')
        st.write(f'Data do Pedido: {self.data}')
        st.write(f'Nome do Cliente: {self.cliente}')
        total_pedido = 0
        for item in self.itens:
            sub_total = item.preco * item.quantidade
            st.write(f" . {item.produto}\t - R$ {item.preco}\t - {item.quantidade} - R$ {sub_total:0.2f}")
            total_pedido += sub_total

        st.write(f"Total Pedido: R$ {total_pedido:0.2f}")


# ###### cache ######
# @st.cache_data
def carrega_carrinho():
    try:
        db = sqlite3.connect("floricultura.db")  # conectando ao banco de dados Floricultura
        cursor = db.cursor()
    except sqlite3.Error as erro:
        st.write("Erro no acesso ao Banco de Dados: ", erro)

    # SELECT SUM(Velocidade) FROM Carros GROUP BY Fabricante
    dado = pd.read_sql_query("SELECT data as Data, SUM(totalgeral) AS Vendas FROM dbcarrinho GROUP BY data ORDER BY data", con=db)

    # cursor.execute("SELECT data as Data, SUM(totalgeral) AS Vendas FROM dbcarrinho GROUP BY data ORDER BY data")  # consulta o bd
    # dado = cursor.fetchall()

    cursor.close()
    db.close()
    return dado


# ###### cache ######
@st.cache_data  # não mexer
def carregar_vendas():
    tabela = pd.read_csv("resultados.csv")  # carrega a tabela resultados da vendas p/ dias
    return tabela


def exibiropcoes():
    st.write("1 - Adicionar um Item")
    st.write("2 - Remover um Item")
    st.write("3 - Exibir Itens e Total")
    st.write("4 - Limpar Carrinho Compras")
    st.write("5 - Sair do Carrinho")


# ##############################################################################################
# relatorio de apresentacao de vendas está ok - não alterar
# ##############################################################################################
def apresenta_vendas():
    with st.container(border=True, height=420):
        qtde_dias = st.selectbox("Selecione o período de pesquisa", ["7D", "15D", "21D", "30D"])
        num_dias = int(qtde_dias.replace("D", ""))
        dados = carrega_carrinho() # dados = carregar_vendas()
        cursor.close()
        db.close()
        dados = dados[-num_dias:] # pega do final da listagem até o final da lista :
        # apresenta na tela ass ultimas vendas
        st.area_chart(dados, x="data", y="totalgeral", width=180, height=300)

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
        page_icon=":bar_chart:", layout="wide")
# #########################################################################################
# funcao sidebar está ok nao alterar
with st.sidebar:
    opcoes = st.sidebar.selectbox(":bar_chart: Menu Principal",
    ("Relatório de Vendas", "Lista de Clientes", "Cotações de Moedas","Lista de Pedidos",
     "Lista de Produtos", "Incluir Clientes", "Incluir Produtos", "Incluir Pedidos"),  # Menu de opções
    )

    st.image("flower.png", width=270)  # Imagem da Flor
    st.button(label="Cotações Moedas", use_container_width=200, type="primary", on_click=pega_cotacoes)
    st.button(label="Java Script", help="Balloom com Java Script", use_container_width=200, type="primary")

# Fim do SideBar ###########################################################################

# #######################################################################################
# Bloco Principal - Bloco Principal - Bloco Principal - Bloco Principal - Bloco Principal
# nome da empresa e linha colorida rainbow - está ok não alterar
with (((st.container(border=True, height=1080)))):
    st.subheader("Floricultura Rosas & Espinhos - 30 anos no mercado.", divider="rainbow")
    if opcoes == "Lista de Pedidos":
        try:
            db = sqlite3.connect("floricultura.db")  # conectando ao banco de dados Floricultura
            cursor = db.cursor()
        except sqlite3.Error as erro:
            st.write("Erro no acesso ao Banco de Dados: ", erro)

        cursor.execute("SELECT * FROM dbcarrinho ORDER BY data")  # consultando o banco de dados
        with st.container(border=True, height=900):
            st.dataframe(data=cursor)
            cursor.close()
            db.close()


    if opcoes == "Incluir Pedidos":
        try:
            db = sqlite3.connect("floricultura.db")  # conectando ao banco de dados Floricultura
            cursor = db.cursor()
        except sqlite3.Error as erro:
            st.write("Erro no acesso ao Banco de Dados: ", erro)

        with st.form(key="include_carrinho"): # Formulario para incluir pedidos de venda ( Carrinho de Compras )
            data = st.text_input(label="Selecione a data do pedido", value=format(date.today(), "%d-%m-%Y"))
            cursor.execute("SELECT * FROM dbclientes ORDER BY nome")  # consultando o banco de dados todos os clientes
            cliente = st.selectbox("Selecione o Cliente:",(cursor))  # mostra os clientes na tela
            cursor.execute("SELECT * FROM dbprodutos ORDER BY produto")  # consultando o banco de dados todos os produtos
            produto1 = st.selectbox("Item 1: ",(cursor), help="Selecione um Item")  # mostra os produtos na tela
            quantidade1 = st.number_input(label="quantidade do item 1", value=0, help="Selecione a quantidade" )
            cursor.execute("SELECT * FROM dbprodutos ORDER BY produto")  # consultando o banco de dados todos os produtos
            produto2 = st.selectbox("Item 2: ", (cursor), help="Selecione um Item")  # mostra os produtos na tela
            quantidade2 = st.number_input(label="quantidade do item 2", value=0, help="Selecione a quantidade")
            cursor.execute("SELECT * FROM dbprodutos ORDER BY produto")  # consultando o banco de dados todos os produtos
            produto3 = st.selectbox("Item 3: ", (cursor), help="Selecione um Item")  # mostra os produtos na tela
            quantidade3 = st.number_input(label="quantidade do item 3", value=0, help="Selecione a quantidade")
            cursor.execute("SELECT * FROM dbprodutos ORDER BY produto")  # consultando o banco de dados todos os produtos
            produto4 = st.selectbox("Item 4: ", (cursor), help="Selecione um Item")  # mostra os produtos na tela
            quantidade4 = st.number_input(label="quantidade do item 4", value=0, help="Selecione a quantidade")

            entrega = st.text_input(label="Insira endereço de entrega", max_chars=100, help="Inserir endereço de entrega")

            db.close()  # fechando o banco de dados
            submeter = st.form_submit_button("Cadastrar", help="Cadastra o pedido de venda", use_container_width=200, type="secondary")
            #  Variaveis usadas no programa
            preco1 = 0
            total1 = 0
            preco2 = 0
            total2 = 0
            preco3 = 0
            total3 = 0
            preco4 = 0
            total4 = 0
            totalgeral = 0
            if submeter and quantidade1 != 0:
                st.write(f"Cliente do pedido: {cliente[0]}")
                st.write(f"Data do Pedido: {data}")
                if quantidade1 != 0:
                    st.write(f"Produto 1 Selecionado: {produto1[0]}")
                    preco1 = produto1[2]
                    total1 = produto1[2] * quantidade1
                    totalgeral += total1
                    st.write(f"Total do Produto 1 R$ {total1:0.2f}")

                if quantidade2 != 0:
                    st.write(f"Produto 2 Selecionado: {produto2[0]}")
                    preco2 = produto2[2]
                    total2 = produto2[2] * quantidade2
                    totalgeral += total2
                    st.write(f"Total do Produto 2 R$ {total2:0.2f}")

                if quantidade3 != 0:
                    st.write(f"Produto 3 Selecionado: {produto3[0]}")
                    preco3 = produto3[2]
                    total3 = produto3[2] * quantidade3
                    totalgeral += total3
                    st.write(f"Total do Produto 3 R$ {total3:0.2f}")

                if quantidade4 != 0:
                    st.write(f"Produto 4 Selecionado: {produto4[0]}")
                    preco4 = produto4[2]
                    total4 = produto4[2] * quantidade4
                    totalgeral += total4
                    st.write(f"Total do Produto 4 R$ {total4:0.2f}")

                if quantidade1 != 0:
                    st.write(f"Endereço de entrega {entrega}")
                    st.write(f"Total Geral do Pedido R$ {totalgeral:0.2f}")

                # salvar aqui no banco de dados
                try:
                    db = sqlite3.connect("floricultura.db")  # conectando ao banco de dados Floricultura
                    cursor = db.cursor()
                except sqlite3.Error as erro:
                    st.write("Erro no acesso ao Banco de Dados: ", erro)
                # * Exemplo * ("INSERT INTO dbclientes VALUES ('" + name + "','" + email + "') ")
                cursor.execute("INSERT INTO dbcarrinho(nome, data, produto1, quantidade1, preco1, total1, produto2, quantidade2, preco2, total2, produto3, quantidade3, preco3, total3, produto4, quantidade4, preco4, total4, totalgeral, entrega) VALUES ('"+cliente[0]+"', '"+data+"','"+produto1[0]+"','"+str(quantidade1)+"','"+str(preco1)+"','"+str(total1)+"','"+produto2[0]+"','"+str(quantidade2)+"','"+str(preco2)+"','"+str(total2)+"','"+produto3[0]+"','"+str(quantidade3)+"','"+str(preco3)+"','"+str(total3)+"' ,'"+produto4[0]+"','"+str(quantidade4)+"','"+str(preco4)+"','"+str(total4)+"','"+str(totalgeral)+"','"+entrega+"');")
                db.commit()     # Gravando no Banco de Dados
                cursor.close()  # Fecha o cursor
                db.close()      # Fecha o Banco de Dados
                st.write("Cliente cadastrado com sucesso !!!", data, cliente[0])


    if opcoes == "Relatório de Vendas":
        st.title(":bar_chart: Tabela das Ultimas Vendas")
        with st.container(border=True, height=500):
            qtde_dias = st.selectbox("Selecione o período de pesquisa", ["7D", "15D", "21D", "30D"])
            num_dias = int(qtde_dias.replace("D", ""))
            dados = carrega_carrinho()   # dados = carregar_vendas()
            dados = dados[-num_dias:]
            # total = round(Vendas.sum(), 2)
            total = round(dados["Vendas"].sum(), 2)
            st.metric("Total das Receitas", round(int(total),2))
            # apresenta na tela ass ultimas vendas
            # st.area_chart(dados, x="Data", y="Vendas", width=180, height=300)
            st.line_chart(dados, x="Data", y="Vendas", width=180, height=300, color=[400, 110, 220])
            # st.plotly_chart(dados, x="Data", y="Vendas", width=180, height=300)


    if opcoes == "Lista de Produtos":
        # Tabela de Produtos da floricultura está ok - não alterar
        with st.container(border=True, height=400):  # Tabela de Produtos
            st.title("Produtos da Floricultura")
            # pro = carregar_produtos()
            # st.dataframe(pro)  # Tabela de Produtos
            db = sqlite3.connect("floricultura.db")  # conectando ao banco de dados
            cursor = db.cursor()
            cursor.execute("SELECT * FROM dbprodutos ORDER BY produto")  # consultando o banco de dados
            with st.container(border=True, height=300):
                # st.table(cursor)
                st.dataframe(cursor)
                db.close()


    if opcoes == "Cotações de Moedas":
        pega_cotacoes()  # pega a cotação das moedas dolar, euro e bitcoin e exib


    if opcoes == "Lista de Clientes":
        st.subheader("Listagem de Clientes")
        db = sqlite3.connect("floricultura.db")     # conectando ao banco de dados
        cursor = db.cursor()
        cursor.execute("SELECT * FROM dbclientes ORDER BY nome")  # consultando o banco de dados
        with st.container(border=True, height=300):
            # st.table(cursor)
            st.dataframe(cursor)
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
                st.write("Cliente cadastrado com sucesso !!!", name, email)

            except sqlite3.Error as erro:
                st.write("Erro no acesso ao Banco de Dados: ", erro)


    if opcoes == "Incluir Produtos":  # Formulario para incluir Produtos no Sistema
        st.subheader("Cadastro de Produtos")
        with st.form(key="include_produtos"):
            produto = st.text_input(label="Insira o novo produto", max_chars=30)
            unidade = st.text_input(label="Insira a unidade", max_chars=3)
            preco = st.number_input(label="Insira o preço")
            button_submit = st.form_submit_button("Cadastrar")

        if button_submit:
            produto = produto.upper()  # produto em maisculo
            unidade = unidade.upper()  # unidade em maisculo
            try:
                db = sqlite3.connect("floricultura.db")  # conectando ao banco de dados
                cursor = db.cursor()
                cursor.execute("INSERT INTO dbprodutos VALUES ('"+produto+"','"+unidade+"','"+str(preco)+"')")
                db.commit()  # Gravando no Banco de Dados
                db.close()   # Fechando o Banco de Dados
                st.write("Produto cadastrado com sucesso !!!", produto, unidade, preco)

            except sqlite3.Error as erro:
                st.write("Erro no acesso ao Banco de Dados: ", erro)


# ##########################################################################################
# ##########################################################################################
# ##########################################################################################
# Rodapé da página com informações importantes - não alterar
with st.container(border=True, height=200):  # Rodapé da Pagina
    # st.write("Patrocinio [Clique aqui] (https://www.hashtagtreinamentos.com/curso-python)")
    st.write("Copyright(C) 2024 - Direitos Reservados - Versão 1.07 - 04/05/2024 15:00 hs")
    with st.container(border=True, height=100):  # Rodapé da Pagina (2)
        st.write("Desenvolvido pela Turma 004 Grupo 005")
        st.write("Linguagem utilizada Python 3.12.2 + Streamlit + Pandas")



#  Fim deste Módulo
#  Notas de uso de dados
#  name = st.text_input(label="Insira seu nome", max_chars=30)
#  email = st.text_input(label="insira seu e-mail", max_chars=60)
#  idade = st.number_input(label="insira a sua idade", format="%d", step=1) ou "%i"

# :bar_chart: icone de barras - para ser usada na linha do navegador e tambem na tabela de vendas
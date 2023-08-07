import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime

# Função para criar a tabela se ela não existir
def create_table():
    conn.execute('''CREATE TABLE IF NOT EXISTS accounts
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 login TEXT,
                 senha TEXT,
                 data_nascimento TEXT,
                 data_criacao TEXT,
                 isp TEXT,
                 ip_criacao TEXT,
                 pais_criacao TEXT,
                 status TEXT)''')

# Função para adicionar uma nova conta no banco de dados
def add_account_db(login, senha, data_nascimento, isp, ip_criacao, pais_criacao, status):
    data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn.execute("INSERT INTO accounts (login, senha, data_nascimento, data_criacao, isp, ip_criacao, pais_criacao, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                 (login, senha, data_nascimento, data_criacao, isp, ip_criacao, pais_criacao, status))
    conn.commit()

# Função para obter todas as contas do banco de dados
def get_all_accounts():
    cursor = conn.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    return accounts

# Conexão com o banco de dados
conn = sqlite3.connect('accounts.db')
create_table()

# Interface do Streamlit
st.title("Sistema de Controle de Contas")

# Formulário para adicionar uma nova conta
with st.form("add_account_form"):
    st.header("Adicionar Nova Conta")
    
    login = st.text_input("Login (Email)")
    senha = st.text_input("Senha", type="password")
    data_nascimento = st.date_input("Data de Nascimento")
    isp = st.text_input("ISP")
    ip_criacao = st.text_input("IP de Criação")
    pais_criacao = st.text_input("País de Criação")
    status = st.selectbox("Status", ["Ativa", "Reserva", "Banida", "Mula", "Recorrendo", "Player Auctions", "Eldorado", "Vendida"])
    
    submit_button = st.form_submit_button("Adicionar Conta")

# Adicionar conta no banco de dados se o botão de envio for pressionado
if submit_button:
    add_account_db(login, senha, data_nascimento, isp, ip_criacao, pais_criacao, status)
    st.success("Conta adicionada com sucesso!")

# Obter todas as contas do banco de dados
accounts = get_all_accounts()

# Filtrar contas por status
selected_status = st.selectbox("Filtrar por Status", ["Todos"] + list(set(account[8] for account in accounts)))
if selected_status != "Todos":
    filtered_accounts = [account for account in accounts if account[8] == selected_status]
else:
    filtered_accounts = accounts

# Mostrar as contas
st.header("Contas")
accounts_df = pd.DataFrame(filtered_accounts, columns=["ID", "Login (Email)", "Senha", "Data de Nascimento", "Data de Criação", "ISP", "IP de Criação", "País de Criação", "Status"])
st.dataframe(accounts_df)
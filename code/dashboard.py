import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Simulando dados de contas
np.random.seed(42)
statuses = ["Ativa", "Reserva", "Banida", "Mula", "Recorrendo", "Player Auctions", "Eldorado", "Vendida"]
n_accounts = 100
data = {
    "Login (Email)": [f"user{i}@example.com" for i in range(n_accounts)],
    "Data de Criação": pd.date_range(start="2023-01-01", periods=n_accounts, freq="D"),
    "Status": np.random.choice(statuses, n_accounts),
}
accounts_df = pd.DataFrame(data)

# Interface do Streamlit
st.title("Dashboard de Controle de Contas")

# Filtrar contas por status
selected_status = st.sidebar.selectbox("Filtrar por Status", ["Todos"] + statuses)
filtered_accounts = accounts_df if selected_status == "Todos" else accounts_df[accounts_df["Status"] == selected_status]

# Conversão da coluna "Mês de Criação" para strings no formato YYYY-MM para evitar erro de serialização
filtered_accounts.loc[:, "Mês de Criação"] = filtered_accounts["Data de Criação"].dt.to_period("M").astype(str)


# Gráfico de barras por status
status_counts = filtered_accounts["Status"].value_counts()
fig_status = px.bar(status_counts, x=status_counts.index, y=status_counts.values, labels={"x": "Status", "y": "Quantidade"})
fig_status.update_layout(
    title="Distribuição de Contas por Status",
    xaxis_title="Status",
    yaxis_title="Quantidade",
)

# Gráfico de linha para data de criação
monthly_counts = filtered_accounts["Mês de Criação"].value_counts().sort_index()
fig_monthly = px.line(monthly_counts, x=monthly_counts.index, y=monthly_counts.values, labels={"x": "Mês", "y": "Quantidade"})
fig_monthly.update_layout(
    title="Criação de Contas ao Longo do Tempo",
    xaxis_title="Mês",
    yaxis_title="Quantidade",
)

# Mostrar gráficos
st.plotly_chart(fig_status, use_container_width=True)
st.plotly_chart(fig_monthly, use_container_width=True)

# Mostrar tabela de contas
st.header("Tabela de Contas")
st.dataframe(filtered_accounts)

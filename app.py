import pandas as pd
import streamlit as st

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Simulador de Custos e Orçamento",
    page_icon="💰",
    layout="wide",
)


# ==========================================
# BASE DE DADOS INTERNA
# ==========================================
@st.cache_data
def carregar_dados():
    data = [
        {
            "Item": "Chapas de Aço",
            "Categoria": "Matéria-Prima",
            "Valor (R$)": 4500.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Resina Epóxi",
            "Categoria": "Matéria-Prima",
            "Valor (R$)": 1800.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Equipe de Montagem",
            "Categoria": "Mão de Obra",
            "Valor (R$)": 6500.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Designer UX/UI",
            "Categoria": "Mão de Obra",
            "Valor (R$)": 3200.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Frete Interestadual",
            "Categoria": "Logística",
            "Valor (R$)": 2400.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Embalagens Especiais",
            "Categoria": "Logística",
            "Valor (R$)": 950.00,
            "Prioridade": "Baixa",
        },
        {
            "Item": "Conta de Luz - Galpão",
            "Categoria": "Energia",
            "Valor (R$)": 1300.00,
            "Prioridade": "Alta",
        },
        {
            "Item": "Gerador de Backup",
            "Categoria": "Energia",
            "Valor (R$)": 800.00,
            "Prioridade": "Baixa",
        },
        {
            "Item": "Furadeiras Industriais",
            "Categoria": "Ferramentas",
            "Valor (R$)": 1500.00,
            "Prioridade": "Média",
        },
        {
            "Item": "Licença de Software CAD",
            "Categoria": "Ferramentas",
            "Valor (R$)": 2100.00,
            "Prioridade": "Alta",
        },
    ]
    return pd.DataFrame(data)


df = carregar_dados()

# ==========================================
# BARRA LATERAL (SIDEBAR) - CONTROLES
# ==========================================
st.sidebar.header("⚙️ Configurações do Projeto")

# 1. Slider de Orçamento
orcamento_total = st.sidebar.slider(
    label="Orçamento Total Disponível (R$)",
    min_value=5000.0,
    max_value=50000.0,
    value=20000.0,
    step=500.0,
    format="R$ %.2f",
)

# Categorias únicas para o filtro
categorias_disponiveis = df["Categoria"].unique().tolist()

# 2. Multiselect de Categorias
categorias_selecionadas = st.sidebar.multiselect(
    label="Filtrar por Categoria",
    options=categorias_disponiveis,
    default=categorias_disponiveis,
)

# ==========================================
# FILTRAGEM DOS DADOS
# ==========================================
df_filtrado = df[df["Categoria"].isin(categorias_selecionadas)]

# ==========================================
# ÁREA PRINCIPAL
# ==========================================
st.title("💰 Simulador de Custos e Orçamento")
st.caption("Acompanhamento financeiro em tempo real e análise de despesas")

# Cálculos para os indicadores
gasto_filtrado = df_filtrado["Valor (R$)"].sum()
saldo_restante = orcamento_total - gasto_filtrado

# 1. PAINEL DE MÉTRICAS (st.columns)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Orçamento Definido",
        value=f"R$ {orcamento_total:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
    )

with col2:
    st.metric(
        label="Gasto Filtrado",
        value=f"R$ {gasto_filtrado:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
    )

with col3:
    st.metric(
        label="Saldo Restante",
        value=f"R$ {saldo_restante:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
        delta=f"R$ {saldo_restante:,.2f}".replace(",", "X")
        .replace(".", ",")
        .replace("X", "."),
    )

st.divider()

# 2. ALERTA VISUAL CONDICIONAL
if gasto_filtrado <= orcamento_total:
    st.success(
        f"✅ **Projeto dentro do orçamento!** Você ainda possui **R$ {saldo_restante:,.2f}** disponíveis."
    )
else:
    excedente = abs(saldo_restante)
    st.error(
        f"🚨 **Atenção! Orçamento estourado.** O valor filtrado excede o limite em **R$ {excedente:,.2f}**."
    )

st.divider()

# 3. GRÁFICO E TABELA
col_grafico, col_tabela = st.columns([1, 1.2])

with col_grafico:
    st.subheader("📊 Gastos por Categoria")

    if not df_filtrado.empty:
        # Agrupamento e soma por categoria
        gastos_por_categoria = (
            df_filtrado.groupby("Categoria")["Valor (R$)"]
            .sum()
            .reset_index()
            .sort_values(by="Valor (R$)", ascending=True)
        )

        # Gráfico nativo horizontal do Streamlit
        st.bar_chart(
            gastos_por_categoria,
            x="Valor (R$)",
            y="Categoria",
            horizontal=True,
            color="#29b5e8",
        )
    else:
        st.info("Nenhuma categoria selecionada para exibir o gráfico.")

with col_tabela:
    st.subheader("📋 Detalhamento dos Itens")

    if not df_filtrado.empty:
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Valor (R$)": st.column_config.NumberColumn(
                    "Valor (R$)", format="R$ %.2f"
                )
            },
        )
    else:
        st.warning("Selecione pelo menos uma categoria no menu lateral.")

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# CONFIGURAÇÃO INICIAL
# ============================================================

st.set_page_config(
    page_title="Sabor do Sertão",
    layout="wide"
)

st.title("Painel de Vendas: Sabor do Sertão")
st.write("Análise das vendas da rede de lanchonetes Sabor do Sertão.")


# ============================================================
# CARREGAMENTO DO CSV
# ============================================================

@st.cache_data
def carregar(arquivo):
    return pd.read_csv(
        arquivo,
        parse_dates=["data"]
    )


arquivo = st.sidebar.file_uploader(
    "Envie o CSV de vendas",
    type="csv"
)

if arquivo is None:
    st.info("Envie o arquivo para começar.")
    st.stop()

df = carregar(arquivo)


# ============================================================
# NÍVEL 1 - EXPLORAÇÃO E TRATAMENTO DOS DADOS
# ============================================================

st.header("1. Exploração dos dados")

st.subheader("Primeiras linhas")

st.dataframe(
    df.head(),
    use_container_width=True
)


st.subheader("Resumo estatístico")

st.dataframe(
    df.describe(),
    use_container_width=True
)


st.subheader("Valores ausentes")

valores_ausentes = df.isnull().sum()

st.dataframe(
    valores_ausentes.rename("Quantidade de valores ausentes"),
    use_container_width=True
)


# Tratamento da coluna avaliacao
if df["avaliacao"].isnull().sum() > 0:

    mediana_avaliacao = df["avaliacao"].median()

    df["avaliacao"] = df["avaliacao"].fillna(mediana_avaliacao)

    st.caption(
        f"A coluna 'avaliacao' possuía valores ausentes. "
        f"Os valores foram preenchidos com a mediana "
        f"({mediana_avaliacao:.1f}), pois a mediana é menos "
        f"sensível a valores extremos."
    )
else:

    st.caption(
        "A coluna 'avaliacao' não possui valores ausentes."
    )


# ============================================================
# NÍVEL 3 - FILTROS
# ============================================================

st.sidebar.header("Filtros")


# Filtro de cidade
cidades = sorted(df["cidade"].unique())

cidades_selecionadas = st.sidebar.multiselect(
    "Cidade",
    options=cidades,
    default=cidades
)


# Filtro de categoria
categorias = sorted(df["categoria"].unique())

categorias_selecionadas = st.sidebar.multiselect(
    "Categoria",
    options=categorias,
    default=categorias
)


# Filtro de data
data_minima = df["data"].min().date()
data_maxima = df["data"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_minima, data_maxima),
    min_value=data_minima,
    max_value=data_maxima
)


# ============================================================
# APLICAÇÃO DOS FILTROS
# ============================================================

df_filtrado = df[
    df["cidade"].isin(cidades_selecionadas)
    & df["categoria"].isin(categorias_selecionadas)
].copy()


# Verifica se o usuário selecionou as duas datas
if len(periodo) == 2:

    data_inicio = pd.Timestamp(periodo[0])
    data_fim = pd.Timestamp(periodo[1])

    df_filtrado = df_filtrado[
        (df_filtrado["data"] >= data_inicio)
        & (df_filtrado["data"] <= data_fim)
    ]


# Verificação caso os filtros não retornem dados
if df_filtrado.empty:

    st.warning(
        "Nenhuma venda foi encontrada com os filtros selecionados."
    )

    st.stop()


# ============================================================
# NÍVEL 2 - INDICADORES / KPIs
# ============================================================

st.header("2. Indicadores")

faturamento_total = df_filtrado["total"].sum()

numero_vendas = len(df_filtrado)

ticket_medio = df_filtrado["total"].mean()

avaliacao_media = df_filtrado["avaliacao"].mean()


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Faturamento total",
        f"R$ {faturamento_total:,.2f}"
    )


with col2:
    st.metric(
        "Número de vendas",
        f"{numero_vendas:,}"
    )


with col3:
    st.metric(
        "Ticket médio",
        f"R$ {ticket_medio:,.2f}"
    )


with col4:
    st.metric(
        "Avaliação média",
        f"{avaliacao_media:.2f} / 5"
    )


# ============================================================
# NÍVEL 4 - GRÁFICOS
# ============================================================

st.header("3. Visualizações")


tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Faturamento mensal",
        "Faturamento por cidade",
        "Produtos mais vendidos",
        "Formas de pagamento",
        "Mapa de calor"
    ]
)


# ------------------------------------------------------------
# GRÁFICO 1 - FATURAMENTO MENSAL
# ------------------------------------------------------------

with tab1:

    faturamento_mensal = (
        df_filtrado
        .groupby(
            df_filtrado["data"].dt.to_period("M")
        )["total"]
        .sum()
        .reset_index()
    )

    faturamento_mensal["data"] = (
        faturamento_mensal["data"]
        .astype(str)
    )

    fig_mensal = px.line(
        faturamento_mensal,
        x="data",
        y="total",
        markers=True,
        title="Faturamento mensal"
    )

    fig_mensal.update_layout(
        xaxis_title="Mês",
        yaxis_title="Faturamento (R$)"
    )

    st.plotly_chart(
        fig_mensal,
        use_container_width=True
    )


# ------------------------------------------------------------
# GRÁFICO 2 - FATURAMENTO POR CIDADE
# ------------------------------------------------------------

with tab2:

    faturamento_cidade = (
        df_filtrado
        .groupby("cidade")["total"]
        .sum()
        .reset_index()
        .sort_values("total", ascending=False)
    )

    fig_cidade = px.bar(
        faturamento_cidade,
        x="cidade",
        y="total",
        title="Faturamento por cidade",
        text_auto=".2s"
    )

    fig_cidade.update_layout(
        xaxis_title="Cidade",
        yaxis_title="Faturamento (R$)"
    )

    st.plotly_chart(
        fig_cidade,
        use_container_width=True
    )


# ------------------------------------------------------------
# GRÁFICO 3 - TOP 5 PRODUTOS
# ------------------------------------------------------------

with tab3:

    produtos_top5 = (
        df_filtrado
        .groupby("produto")["quantidade"]
        .sum()
        .reset_index()
        .sort_values(
            "quantidade",
            ascending=False
        )
        .head(5)
    )

    produtos_top5 = produtos_top5.sort_values(
        "quantidade",
        ascending=True
    )

    fig_produtos = px.bar(
        produtos_top5,
        x="quantidade",
        y="produto",
        orientation="h",
        title="Top 5 produtos mais vendidos",
        text="quantidade"
    )

    fig_produtos.update_layout(
        xaxis_title="Quantidade vendida",
        yaxis_title="Produto"
    )

    st.plotly_chart(
        fig_produtos,
        use_container_width=True
    )


# ------------------------------------------------------------
# GRÁFICO 4 - FORMAS DE PAGAMENTO
# ------------------------------------------------------------

with tab4:

    pagamentos = (
        df_filtrado["pagamento"]
        .value_counts()
        .reset_index()
    )

    pagamentos.columns = [
        "pagamento",
        "quantidade"
    ]

    fig_pagamentos = px.pie(
        pagamentos,
        names="pagamento",
        values="quantidade",
        title="Participação das formas de pagamento"
    )

    st.plotly_chart(
        fig_pagamentos,
        use_container_width=True
    )


# ------------------------------------------------------------
# GRÁFICO 5 - MAPA DE CALOR
# ------------------------------------------------------------

with tab5:

    vendas_horario = (
        df_filtrado
        .groupby(["hora", df_filtrado["data"].dt.day_name()])
        .size()
        .reset_index(name="vendas")
    )

    # Tradução dos dias para facilitar a leitura
    traducao_dias = {
        "Monday": "Segunda",
        "Tuesday": "Terça",
        "Wednesday": "Quarta",
        "Thursday": "Quinta",
        "Friday": "Sexta",
        "Saturday": "Sábado",
        "Sunday": "Domingo"
    }

    vendas_horario["dia_semana"] = (
        vendas_horario["data"]
        .map(traducao_dias)
    )

    fig_heatmap = px.density_heatmap(
        vendas_horario,
        x="dia_semana",
        y="hora",
        z="vendas",
        title="Vendas por dia da semana e hora"
    )

    fig_heatmap.update_layout(
        xaxis_title="Dia da semana",
        yaxis_title="Hora"
    )

    st.plotly_chart(
        fig_heatmap,
        use_container_width=True
    )


# ============================================================
# NÍVEL 5 - INSIGHTS
# ============================================================

st.header("4. Insights para gestão")


# Cidade com maior faturamento
cidade_destaque = (
    df_filtrado
    .groupby("cidade")["total"]
    .sum()
    .idxmax()
)

valor_cidade_destaque = (
    df_filtrado
    .groupby("cidade")["total"]
    .sum()
    .max()
)


# Produto mais vendido
produto_destaque = (
    df_filtrado
    .groupby("produto")["quantidade"]
    .sum()
    .idxmax()
)

quantidade_produto_destaque = (
    df_filtrado
    .groupby("produto")["quantidade"]
    .sum()
    .max()
)


# Forma de pagamento mais utilizada
pagamento_destaque = (
    df_filtrado["pagamento"]
    .value_counts()
    .idxmax()
)

quantidade_pagamento_destaque = (
    df_filtrado["pagamento"]
    .value_counts()
    .max()
)


st.markdown(
    f"""
    **1. Cidade com maior faturamento:**  
    A cidade de **{cidade_destaque}** apresentou o maior
    faturamento no período selecionado, totalizando
    **R$ {valor_cidade_destaque:,.2f}**.

    **2. Produto mais vendido:**  
    O produto **{produto_destaque}** foi o mais vendido em
    quantidade, com **{quantidade_produto_destaque:,} unidades**.

    **3. Forma de pagamento mais utilizada:**  
    A forma de pagamento mais utilizada foi **{pagamento_destaque}**,
    com **{quantidade_pagamento_destaque:,} vendas.
    """
)


# ============================================================
# EXPORTAÇÃO DOS DADOS FILTRADOS
# ============================================================

st.header("5. Exportar dados")

csv_filtrado = df_filtrado.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Baixar CSV filtrado",
    data=csv_filtrado,
    file_name="vendas_sabor_do_sertao_filtradas.csv",
    mime="text/csv"
)


# ============================================================
# BÔNUS - EXPLORADOR LIVRE
# ============================================================

st.header("6. Explorador livre")

tab_explorador = st.tabs(["Explorador livre"])[0]

with tab_explorador:

    st.write(
        "Use esta área para carregar outro CSV e criar uma visualização "
        "escolhendo os eixos e o tipo de gráfico."
    )

    arquivo_explorador = st.file_uploader(
        "Envie um CSV para explorar",
        type="csv",
        key="explorador_csv"
    )

    if arquivo_explorador is not None:

        df_explorador = pd.read_csv(
            arquivo_explorador
        )

        st.subheader("Dados carregados")

        st.dataframe(
            df_explorador.head(),
            use_container_width=True
        )

        col_x, col_y = st.columns(2)

        with col_x:

            eixo_x = st.selectbox(
                "Escolha o eixo X",
                options=df_explorador.columns
            )

        with col_y:

            eixo_y = st.selectbox(
                "Escolha o eixo Y",
                options=df_explorador.columns
            )

        tipo_grafico = st.selectbox(
            "Tipo de gráfico",
            options=[
                "Barras",
                "Linha",
                "Dispersão"
            ]
        )

        if tipo_grafico == "Barras":

            fig_livre = px.bar(
                df_explorador,
                x=eixo_x,
                y=eixo_y,
                title=f"{eixo_y} por {eixo_x}"
            )

        elif tipo_grafico == "Linha":

            fig_livre = px.line(
                df_explorador,
                x=eixo_x,
                y=eixo_y,
                title=f"{eixo_y} por {eixo_x}"
            )

        else:

            fig_livre = px.scatter(
                df_explorador,
                x=eixo_x,
                y=eixo_y,
                title=f"{eixo_y} por {eixo_x}"
            )

        st.plotly_chart(
            fig_livre,
            use_container_width=True
        )

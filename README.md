# Sabor do Sertão — Painel de Análise de Dados

Painel interativo de análise de vendas desenvolvido em Python com Streamlit, Pandas e Plotly.

O projeto foi desenvolvido como atividade prática de análise de dados, utilizando dados fictícios da rede de lanchonetes Sabor do Sertão.

## Objetivo

O painel permite analisar as vendas da empresa e responder perguntas como:

- Qual cidade apresenta maior faturamento?
- Quais produtos são mais vendidos?
- Qual é a forma de pagamento mais utilizada?
- Como o faturamento varia ao longo do tempo?
- Qual é o ticket médio das vendas?
- Qual é a avaliação média dos clientes?

## Tecnologias utilizadas

- Python 3
- Streamlit
- Pandas
- Plotly
- NumPy

## Funcionalidades

O painel possui:

- Visualização dos primeiros registros dos dados
- Estatísticas descritivas
- Verificação e tratamento de valores ausentes
- Indicadores de faturamento, vendas, ticket médio e avaliação
- Filtros por cidade
- Filtros por categoria
- Filtro por período
- Gráfico de faturamento mensal
- Gráfico de faturamento por cidade
- Ranking dos produtos mais vendidos
- Análise das formas de pagamento
- Mapa de calor
- Insights gerenciais
- Download dos dados filtrados em CSV
- Explorador livre para criação de gráficos personalizados

## Como executar o projeto

### 1. Instalar as dependências

Com o Python instalado, execute:

    pip install -r requirements.txt

### 2. Gerar os dados

Execute:

    python gerar_dados.py

Esse comando gera o arquivo:

    vendas_sabor_do_sertao.csv

### 3. Executar o painel

Execute:

    streamlit run app.py

Depois, acesse o endereço apresentado pelo Streamlit no terminal.

## Estrutura do projeto

    sabor_sertao/
    ├── app.py
    ├── gerar_dados.py
    ├── vendas_sabor_do_sertao.csv
    ├── requirements.txt
    └── README.md

## Dados

Os dados utilizados no projeto são fictícios e foram gerados pelo arquivo `gerar_dados.py`.

O conjunto possui informações sobre:

- Data
- Hora
- Cidade
- Categoria
- Produto
- Preço unitário
- Quantidade
- Forma de pagamento
- Avaliação
- Total da venda

## Projeto

**Atividade Prática: Painel de Análise de Dados com Streamlit**

Projeto desenvolvido para fins acadêmicos.

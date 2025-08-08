import streamlit as st
import pandas as pd
import plotly.express as px

#! ---- Configuração da página ----
#* Define o título da página, o icone e o layout para ocupar toda a largura
# 'set_page_config' é usado para configurar as propriedades da página do Streamlit
# 'page_title' define o título que será exibido na aba do navegador
# 'page_icon' define o ícone que será exibido na aba do navegador
# 'layout' define o layout da página como "wide" para ocupar toda a largura disponível
st.set_page_config(
    page_title = "Dashboard de Salários da Área de Dados",
    page_icon = "📊",
    layout = "wide"
)

#! ---- Carregamento dos dados ----
#* Carrega os dados de salários de um arquivo CSV com pandas
# 'read_csv' lê o arquivo CSV diretamente da URL fornecida
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

#! ---- Barra Lateral - Filtros ----
#* Cria uma barra lateral para filtros
# 'sidebar' cria uma barra lateral onde os filtros serão exibidos
st.sidebar.header("🔍 Filtros")

#* Filtro de Ano
# 'sorted' é usado para garantir que os anos sejam exibidos em ordem crescente
# 'unique' é usado para obter os anos únicos do DataFrame
# 'multiselect' permite que o usuário selecione múltiplos anos
# 'default' define os anos selecionados inicialmente como todos os disponíveis
anos_disponiveis = sorted(df["ano"].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

#* Filtro de Senioridade
# 'sorted' é usado para garantir que as senioridades sejam exibidas em ordem alfabética
# 'unique' é usado para obter as senioridades únicas do DataFrame
# 'multiselect' permite que o usuário selecione múltiplas senioridades
# 'default' define as senioridades selecionadas inicialmente como todas as disponíveis
senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

#* Filtro por Tipo de Contrato
# 'sorted' é usado para garantir que os tipos de contrato sejam exibidos em ordem alfabética
# 'unique' é usado para obter os tipos de contrato únicos do DataFrame
# 'multiselect' permite que o usuário selecione múltiplos tipos de contrato
# 'default' define os tipos de contrato selecionados inicialmente como todos os disponíveis
contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

#* Filtro de tamnanho da Empresa
# 'sorted' é usado para garantir que os tamanhos de empresa sejam exibidos em ordem alfabética
# 'unique' é usado para obter os tamanhos de empresa únicos do DataFrame
# 'multiselect' permite que o usuário selecione múltiplos tamanhos de empresa
# 'default' define os tamanhos de empresa selecionados inicialmente como todos os disponíveis
tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

#! ---- Filtragem do DataFrame ----
#* O DataFrame é filtrado com base nos filtros selecionados na barra lateral
# O DataFrame 'df' é filtrado para incluir apenas as linhas que correspondem aos anos, senioridades, tipos de contrato e tamanhos de empresa selecionados pelo usuário
df_filtrado = df[
    (df["ano"].isin(anos_selecionados)) &
    (df["senioridade"].isin(senioridades_selecionadas)) &
    (df["contrato"].isin(contratos_selecionados)) &
    (df["tamanho_empresa"].isin(tamanhos_selecionados))
]

#! ---- Conteudo Principal ----
#* Exibe o título e a descrição do dashboard
# 'title' exibe o título do dashboard
# 'markdown' exibe uma descrição do dashboard
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utileze os filtros na barra lateral para refinar sua análise.")

#! ---- Metricas Principais ----
#* Exibe as métricas principais do DataFrame filtrado
# 'subheader' exibe um subtítulo para a seção de métricas principais
st.subheader("📊 Métricas gerais (Salário Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado["usd"].mean()
    salario_maximo = df_filtrado["usd"].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de Registros", total_registros)
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

#! ---- Análises Visuais com Plotly ----
#* Exibe gráficos interativos usando Plotly
st.subheader("📈 Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title='Distribuição de Salários Anuais',
            labels={'usd': 'Faixa Salarial (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de distribuição de salários.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            values='quantidade',
            names='tipo_trabalho',
            title='Proporção por tipo de Trabalho',
            labels={'tipo_trabalho': 'Tipo de Trabalho', 'quantidade': 'Quantidade'},
            hole=0.5
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de proporção por tipo de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        # '==' é usado para filtrar os dados para Cientistas de Dados
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        # 'groupby' é usado para agrupar os dados por país e calcular a média salarial
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
        grafico_paises = px.choropleth(
            media_ds_pais,
            locations='residencia_iso3',
            locationmode='ISO-3',
            color='usd',
            hover_name='residencia_iso3',
            title='Salário Médio de Cientista de Dados por País',
            labels={'usd': 'Salário Médio Anual (USD)'},
            color_continuous_scale='rdylgn')
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de salário médio de Cientista de Dados por País.")


#! ---- Tabela da Dados Detalhados ----
st.subheader("📋 Tabela de Dados Detalhados")
st.dataframe(df_filtrado)

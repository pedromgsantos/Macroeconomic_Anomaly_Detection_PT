# ===================================================================
# DASHBOARD INTERATIVO - ANÁLISE DE ANOMALIAS MACROECONÓMICAS (v2)
# ===================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Análise de Anomalias Macroeconómicas",
    page_icon="📈",
    layout="wide"
)

# --- FUNÇÃO DE CACHE PARA CARREGAR E PREPARAR OS DADOS ---
@st.cache_data
def carregar_e_preparar_dados():
    caminho_dados_originais = 'data/dados_processados_trimestrais.csv'
    df = pd.read_csv(caminho_dados_originais, index_col=0, parse_dates=True)
    df.index.name = 'data'
    df.rename(columns={
        'PIB_var_homologa': 'pib',
        'Credito_Empresas_Total': 'credito_empresas',
        'Credito_Particulares_Total': 'credito_particulares',
        'Endividamento_Total': 'endividamento'
    }, inplace=True)
    
    # Adicionar as colunas de anomalia
    anomalias_isoforest_datas = ['2012-06-30', '2012-09-30', '2012-12-31', '2020-06-30', '2021-06-30', '2022-03-31']
    anomalias_stl_datas = ['2020-06-30', '2021-06-30', '2011-09-30', '2017-03-31', '2017-06-30', '2018-12-31', '2019-03-31']
    anomalias_prophet_datas = ['2020-06-30', '2021-06-30', '2021-12-31', '2022-09-30']

    df['anomalia_isoforest'] = df.index.isin(pd.to_datetime(anomalias_isoforest_datas)).astype(int)
    df['anomalia_stl'] = df.index.isin(pd.to_datetime(anomalias_stl_datas)).astype(int)
    df['anomalia_prophet'] = df.index.isin(pd.to_datetime(anomalias_prophet_datas)).astype(int)
    df['contagem_anomalias'] = df[['anomalia_isoforest', 'anomalia_stl', 'anomalia_prophet']].sum(axis=1)

    return df

# --- CARREGAMENTO DOS DADOS ---
df_final = carregar_e_preparar_dados()

# --- SIDEBAR DE CONTROLOS ---
st.sidebar.header("Controlos de Visualização")

# Seletor de Variável
lista_variaveis = {
    'pib': 'PIB (Variação Homóloga %)',
    'credito_empresas': 'Crédito a Empresas',
    'credito_particulares': 'Crédito a Particulares',
    'endividamento': 'Endividamento Total'
}
variavel_selecionada_key = st.sidebar.selectbox(
    "Selecione a série temporal para visualizar:",
    options=list(lista_variaveis.keys()),
    format_func=lambda x: lista_variaveis[x] # Mostra o nome bonito na UI
)

# Checkboxes para filtrar modelos
st.sidebar.markdown("---")
st.sidebar.markdown("**Exibir anomalias dos modelos:**")
mostrar_isoforest = st.sidebar.checkbox("Isolation Forest (Sistémica)", value=True)
mostrar_stl = st.sidebar.checkbox("Decomposição STL (Ponto de Viragem)", value=True)
mostrar_prophet = st.sidebar.checkbox("Prophet (Desvio da Previsão)", value=True)


# --- LAYOUT PRINCIPAL ---
st.title("📈 Análise de Anomalias Macroeconómicas em Portugal")
st.markdown("Dashboard interativo para explorar anomalias em séries temporais económicas.")

# --- GRÁFICO PRINCIPAL (agora dinâmico) ---
st.header(f"Análise Visual de Anomalias em: {lista_variaveis[variavel_selecionada_key]}")

fig = go.Figure()

# Adiciona a linha da série selecionada
fig.add_trace(go.Scatter(x=df_final.index, y=df_final[variavel_selecionada_key], mode='lines', name=lista_variaveis[variavel_selecionada_key], line=dict(color='lightgrey', width=2)))

# Adiciona marcadores de anomalia condicionalmente
if mostrar_isoforest:
    df_anom = df_final[df_final['anomalia_isoforest'] == 1]
    fig.add_trace(go.Scatter(x=df_anom.index, y=df_anom[variavel_selecionada_key], mode='markers', name='Anomalia: Isolation Forest', marker=dict(color='red', size=10, symbol='circle')))
if mostrar_stl:
    df_anom = df_final[df_final['anomalia_stl'] == 1]
    fig.add_trace(go.Scatter(x=df_anom.index, y=df_anom[variavel_selecionada_key], mode='markers', name='Anomalia: STL', marker=dict(color='green', size=10, symbol='diamond')))
if mostrar_prophet:
    df_anom = df_final[df_final['anomalia_prophet'] == 1]
    fig.add_trace(go.Scatter(x=df_anom.index, y=df_anom[variavel_selecionada_key], mode='markers', name='Anomalia: Prophet', marker=dict(color='purple', size=10, symbol='x')))

# Adiciona marcadores de consenso
df_consenso = df_final[df_final['contagem_anomalias'] > 1]
fig.add_trace(go.Scatter(x=df_consenso.index, y=df_consenso[variavel_selecionada_key], mode='markers', name='Consenso', marker=dict(color='gold', size=16, symbol='star', line=dict(color='black', width=1))))

# Melhora o layout
fig.update_layout(xaxis_title='Data', yaxis_title='Valor', legend_title='Legenda', template='plotly_white', height=500)
st.plotly_chart(fig, use_container_width=True)

# --- ANÁLISE ESCRITA E TABELA DE DADOS ---
with st.expander("Ver Análise Detalhada e Tabela de Anomalias"):
    st.header("Interpretação dos Resultados")
    st.markdown("""
    A análise combina três modelos distintos para uma deteção robusta de anomalias:
    - **Isolation Forest (vermelho):** Deteta desequilíbrios na *relação* entre todas as variáveis. Ideal para encontrar anomalias sistémicas, como a crise da dívida soberana de 2012.
    - **Decomposição STL (verde):** Identifica pontos de viragem e choques em *cada variável individualmente*. Foi eficaz a encontrar o início de um *credit crunch* ou o fundo de um ciclo de endividamento.
    - **Prophet (roxo):** Deteta anomalias ao comparar os dados reais do PIB com a sua *própria previsão*. É especialista em encontrar surpresas no crescimento económico, tanto positivas como negativas.
    - **Consenso (dourado):** Pontos detetados por múltiplos modelos, representando os eventos mais extremos e inequívocos, como o choque da COVID-19 em 2020.
    """)

    st.header("Tabela Detalhada das Anomalias")
    df_comparativo = df_final[df_final['contagem_anomalias'] > 0].copy()
    colunas_tabela = ['pib', 'credito_empresas', 'credito_particulares', 'endividamento', 'anomalia_isoforest', 'anomalia_stl', 'anomalia_prophet', 'contagem_anomalias']
    st.dataframe(df_comparativo.sort_values(by=['contagem_anomalias', 'data'], ascending=[False, True])[colunas_tabela])
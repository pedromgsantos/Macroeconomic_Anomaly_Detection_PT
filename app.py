# ===================================================================
# DASHBOARD INTERATIVO - ANÁLISE DE ANOMALIAS MACROECONÓMICAS (v3 - Dinâmico)
# ===================================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.seasonal import STL
from prophet import Prophet
import logging

# Configurar o logger do Prophet para ser menos verboso
logging.getLogger('cmdstanpy').setLevel(logging.WARNING)

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Monitorização de Anomalias Macroeconómicas",
    page_icon="🚨",
    layout="wide"
)

# --- FUNÇÃO DE CACHE PARA CARREGAR E EXECUTAR OS MODELOS ---
@st.cache_data
def carregar_e_modelar_dados():
    # 1. Carregar os dados já processados pelo script update_data.py
    caminho_dados = 'data/dados_processados_trimestrais.csv'
    df = pd.read_csv(caminho_dados, index_col=0, parse_dates=True)
    df.index.name = 'data'
    
    # Renomear colunas para nomes mais curtos
    df.rename(columns={
        'PIB_var_homologa': 'pib',
        'Credito_Empresas_Total': 'credito_empresas',
        'Credito_Particulares_Total': 'credito_particulares',
        'Endividamento_Total': 'endividamento'
    }, inplace=True)

    # --- 2. Executar Modelos de Deteção de Anomalias ---

    # a) Isolation Forest (Sistémico)
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)
    model_iso = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    df['anomaly_isoforest_pred'] = model_iso.fit_predict(df_scaled)
    df['anomalia_isoforest'] = df['anomaly_isoforest_pred'].apply(lambda x: 1 if x == -1 else 0)

    # b) Decomposição STL (Pontos de Viragem)
    df['anomalia_stl'] = 0
    for coluna in ['pib', 'credito_empresas', 'credito_particulares', 'endividamento']:
        stl = STL(df[coluna], period=4)
        resultado_stl = stl.fit()
        residuos = resultado_stl.resid
        limiar = residuos.std() * 2.5
        anomalias_stl_idx = residuos[abs(residuos) > limiar].index
        df.loc[anomalias_stl_idx, 'anomalia_stl'] = 1

    # c) Prophet (Desvio da Previsão no PIB)
    df_prophet_pib = df[['pib']].reset_index().rename(columns={'data': 'ds', 'pib': 'y'})
    model_prophet = Prophet(interval_width=0.95, yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    model_prophet.fit(df_prophet_pib)
    forecast = model_prophet.predict(df_prophet_pib[['ds']])
    df_forecast = forecast.set_index('ds')
    
    df['anomalia_prophet'] = ((df['pib'] < df_forecast['yhat_lower']) | (df['pib'] > df_forecast['yhat_upper'])).astype(int)

    # 3. Calcular a contagem final de anomalias
    df['contagem_anomalias'] = df[['anomalia_isoforest', 'anomalia_stl', 'anomalia_prophet']].sum(axis=1)

    return df.drop(columns=['anomaly_isoforest_pred'])

# --- CARREGAMENTO E MODELAGEM DOS DADOS ---
# A função só será re-executada se o ficheiro .csv for alterado.
df_final = carregar_e_modelar_dados()

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
    format_func=lambda x: lista_variaveis[x]
)

# Checkboxes para filtrar modelos
st.sidebar.markdown("---")
st.sidebar.markdown("**Exibir anomalias dos modelos:**")
mostrar_isoforest = st.sidebar.checkbox("Isolation Forest (Sistémica)", value=True)
mostrar_stl = st.sidebar.checkbox("Decomposição STL (Ponto de Viragem)", value=True)
mostrar_prophet = st.sidebar.checkbox("Prophet (Desvio da Previsão)", value=True)

# --- LAYOUT PRINCIPAL ---
st.title("🚨 Monitorização de Anomalias Macroeconómicas em Portugal")

# --- SISTEMA DE ALERTA ---
ultimo_ponto = df_final.iloc[-1]
if ultimo_ponto['contagem_anomalias'] > 0:
    st.error(f"**ALERTA:** Anomalia detetada no último trimestre disponível ({ultimo_ponto.name.strftime('%Y-%m-%d')})!")

st.markdown("Dashboard interativo para explorar anomalias em séries temporais económicas.")

# --- GRÁFICO PRINCIPAL ---
st.header(f"Análise Visual de Anomalias em: {lista_variaveis[variavel_selecionada_key]}")

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_final.index, y=df_final[variavel_selecionada_key], mode='lines', name=lista_variaveis[variavel_selecionada_key], line=dict(color='lightgrey', width=2)))

if mostrar_isoforest:
    df_anom = df_final[df_final['anomalia_isoforest'] == 1]
    fig.add_trace(go.Scatter(x=df_anom.index, y=df_anom[variavel_selecionada_key], mode='markers', name='Anomalia: Isolation Forest', marker=dict(color='red', size=10, symbol='circle')))
if mostrar_stl:
    df_anom = df_final[df_final['anomalia_stl'] == 1]
    fig.add_trace(go.Scatter(x=df_anom.index, y=df_anom[variavel_selecionada_key], mode='markers', name='Anomalia: STL', marker=dict(color='green', size=10, symbol='diamond')))
if mostrar_prophet:
    df_anom = df_final[df_final['anomalia_prophet'] == 1]
    fig.add_trace(go.Scatter(x=df_anom.index, y=df_anom[variavel_selecionada_key], mode='markers', name='Anomalia: Prophet', marker=dict(color='purple', size=10, symbol='x')))

df_consenso = df_final[df_final['contagem_anomalias'] > 1]
fig.add_trace(go.Scatter(x=df_consenso.index, y=df_consenso[variavel_selecionada_key], mode='markers', name='Consenso (≥2 modelos)', marker=dict(color='gold', size=16, symbol='star', line=dict(color='black', width=1))))

fig.update_layout(xaxis_title='Data', yaxis_title='Valor', legend_title='Legenda', template='plotly_white', height=500)
st.plotly_chart(fig, use_container_width=True)

# --- ANÁLISE ESCRITA E TABELA DE DADOS ---
with st.expander("Ver Análise Detalhada e Tabela de Anomalias"):
    st.header("Interpretação dos Modelos")
    st.markdown("""
    A análise combina três modelos distintos para uma deteção robusta:
    - **Isolation Forest (vermelho):** Deteta desequilíbrios na *relação* entre todas as variáveis. Ideal para encontrar anomalias sistémicas.
    - **Decomposição STL (verde):** Identifica pontos de viragem e choques em *cada variável individualmente*.
    - **Prophet (roxo):** Deteta anomalias ao comparar os dados reais do PIB com a sua *própria previsão*. É especialista em encontrar surpresas no crescimento económico.
    - **Consenso (dourado):** Pontos detetados por múltiplos modelos, representando os eventos mais extremos e inequívocos.
    """)

    st.header("Tabela Detalhada das Anomalias")
    df_comparativo = df_final[df_final['contagem_anomalias'] > 0].copy()
    colunas_tabela = ['pib', 'credito_empresas', 'credito_particulares', 'endividamento', 'anomalia_isoforest', 'anomalia_stl', 'anomalia_prophet', 'contagem_anomalias']
    st.dataframe(df_comparativo.sort_values(by=['contagem_anomalias', 'data'], ascending=[False, True])[colunas_tabela])
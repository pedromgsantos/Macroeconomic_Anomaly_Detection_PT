# Deteção de Anomalias na Macroeconomia Portuguesa

## 🎯 Objetivo

Este projeto visa desenvolver um sistema de deteção de anomalias para indicadores macroeconómicos de Portugal, utilizando dados públicos do BPstat. O objetivo é identificar períodos de comportamento atípico que possam sinalizar stress económico ou mudanças estruturais, contribuindo para uma análise mais robusta da estabilidade financeira.

## 📂 Fontes de Dados

Os dados utilizados são séries temporais obtidas junto do BPstat (Banco de Portugal) e abrangem os seguintes indicadores:

*   **PIB a preços de mercado (trimestral):** `pib_trimestral.csv`
*   **Crédito concedido a novas operações de empréstimos a empresas (mensal):** `credito_empresas.csv`
*   **Crédito concedido a novas operações de empréstimos a particulares (mensal):** `credito_particulares.csv`
*   **Endividamento do setor não financeiro (mensal):** `endividamento_setor_devedor.csv`

Todos os ficheiros de dados estão localizados na pasta `/data/`.

## 🧪 Pipeline de Análise

O projeto segue um pipeline estruturado de ciência de dados:

1.  **Análise Exploratória dos Dados (EDA):** Leitura, limpeza e visualização inicial das séries temporais para compreender as suas características (tendências, sazonalidade, etc.).
2.  **Pré-processamento e Feature Engineering:** Tratamento de dados em falta, alinhamento da frequência temporal (resampling) e normalização das séries para permitir a sua comparação.
3.  **Modelação e Deteção de Anomalias:** Aplicação e comparação de diferentes algoritmos, tais como:
    *   Decomposição STL (Seasonal-Trend decomposition using LOESS)
    *   Isolation Forest
    *   Facebook Prophet
    *   Autoencoders (opcional)
4.  **Visualização Interativa:** Desenvolvimento de um dashboard (provavelmente com Plotly Dash ou Streamlit) para explorar as séries temporais e as anomalias detetadas de forma interativa.
5.  **Análise de Resultados e Conclusões:** Interpretação das anomalias no contexto macroeconómico português e documentação dos insights obtidos.

## 🧱 Estrutura do Projeto

```
anomalias_macro_pt/
│
├── data/
│   ├── pib_trimestral.csv
│   ├── credito_empresas.csv
│   ├── credito_particulares.csv
│   └── endividamento_setor_devedor.csv
│
├── notebooks/
│   ├── 01_analise_exploratoria.ipynb
│   └── ...
│
├── src/
│   ├── data_preprocessing.py
│   └── anomaly_detection.py
│
├── results/
│   └── anomaly_periods.csv
│
├── .gitignore
└── README.md
```

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python
*   **Bibliotecas Principais:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, Plotly, Statsmodels.
*   **Ambiente:** Jupyter Notebooks / VS Code

---

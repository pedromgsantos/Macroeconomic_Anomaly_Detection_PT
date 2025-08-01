# Deteção de Anomalias na Macroeconomia Portuguesa

## 🎯 Objetivo

Este projeto visa desenvolver um sistema de deteção de anomalias para indicadores macroeconómicos de Portugal, utilizando dados públicos do BPstat. O objetivo é identificar períodos de comportamento atípico que possam sinalizar stress económico ou mudanças estruturais, culminando numa ferramenta de análise visual e interativa (dashboard) para explorar estes eventos.

## 📂 Fontes de Dados

Os dados utilizados são séries temporais obtidas junto do BPstat (Banco de Portugal) e abrangem os seguintes indicadores:

*   **PIB a preços de mercado (trimestral):** `pib_trimestral.csv`
*   **Crédito concedido a novas operações de empréstimos a empresas (mensal):** `credito_empresas.csv`
*   **Crédito concedido a novas operações de empréstimos a particulares (mensal):** `credito_particulares.csv`
*   **Endividamento do setor não financeiro (mensal):** `endividamento_setor_devedor.csv`

Todos os ficheiros de dados estão localizados na pasta `/data/`.

## 🧪 Pipeline de Análise

O projeto segue um pipeline estruturado de ciência de dados:

1.  **Análise Exploratória e Pré-processamento:** Leitura, limpeza e alinhamento da frequência temporal das séries. Os dados mensais foram agregados para uma frequência trimestral para se alinharem com o PIB. O resultado é o ficheiro `data/dados_processados_trimestrais.csv`.

2.  **Modelação e Deteção de Anomalias:** Foram aplicados três modelos complementares para uma deteção robusta:
    *   **Isolation Forest (Análise Sistémica):** Para detetar anomalias multivariadas, ou seja, desequilíbrios na *relação* entre todas as variáveis em simultâneo (ex: crises sistémicas).
    *   **Decomposição STL (Pontos de Viragem):** Para identificar anomalias univariadas em cada série, destacando choques súbitos ou pontos de viragem nos resíduos.
    *   **Prophet (Desvio da Previsão):** Para detetar anomalias no PIB quando o valor real se desvia significativamente do que era esperado pelo modelo de previsão.

3.  **Análise Comparativa e Visualização:** Os resultados dos três modelos foram consolidados e analisados. Foi desenvolvido um dashboard interativo com Streamlit para permitir a exploração visual das séries temporais e das anomalias detetadas.

## 🧱 Estrutura do Projeto

```
anomalias_macro_pt/
│
├── data/
│ ├── credito_empresas.csv # Dados brutos
│ ├── credito_particulares.csv # Dados brutos
│ ├── endividamento_setor_dev...csv # Dados brutos
│ ├── pib_trimestral.csv # Dados brutos
│ └── dados_processados_trimestrais.csv # Output do notebook 01
│
├── notebooks/
│ ├── 01_analise_exploratoria.ipynb # Limpeza e pré-processamento
│ ├── 02_modelagem_anomalias.ipynb # Aplicação dos modelos
│ └── 03_analise_comparativa.ipynb # Consolidação e análise dos resultados
│
├── .gitignore
├── app.py # Script principal do dashboard Streamlit
├── environment_dev.yml # Ficheiro para recriar o ambiente Conda
└── requirements.txt # Ficheiro para instalar dependências com Pip
```

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Python 3.9+
*   **Análise de Dados:** Pandas, NumPy, Statsmodels
*   **Machine Learning:** Scikit-learn (Isolation Forest), Prophet
*   **Visualização:** Matplotlib, Seaborn, Plotly
*   **Dashboard Interativo:** Streamlit
*   **Ambiente:** Jupyter Notebooks / VS Code
*   **Gestão de Dependências:** Conda, Pip

---

## 🚀 Como Executar Localmente

Para executar o dashboard interativo na sua máquina local, siga os passos abaixo.

### Pré-requisitos
*   Ter o [Conda](https://docs.conda.io/en/latest/miniconda.html) ou [Python](https://www.python.org/downloads/) instalado.
*   Git para clonar o repositório.

### Passos
1.  **Clonar o Repositório:**
    ```bash
    git clone https://github.com/pedromgsantos/anomalias_macro_pt
    cd anomalias_macro_pt
    ```

2.  **Configurar o Ambiente (Pip):**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Executar o Dashboard Streamlit:**
    Com o ambiente ativado, execute o seguinte comando no terminal:
    ```bash
    streamlit run app.py
    ```


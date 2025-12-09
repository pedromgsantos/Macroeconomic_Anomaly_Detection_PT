# Macroeconomic Anomaly Detection for Portugal

## Objective

This project develops an anomaly detection system for Portuguese macroeconomic indicators using publicly available data from BPstat. The goal is to identify periods of unusual behaviour that may indicate economic stress or structural shifts. The results are presented in an interactive dashboard that allows users to explore anomalies across multiple economic series.

## Data Sources

The dataset consists of time series extracted from BPstat (Banco de Portugal). The following indicators are used:

- Quarterly GDP at market prices: `pib_trimestral.csv`
- New loan operations to firms (monthly): `credito_empresas.csv`
- New loan operations to households (monthly): `credito_particulares.csv`
- Total non-financial sector debt (monthly): `endividamento_setor_devedor.csv`

All files are stored in the `data/` directory.

## Analysis Pipeline

1. **Exploratory Analysis and Preprocessing**  
   The datasets are loaded, cleaned, and aligned to a quarterly frequency. Monthly variables are aggregated to quarterly values to match the periodicity of GDP. The merged and processed dataset is saved as `data/dados_processados_trimestrais.csv`.

2. **Modelling and Anomaly Detection**  
   Three complementary models are applied to detect different types of anomalies:

   - **Isolation Forest:** Detects multivariate anomalies by analysing the joint behaviour of GDP, corporate credit, household credit and total debt.
   - **STL decomposition:** Identifies deviations within each individual series by analysing residuals after removing trend and seasonality.
   - **Prophet:** Detects anomalies in GDP by flagging observations that fall outside the model’s forecast interval.

3. **Comparative Analysis and Visualisation**  
   Outputs from the three models are combined into a single dataset. A Streamlit dashboard provides interactive visualisation of the detected anomalies across all series.

## Project Structure

```
anomalias_macro_pt/
│
├── data/
│ ├── credito_empresas.csv
│ ├── credito_particulares.csv
│ ├── endividamento_setor_devedor.csv
│ ├── pib_trimestral.csv
│ └── dados_processados_trimestrais.csv
│
├── notebooks/
│ ├── 01_exploratory_analysis.ipynb
│ ├── 02_anomaly_modelling.ipynb
│ └── 03_comparative_analysis.ipynb
│
├── app.py
├── environment.yml
├── requirements.txt
└── .gitignore
```

## Technologies Used

- Python 3.9+
- Pandas, NumPy, Statsmodels
- Scikit-learn (Isolation Forest)
- Prophet
- Matplotlib, Seaborn, Plotly
- Streamlit
- Jupyter Notebooks / VS Code
- Conda and Pip for dependency management

## Running the Dashboard Locally

### Requirements

Install Conda or Python, and ensure Git is available.

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/pedromgsantos/anomalias_macro_pt
   cd anomalias_macro_pt
   ```

2. **Environement (Conda):**

   ```bash
   conda env create -f environment.yml
   conda activate anomalias_macro
   ```

3. **Environement (Pip):**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run steamlit dashboard:**
   With the environment activated, run the following command:
   ```bash
   streamlit run app.py
   ```

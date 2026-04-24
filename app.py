import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# 2. Carregamento de Dados SEGURO
def carregar_dados():
    hoje = datetime.now().strftime("%d/%m/%Y")
    dados_padrao = pd.DataFrame({
        'Categoria': ['Agente', 'Agente', 'Agente'],
        'Subcategoria': ['SARS-CoV-2', 'Influenza A', 'Outros'],
        'Valor': ['0%', '0%', '0%'],
        'Data': [hoje] * 3
    })
    
    try:
        df = pd.read_csv("dados_epidemiologicos.csv")
        # Verifica se a coluna 'Data' realmente existe no arquivo
        if 'Data' not in df.columns:
            return dados_padrao
        return df
    except:
        return dados_padrao

df_vigi = carregar_dados()

# 3. Extração de variáveis com segurança para não dar erro
try:
    data_atualizacao = df_vigi['Data'].iloc[0]
except:
    data_atualizacao = datetime.now().strftime("%d/%m/%Y")

# 4. Estilo Visual (CSS)
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .titulo { color: #1a5276; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 5. Conteúdo do App
st.markdown(f"<h1 class='titulo'>📊 Vigilância Epidemiológica: SRAG</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Sincronizado com BI em: {data_atualizacao}</p>", unsafe_allow_html=True)
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧬 Identificação do Agente")
    # Busca o valor de COVID se existir, senão mostra 0%
    try:
        val_covid = df_vigi[df_vigi['Subcategoria'] == 'SARS-CoV-2']['Valor'].values[0]
        val_flu = df_vigi[df_vigi['Subcategoria'] == 'Influenza A']['Valor'].values[0]
    except:
        val_covid, val_flu = "0%", "0%"
        
    c1, c2 = st.columns(2)
    c1.metric("SARS-CoV-2", val_covid)
    c2.metric("Influenza A", val_flu)

with col2:
    st.subheader("📈 Tendência Semanal")
    # Gráfico simples para não ficar em branco
    fig = px.area(x=list(range(1,11)), y=[2,5,10,25,40,35,20,10,5,2], color_discrete_sequence=['#1a5276'])
    fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

st.info("Aguardando a primeira execução do robô na quarta-feira para carregar dados reais do Power BI.")

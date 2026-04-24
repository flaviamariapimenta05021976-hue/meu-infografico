import streamlit as st
import pandas as pd

# Configura o site
st.set_page_config(page_title="Infográfico Vigilância", layout="wide")

# Estilo para ficar parecido com a sua imagem original
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px #ddd; }
    </style>
""", unsafe_allow_html=True)

# Tenta ler os dados que o robô salvou
try:
    df = pd.read_csv("dados_epidemiologicos.csv")
    info = df.iloc[0]
except:
    info = {"data": "Sem dados", "srag_total": "0", "covid": "0%", "influenza": "0%"}

st.title("📊 Infográfico de Vigilância Epidemiológica")
st.info(f"Dados atualizados automaticamente em: {info['data']}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total de Casos SRAG", value=info['srag_total'])
    st.caption("Fonte: BI de Monitoramento - Aba SRAG")

with col2:
    st.metric(label="Predomínio COVID-19", value=info['covid'])
    st.caption("Fonte: BI de Monitoramento - Aba Agentes")

with col3:
    st.metric(label="Predomínio Influenza", value=info['influenza'])
    st.caption("Fonte: BI de Monitoramento - Aba Agentes")

st.divider()
st.markdown("---")
st.write("Configurado para atualização automática toda quarta-feira.")
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# ESTILO CSS PARA DESIGN PROFISSIONAL (QUADRANTES)
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stApp { max-width: 1400px; margin: 0 auto; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        height: 100%;
    }
    .titulo-principal {
        color: #1a5276;
        font-family: 'Arial Black', sans-serif;
        text-align: center;
        padding: 20px;
        background: white;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .secao-header {
        color: #1a5276;
        font-weight: bold;
        border-bottom: 2px solid #1a5276;
        padding-bottom: 5px;
        margin-bottom: 15px;
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# CARREGAMENTO DE DADOS
def carregar_dados():
    if os.path.exists("dados_epidemiologicos.csv"):
        return pd.read_csv("dados_epidemiologicos.csv").iloc[0]
    return {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "srag_total": "1.240", "covid": "68%", "flu_a": "12%", "flu_b": "5%", "rsv": "15%"
    }

dados = carregar_dados()

# HEADER
st.markdown(f"""
    <div class="titulo-principal">
        <h1>Vigilância Epidemiológica: Doenças Respiratórias</h1>
        <p style="color: gray; margin-bottom: 0;">SIVEP-Gripe | e-SUS | VIVVER — Última Atualização: {dados['data']}</p>
    </div>
""", unsafe_allow_html=True)

# LAYOUT EM QUADRANTES (2 COLUNAS x 2 LINHAS)
col_esq, col_dir = st.columns(2, gap="medium")

# --- QUADRANTE 1: MONITORAMENTO (SUPERIOR ESQUERDO) ---
with col_esq:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="secao-header">Monitoramento de Casos de SRAG</p>', unsafe_allow_html=True)
    
    q1_c1, q1_c2 = st.columns([1, 1.2])
    with q1_c1:
        st.write("**Perfil Epidemiológico**")
        st.image("análise por sexo.png", use_container_width=True)
        st.write("**Comorbidades**")
        st.image("comorbidades.png", use_container_width=True)
    
    with q1_c2:
        st.image("perfil epidemiologico.png", use_container_width=True)
    
    st.markdown("---")
    st.write("**Identificação do Agente Etiológico**")
    
    # Grid de Vírus
    v1, v2, v3, v4 = st.columns(4)
    v1.image("SARS_COV.png", caption=f"COVID: {dados['covid']}")
    v2.image("influenza A.png", caption=f"Flu A: {dados['flu_a']}")
    v3.image("influenza B.png", caption=f"Flu B: {dados['flu_b']}")
    v4.image("RSV.png", caption=f"RSV: {dados['rsv']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- QUADRANTE 2: GESTÃO (SUPERIOR DIREITO) ---
with col_dir:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="secao-header">Gestão e Localização do Atendimento</p>', unsafe_allow_html=True)
    
    st.write("**Capilaridade do Atendimento**")
    st.image("capilaridade.jpg", use_container_width=True)
    
    st.info("📍 Monitoramento em tempo real das UBS via sistema VIVVER.")
    st.markdown('</div>', unsafe_allow_html=True)

# SEGUNDA LINHA DE QUADRANTES
col_inf_esq, col_inf_dir = st.columns(2, gap="medium")

# --- QUADRANTE 3: TENDÊNCIA (INFERIOR ESQUERDO) ---
with col_inf_esq:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="secao-header">Tendência por Semana Epidemiológica</p>', unsafe_allow_html=True)
    
    # Gráfico interativo de tendência
    semanas = list(range(1, 16))
    casos = [12, 18, 45, 90, 160, 280, 420, 380, 250, 150, 90, 45, 20, 10, 5]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=semanas, y=casos, fill='tozeroy', line_color='#1a5276', name='Notificações'))
    fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- QUADRANTE 4: FONTES (INFERIOR DIREITO) ---
with col_inf_dir:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="secao-header">Ciclos Sazonais e Fontes Integradas</p>', unsafe_allow_html=True)
    
    c4_1, c4_2 = st.columns([1, 1])
    with c4_1:
        st.write("**Comparativo 2023/24**")
        # Pequeno gráfico de linhas
        st.line_chart([10, 20, 50, 40, 20], height=120)
    with c4_2:
        st.write("**Fontes Oficiais**")
        st.image("Fontes de informação integradas.jpg", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Subsecretaria de Saúde — Núcleo de Informação em Saúde (NIS)</p>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# 2. ESTILO CSS REFINADO (Dashboard Executivo)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stApp { max-width: 1280px; margin: 0 auto; }
    
    /* Cartões Modernos */
    .card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 16px;
    }
    
    /* Cabeçalho de Secção */
    .secao-header {
        color: #1e293b;
        font-weight: 800;
        font-size: 1.25rem;
        border-left: 5px solid #3b82f6;
        padding-left: 12px;
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Título do App */
    .titulo-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border-radius: 12px;
        margin-bottom: 30px;
    }
    
    .status-badge {
        background: #dbeafe;
        color: #1e40af;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 3. FUNÇÃO AUXILIAR PARA IMAGENS (Evita o ícone de erro quebrado)
def exibir_imagem(caminho, legenda=None, width=None):
    if os.path.exists(caminho):
        if width:
            st.image(caminho, caption=legenda, width=width)
        else:
            st.image(caminho, caption=legenda, use_container_width=True)
    else:
        # Se a imagem não existir, mostra um placeholder elegante
        st.info(f"Ficheiro '{caminho}' não encontrado no GitHub.")

# 4. CARREGAMENTO DE DADOS
def carregar_dados():
    if os.path.exists("dados_epidemiologicos.csv"):
        try:
            return pd.read_csv("dados_epidemiologicos.csv").iloc[0]
        except:
            pass
    return {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "srag_total": "1.240", "covid": "68%", "flu_a": "12%", "flu_b": "5%", "rsv": "15%"
    }

dados = carregar_dados()

# --- HEADER PRINCIPAL ---
st.markdown(f"""
    <div class="titulo-container">
        <h1 style='margin:0; font-size: 2.2rem;'>Vigilância Epidemiológica: SRAG e Síndrome Gripal</h1>
        <p style='opacity: 0.9; margin-top:10px;'>Monitoramento Integrado: SIVEP-Gripe | e-SUS | VIVVER</p>
        <span class="status-badge">Última Atualização: {dados['data']}</span>
    </div>
""", unsafe_allow_html=True)

# --- CORPO DO DASHBOARD ---
col_monitor, col_gestao = st.columns(2, gap="large")

# ==============================================================================
# QUADRANTE 1: MONITORAMENTO (ESQUERDA)
# ==============================================================================
with col_monitor:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="secao-header">Monitoramento de Casos de SRAG</p>', unsafe_allow_html=True)
    
    # Perfil e Imagem Central
    c1, c2 = st.columns([1, 1.3])
    with c1:
        st.write("**Perfil por Sexo**")
        exibir_imagem("análise por sexo.png")
        st.write("**Comorbidades**")
        exibir_imagem("comorbidades.png")
    
    with c2:
        exibir_imagem("perfil epidemiologico.png")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("**Identificação do Agente Etiológico**")
    
    # Linha de Agentes (Vírus)
    ca1, ca2 = st.columns([0.4, 1.6])
    with ca1:
        exibir_imagem("agente etiologico.png")
    with ca2:
        v1, v2, v3, v4 = st.columns(4)
        with v1: exibir_imagem("SARS_COV.png", legenda=f"COVID: {dados['covid']}")
        with v2: exibir_imagem("influenza A.png", legenda=f"Flu A: {dados['flu_a']}")
        with v3: exibir_imagem("influenza B.png", legenda=f"Flu B: {dados['flu_b']}")
        with v4: exibir_imagem("RSV.png", legenda=f"RSV: {dados['rsv']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Tendência Semanal (Abaixo do monitoramento)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="secao-header">Tendência por Semana Epidemiológica</p>', unsafe_allow_html=True)
    semanas = list(range(1, 17))
    notificacoes = [10, 15, 35, 70, 140, 260, 390, 420, 350, 210, 130, 80, 45, 25, 15, 10]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=semanas, y=notificacoes, fill='tozeroy', line_color='#2563eb', name='Casos'))
    fig.update_layout(height=220, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# QUADRANTE 2: GESTÃO (DIREITA)
# ==============================================================================
with col_gestao:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="secao-header">Gestão e Localização</p>', unsafe_allow_html=True)
    
    st.write("**Capilaridade do Atendimento**")
    exibir_imagem("capilaridade.jpg")
    
    st.info("📍 Monitoramento georreferenciado das UBS e Distritos Sanitários.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Ciclos e Fontes
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<p class="secao-header">Ciclos Sazonais e Fontes</p>', unsafe_allow_html=True)
    
    f1, f2 = st.columns(2)
    with f1:
        st.write("**Histórico 2023/24**")
        st.line_chart([10, 30, 90, 70, 20], height=150)
    with f2:
        st.write("**Fontes Integradas**")
        exibir_imagem("Fontes de informação integradas.jpg")
    
    st.markdown('</div>', unsafe_allow_html=True)

# RODAPÉ
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>Subsecretaria de Vigilância em Saúde — Núcleo de Informação em Saúde (NIS)</p>", unsafe_allow_html=True)

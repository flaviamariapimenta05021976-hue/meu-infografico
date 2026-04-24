import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# 2. ESTILO CSS AVANÇADO (Layout de Infográfico)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background-color: #f0f2f5;
    }
    
    /* Content wrapper */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Título Superior */
    .main-header {
        background-color: #1a5276;
        color: white;
        padding: 2.5rem;
        border-radius: 15px 15px 0 0;
        text-align: center;
        margin-bottom: 0;
    }
    
    /* Cartões de Conteúdo */
    .infographic-card {
        background-color: white;
        padding: 25px;
        border-radius: 0 0 15px 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #e1e4e8;
        min-height: 800px;
    }
    
    .section-title {
        color: #1a5276;
        font-size: 22px;
        font-weight: 700;
        border-bottom: 3px solid #1a5276;
        padding-bottom: 10px;
        margin-bottom: 25px;
        text-transform: uppercase;
    }
    
    .sub-title {
        font-weight: 700;
        color: #2c3e50;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Estilo para as métricas/percentagens */
    .stat-label {
        font-size: 0.85rem;
        font-weight: bold;
        text-align: center;
        color: #1a5276;
    }
    </style>
""", unsafe_allow_html=True)

# 3. FUNÇÃO PARA CARREGAR IMAGENS SEM ERRO VISUAL
def img(caminho, width=None):
    if os.path.exists(caminho):
        if width:
            st.image(caminho, width=width)
        else:
            st.image(caminho, use_container_width=True)
    else:
        st.markdown(f"<div style='border:1px dashed #ccc; padding:10px; text-align:center; color:#999;'>🖼️ {caminho}</div>", unsafe_allow_html=True)

# 4. DADOS
def carregar_dados():
    if os.path.exists("dados_epidemiologicos.csv"):
        try: return pd.read_csv("dados_epidemiologicos.csv").iloc[0]
        except: pass
    return {
        "data": datetime.now().strftime("%d/%m/%Y"),
        "covid": "68%", "flu_a": "12%", "flu_b": "5%", "rsv": "15%"
    }

dados = carregar_dados()

# --- ESTRUTURA DO INFOGRÁFICO ---

# Cabeçalho único
st.markdown(f"""
    <div class="main-header">
        <h1 style='margin:0; font-size: 2.5rem;'>Vigilância Epidemiológica</h1>
        <p style='margin:5px 0 0 0; opacity:0.8; font-size: 1.1rem;'>Doenças Respiratórias (SRAG e Síndrome Gripal)</p>
        <p style='margin:10px 0 0 0; font-weight:bold; font-size: 0.9rem;'>SIVEP-Gripe | e-SUS | VIVVER — Atualizado em: {dados['data']}</p>
    </div>
""", unsafe_allow_html=True)

# Container Principal (Branco)
with st.container():
    st.markdown('<div class="infographic-card">', unsafe_allow_html=True)
    
    col_monitor, col_gestao = st.columns(2, gap="large")
    
    # ==========================================================================
    # COLUNA ESQUERDA: MONITORIZAÇÃO
    # ==========================================================================
    with col_monitor:
        st.markdown('<div class="section-title">Monitorização de Casos de SRAG</div>', unsafe_allow_html=True)
        
        # Sub-bloco 1: Perfil e Imagem Central
        st.markdown('<p class="sub-title">Perfil Epidemiológico Detalhado</p>', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1.2])
        with c1:
            img("análise por sexo.png")
            st.markdown('<p class="sub-title" style="margin-top:20px;">Comorbilidades</p>', unsafe_allow_html=True)
            img("comorbidades.png")
        with c2:
            img("perfil epidemiologico.png")
            
        st.markdown("<hr style='margin:25px 0; border:0; border-top:1px solid #eee;'>", unsafe_allow_html=True)
        
        # Sub-bloco 2: Agentes Etiológicos
        st.markdown('<p class="sub-title">Identificação do Agente Etiológico</p>', unsafe_allow_html=True)
        ca1, ca2 = st.columns([0.4, 1.6])
        with ca1:
            img("agente etiologico.png")
        with ca2:
            # Grelha de 4 colunas para os vírus
            v1, v2, v3, v4 = st.columns(4)
            with v1: 
                img("SARS_COV.png")
                st.markdown(f"<p class='stat-label'>COVID<br>{dados['covid']}</p>", unsafe_allow_html=True)
            with v2: 
                img("influenza A.png")
                st.markdown(f"<p class='stat-label'>FLU A<br>{dados['flu_a']}</p>", unsafe_allow_html=True)
            with v3: 
                img("influenza B.png")
                st.markdown(f"<p class='stat-label'>FLU B<br>{dados['flu_b']}</p>", unsafe_allow_html=True)
            with v4: 
                img("RSV.png")
                st.markdown(f"<p class='stat-label'>RSV<br>{dados['rsv']}</p>", unsafe_allow_html=True)

        st.markdown("<hr style='margin:25px 0; border:0; border-top:1px solid #eee;'>", unsafe_allow_html=True)

        # Sub-bloco 3: Gráfico de Tendência
        st.markdown('<p class="sub-title">Tendência por Semana Epidemiológica</p>', unsafe_allow_html=True)
        semanas = list(range(1, 21))
        casos = [10, 15, 30, 65, 120, 240, 380, 410, 320, 200, 110, 70, 40, 20, 15, 10, 5, 2, 1, 1]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=semanas, y=casos, fill='tozeroy', line_color='#1a5276', name='Notificações'))
        fig.update_layout(height=230, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    # ==========================================================================
    # COLUNA DIREITA: GESTÃO
    # ==========================================================================
    with col_gestao:
        st.markdown('<div class="section-title">Gestão e Localização do Atendimento</div>', unsafe_allow_html=True)
        
        # Capilaridade
        st.markdown('<p class="sub-title">Capilaridade do Atendimento</p>', unsafe_allow_html=True)
        img("capilaridade.jpg")
        
        st.markdown("<div style='background-color:#eaf2f8; padding:15px; border-radius:8px; margin:20px 0; color:#1a5276; font-size:0.9rem;'>📍 Monitoramento georreferenciado de atendimentos distribuídos por distritos sanitários e unidades de saúde.</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin:25px 0; border:0; border-top:1px solid #eee;'>", unsafe_allow_html=True)

        # Ciclos Sazonais
        st.markdown('<p class="sub-title">Ciclos Sazonais e Fontes Integradas</p>', unsafe_allow_html=True)
        f1, f2 = st.columns([1, 1])
        with f1:
            st.write("**Histórico 2023 vs 2024**")
            st.line_chart([5, 15, 55, 110, 90, 40, 15], height=180)
        with f2:
            st.write("**Fluxo de Dados**")
            img("Fontes de informação integradas.jpg")
            
        st.markdown("<div style='height:120px;'></div>", unsafe_allow_html=True) # Espaçador

    st.markdown('</div>', unsafe_allow_html=True)

# RODAPÉ
st.markdown("""
    <div style='text-align:center; padding:20px; color:#666; font-size:0.8rem;'>
        Subsecretaria de Vigilância em Saúde — Núcleo de Informação em Saúde (NIS)<br>
        Relatório Gerado Automaticamente — Conteúdo de Carácter Informativo
    </div>
""", unsafe_allow_html=True)

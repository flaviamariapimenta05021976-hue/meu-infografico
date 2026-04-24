import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. Configuração da Página
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# 2. Estilo Visual (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .section-title { color: #1a5276; font-weight: bold; border-bottom: 2px solid #dee2e6; padding-bottom: 5px; margin-bottom: 20px; font-size: 24px; }
    </style>
""", unsafe_allow_html=True)

# 3. Cabeçalho
st.markdown("<h1 style='text-align: center;'>Vigilância Epidemiológica: Doenças Respiratórias (SRAG e Síndrome Gripal)</h1>", unsafe_allow_html=True)
st.write("---")

# 4. Divisão em Colunas
col_monitor, col_gestao = st.columns([1, 1], gap="large")

# --------------------------------------------------------------------------------
# COLUNA 1: MONITORAMENTO DE CASOS
# --------------------------------------------------------------------------------
with col_monitor:
    st.markdown("<div class='section-title'>Monitoramento de Casos de SRAG</div>", unsafe_allow_html=True)
    
    # Bloco Superior: Perfil e Humano Central
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("**Perfil Epidemiológico Detalhado**")
        st.image("análise por sexo.png", use_container_width=True)
        st.write("")
        st.markdown("**Comorbidades**")
        st.image("comorbidades.png", width=250)
    with c2:
        # Aqui usamos o perfil epidemiológico como imagem central (humano)
        st.image("perfil epidemiologico.png", use_container_width=True)

    # Bloco do Meio: Agente Etiológico
    st.write("---")
    st.markdown("**Identificação do Agente Etiológico**")
    ca1, ca2 = st.columns([0.4, 1.6])
    with ca1:
        st.image("agente etiologico.png", width=120)
    with ca2:
        # Organiza os ícones dos vírus em grelha
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.image("influenza A.png", caption="12%")
        with m2: st.image("influenza B.png", caption="5%")
        with m3: st.image("SARS_COV.png", caption="68%")
        with m4: st.image("RSV.png", caption="15%")

    # Bloco Inferior: Tendência (Gráfico Gerado por Código)
    st.write("---")
    st.markdown("**Tendência por Semana Epidemiológica**")
    semanas = list(range(1, 21))
    casos = [5, 12, 25, 50, 110, 200, 280, 260, 190, 120, 80, 45, 20, 10, 5, 3, 2, 1, 1, 1]
    fig_onda = go.Figure()
    fig_onda.add_trace(go.Scatter(x=semanas, y=casos, fill='tozeroy', line_color='#1a5276'))
    fig_onda.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_onda, use_container_width=True)

# --------------------------------------------------------------------------------
# COLUNA 2: GESTÃO E LOCALIZAÇÃO
# --------------------------------------------------------------------------------
with col_gestao:
    st.markdown("<div class='section-title'>Gestão e Localização do Atendimento</div>", unsafe_allow_html=True)
    
    # Capilaridade
    st.markdown("**Capilaridade do Atendimento**")
    st.image("capilaridade.jpg", use_container_width=True)

    # Ciclos Sazonais (Gráfico Gerado por Código para dinamismo)
    st.write("---")
    st.markdown("**Ciclos Sazonais (Comparativo)**")
    c_ano1, c_ano2 = st.columns(2)
    with c_ano1:
        st.caption("2023")
        st.line_chart([10, 25, 40, 35, 15], height=150)
    with c_ano2:
        st.caption("2024")
        st.line_chart([5, 20, 65, 55, 25], height=150)

    # Fontes de Informação
    st.write("---")
    st.markdown("**Fontes de Informação Integradas**")
    st.image("Fontes de informação integradas.jpg", use_container_width=True)

# Rodapé
st.divider()
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Dados extraídos automaticamente. NIS - Núcleo de Informação em Saúde.</p>", unsafe_allow_html=True)

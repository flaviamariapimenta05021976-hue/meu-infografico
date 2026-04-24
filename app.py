import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# Estilo CSS para imitar o layout profissional
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .header-box { text-align: center; padding: 10px; margin-bottom: 20px; }
    .section-title { color: #000000; font-weight: bold; border-bottom: 2px solid #dee2e6; padding-bottom: 10px; margin-bottom: 20px; font-size: 24px; }
    .footer-text { font-size: 12px; color: #6c757d; text-align: center; margin-top: 50px; }
    </style>
""", unsafe_allow_html=True)

# Título Principal
st.markdown("<h1 style='text-align: center;'>Vigilância Epidemiológica: Doenças Respiratórias (SRAG e Síndrome Gripal)</h1>", unsafe_allow_html=True)
st.write("---")

# Layout de duas colunas principais
col_monitoramento, col_gestao = st.columns([1, 1], gap="large")

# --------------------------------------------------------------------------------
# COLUNA 1: MONITORAMENTO DE CASOS
# --------------------------------------------------------------------------------
with col_monitoramento:
    st.markdown("<div class='section-title'>Monitoramento de Casos de SRAG</div>", unsafe_allow_html=True)
    
    # Perfil Epidemiológico e Imagem Central (Pulmão/Humano)
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("**Perfil Epidemiológico Detalhado**")
        st.caption("Análise de casos por sexo")
        # Gráfico de barras simples para sexo
        fig_sexo = px.bar(x=[55, 45], y=["Feminino", "Masculino"], orientation='h', height=150, color_discrete_sequence=['#5dade2'])
        fig_sexo.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sexo, use_container_width=True)
        
        st.markdown("**Comorbidades**")
        try: st.image("comorbidades.png", width=200)
        except: st.info("Suba 'comorbidades.png'")

    with c2:
        try: st.image("humano_central.png", use_container_width=True)
        except: st.info("Suba 'humano_central.png'")

    # Agentes Etiológicos
    st.write("---")
    st.markdown("**Identificação do Agente Etiológico**")
    ca1, ca2 = st.columns([0.5, 1.5])
    with ca1:
        try: st.image("microscopio.png", width=100)
        except: st.write("🔬")
    with ca2:
        # Métricas de agentes
        m1, m2 = st.columns(2)
        m1.metric("Influenza A", "12%", delta_color="normal")
        m2.metric("Influenza B", "5%")
        m3, m4 = st.columns(2)
        m3.metric("SARS-CoV-2", "68%")
        m4.metric("RSV", "15%")

    # Tendência por Semana
    st.write("---")
    st.markdown("**Tendência por Semana Epidemiológica**")
    semanas = list(range(1, 31))
    notificacoes = [5, 10, 20, 50, 120, 250, 300, 280, 200, 100, 50, 20] + [10]*18
    fig_onda = go.Figure()
    fig_onda.add_trace(go.Scatter(x=semanas, y=notificacoes, fill='tozeroy', name='Notificações', line_color='#2e86c1'))
    fig_onda.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_onda, use_container_width=True)

# --------------------------------------------------------------------------------
# COLUNA 2: GESTÃO E LOCALIZAÇÃO
# --------------------------------------------------------------------------------
with col_gestao:
    st.markdown("<div class='section-title'>Gestão e Localização do Atendimento</div>", unsafe_allow_html=True)
    
    # Capilaridade (Mapa das UBS)
    st.markdown("**Capilaridade do Atendimento**")
    st.caption("Monitoramento de atendimentos distribuídos por distritos sanitários e UBS.")
    try: st.image("mapa_ubs.png", use_container_width=True)
    except: st.info("Suba 'mapa_ubs.png'")

    # Ciclos Sazonais
    st.write("---")
    st.markdown("**Ciclos Sazonais 2023/24**")
    try: st.image("ciclos_sazonais.png", use_container_width=True)
    except:
        c1, c2 = st.columns(2)
        c1.line_chart([10, 20, 50, 40, 20])
        c2.line_chart([5, 15, 80, 60, 30])

    # Fontes de Informação
    st.write("---")
    st.markdown("**Fontes de Informação Integradas**")
    try: st.image("fontes_integradas.png", use_container_width=True)
    except: st.success("SIVEP-Gripe + e-SUS + VIVVER")

# Rodapé
st.markdown("<div class='footer-text'>Consolidação de dados provenientes do SIVEP-Gripe, e-SUS e sistema VIVVER.</div>", unsafe_allow_html=True)

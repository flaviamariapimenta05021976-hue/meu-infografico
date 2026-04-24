import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# 1. CONFIGURAÇÃO DA PÁGINA (OTIMIZADA PARA DASHBOARD EXECUTIVO)
st.set_page_config(page_title="Vigilância Epidemiológica - Infográfico Semanal", layout="wide")

# 2. DESIGN SYSTEM E UX DESIGN (CSS AVANÇADO)
# Paleta: Marinho Institucional (#002147), Azul Saúde (#3498db), Alerta Laranja (#FF8C00)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: #f4f7f6;
    }
    
    .main-infographic {
        background-color: white;
        padding: 40px;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        border: 1px solid #e0e6ed;
    }

    .header-banner {
        background: linear-gradient(135deg, #002147 0%, #1a5276 100%);
        color: white;
        padding: 30px;
        border-radius: 20px 20px 0 0;
        text-align: center;
        border-bottom: 5px solid #FF8C00;
    }

    .section-header {
        color: #002147;
        font-size: 20px;
        font-weight: 900;
        border-left: 6px solid #FF8C00;
        padding-left: 15px;
        margin-bottom: 25px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        text-align: center;
    }

    .top5-item {
        background: #ffffff;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 8px;
        border-left: 4px solid #3498db;
        display: flex;
        justify-content: space-between;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .footer {
        text-align: center;
        padding: 30px;
        font-size: 13px;
        color: #7f8c8d;
        background: #ffffff;
        margin-top: 20px;
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. ENGINE DE DADOS (INTEGRAÇÃO SIVEP / e-SUS / VIVVER)
def load_surveillance_data():
    # Simulando processamento de bases SIVEP, e-SUS e VIVVER
    hoje = "23 de Abril de 2026"
    
    # Ranking Top 5 Prevalência (Mock data baseado em carga assistencial VIVVER)
    top_5_data = [
        {"unidade": "Hospital Municipal Central", "casos": 142},
        {"unidade": "UPA Distrito Norte", "casos": 98},
        {"unidade": "UBS Vila Esperança", "casos": 76},
        {"unidade": "Hospital Regional Sul", "casos": 65},
        {"unidade": "UBS Jardim Glória", "casos": 54}
    ]
    
    return {
        "data_extracao": hoje,
        "total_srag": 1240,
        "prev_covid": "64%",
        "prev_flu": "18%",
        "top5": top_5_data
    }

data = load_surveillance_data()

# 4. FUNÇÃO DE RENDERIZAÇÃO DE IMAGENS INSTITUCIONAIS
def render_institutional_img(path, width=None):
    if os.path.exists(path):
        st.image(path, width=width, use_container_width=(width is None))
    else:
        st.markdown(f"<div style='background:#eee; padding:20px; border-radius:10px; text-align:center;'>[Imagem: {path}]</div>", unsafe_allow_html=True)

# --- INÍCIO DO INFOGRÁFICO ---

# CABEÇALHO
st.markdown(f"""
    <div class="header-banner">
        <h1 style='margin:0; font-size: 2.4rem; letter-spacing: -1px;'>INFORME SEMANAL DE VIGILÂNCIA</h1>
        <p style='margin:5px 0 0 0; opacity:0.9; font-size: 1.2rem;'>Monitoramento de Doenças Respiratórias (SRAG e SG)</p>
        <div style='margin-top:15px;'><span style='background:#FF8C00; color:white; padding:5px 15px; border-radius:20px; font-weight:bold;'>ATUALIZADO EM: {data['data_extracao']}</span></div>
    </div>
""", unsafe_allow_html=True)

# CONTAINER PRINCIPAL
with st.container():
    st.markdown('<div class="main-infographic">', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2, gap="large")

    # ==========================================================================
    # LADO ESQUERDO: MONITORAMENTO SRAG (SIVEP + e-SUS)
    # ==========================================================================
    with col_left:
        st.markdown('<p class="section-header">Monitoramento de SRAG</p>', unsafe_allow_html=True)
        
        # Grid Perfil
        c1, c2 = st.columns([1, 1.2])
        with c1:
            st.markdown("🔍 **Perfil por Sexo**")
            render_institutional_img("análise por sexo.png")
            st.markdown("<br>🩺 **Comorbidades**", unsafe_allow_html=True)
            render_institutional_img("comorbidades.png")
        with c2:
            render_institutional_img("perfil epidemiologico.png")

        st.markdown("---")
        
        # Identificação de Agentes
        st.markdown("🧬 **Agentes Etiológicos Identificados**")
        v1, v2, v3, v4 = st.columns(4)
        with v1: 
            render_institutional_img("SARS_COV.png")
            st.markdown(f"<p style='text-align:center; font-weight:bold; color:#002147;'>COVID<br>{data['prev_covid']}</p>", unsafe_allow_html=True)
        with v2: 
            render_institutional_img("influenza A.png")
            st.markdown(f"<p style='text-align:center; font-weight:bold; color:#002147;'>FLU A<br>{data['prev_flu']}</p>", unsafe_allow_html=True)
        with v3: 
            render_institutional_img("influenza B.png")
            st.markdown(f"<p style='text-align:center; font-weight:bold; color:#002147;'>FLU B<br>5%</p>", unsafe_allow_html=True)
        with v4: 
            render_institutional_img("RSV.png")
            st.markdown(f"<p style='text-align:center; font-weight:bold; color:#002147;'>VSR<br>13%</p>", unsafe_allow_html=True)

        st.markdown("---")
        
        # Gráfico de Tendência (Plotly Area Chart)
        st.markdown("📈 **Tendência por Semana Epidemiológica**")
        semanas = list(range(1, 16))
        casos_srag = [15, 22, 45, 98, 160, 245, 380, 410, 320, 210, 130, 75, 40, 20, 10]
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=semanas, y=casos_srag, fill='tozeroy', 
            line=dict(color='#002147', width=3),
            fillcolor='rgba(52, 152, 219, 0.2)',
            name='Casos SRAG'
        ))
        fig_trend.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), plot_bgcolor='white', xaxis_title="Semana Epi", yaxis_title="Notificações")
        st.plotly_chart(fig_trend, use_container_width=True)

    # ==========================================================================
    # LADO DIREITO: GESTÃO TERRITORIAL (VIVVER)
    # ==========================================================================
    with col_right:
        st.markdown('<p class="section-header">Gestão Territorial e Carga</p>', unsafe_allow_html=True)
        
        # Capilaridade
        st.markdown("📍 **Capilaridade e Dispersão Geográfica**")
        render_institutional_img("capilaridade.jpg")
        
        # TOP 5 UNIDADES (RANKING)
        st.markdown("<br>🏆 **Top 5 Unidades com Maior Prevalência**", unsafe_allow_html=True)
        for i, item in enumerate(data['top5']):
            st.markdown(f"""
                <div class="top5-item">
                    <span><b>{i+1}º</b> {item['unidade']}</span>
                    <span style='color:#1a5276; font-weight:bold;'>{item['casos']} atendimentos</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Ciclos Sazonais
        st.markdown("❄️ **Ciclos Sazonais Comparativos: 2023 vs 2024**")
        # Gráfico comparativo
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul']
        fig_sazonal = go.Figure()
        fig_sazonal.add_trace(go.Scatter(x=meses, y=[10, 20, 60, 120, 200, 180, 140], name='2023', line=dict(dash='dash', color='#bdc3c7')))
        fig_sazonal.add_trace(go.Scatter(x=meses, y=[15, 35, 85, 160, 250, 220, 190], name='2024', line=dict(width=4, color='#FF8C00')))
        fig_sazonal.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_sazonal, use_container_width=True)

        st.markdown("---")
        st.markdown("🔗 **Integração de Fluxos**")
        render_institutional_img("Fontes de informação integradas.jpg")

    st.markdown('</div>', unsafe_allow_html=True)

# RODAPÉ INSTITUCIONAL
st.markdown(f"""
    <div class="footer">
        <p><b>Créditos:</b> NIS (Núcleo de Informação em Saúde) | DIVEPI (Diretoria de Vigilância Epidemiológica) | CIEVS</p>
        <p style='margin-top:5px;'>Relatório Automático Gerado para Subsecretaria de Saúde — {data['data_extracao']}</p>
        <p style='color:#bdc3c7; font-size:10px;'>Código Ref: Surveillance_V4_2026</p>
    </div>
""", unsafe_allow_html=True)

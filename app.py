"""
Infográfico Epidemiológico para Streamlit Cloud
Vigilância de Doenças Respiratórias - Subsecretaria de Saúde
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Vigilância Epidemiológica - SRAG",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DESIGN SYSTEM E CSS PERSONALIZADO
# ============================================================================
st.markdown("""
    <style>
    /* Importação de fontes modernas */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&family=Open+Sans:wght@400;600;700&display=swap');
    
    /* Reset e estilo base */
    .stApp {
        background: linear-gradient(135deg, #f0f7fa 0%, #e8f0f5 100%);
        font-family: 'Roboto', 'Open Sans', sans-serif;
    }
    
    /* Container principal do infográfico */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Header institucional */
    .header-banner {
        background: linear-gradient(135deg, #002147 0%, #0a3d62 100%);
        color: white;
        padding: 35px;
        border-radius: 20px 20px 0 0;
        text-align: center;
        border-bottom: 5px solid #FF8C00;
        margin-bottom: 0;
    }
    
    .header-banner h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }
    
    .header-banner p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 10px;
    }
    
    .update-badge {
        display: inline-block;
        background: #FF8C00;
        padding: 8px 25px;
        border-radius: 30px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 15px;
    }
    
    /* Container do conteúdo principal */
    .content-container {
        background: white;
        padding: 30px;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Títulos das seções */
    .section-title {
        color: #002147;
        font-size: 1.3rem;
        font-weight: 700;
        border-left: 5px solid #FF8C00;
        padding-left: 15px;
        margin: 25px 0 20px 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .section-subtitle {
        color: #0a3d62;
        font-size: 1rem;
        font-weight: 600;
        margin: 15px 0 10px 0;
        padding-left: 10px;
        border-left: 3px solid #3498db;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e0e6ed;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,33,71,0.1);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #002147;
    }
    
    .metric-label {
        font-size: 0.85rem;
        color: #7f8c8d;
        margin-top: 5px;
    }
    
    /* Lista de comorbidades */
    .comorb-list {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
    }
    
    .comorb-item {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #e0e6ed;
    }
    
    .comorb-item:last-child {
        border-bottom: none;
    }
    
    .comorb-name {
        font-weight: 500;
        color: #2c3e50;
    }
    
    .comorb-bar {
        background: #3498db;
        height: 8px;
        border-radius: 4px;
        margin: 5px 0;
        transition: width 0.5s ease;
    }
    
    .comorb-percent {
        font-weight: 700;
        color: #FF8C00;
    }
    
    /* Ranking Top 5 */
    .top5-item {
        background: #ffffff;
        padding: 12px 18px;
        margin-bottom: 10px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-left: 4px solid #3498db;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.2s;
    }
    
    .top5-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .top5-rank {
        font-size: 1.2rem;
        font-weight: 700;
        color: #FF8C00;
        width: 40px;
    }
    
    .top5-name {
        flex: 1;
        font-weight: 500;
        color: #2c3e50;
    }
    
    .top5-value {
        font-weight: 800;
        color: #002147;
        font-size: 1.1rem;
    }
    
    .top5-unit {
        font-size: 0.75rem;
        color: #7f8c8d;
        margin-left: 5px;
    }
    
    /* Distritos */
    .distrito-item {
        background: #f8f9fa;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-right: 3px solid #3498db;
    }
    
    .distrito-name {
        font-weight: 600;
        color: #002147;
    }
    
    .distrito-stats {
        font-size: 0.8rem;
        color: #7f8c8d;
    }
    
    .distrito-value {
        font-weight: 700;
        color: #3498db;
        font-size: 1.2rem;
    }
    
    /* Footer */
    .footer {
        background: #f8f9fa;
        padding: 25px;
        text-align: center;
        border-radius: 15px;
        margin-top: 30px;
        border-top: 1px solid #e0e6ed;
    }
    
    .footer p {
        margin: 5px 0;
        font-size: 0.8rem;
        color: #7f8c8d;
    }
    
    .footer strong {
        color: #002147;
    }
    
    hr {
        margin: 20px 0;
        border: none;
        border-top: 2px solid #ecf0f1;
    }
    
    /* Badges */
    .alert-badge {
        display: inline-block;
        background: #fee5e5;
        color: #e74c3c;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-left: 10px;
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .header-banner h1 { font-size: 1.5rem; }
        .section-title { font-size: 1.1rem; }
        .metric-value { font-size: 1.8rem; }
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÃO PARA CARREGAR DADOS (SIMULADOS - SUBSTITUIR POR LEITURA REAL)
# ============================================================================
@st.cache_data(ttl=3600)  # Cache de 1 hora
def load_data():
    """
    Carrega e processa dados das bases SIVEP-Gripe, e-SUS e VIVVER
    Substituir pela leitura real dos CSVs/Excel quando disponíveis
    """
    
    data_atual = datetime.now()
    
    # Dados simulados baseados em tendências reais
    dados = {
        "data_extracao": data_atual.strftime("%d de %B de %Y"),
        "data_hora": data_atual.strftime("%d/%m/%Y %H:%M"),
        
        # Totais consolidados
        "total_srag": 1247,
        "total_atendimentos": 4850,
        "ocupacao_uti": 68,
        "obitos": 38,
        
        # Tendência por semana epidemiológica (últimas 16 semanas)
        "semanas_epi": list(range(1, 17)),
        "casos_srag_semanal": [12, 18, 25, 42, 78, 125, 198, 267, 310, 345, 398, 420, 445, 432, 398, 345],
        
        # Ciclos sazonais
        "meses": ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        "casos_2023": [45, 52, 68, 95, 142, 198, 245, 267, 234, 189, 145, 98],
        "casos_2024": [38, 48, 72, 112, 168, 235, 289, 312, 278, 225, 178, 124],
        
        # Agentes etiológicos
        "agentes": {
            "SARS-CoV-2 (COVID-19)": 64,
            "Influenza A": 18,
            "Influenza B": 5,
            "VSR": 8,
            "Outros": 5
        },
        
        # Comorbidades
        "comorbidades": {
            "Cardiopatia": 32,
            "Diabetes Mellitus": 28,
            "Pneumopatia": 18,
            "Imunossupressão": 12,
            "Obesidade": 10
        },
        
        # Perfil demográfico
        "perfil_sexo": {"Masculino": 52, "Feminino": 48},
        "perfil_idade": {
            "0-4 anos": 8,
            "5-17 anos": 12,
            "18-39 anos": 25,
            "40-59 anos": 30,
            "60+ anos": 25
        },
        
        # Top 5 Unidades com maior prevalência (VIVVER)
        "top5_unidades": [
            {"rank": 1, "nome": "Hospital Municipal Central", "casos": 342, "tipo": "Hospital"},
            {"rank": 2, "nome": "UPA Distrito Norte", "casos": 287, "tipo": "UPA"},
            {"rank": 3, "nome": "UBS Vila Esperança", "casos": 198, "tipo": "UBS"},
            {"rank": 4, "nome": "Hospital Regional Sul", "casos": 176, "tipo": "Hospital"},
            {"rank": 5, "nome": "UBS Jardim Glória", "casos": 145, "tipo": "UBS"}
        ],
        
        # Capilaridade por distrito
        "distritos": [
            {"nome": "Centro", "ubs": 8, "atendimentos": 1250, "cobertura": 92},
            {"nome": "Norte", "ubs": 6, "atendimentos": 980, "cobertura": 85},
            {"nome": "Sul", "ubs": 5, "atendimentos": 875, "cobertura": 78},
            {"nome": "Leste", "ubs": 4, "atendimentos": 645, "cobertura": 70},
            {"nome": "Oeste", "ubs": 7, "atendimentos": 1120, "cobertura": 88}
        ],
        
        # Tendência percentual
        "tendencia_percentual": 12.5  # aumento percentual em relação à semana anterior
    }
    
    return dados

# ============================================================================
# FUNÇÕES DE GRÁFICOS PLOTLY
# ============================================================================
def grafico_tendencia_srag(dados):
    """Gráfico de área para tendência de SRAG"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dados["semanas_epi"],
        y=dados["casos_srag_semanal"],
        mode='lines+markers',
        name='Casos SRAG',
        fill='tozeroy',
        line=dict(color='#002147', width=3),
        fillcolor='rgba(52, 152, 219, 0.25)',
        marker=dict(size=8, color='#3498db', symbol='circle'),
        hovertemplate='<b>Semana %{x}</b><br>Casos: %{y:,}<extra></extra>'
    ))
    
    # Linha de tendência
    z = np.polyfit(dados["semanas_epi"], dados["casos_srag_semanal"], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=dados["semanas_epi"],
        y=p(dados["semanas_epi"]),
        mode='lines',
        name='Tendência',
        line=dict(color='#FF8C00', width=2, dash='dash'),
        opacity=0.7
    ))
    
    # Linha de alerta
    fig.add_hline(y=350, line_dash="dash", line_color="#e74c3c",
                  annotation_text="🚨 Nível de Alerta", 
                  annotation_position="top right",
                  annotation_font=dict(size=10, color="#e74c3c"))
    
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=30, b=30),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Roboto, Open Sans", size=11, color="#2c3e50"),
        xaxis=dict(
            title="<b>Semana Epidemiológica</b>",
            showgrid=True,
            gridcolor='#ecf0f1',
            tickmode='linear',
            tick0=1,
            dtick=2
        ),
        yaxis=dict(
            title="<b>Número de Notificações</b>",
            showgrid=True,
            gridcolor='#ecf0f1'
        ),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig


def grafico_ciclos_sazonais(dados):
    """Gráfico comparativo de ciclos sazonais"""
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dados["meses"],
        y=dados["casos_2023"],
        mode='lines+markers',
        name='2023',
        line=dict(color='#95a5a6', width=2, dash='dot'),
        marker=dict(size=6, color='#95a5a6', symbol='diamond'),
        hovertemplate='<b>%{x}/2023</b><br>Casos: %{y:,}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=dados["meses"],
        y=dados["casos_2024"],
        mode='lines+markers',
        name='2024',
        line=dict(color='#FF8C00', width=3),
        marker=dict(size=8, color='#FF8C00', symbol='circle'),
        hovertemplate='<b>%{x}/2024</b><br>Casos: %{y:,}<extra></extra>'
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=40, r=40, t=30, b=30),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Roboto, Open Sans", size=11, color="#2c3e50"),
        xaxis=dict(title="<b>Mês</b>", showgrid=False),
        yaxis=dict(title="<b>Casos Notificados</b>", showgrid=True, gridcolor='#ecf0f1'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode='x unified'
    )
    
    return fig


def grafico_agentes_etiológicos(dados):
    """Gráfico de rosca para agentes etiológicos"""
    
    labels = list(dados["agentes"].keys())
    values = list(dados["agentes"].values())
    colors = ['#1a5276', '#2471a3', '#2e86c1', '#3498db', '#85c1e9']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.45,
        marker=dict(colors=colors, line=dict(color='white', width=2)),
        textinfo='label+percent',
        textposition='auto',
        textfont=dict(size=10, color='white', weight='bold'),
        hovertemplate='<b>%{label}</b><br>Percentual: %{percent}<br>Valor: %{value}%<extra></extra>'
    )])
    
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='white',
        font=dict(family="Roboto, Open Sans", size=11),
        showlegend=False
    )
    
    return fig


def grafico_top5_unidades(dados):
    """Gráfico de barras horizontal para Top 5 unidades"""
    
    unidades = [u["nome"] for u in dados["top5_unidades"]]
    casos = [u["casos"] for u in dados["top5_unidades"]]
    cores = ['#1a5276', '#2471a3', '#2e86c1', '#3498db', '#5dade2']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=casos,
        y=unidades,
        orientation='h',
        marker=dict(
            color=cores,
            line=dict(color='white', width=2),
            gradient=dict(type='vertical')
        ),
        text=casos,
        textposition='outside',
        textfont=dict(size=12, color='#1a5276', weight='bold'),
        hovertemplate='<b>%{y}</b><br>Atendimentos: %{x:,}<extra></extra>'
    ))
    
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=80, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Roboto, Open Sans", size=11),
        xaxis_title="<b>Número de Atendimentos</b>",
        yaxis_title=None,
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11))
    )
    
    return fig

# ============================================================================
# CARREGAR DADOS
# ============================================================================
dados = load_data()

# ============================================================================
# CONTEÚDO PRINCIPAL
# ============================================================================

# HEADER
st.markdown(f"""
    <div class="main-container">
        <div class="header-banner">
            <h1>📊 INFORME SEMANAL DE VIGILÂNCIA EPIDEMIOLÓGICA</h1>
            <p>Monitoramento Integrado de Doenças Respiratórias | SRAG e Síndromes Gripais</p>
            <div class="update-badge">
                🗓️ ATUALIZADO EM: {dados['data_extracao'].upper()}
            </div>
        </div>
        <div class="content-container">
""", unsafe_allow_html=True)

# ============================================================================
# MÉTRICAS PRINCIPAIS (TOP DASHBOARD)
# ============================================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dados['total_srag']:,}</div>
            <div class="metric-label">🏥 Internações por SRAG</div>
            <div style="font-size:12px; color:#27ae60; margin-top:5px;">⬆️ +{dados['tendencia_percentual']}% vs semana anterior</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dados['ocupacao_uti']}%</div>
            <div class="metric-label">🛏️ Ocupação de UTIs</div>
            <div style="font-size:12px; color:#e74c3c;">{'🔴 Nível crítico' if dados['ocupacao_uti'] > 70 else '🟡 Atenção'}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dados['total_atendimentos']:,}</div>
            <div class="metric-label">🏥 Atendimentos (últimos 7 dias)</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{dados['obitos']}</div>
            <div class="metric-label">⚠️ Óbitos confirmados</div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# COLUNAS PRINCIPAIS: MONITORAMENTO SRAG (ESQUERDA) | GESTÃO TERRITORIAL (DIREITA)
# ============================================================================
col_left, col_right = st.columns(2, gap="large")

# ============================================================================
# LADO ESQUERDO: MONITORAMENTO DE SRAG
# ============================================================================
with col_left:
    st.markdown('<div class="section-title">🔬 MONITORAMENTO DE SRAG</div>', unsafe_allow_html=True)
    
    # Perfil demográfico em cards
    st.markdown('<div class="section-subtitle">👥 Perfil Demográfico</div>', unsafe_allow_html=True)
    
    col_sexo, col_idade = st.columns(2)
    
    with col_sexo:
        st.markdown(f"""
            <div style="background:#f8f9fa; padding:15px; border-radius:12px; text-align:center;">
                <div style="font-size:2rem;">👨 👩</div>
                <div><strong>Masculino:</strong> {dados['perfil_sexo']['Masculino']}%</div>
                <div><strong>Feminino:</strong> {dados['perfil_sexo']['Feminino']}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_idade:
        idade_text = "<br>".join([f"{k}: {v}%" for k, v in dados['perfil_idade'].items()])
        st.markdown(f"""
            <div style="background:#f8f9fa; padding:15px; border-radius:12px;">
                <strong>📊 Distribuição etária:</strong><br>
                {idade_text}
            </div>
        """, unsafe_allow_html=True)
    
    # Comorbidades
    st.markdown('<div class="section-subtitle">🩺 Comorbidades Associadas</div>', unsafe_allow_html=True)
    
    comorb_html = '<div class="comorb-list">'
    for nome, percent in dados['comorbidades'].items():
        comorb_html += f"""
            <div class="comorb-item">
                <span class="comorb-name">{nome}</span>
                <span class="comorb-percent">{percent}%</span>
            </div>
            <div class="comorb-bar" style="width: {percent}%;"></div>
        """
    comorb_html += '</div>'
    st.markdown(comorb_html, unsafe_allow_html=True)
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # Agentes Etiológicos
    st.markdown('<div class="section-subtitle">🧬 Agentes Etiológicos Identificados</div>', unsafe_allow_html=True)
    
    fig_agentes = grafico_agentes_etiológicos(dados)
    st.plotly_chart(fig_agentes, use_container_width=True)
    
    # Gráfico de Tendência
    st.markdown('<div class="section-subtitle">📈 Tendência por Semana Epidemiológica</div>', unsafe_allow_html=True)
    
    fig_tendencia = grafico_tendencia_srag(dados)
    st.plotly_chart(fig_tendencia, use_container_width=True)

# ============================================================================
# LADO DIREITO: GESTÃO TERRITORIAL
# ============================================================================
with col_right:
    st.markdown('<div class="section-title">🏥 GESTÃO TERRITORIAL E CARGA ASSISTENCIAL</div>', unsafe_allow_html=True)
    
    # Top 5 Unidades
    st.markdown('<div class="section-subtitle">⭐ Top 5 Unidades com Maior Prevalência</div>', unsafe_allow_html=True)
    
    # Usar gráfico de barras do Plotly
    fig_top5 = grafico_top5_unidades(dados)
    st.plotly_chart(fig_top5, use_container_width=True)
    
    # Capilaridade por Distrito
    st.markdown('<div class="section-subtitle">📍 Capilaridade por Distrito</div>', unsafe_allow_html=True)
    
    for distrito in dados['distritos']:
        st.markdown(f"""
            <div class="distrito-item">
                <div>
                    <div class="distrito-name">{distrito['nome']}</div>
                    <div class="distrito-stats">
                        🏥 {distrito['ubs']} UBS | 👥 {distrito['atendimentos']:,} atend. | 📊 {distrito['cobertura']}% cobertura
                    </div>
                </div>
                <div class="distrito-value">
                    {distrito['ubs']} 🏛️
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # Ciclos Sazonais
    st.markdown('<div class="section-subtitle">❄️ Ciclos Sazonais Comparativos</div>', unsafe_allow_html=True)
    
    fig_ciclos = grafico_ciclos_sazonais(dados)
    st.plotly_chart(fig_ciclos, use_container_width=True)
    
    st.markdown('<hr>', unsafe_allow_html=True)
    
    # Integração de Fluxos
    st.markdown("""
        <div style="background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%); 
                    padding: 20px; border-radius: 15px; text-align: center; margin-top: 20px;">
            <div style="font-size: 2rem; margin-bottom: 10px;">🔄</div>
            <div style="font-weight: 700; color: #002147; margin-bottom: 5px;">INTEGRAÇÃO DE FLUXOS ASSISTENCIAIS</div>
            <div style="font-size: 0.85rem; color: #2c3e50;">SIVEP-Gripe | e-SUS | VIVVER</div>
            <div style="font-size: 0.75rem; color: #7f8c8d; margin-top: 10px;">
                ✅ Dados consolidados em tempo real<br>
                📊 Monitoramento contínuo da situação epidemiológica
            </div>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# FOOTER INSTITUCIONAL
# ============================================================================
st.markdown(f"""
    <div class="footer">
        <p><strong>📋 CRÉDITOS INSTITUCIONAIS</strong></p>
        <p>
            <strong>NIS</strong> (Núcleo de Informação em Saúde) | 
            <strong>DIVEPI</strong> (Diretoria de Vigilância Epidemiológica) | 
            <strong>CIEVS</strong> (Centro de Informações Estratégicas)
        </p>
        <p>📅 Gerado automaticamente em {dados['data_hora']} | Subsecretaria de Saúde</p>
        <p style="font-size: 0.7rem; color: #bdc3c7;">Sistema de Vigilância Epidemiológica v2.0 - Dados oficiais do município</p>
    </div>
""", unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# ============================================================================
# BARRA LATERAL COM INFORMAÇÕES ADICIONAIS
# ============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/coronavirus.png", width=60)
    st.markdown("## 📋 Sobre o Sistema")
    st.markdown("""
    **Fontes de Dados Integradas:**
    - 🏥 SIVEP-Gripe (Casos Graves)
    - 🩺 e-SUS (Casos Leves)
    - 📊 VIVVER (Atendimentos Clínicos)
    
    ---
    **Legendas:**
    - 🔴 **Alerta Crítico** (>350 casos/semana)
    - 🟡 **Atenção** (250-350 casos)
    - 🟢 **Controle** (<250 casos)
    
    ---
    **Próxima atualização:**
    {}
    """.format((datetime.now().replace(day=datetime.now().day + 7)).strftime("%d/%m/%Y")))
    
    st.markdown("---")
    st.caption("© 2026 - Secretaria Municipal de Saúde")

"""
INFOGRAFÉPIDEMIOLÓGICO - SRAG
Dashboard para monitoramento de Síndrome Respiratória Aguda Grave
Com integração de dados reais dos painéis Power BI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Vigilância Epidemiológica - SRAG",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CSS PERSONALIZADO
# ============================================================================

st.markdown("""
<style>
    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #002147 0%, #0a3d62 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 600;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .update-badge {
        background: #FF8C00;
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin-top: 1rem;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    /* Títulos das seções */
    .section-title {
        color: #002147;
        font-size: 1.3rem;
        font-weight: bold;
        border-left: 5px solid #FF8C00;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.2rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        transition: transform 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: bold;
        color: #002147;
        margin-bottom: 0.3rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }
    
    /* Lista de unidades */
    .top5-item {
        background: white;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.2s;
    }
    
    .top5-item:hover {
        transform: translateX(5px);
        border-left-color: #FF8C00;
    }
    
    .top5-nome {
        font-weight: 600;
        color: #333;
    }
    
    .top5-valor {
        color: #002147;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    /* Indicadores de alerta */
    .alert-card {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .critical-card {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Footer */
    .footer {
        background: #f8f9fa;
        padding: 1.5rem;
        text-align: center;
        border-radius: 10px;
        margin-top: 2rem;
        font-size: 0.8rem;
        color: #7f8c8d;
        border-top: 1px solid #dee2e6;
    }
    
    /* Badges */
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    
    .status-critical {
        background: #dc3545;
        color: white;
    }
    
    .status-warning {
        background: #ffc107;
        color: #333;
    }
    
    .status-normal {
        background: #28a745;
        color: white;
    }
    
    /* Sidebar custom */
    .sidebar-info {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES DE CARREGAMENTO DE DADOS
# ============================================================================

@st.cache_data(ttl=3600, show_spinner="Carregando dados dos painéis...")
def load_real_data():
    """
    Carrega os dados REAIS extraídos dos painéis Power BI
    """
    dados = {
        "data_atualizacao": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "data_extenso": datetime.now().strftime("%d de %B de %Y"),
        "source": "simulado"  # Será alterado se encontrar dados reais
    }
    
    try:
        # Tenta carregar métricas reais
        df_metricas = pd.read_csv("metricas_reais.csv")
        metricas_dict = {}
        for _, row in df_metricas.iterrows():
            try:
                # Tenta converter para número
                valor = row["valor"]
                if isinstance(valor, str):
                    if '%' in valor:
                        valor = float(valor.replace('%', '').replace(',', '.'))
                    elif valor.replace('.', '').replace(',', '').isdigit():
                        valor = float(valor.replace(',', '.'))
                metricas_dict[row["indicador"]] = valor
            except:
                metricas_dict[row["indicador"]] = row["valor"]
        
        dados["source"] = "real"
        dados["metricas"] = metricas_dict
        
        # Tenta carregar unidades reais
        try:
            df_unidades = pd.read_csv("unidades_reais.csv")
            if "unidade" in df_unidades.columns:
                dados["unidades"] = df_unidades["unidade"].tolist()
            elif "nome" in df_unidades.columns:
                dados["unidades"] = df_unidades["nome"].tolist()
        except:
            dados["unidades"] = []
        
        # Tenta carregar distritos reais
        try:
            df_distritos = pd.read_csv("distritos_reais.csv")
            if "distrito" in df_distritos.columns:
                dados["distritos"] = df_distritos["distrito"].tolist()
            elif "nome" in df_distritos.columns:
                dados["distritos"] = df_distritos["nome"].tolist()
        except:
            dados["distritos"] = []
        
        # Tenta carregar casos por semana
        try:
            df_casos = pd.read_csv("casos_reais_por_semana.csv")
            if "semana_epidemiologica" in df_casos.columns:
                dados["semanas"] = df_casos["semana_epidemiologica"].tolist()
                dados["casos_semanais"] = df_casos["casos_srag"].tolist()
            else:
                dados["semanas"] = list(range(1, len(df_casos) + 1))
                dados["casos_semanais"] = df_casos.iloc[:, 0].tolist()
        except:
            dados["semanas"] = list(range(1, 17))
            dados["casos_semanais"] = []
        
        print("✅ Dados reais carregados com sucesso!")
        
    except Exception as e:
        print(f"⚠️ Erro ao carregar dados reais: {e}")
        dados["source"] = "simulado"
        dados = load_simulated_data(dados)
    
    return dados


def load_simulated_data(dados):
    """
    Dados simulados para fallback quando os dados reais não estão disponíveis
    """
    dados.update({
        "total_srag": 1247,
        "ocupacao_uti": 68,
        "total_atendimentos": 4850,
        "obitos": 38,
        "semanas": list(range(1, 17)),
        "casos_semanais": [12, 18, 25, 42, 78, 125, 198, 267, 310, 345, 398, 420, 445, 432, 398, 345],
        "meses": ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
        "casos_2023": [45, 52, 68, 95, 142, 198, 245, 267, 234, 189, 145, 98],
        "casos_2024": [38, 48, 72, 112, 168, 235, 289, 312, 278, 225, 178, 124],
        "agentes": {
            "COVID-19": 64,
            "Influenza A": 18,
            "Influenza B": 5,
            "VSR": 8,
            "Outros": 5
        },
        "top5": [
            {"nome": "Hospital Municipal Central", "casos": 342},
            {"nome": "UPA Distrito Norte", "casos": 287},
            {"nome": "UBS Vila Esperança", "casos": 198},
            {"nome": "Hospital Regional Sul", "casos": 176},
            {"nome": "UBS Jardim Glória", "casos": 145}
        ],
        "distritos": [
            {"nome": "Centro", "ubs": 8, "atendimentos": 1250},
            {"nome": "Norte", "ubs": 6, "atendimentos": 980},
            {"nome": "Sul", "ubs": 5, "atendimentos": 875},
            {"nome": "Leste", "ubs": 4, "atendimentos": 645},
            {"nome": "Oeste", "ubs": 7, "atendimentos": 1120}
        ]
    })
    
    if not dados.get("unidades"):
        dados["unidades"] = [item["nome"] for item in dados["top5"]]
    
    if not dados.get("distritos_reais"):
        dados["distritos_reais"] = [item["nome"] for item in dados["distritos"]]
    
    return dados


def get_alert_level(ocupacao_uti):
    """Retorna o nível de alerta baseado na ocupação UTI"""
    if ocupacao_uti >= 80:
        return "CRÍTICO", "critical"
    elif ocupacao_uti >= 60:
        return "ALERTA", "warning"
    else:
        return "NORMAL", "normal"


def calculate_trend(casos_semanais):
    """Calcula a tendência baseada nos últimos 4 semanas"""
    if len(casos_semanais) >= 4:
        ultimas_4 = casos_semanais[-4:]
        if ultimas_4[-1] > ultimas_4[0] * 1.1:
            return "📈 CRESCENTE", "critical"
        elif ultimas_4[-1] < ultimas_4[0] * 0.9:
            return "📉 DECRESCENTE", "normal"
    return "➡️ ESTÁVEL", "warning"

# ============================================================================
# FUNÇÕES DOS GRÁFICOS
# ============================================================================

def grafico_tendencia(dados):
    """Gráfico de área para tendência de SRAG"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dados["semanas"],
        y=dados["casos_semanais"],
        mode='lines+markers',
        name='Casos SRAG',
        fill='tozeroy',
        line=dict(color='#002147', width=3),
        fillcolor='rgba(52, 152, 219, 0.3)',
        marker=dict(size=8, color='#3498db', symbol='circle')
    ))
    
    # Calcula linha de alerta (80% do máximo)
    if dados["casos_semanais"]:
        max_casos = max(dados["casos_semanais"])
        nivel_alerta = max_casos * 0.8
        
        fig.add_hline(
            y=nivel_alerta,
            line_dash="dash",
            line_color="#e74c3c",
            annotation_text=f"🚨 Nível de Alerta ({int(nivel_alerta)} casos)",
            annotation_position="top right"
        )
    
    fig.update_layout(
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='white',
        xaxis_title="<b>Semana Epidemiológica</b>",
        yaxis_title="<b>Número de Notificações</b>",
        font=dict(family="Arial, sans-serif", size=12),
        hovermode='x unified'
    )
    
    fig.update_xaxis(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxis(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    
    return fig


def grafico_ciclos(dados):
    """Gráfico comparativo de ciclos sazonais"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dados["meses"],
        y=dados["casos_2023"],
        mode='lines+markers',
        name='2023',
        line=dict(color='#95a5a6', width=2, dash='dash'),
        marker=dict(size=8, color='#95a5a6', symbol='circle')
    ))
    
    fig.add_trace(go.Scatter(
        x=dados["meses"],
        y=dados["casos_2024"],
        mode='lines+markers',
        name='2024',
        line=dict(color='#FF8C00', width=3),
        marker=dict(size=10, color='#FF8C00', symbol='circle')
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='white',
        xaxis_title="<b>Mês</b>",
        yaxis_title="<b>Casos Notificados</b>",
        font=dict(family="Arial, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_xaxis(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxis(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    
    return fig


def grafico_distritos(dados):
    """Gráfico de barras para distribuição por distrito"""
    if not dados.get("distritos"):
        return None
    
    df = pd.DataFrame(dados["distritos"])
    
    fig = px.bar(
        df,
        x="nome",
        y="atendimentos",
        color="atendimentos",
        color_continuous_scale=['#3498db', '#002147'],
        text="atendimentos",
        title="Atendimentos por Distrito"
    )
    
    fig.update_traces(textposition='outside', texttemplate='%{text:,}')
    fig.update_layout(
        height=350,
        plot_bgcolor='white',
        xaxis_title="<b>Distrito</b>",
        yaxis_title="<b>Número de Atendimentos</b>",
        showlegend=False
    )
    
    return fig

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Carrega os dados
    dados = load_real_data()
    
    # HEADER
    fonte_dados = "DADOS REAIS DOS PAINÉIS" if dados["source"] == "real" else "DADOS SIMULADOS (FALLBACK)"
    cor_fonte = "#28a745" if dados["source"] == "real" else "#ffc107"
    
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 INFORME SEMANAL DE VIGILÂNCIA EPIDEMIOLÓGICA</h1>
        <p>Monitoramento de Doenças Respiratórias - SRAG e Síndromes Gripais</p>
        <div class="update-badge">
            🗓️ ATUALIZADO EM: {dados['data_extenso'].upper()}
        </div>
        <div style="margin-top: 0.5rem; font-size: 0.8rem;">
            <span class="status-badge status-normal" style="background: {cor_fonte};">{fonte_dados}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Seção de Alertas
    if dados["source"] == "real":
        ocupacao = dados.get("metricas", {}).get("ocupacao_uti", dados.get("ocupacao_uti", 0))
    else:
        ocupacao = dados.get("ocupacao_uti", 0)
    
    nivel_alerta, tipo_alerta = get_alert_level(ocupacao)
    tendencia, tipo_tendencia = calculate_trend(dados["casos_semanais"])
    
    col_alert1, col_alert2 = st.columns(2)
    
    with col_alert1:
        alert_class = "critical-card" if tipo_alerta == "critical" else "alert-card"
        st.markdown(f"""
        <div class="{alert_class}">
            <strong>⚠️ OCUPAÇÃO UTI:</strong> {ocupacao:.0f}% - Nível {nivel_alerta}
        </div>
        """, unsafe_allow_html=True)
    
    with col_alert2:
        alert_class = "critical-card" if tipo_tendencia == "critical" else "alert-card"
        emoji = "📈" if "CRESCENTE" in tendencia else "📉" if "DECRESCENTE" in tendencia else "➡️"
        st.markdown(f"""
        <div class="{alert_class}">
            <strong>{emoji} TENDÊNCIA:</strong> {tendencia}
        </div>
        """, unsafe_allow_html=True)
    
    # MÉTRICAS PRINCIPAIS
    st.markdown('<div class="section-title">📈 INDICADORES PRINCIPAIS</div>', unsafe_allow_html=True)
    
    if dados["source"] == "real":
        metricas = dados.get("metricas", {})
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            valor = metricas.get("total_srag", dados.get("total_srag", 0))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{int(valor):,}</div>
                <div class="metric-label">🏥 Internações SRAG</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            valor = metricas.get("ocupacao_uti", dados.get("ocupacao_uti", 0))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{float(valor):.0f}%</div>
                <div class="metric-label">🛏️ Ocupação UTIs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            valor = metricas.get("internacoes", dados.get("total_atendimentos", 0))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{int(valor):,}</div>
                <div class="metric-label">🏥 Internações (Total)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            valor = metricas.get("obitos", dados.get("obitos", 0))
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{int(valor)}</div>
                <div class="metric-label">⚠️ Óbitos</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{dados['total_srag']:,}</div>
                <div class="metric-label">🏥 Internações SRAG</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{dados['ocupacao_uti']:.0f}%</div>
                <div class="metric-label">🛏️ Ocupação UTIs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{dados['total_atendimentos']:,}</div>
                <div class="metric-label">🏥 Atendimentos (7d)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{dados['obitos']}</div>
                <div class="metric-label">⚠️ Óbitos</div>
            </div>
            """, unsafe_allow_html=True)
    
    # DUAS COLUNAS PRINCIPAIS
    st.markdown('<div class="section-title">🔬 ANÁLISE EPIDEMIOLÓGICA</div>', unsafe_allow_html=True)
    col_left, col_right = st.columns(2, gap="large")
    
    # COLUNA ESQUERDA
    with col_left:
        # Gráfico de Tendência
        st.subheader("📈 Tendência por Semana Epidemiológica")
        fig_tendencia = grafico_tendencia(dados)
        st.plotly_chart(fig_tendencia, use_container_width=True)
        
        # Agentes Etiológicos (apenas simulado ou se disponível)
        if dados["source"] == "simulado":
            st.subheader("🧬 Agentes Etiológicos")
            fig_agentes = px.pie(
                values=list(dados["agentes"].values()),
                names=list(dados["agentes"].keys()),
                color_discrete_sequence=['#1a5276', '#2471a3', '#2e86c1', '#3498db', '#85c1e9'],
                hole=0.4
            )
            fig_agentes.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
            fig_agentes.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_agentes, use_container_width=True)
    
    # COLUNA DIREITA
    with col_right:
        # Top Unidades
        st.subheader("⭐ Unidades com Maior Prevalência")
        
        if dados["source"] == "real" and dados.get("unidades"):
            for i, unidade in enumerate(dados["unidades"][:5], 1):
                st.markdown(f"""
                <div class="top5-item">
                    <span class="top5-nome">{i}. {unidade}</span>
                    <span class="top5-valor">Em monitoramento</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            for item in dados["top5"]:
                st.markdown(f"""
                <div class="top5-item">
                    <span class="top5-nome">{item['nome']}</span>
                    <span class="top5-valor">{item['casos']} atendimentos</span>
                </div>
                """, unsafe_allow_html=True)
        
        # Distribuição por Distrito
        st.subheader("📍 Distribuição por Distrito")
        
        if dados["source"] == "real" and dados.get("distritos_reais"):
            for distrito in dados["distritos_reais"][:5]:
                st.markdown(f"""
                <div class="top5-item">
                    <span class="top5-nome">{distrito}</span>
                    <span class="top5-valor">Em monitoramento</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            df_distritos = pd.DataFrame(dados["distritos"])
            st.dataframe(
                df_distritos,
                column_config={
                    "nome": "Distrito",
                    "ubs": st.column_config.NumberColumn("UBS", format="%d"),
                    "atendimentos": st.column_config.NumberColumn("Atendimentos", format="%d")
                },
                hide_index=True,
                use_container_width=True
            )
        
        # Ciclos Sazonais
        st.subheader("❄️ Ciclos Sazonais Comparativos")
        fig_ciclos = grafico_ciclos(dados)
        st.plotly_chart(fig_ciclos, use_container_width=True)
    
    # Indicadores Derivados (se houver dados reais)
    if dados["source"] == "real" and dados.get("metricas"):
        st.markdown('<div class="section-title">📊 INDICADORES DERIVADOS</div>', unsafe_allow_html=True)
        
        col_i1, col_i2, col_i3 = st.columns(3)
        
        with col_i1:
            total_srag = dados["metricas"].get("total_srag", 0)
            obitos = dados["metricas"].get("obitos", 0)
            letalidade = (obitos / total_srag * 100) if total_srag > 0 else 0
            st.metric(
                "Taxa de Letalidade",
                f"{letalidade:.1f}%",
                delta="Óbitos / SRAG",
                delta_color="inverse"
            )
        
        with col_i2:
            internacoes = dados["metricas"].get("internacoes", 0)
            uti = dados["metricas"].get("ocupacao_uti", 0)
            st.metric(
                "Proporção UTI",
                f"{uti:.0f}%",
                delta="Das internações"
            )
        
        with col_i3:
            st.metric(
                "Coleta de Dados",
                dados["data_atualizacao"].split()[0],
                delta="Última atualização"
            )
    
    # FOOTER
    st.markdown(f"""
    <div class="footer">
        <strong>📋 CRÉDITOS INSTITUCIONAIS</strong><br>
        NIS (Núcleo de Informação em Saúde) | DIVEPI (Diretoria de Vigilância Epidemiológica) | CIEVS<br>
        Relatório Gerado para Subsecretaria de Saúde — {dados['data_atualizacao']}
    </div>
    """, unsafe_allow_html=True)
    
    # Instruções
    st.markdown("---")
    st.caption("💡 **Dica:** Para salvar como imagem, pressione Ctrl+P (ou Cmd+P) e selecione 'Salvar como PDF'")
    
    # Informações de debug (apenas em desenvolvimento)
    if dados["source"] == "simulado":
        st.info("ℹ️ **Modo de demonstração:** O dashboard está usando dados simulados. Conecte o coletor de dados para visualizar informações reais dos painéis.")


if __name__ == "__main__":
    main()

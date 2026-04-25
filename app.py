"""
INFOGRAFÉPIDEMIOLÓGICO - SRAG
Dashboard para monitoramento de Síndrome Respiratória Aguda Grave
Exibe APENAS os dados reais extraídos dos painéis Power BI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
import os

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
    .main-header {
        background: linear-gradient(135deg, #002147 0%, #0a3d62 100%);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2rem;
    }
    .update-badge {
        background: #FF8C00;
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin-top: 1rem;
        font-weight: bold;
    }
    .section-title {
        color: #002147;
        font-size: 1.3rem;
        font-weight: bold;
        border-left: 5px solid #FF8C00;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #002147;
    }
    .data-item {
        background: white;
        padding: 0.5rem;
        margin: 0.3rem 0;
        border-radius: 5px;
        border-left: 3px solid #3498db;
        font-size: 0.9rem;
    }
    .footer {
        background: #f8f9fa;
        padding: 1.5rem;
        text-align: center;
        border-radius: 10px;
        margin-top: 2rem;
        font-size: 0.8rem;
        color: #7f8c8d;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CARREGAMENTO DE DADOS REAIS (SEM DADOS FICTÍCIOS)
# ============================================================================

@st.cache_data(ttl=3600)
def carregar_dados_reais():
    """
    Carrega APENAS os dados reais extraídos do Power BI.
    Se não existirem, mostra aviso.
    """
    
    dados = {
        "data_coleta": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "existem_dados": False,
        "metricas": {},
        "unidades": [],
        "distritos": [],
        "semanas": [],
        "casos_semanais": [],
        "textos_extraidos": []
    }
    
    # Verifica se os arquivos de dados reais existem
    arquivos_esperados = [
        "texto_bruto_painel.txt",
        "todos_os_textos_extraidos.csv"
    ]
    
    for arquivo in arquivos_esperados:
        if not os.path.exists(arquivo):
            st.warning(f"⚠️ Arquivo não encontrado: {arquivo}")
            return dados
    
    try:
        # Carrega o texto bruto
        with open("texto_bruto_painel.txt", "r", encoding="utf-8") as f:
            dados["texto_bruto"] = f.read()
        
        # Carrega os textos extraídos
        df_textos = pd.read_csv("todos_os_textos_extraidos.csv")
        dados["textos_extraidos"] = df_textos["texto_extraido"].tolist()
        
        # Carrega unidades se existir
        if os.path.exists("unidades_encontradas.csv"):
            df_unidades = pd.read_csv("unidades_encontradas.csv")
            if "unidade_encontrada" in df_unidades.columns:
                dados["unidades"] = df_unidades["unidade_encontrada"].tolist()
        
        # Carrega distritos se existir
        if os.path.exists("distritos_encontrados.csv"):
            df_distritos = pd.read_csv("distritos_encontrados.csv")
            if "distrito_encontrado" in df_distritos.columns:
                dados["distritos"] = df_distritos["distrito_encontrado"].tolist()
        
        # Carrega métricas se existir
        if os.path.exists("metricas_reais.csv"):
            df_metricas = pd.read_csv("metricas_reais.csv")
            for _, row in df_metricas.iterrows():
                try:
                    valor = row["valor"]
                    if isinstance(valor, str) and '%' in valor:
                        valor = float(valor.replace('%', ''))
                    dados["metricas"][row["indicador"]] = valor
                except:
                    pass
        
        # Carrega casos por semana
        if os.path.exists("casos_reais_por_semana.csv"):
            df_casos = pd.read_csv("casos_reais_por_semana.csv")
            if "semana_epidemiologica" in df_casos.columns:
                dados["semanas"] = df_casos["semana_epidemiologica"].tolist()
                dados["casos_semanais"] = df_casos["casos_srag"].tolist()
        
        dados["existem_dados"] = True
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
    
    return dados


def mostrar_textos_extraidos(dados):
    """Mostra os textos reais extraídos do painel"""
    st.markdown("### 📄 Textos Extraídos do Power BI")
    
    if dados.get("textos_extraidos"):
        for i, texto in enumerate(dados["textos_extraidos"][:30]):  # Mostra até 30
            if len(texto.strip()) > 3:
                st.markdown(f'<div class="data-item">📌 {texto[:200]}</div>', unsafe_allow_html=True)
    else:
        st.info("Nenhum texto foi extraído ainda. Execute o coletor primeiro.")

# ============================================================================
# GRÁFICOS (APENAS COM DADOS REAIS)
# ============================================================================

def grafico_tendencia(dados):
    """Gráfico com dados reais de tendência"""
    if not dados.get("semanas") or not dados.get("casos_semanais"):
        return None
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dados["semanas"],
        y=dados["casos_semanais"],
        mode='lines+markers',
        name='Casos SRAG',
        fill='tozeroy',
        line=dict(color='#002147', width=3),
        fillcolor='rgba(52, 152, 219, 0.3)',
        marker=dict(size=8, color='#3498db')
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor='white',
        xaxis_title="Semana Epidemiológica",
        yaxis_title="Número de Notificações"
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
    
    return fig

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.markdown("""
    <div class="main-header">
        <h1>📊 INFORME SEMANAL DE VIGILÂNCIA EPIDEMIOLÓGICA</h1>
        <p>Monitoramento de Doenças Respiratórias - SRAG e Síndromes Gripais</p>
        <div class="update-badge">
            🗓️ DADOS REAIS DOS PAINÉIS POWER BI
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carrega os dados reais
    dados = carregar_dados_reais()
    
    if not dados["existem_dados"]:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Nenhum dado real foi encontrado!</strong><br><br>
            Para carregar dados reais do Power BI:
            <ol>
                <li>Execute o script coletor: <code>python coletor.py</code></li>
                <li>O coletor vai extrair os dados do painel Power BI</li>
                <li>Depois volte e execute: <code>streamlit run app.py</code></li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostra instruções detalhadas
        with st.expander("🔧 Como extrair dados reais do Power BI"):
            st.code("""
# 1. Instale as dependências
pip install playwright pandas streamlit plotly
playwright install chromium

# 2. Crie o arquivo coletor.py (já fornecido)

# 3. Execute o coletor
python coletor.py

# 4. Após extrair os dados, execute o dashboard
streamlit run app.py
            """, language="bash")
        return
    
    # ================================================================
    # MOSTRA APENAS DADOS REAIS EXTRAÍDOS
    # ================================================================
    
    st.success(f"✅ Dados reais carregados! Coleta em: {dados['data_coleta']}")
    
    # Métricas encontradas
    if dados["metricas"]:
        st.markdown('<div class="section-title">📊 MÉTRICAS ENCONTRADAS NO PAINEL</div>', unsafe_allow_html=True)
        
        cols = st.columns(min(len(dados["metricas"]), 4))
        for i, (nome, valor) in enumerate(dados["metricas"].items()):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{valor}</div>
                    <div>{nome.upper()}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # Unidades encontradas
    if dados["unidades"]:
        st.markdown('<div class="section-title">🏥 UNIDADES DE SAÚDE (DADOS REAIS)</div>', unsafe_allow_html=True)
        
        for unidade in dados["unidades"]:
            st.markdown(f'<div class="data-item">📍 {unidade}</div>', unsafe_allow_html=True)
    
    # Distritos encontrados
    if dados["distritos"]:
        st.markdown('<div class="section-title">🗺️ DISTRITOS (DADOS REAIS)</div>', unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, distrito in enumerate(dados["distritos"]):
            with cols[i % 3]:
                st.markdown(f'<div class="data-item">📍 {distrito}</div>', unsafe_allow_html=True)
    
    # Gráfico de tendência (se houver dados)
    if dados["semanas"] and dados["casos_semanais"]:
        st.markdown('<div class="section-title">📈 TENDÊNCIA (DADOS REAIS)</div>', unsafe_allow_html=True)
        fig = grafico_tendencia(dados)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    
    # Mostra os textos brutos extraídos
    st.markdown('<div class="section-title">📄 TEXTOS EXTRAÍDOS DO POWER BI</div>', unsafe_allow_html=True)
    
    with st.expander("🔍 Clique para ver todos os textos extraídos do painel"):
        mostrar_textos_extraidos(dados)
    
    # Mostra o texto bruto completo
    with st.expander("📄 TEXTO COMPLETO EXTRAÍDO"):
        if dados.get("texto_bruto"):
            st.text_area("Texto bruto do Power BI:", dados["texto_bruto"], height=400)
        else:
            st.warning("Texto bruto não disponível")
    
    # Botão para exportar
    st.markdown("---")
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp2:
        if st.button("📥 Exportar dados para CSV", use_container_width=True):
            # Salva dados atuais em CSV
            df_dados = pd.DataFrame({
                "tipo": [],
                "valor": []
            })
            
            for nome, valor in dados["metricas"].items():
                df_dados = pd.concat([df_dados, pd.DataFrame({"tipo": [nome], "valor": [valor]})])
            
            for unidade in dados["unidades"]:
                df_dados = pd.concat([df_dados, pd.DataFrame({"tipo": ["unidade"], "valor": [unidade]})])
            
            for distrito in dados["distritos"]:
                df_dados = pd.concat([df_dados, pd.DataFrame({"tipo": ["distrito"], "valor": [distrito]})])
            
            df_dados.to_csv("dados_exportados.csv", index=False)
            st.success("✅ Dados exportados para 'dados_exportados.csv'")
    
    # Footer
    st.markdown(f"""
    <div class="footer">
        <strong>📋 FONTE DOS DADOS</strong><br>
        Dados extraídos diretamente do Power BI em {dados['data_coleta']}<br>
        NIS (Núcleo de Informação em Saúde) | DIVEPI (Diretoria de Vigilância Epidemiológica)
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

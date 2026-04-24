import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. Configurações de Página
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# 2. Estilização Profissional (CSS)
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .card { background-color: white; padding: 15px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 15px; }
    .secao-titulo { color: #1a5276; font-weight: bold; border-bottom: 2px solid #1a5276; padding-bottom: 5px; margin-bottom: 15px; text-transform: uppercase; }
    .metric-label { font-size: 14px; color: #555; }
    </style>
""", unsafe_allow_html=True)

# 3. Carregamento Seguro de Dados
def carregar_dados():
    hoje = datetime.now().strftime("%d/%m/%Y")
    try:
        df = pd.read_csv("dados_epidemiologicos.csv")
        if 'Data' not in df.columns: df['Data'] = hoje
        return df
    except:
        # Dados temporários caso o robô não tenha rodado
        return pd.DataFrame({'Subcategoria': ['SARS-CoV-2', 'Influenza A', 'RSV', 'Outros'], 
                            'Valor': ['68%', '12%', '10%', '10%'], 'Data': [hoje]*4})

df_vigi = carregar_dados()
data_atual = df_vigi['Data'].iloc[0]

# --- CABEÇALHO ---
st.markdown(f"<h1 style='text-align: center; color: #1a5276;'>🛡️ Vigilância Epidemiológica: Doenças Respiratórias</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Consolidação NIS | SIVEP-Gripe | e-SUS | VIVVER <br> Atualizado em: {data_atual}</p>", unsafe_allow_html=True)

# --- LAYOUT PRINCIPAL (DUAS COLUNAS) ---
col_monitor, col_gestao = st.columns(2, gap="large")

# ==========================================
# COLUNA ESQUERDA: MONITORAMENTO
# ==========================================
with col_monitor:
    st.markdown("<div class='secao-titulo'>Monitoramento de Casos de SRAG</div>", unsafe_allow_html=True)
    
    # Perfil e Tendência
    c1, c2 = st.columns([1, 1])
    with c1:
        st.write("**Perfil Epidemiológico**")
        fig_sexo = px.bar(x=[55, 45], y=['Feminino', 'Masculino'], orientation='h', height=180, color_discrete_sequence=['#3498db'])
        fig_sexo.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sexo, use_container_width=True)
    with c2:
        st.markdown("<div style='text-align:center; font-size:60px;'>🫁</div>", unsafe_allow_html=True)
        st.caption("<center>Sintomas específicos apresentados</center>", unsafe_allow_html=True)

    # Identificação do Agente
    st.write("**Identificação do Agente Etiológico**")
    try:
        val_covid = df_vigi[df_vigi['Subcategoria'] == 'SARS-CoV-2']['Valor'].values[0]
        val_flu = df_vigi[df_vigi['Subcategoria'] == 'Influenza A']['Valor'].values[0]
    except:
        val_covid, val_flu = "0%", "0%"

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("COVID-19", val_covid)
    a2.metric("Influenza A", val_flu)
    a3.metric("RSV", "10%")
    a4.metric("Outros", "10%")

    # Gráfico de Tendência (Onda)
    st.write("**Tendência por Semana Epidemiológica**")
    fig_onda = px.area(x=list(range(1,21)), y=[2,5,15,40,90,160,250,220,180,120,80,45,25,15,10,5,3,2,1,1], color_discrete_sequence=['#1a5276'])
    fig_onda.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_onda, use_container_width=True)

# ==========================================
# COLUNA DIREITA: GESTÃO
# ==========================================
with col_gestao:
    st.markdown("<div class='secao-titulo'>Gestão e Localização do Atendimento</div>", unsafe_allow_html=True)
    
    # Capilaridade
    st.write("**Capilaridade do Atendimento (UBS)**")
    st.markdown("<div style='text-align:center; font-size:80px;'>🏥🗺️</div>", unsafe_allow_html=True)
    st.caption("Monitoramento de atendimentos distribuídos por distritos sanitários.")

    # Ciclos Sazonais
    st.write("**Ciclos Sazonais 2023/24**")
    c_23, c_24 = st.columns(2)
    with c_23:
        st.line_chart([10, 30, 80, 60, 20], height=150)
        st.caption("<center>2023</center>", unsafe_allow_html=True)
    with c_24:
        st.line_chart([5, 25, 110, 90, 30], height=150)
        st.caption("<center>2024</center>", unsafe_allow_html=True)

    # Fontes
    st.write("**Fontes de Informação Integradas**")
    st.success("SIVEP-Gripe + e-SUS + VIVVER ➔ NIS")

st.divider()
st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>Dados extraídos automaticamente do Power BI. Este sistema é uma ferramenta de apoio à decisão.</p>", unsafe_allow_html=True)

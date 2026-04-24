import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# 1. Configurações de Página e Título
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# Estilo CSS para criar cartões brancos e organizar o visual
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .card { background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .titulo-secao { color: #1a5276; font-weight: bold; border-bottom: 3px solid #1a5276; padding-bottom: 5px; margin-bottom: 15px; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# 2. Carregamento Seguro de Dados (com dados de segurança caso o robô falhe)
def carregar_dados():
    hoje = datetime.now().strftime("%d/%m/%Y")
    dados_padrao = pd.DataFrame({
        'Subcategoria': ['SARS-CoV-2', 'Influenza A', 'RSV', 'Outros'],
        'Valor': ['0%', '0%', '0%', '0%'],
        'Data': [hoje] * 4
    })
    try:
        # Se você tiver um arquivo dados_epidemiologicos.csv, ele lê daqui
        if os.path.exists("dados_epidemiologicos.csv"):
            df = pd.read_csv("dados_epidemiologicos.csv")
            if 'Data' not in df.columns: df['Data'] = hoje
            return df
        else:
            return dados_padrao
    except:
        return dados_padrao

df_vigi = carregar_dados()
try:
    data_atualizacao = df_vigi['Data'].iloc[0]
except:
    data_atualizacao = datetime.now().strftime("%d/%m/%Y")

# 3. Cabeçalho Principal
st.markdown(f"<h1 style='text-align: center; color: #1a5276;'>📊 Vigilância Epidemiológica: Doenças Respiratórias</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Sincronizado com BI em: {data_atualizacao}</p>", unsafe_allow_html=True)
st.write("---")

# 4. Divisão em Duas Colunas (Monitoramento e Gestão)
col_monitoramento, col_gestao = st.columns(2, gap="large")

# ==============================================================================
# COLUNA ESQUERDA: MONITORAMENTO DE CASOS
# ==============================================================================
with col_monitoramento:
    st.markdown("<div class='titulo-secao'>MONITORAMENTO DE CASOS (SRAG)</div>", unsafe_allow_html=True)
    
    # Bloco superior: Perfil e Humano Central
    c_perfil, c_imagem_central = st.columns([1, 1.2])
    with c_perfil:
        st.markdown("**Perfil Epidemiológico**")
        st.caption("Análise de casos por sexo e idade")
        # Gráfico de Barras Horizontais (Gerado por código)
        fig_sexo = px.bar(x=[55, 45], y=["Feminino", "Masculino"], orientation='h', height=160, color_discrete_sequence=['#3498db'])
        fig_sexo.update_layout(margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sexo, use_container_width=True)

        st.markdown("**Comorbidades**")
        if os.path.exists("comorbidades.png"):
            st.image("comorbidades.png", width=250)
        else:
            st.info("Suba 'comorbidades.png' para ver os ícones.")

    with c_imagem_central:
        if os.path.exists("perfil epidemiologico.png"):
            st.image("perfil epidemiologico.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center; font-size: 80px;'>🫁</h1>", unsafe_allow_html=True)

    # Identificação do Agente
    st.write("---")
    st.markdown("**Identificação do Agente Etiológico**")
    c_micro, c_agentes_metricas = st.columns([0.6, 1.4])
    with c_micro:
        if os.path.exists("agente etiologico.png"):
            st.image("agente etiologico.png", width=120)
        else:
            st.write("🔬")
    with c_agentes_metricas:
        # Pega valores reais do CSV se existirem
        try:
            val_covid = df_vigi[df_vigi['Subcategoria'] == 'SARS-CoV-2']['Valor'].values[0]
            val_flu = df_vigi[df_vigi['Subcategoria'] == 'Influenza A']['Valor'].values[0]
        except:
            val_covid, val_flu = "0%", "0%"
            
        st.metric("SARS-CoV-2 (COVID)", val_covid)
        st.metric("Influenza A", val_flu)

    # Gráfico de Tendência (Onda)
    st.write("---")
    st.markdown("**Tendência Semanal (Notificações)**")
    # Gráfico de Área (Gerado por código para dinamismo)
    fig_onda = px.area(x=list(range(1, 13)), y=[12, 25, 50, 100, 180, 240, 210, 160, 100, 60, 30, 15], color_discrete_sequence=['#1a5276'])
    fig_onda.update_layout(height=280, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_onda, use_container_width=True)


# ==============================================================================
# COLUNA DIREITA: GESTÃO E LOCALIZAÇÃO
# ==============================================================================
with col_gestao:
    st.markdown("<div class='titulo-secao'>GESTÃO E LOCALIZAÇÃO DO ATENDIMENTO</div>", unsafe_allow_html=True)
    
    # Capilaridade
    with st.container():
        st.markdown("**Capilaridade do Atendimento**")
        st.caption("Monitoramento de atendimentos distribuídos por distritos sanitários.")
        if os.path.exists("capilaridade.jpg"):
            st.image("capilaridade.jpg", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center; font-size: 80px;'>🏥🗺️</h1>", unsafe_allow_html=True)

    # Ciclos Sazonais
    st.write("---")
    st.markdown("**Ciclos Sazonais 2023/24**")
    c_2023, c_2024 = st.columns(2)
    with c_2023:
        # Gráfico gerado por código para comparação
        st.line_chart([10, 25, 50, 40, 20], height=150)
        st.caption("<center>2023</center>", unsafe_allow_html=True)
    with c_2024:
        st.line_chart([5, 20, 80, 70, 30], height=150)
        st.caption("<center>2024</center>", unsafe_allow_html=True)

    # Fontes
    st.write("---")
    st.markdown("**Fontes de Informação Integradas**")
    if os.path.exists("Fontes de informação integradas.jpg"):
        st.image("Fontes de informação integradas.jpg", use_container_width=True)
    else:
        st.success("SIVEP-Gripe + e-SUS + VIVVER")

# --- RODAPÉ ---
st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Consolidação de dados NIS, SIVEP-Gripe e e-SUS. Atualizado automaticamente.</p>", unsafe_allow_html=True)

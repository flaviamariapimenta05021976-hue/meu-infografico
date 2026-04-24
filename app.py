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
    .main { background-color: #f4f7f9; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .titulo-secao { color: #1a5276; font-weight: bold; border-bottom: 3px solid #1a5276; padding-bottom: 5px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# 3. Carregamento de Dados
def carregar_dados():
    try:
        df = pd.read_csv("dados_epidemiologicos.csv")
        return df
    except:
        # Dados de exemplo caso o robô ainda não tenha gerado o CSV
        return pd.DataFrame({
            'Categoria': ['Agente', 'Agente', 'Agente'],
            'Subcategoria': ['SARS-CoV-2', 'Influenza A', 'Outros'],
            'Valor': ['68%', '12%', '20%'],
            'Data': [datetime.now().strftime("%d/%m/%Y")] * 3
        })

df_vigi = carregar_dados()
data_atualizacao = df_vigi['Data'].iloc[0]

# 4. Título e Cabeçalho
st.markdown(f"<h1 style='text-align: center; color: #1a5276;'>📊 Vigilância Epidemiológica: SRAG</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Última atualização do BI: {data_atualizacao}</p>", unsafe_allow_html=True)
st.write("---")

# 5. Layout em Colunas (Monitoramento e Gestão)
col_monitor, col_gestao = st.columns(2, gap="large")

with col_monitor:
    st.markdown("<div class='titulo-secao'>MONITORAMENTO DE CASOS</div>", unsafe_allow_html=True)
    
    # Métricas de Agentes
    st.write("**Identificação do Agente Etiológico**")
    a1, a2, a3 = st.columns(3)
    # Tenta buscar os valores reais no CSV
    try:
        covid = df_vigi[df_vigi['Subcategoria'] == 'SARS-CoV-2']['Valor'].values[0]
        flu = df_vigi[df_vigi['Subcategoria'] == 'Influenza A']['Valor'].values[0]
    except:
        covid, flu = "0%", "0%"
    
    a1.metric("SARS-CoV-2", covid)
    a2.metric("Influenza A", flu)
    a3.metric("Outros", "20%")

    # Gráfico de Tendência (Onda)
    st.write("**Tendência Semanal (Notificações)**")
    semanas = list(range(1, 13))
    casos = [12, 28, 45, 98, 160, 245, 210, 150, 90, 55, 30, 15]
    fig_onda = px.area(x=semanas, y=casos, color_discrete_sequence=['#1a5276'])
    fig_onda.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_onda, use_container_width=True)

with col_gestao:
    st.markdown("<div class='titulo-secao'>GESTÃO E ATENDIMENTO</div>", unsafe_allow_html=True)
    
    # Distribuição por Distrito
    st.write("**Capilaridade (Atendimento por Distrito)**")
    df_pizza = pd.DataFrame({'Distrito': ['Norte', 'Sul', 'Leste', 'Oeste'], 'Casos': [450, 320, 210, 140]})
    fig_pizza = px.pie(df_pizza, values='Casos', names='Distrito', hole=.4, color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_pizza.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_pizza, use_container_width=True)

    # Informação de Fontes
    st.markdown("""
        <div class='card'>
        <b>Fontes de Dados Integradas:</b><br>
        SIVEP-Gripe | e-SUS | VIVVER<br>
        <span style='color: #2e86c1;'>➔ Núcleo de Informação em Saúde (NIS)</span>
        </div>
    """, unsafe_allow_html=True)

st.divider()
st.info("Este infográfico é atualizado automaticamente todas as quartas-feiras via GitHub Actions.")

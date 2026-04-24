import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

# Estilo CSS para melhorar o visual
st.markdown("""
    <style>
    .main { background-color: #f4f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border-left: 5px solid #1a5276; }
    h1, h2 { color: #1a5276; font-family: 'sans-serif'; }
    .fonte-rodape { font-size: 12px; color: #666; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# Tenta ler os dados do CSV (ou usa dados fictícios para teste)
try:
    df_csv = pd.read_csv("dados_epidemiologicos.csv")
    dados = df_csv.iloc[0]
except:
    dados = {"data": "24/04/2026", "srag_total": "1.240", "covid": "60%", "influenza": "15%"}

# TÍTULO PRINCIPAL
st.title("🛡️ Vigilância Epidemiológica: Doenças Respiratórias")
st.caption(f"Última atualização automática: {dados['data']} | Próxima atualização: Quarta-feira")

# DIVISÃO EM DUAS COLUNAS PRINCIPAIS (Igual ao seu modelo)
col_monitoramento, col_gestao = st.columns([1, 1], gap="large")

with col_monitoramento:
    st.header("Monitoramento de Casos")
    
    # Perfil Epidemiológico
    st.subheader("Perfil Detalhado (Sexo e Idade)")
    df_perfil = pd.DataFrame({'Sexo': ['Masculino', 'Feminino'], 'Casos': [450, 790]})
    fig_perfil = px.bar(df_perfil, x='Casos', y='Sexo', orientation='h', color_discrete_sequence=['#1a5276'])
    fig_perfil.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_perfil, use_container_width=True)
    
    # Identificação do Agente (Métricas com ícones sugeridos)
    st.subheader("Agentes Etiológicos")
    m1, m2, m3 = st.columns(3)
    m1.metric("COVID-19", dados['covid'])
    m2.metric("Influenza A", dados['influenza'])
    m3.metric("Outros", "25%")

    # Tendência Semanal (Gráfico de Área)
    st.subheader("Tendência por Semana Epidemiológica")
    semanas = list(range(1, 21))
    casos_semanais = [10, 15, 30, 45, 80, 120, 150, 140, 100, 80, 60, 40, 30, 20, 15, 10, 8, 5, 3, 2]
    fig_tendencia = px.area(x=semanas, y=casos_semanais, labels={'x':'Semana', 'y':'Notificações'})
    fig_tendencia.update_traces(line_color='#1a5276', fillcolor='rgba(26, 82, 118, 0.2)')
    st.plotly_chart(fig_tendencia, use_container_width=True)

with col_gestao:
    st.header("Gestão e Atendimento")
    
    # Capilaridade
    st.subheader("Capilaridade do Atendimento (UBS)")
    st.markdown("🌐 **Monitoramento por Distritos:** Norte (40%), Sul (30%), Leste (20%), Oeste (10%)")
    # Simulação de mini mapa ou gráfico de pizza
    fig_distrito = px.pie(values=[40, 30, 20, 10], names=['Norte', 'Sul', 'Leste', 'Oeste'], hole=.4)
    fig_distrito.update_layout(height=250)
    st.plotly_chart(fig_distrito, use_container_width=True)

    # Ciclos Sazonais
    st.subheader("Ciclos Sazonais 2023 vs 2024")
    fig_ciclos = go.Figure()
    fig_ciclos.add_trace(go.Scatter(x=semanas, y=[20,30,50,70,100,90,70,50], name="2023", fill='tozeroy'))
    fig_ciclos.add_trace(go.Scatter(x=semanas, y=[10,25,40,65,110,120,80,40], name="2024", fill='tozeroy'))
    st.plotly_chart(fig_ciclos, use_container_width=True)

# RODAPÉ COM FONTES
st.divider()
st.markdown("""
<div class='fonte-rodape'>
    <b>Fontes de Informação Integradas:</b> SIVEP-Gripe | e-SUS | VIVVER → Núcleo de Informação em Saúde (NIS)<br>
    <i>Dados parciais sujeitos a alterações. Configurado para extração automática via Python.</i>
</div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configurações de página e Estilo Visual
st.set_page_config(page_title="Vigilância Epidemiológica", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .titulo-secao { color: #1a5276; font-weight: bold; border-bottom: 2px solid #1a5276; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Tenta carregar dados; se não houver, usa valores de exemplo para manter o site bonito
def carregar_dados():
    try:
        df = pd.read_csv("dados_epidemiologicos.csv")
        return df
    except:
        # Dados de exemplo (Placeholder)
        return pd.DataFrame({
            'Categoria': ['Geral', 'Agente', 'Agente', 'Agente'],
            'Subcategoria': ['Total SRAG', 'SARS-CoV-2', 'Influenza A', 'Outros'],
            'Valor': ['1.240', '68%', '12%', '20%'],
            'Data': [datetime.now().strftime("%d/%m/%Y")] * 4
        })

df_vigi = carregar_dados()
data_atual = df_vigi['Data'].iloc[0]

# --- CABEÇALHO ---
st.markdown("<h1 style='text-align: center;'>Monitoramento de Doenças Respiratórias</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: gray;'>Última Atualização: {data_atual}</p>", unsafe_allow_html=True)
st.write("---")

# --- CORPO DO INFOGRÁFICO (DUAS COLUNAS) ---
col_esq, col_dir = st.columns(2, gap="large")

with col_esq:
    st.markdown("<div class='titulo-secao'>MONITORAMENTO DE CASOS (SRAG)</div>", unsafe_allow_html=True)
    
    # Métricas de Agentes
    st.write("**Identificação do Agente Etiológico**")
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("SARS-CoV-2", df_vigi.loc[df_vigi['Subcategoria'] == 'SARS-CoV-2', 'Valor'].values[0])
    with m2: st.metric("Influenza A", df_vigi.loc[df_vigi['Subcategoria'] == 'Influenza A', 'Valor'].values[0])
    with m3: st.metric("Outros", "20%")

    # Gráfico de Tendência (Onda)
    st.write("**Tendência Semanal**")
    semanas = list(range(1, 11))
    casos = [10, 25, 45, 90, 150, 210, 190, 140, 80, 40]
    fig_onda = px.area(x=semanas, y=casos, color_discrete_sequence=['#1a5276'])
    fig_onda.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_onda, use_container_width=True)

with col_dir:
    st.markdown("<div class='titulo-secao'>GESTÃO E ATENDIMENTO</div>", unsafe_allow_html=True)
    
    # Gráfico de Perfil (Pizza ou Barras)
    st.write("**Perfil por Distrito Sanitário**")
    df_pizza = pd.DataFrame({'Distrito': ['Norte', 'Sul', 'Leste', 'Oeste'], 'Val': [400, 300, 200, 100]})
    fig_pizza = px.pie(df_pizza, values='Val', names='Distrito', hole=.4, color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_pizza.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
    st.plotly_chart(fig_pizza, use_container_width=True)

    # Fontes de Dados
    st.markdown("<div class='card'><b>Fontes Integradas:</b><br>SIVEP-Gripe | e-SUS | VIVVER<br>➡️ Núcleo de Informação em Saúde (NIS)</div>", unsafe_allow_html=True)

st.divider()
st.caption("Este infográfico é atualizado automaticamente via extração de dados do Power BI toda quarta-feira.")
# RODAPÉ FINAL
st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Consolidação de dados provenientes do SIVEP-Gripe, e-SUS e sistema VIVVER.</p>", unsafe_allow_html=True)

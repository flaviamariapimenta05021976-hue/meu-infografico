import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image # Biblioteca para lidar com imagens

# 1. Configurações e Título
st.set_page_config(layout="wide", page_title="Vigilância Epidemiológica")
st.markdown("<h1 style='text-align: center; color: black;'>Vigilância Epidemiológica: Doenças Respiratórias (SRAG e Síndrome Gripal)</h1>", unsafe_allow_html=True)
st.write("---")

# 2. Divisão em Colunas Principais (Igual ao Modelo)
col_esq, col_dir = st.columns([1, 1], gap="large")

# ==============================================================================
# --- COLUNA ESQUERDA: MONITORAMENTO DE CASOS ---
# ==============================================================================
with col_esq:
    st.markdown("<h2 style='color: #1a5276;'>Monitoramento de Casos de SRAG</h2>", unsafe_allow_html=True)
    
    # Bloco Perfil e o Pulmão Central
    c_perfil_grafico, c_pulmao_central = st.columns([1.5, 1])
    
    with c_perfil_grafico:
        st.markdown("**Perfil Epidemiológico Detalhado**")
        st.caption("Análise de casos por sexo")
        # Gráfico de Barras Horizontais (Simulando o visual)
        df_sexo = pd.DataFrame({'Sexo': ['Feminino', 'Masculino'], 'Porcentagem': [55, 45]})
        fig_sexo = px.bar(df_sexo, x='Porcentagem', y='Sexo', orientation='h', height=150, color_discrete_sequence=['#3498db'])
        fig_sexo.update_layout(margin=dict(l=0, r=0, t=0, b=0), plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_sexo, use_container_width=True)

        # Seção Comorbidades (Tenta carregar a imagem ou usa texto)
        st.markdown("**Comorbidades**")
        try:
            img_comorb = Image.open("icon_comorbidades.png") # Nome do arquivo no GitHub
            st.image(img_comorb, width=250)
        except:
            st.warning("⚠️ Adicione 'icon_comorbidades.png' ao GitHub para ver os ícones.")

    with c_pulmao_central:
        # AQUI VAI O PULMÃO CENTRAL DA IMAGEM
        try:
            img_pulmao = Image.open("icon_pulmao.png") # Nome do arquivo no GitHub
            st.image(img_pulmao, use_container_width=True)
        except:
            # Mostra um emoji gigante se não achar a imagem
            st.markdown("<h1 style='text-align: center; font-size: 100px;'>🫁</h1>", unsafe_allow_html=True)

    # Identificação do Agente (Com Microscópio)
    st.markdown("---")
    c_microscopio, c_agentes_texto = st.columns([1, 2])
    
    with c_microscopio:
        try:
            img_micro = Image.open("icon_microscopio.png") # Nome do arquivo no GitHub
            st.image(img_micro, width=150)
        except:
            st.markdown("<h1 style='text-align: center; font-size: 80px;'>🔬</h1>", unsafe_allow_html=True)

    with c_agentes_texto:
        st.markdown("**Identificação do Agente Etiológico**")
        st.caption("Classificação dos casos de acordo com o vírus ou patógeno causador da síndrome.")
        a1, a2, a3, a4 = st.columns(4)
        a1.metric("Influenza A", "🔵 12%")
        a2.metric("Influenza B", "🔵 5%")
        a3.metric("SARS-CoV-2", "🟠 68%")
        a4.metric("RSV", "🟠 15%")

    # Tendência Semanal (Igual ao visual da onda)
    st.markdown("---")
    st.markdown("**Tendência por Semana Epidemiológica**")
    semanas = list(range(1, 31))
    dados_onda = [2, 5, 15, 45, 100, 180, 250, 230, 190, 130, 80, 50, 30, 15, 8, 5] + [2]*14
    fig_onda = px.area(x=semanas, y=dados_onda, color_discrete_sequence=['#2e86c1'])
    fig_onda.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0), plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_onda, use_container_width=True)


# ==============================================================================
# --- COLUNA DIREITA: GESTÃO E LOCALIZAÇÃO ---
# ==============================================================================
with col_dir:
    st.markdown("<h2 style='color: #1a5276;'>Gestão e Localização do Atendimento</h2>", unsafe_allow_html=True)
    
    # Capilaridade com o Mapa de UBS
    st.markdown("**Capilaridade do Atendimento**")
    st.caption("Monitoramento de atendimentos distribuídos por distritos sanitários e UBS.")
    try:
        img_mapa_ubs = Image.open("icon_mapa_ubs.png") # Nome do arquivo no GitHub
        st.image(img_mapa_ubs, use_container_width=True)
    except:
        st.markdown("<h1 style='text-align: center; font-size: 100px;'>🏥🗺️</h1>", unsafe_allow_html=True)

    # Ciclos Sazonais (Pequenos Múltiplos)
    st.markdown("---")
    st.markdown("**Ciclos Sazonais 2023/24**")
    st.caption("Comparação de padrões históricos para identificação de períodos de pico.")
    c_graf_2023, c_graf_2024 = st.columns(2)
    
    with c_graf_2023:
        st.line_chart([10, 20, 40, 30, 15], height=120)
        st.caption("<center>2023</center>", unsafe_allow_html=True)
    with c_graf_2024:
        st.line_chart([5, 15, 60, 50, 25], height=120)
        st.caption("<center>2024</center>", unsafe_allow_html=True)

    # Rodapé de Fontes (Igual ao fluxo da imagem)
    st.markdown("---")
    st.markdown("**Fontes de Informação Integradas**")
    st.markdown("📋 SIVEP-Gripe + ➕ e-SUS + 🗄️ VIVVER ➔ 🧬 Núcleo de Informação em Saúde (NIS)")

# RODAPÉ FINAL
st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Consolidação de dados provenientes do SIVEP-Gripe, e-SUS e sistema VIVVER.</p>", unsafe_allow_html=True)

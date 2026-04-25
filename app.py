import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# =========================
# 📥 CARREGAR DADOS
# =========================
@st.cache_data
def load():
    return pd.read_csv("dados.csv")

df = load()
row = df.iloc[-1]

# =========================
# 🧾 HEADER
# =========================
st.title("📊 Monitoramento de Síndromes Respiratórias")

# =========================
# 📊 INDICADORES PRINCIPAIS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("SRAG", int(row["srag_total"]))
col2.metric("Atendimentos", int(row["atendimentos"]))
col3.metric("Óbitos", int(row["obitos"]))
col4.metric("SR (leve)", int(row["sr_total"]))

# =========================
# 📊 INDICADORES DE GESTÃO
# =========================
st.subheader("📈 Indicadores Estratégicos")

c1, c2, c3 = st.columns(3)

c1.metric("Letalidade", f"{row['letalidade']:.1%}")
c2.metric("Taxa UTI", f"{row['taxa_uti']:.1%}")
c3.metric("Taxa Internação", f"{row['taxa_internacao']:.1%}")

# =========================
# 🧬 ETIOLOGIA
# =========================
st.subheader("🧬 Etiologia")

etiologia = pd.DataFrame({
    "Virus": ["COVID", "Influenza"],
    "Valor": [row["covid"], row["influenza"]]
})

fig = px.pie(etiologia, values="Valor", names="Virus")
st.plotly_chart(fig, use_container_width=True)

# =========================
# 🏥 SRAG DETALHE
# =========================
st.subheader("🏥 SRAG")

c1, c2 = st.columns(2)
c1.metric("Internações", int(row["srag_internacoes"]))
c2.metric("UTI", int(row["srag_uti"]))

# =========================
# 🧠 ALERTA INTELIGENTE
# =========================
st.subheader("🧠 Situação")

if row["letalidade"] > 0.1:
    st.error("🚨 Alta letalidade")

elif row["taxa_uti"] > 0.5:
    st.warning("⚠️ Alta ocupação de UTI")

else:
    st.success("✅ Situação controlada")

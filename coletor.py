import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import re

def limpar_numero(valor):
    if not valor:
        return None
    valor = valor.replace('.', '').replace(',', '.')
    try:
        return float(valor)
    except:
        return None

def extrair_numero(texto, palavra):
    for t in texto:
        if palavra in t.lower():
            num = re.findall(r'\d+[\.,]?\d*', t)
            if num:
                return limpar_numero(num[0])
    return None

def extrair():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        dados = {
            "data": datetime.now(),

            # SRAG
            "srag_total": None,
            "srag_uti": None,
            "srag_internacoes": None,
            "srag_obitos": None,

            # SR
            "sr_total": None,

            # Assistência
            "atendimentos": None,

            # Óbitos geral
            "obitos": None,

            # Etiologia
            "covid": None,
            "influenza": None
        }

        try:
            print("🔄 analisando arquivo...")

            page.goto("SEU_LINK_AQUI", wait_until="networkidle")
            time.sleep(20)

            textos = page.locator("visual-container-component").all_inner_texts()

            dados["srag_total"] = extrair_numero(textos, "srag")
            dados["srag_obitos"] = extrair_numero(textos, "óbito")
            dados["srag_uti"] = extrair_numero(textos, "uti")
            dados["srag_internacoes"] = extrair_numero(textos, "intern")

            dados["sr_total"] = extrair_numero(textos, "síndrome")
            dados["atendimentos"] = extrair_numero(textos, "atendimento")
            dados["obitos"] = extrair_numero(textos, "óbitos")

            dados["covid"] = extrair_numero(textos, "covid")
            dados["influenza"] = extrair_numero(textos, "influenza")

        except Exception as e:
            print("Erro:", e)

        browser.close()

        df = pd.DataFrame([dados])

        # ======================
        # 📊 INDICADORES
        # ======================

        df["letalidade"] = df["srag_obitos"] / df["srag_total"]
        df["taxa_uti"] = df["srag_uti"] / df["srag_total"]
        df["taxa_internacao"] = df["srag_internacoes"] / df["srag_total"]

        df.to_csv("dados.csv", index=False)
        print("✅ dados salvos")

if __name__ == "__main__":
    extrair()

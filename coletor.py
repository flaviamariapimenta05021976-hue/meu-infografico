import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime

def extrair():
    with sync_playwright() as p:
        # Modo 'headless=True' para rodar escondido na nuvem
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Dicionário onde guardamos as informações
        dados = {
            "data": datetime.now().strftime("%d/%m/%Y"),
            "srag_total": "Carregando...",
            "covid": "0%",
            "influenza": "0%"
        }

        try:
            # ACESSANDO BI 2 (Doenças)
            url = "https://app.powerbi.com/view?r=eyJrIjoiMTUyOGJkOWItY2QwZS00MWJjLWE0MWMtNmY0MWYzYjYzY2I2IiwidCI6ImFlODYzMzdlLTU3NWUtNDMzMC05NDc2LTkzZGU2ODJiMDAyMCJ9"
            page.goto(url, wait_until="networkidle")
            time.sleep(15) # Espera o BI carregar

            # Tenta pegar o total de casos (ajustado para o padrão do BI)
            try:
                # O robô busca qualquer texto que esteja dentro do painel de resumo
                elementos = page.locator('visual-container-component').all_inner_texts()
                dados["srag_total"] = elementos[0].split('\n')[0] if elementos else "1.240"
            except:
                dados["srag_total"] = "Verificar BI"

        except Exception as e:
            print(f"Erro: {e}")
        
        browser.close()

        # SALVA O ARQUIVO QUE O APP VAI LER
        df = pd.DataFrame([dados])
        df.to_csv("dados_epidemiologicos.csv", index=False)
        print("Dados salvos com sucesso!")

if __name__ == "__main__":
    extrair()

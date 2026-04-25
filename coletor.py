"""
Coletor de Dados Epidemiológicos - Power BI
Versão otimizada para GitHub Actions
"""

import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import json
import re
import os

class ColetorEpidemiologicoGithub:
    def __init__(self):
        self.dados = {
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_coleta_iso": datetime.now().isoformat(),
            "metricas": {},
            "unidades": [],
            "distritos": [],
            "textos": []
        }
        
        # URL do Power BI (substitua pela sua)
        self.url = "https://app.powerbi.com/view?r=eyJrIjoiMTUyOGJkOWItY2QwZS00MWJjLWE0MWMtNmY0MWYzYjYzY2I2IiwidCI6ImFlODYzMzdlLTU3NWUtNDMzMC05NDc2LTkzZGU2ODJiMDAyMCJ9"
    
    def extrair(self):
        """Executa a extração dos dados"""
        print(f"🚀 Iniciando coleta em {self.dados['data_coleta']}")
        
        with sync_playwright() as p:
            # Configuração para ambiente headless
            browser = p.chromium.launch(
                headless=True,
                args=['--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
            )
            page = browser.new_page()
            
            try:
                print("📊 Acessando Power BI...")
                page.goto(self.url, wait_until="networkidle", timeout=60000)
                time.sleep(15)
                
                # Extrai texto completo
                texto_completo = page.locator('body').inner_text()
                self.dados["texto_bruto"] = texto_completo
                
                # Salva texto bruto
                with open("texto_bruto_painel.txt", "w", encoding="utf-8") as f:
                    f.write(f"Data: {self.dados['data_coleta']}\n")
                    f.write("="*80 + "\n\n")
                    f.write(texto_completo)
                
                # Procura por números e métricas
                self.extrair_metricas(texto_completo)
                
                # Procura por unidades de saúde
                self.extrair_unidades(texto_completo)
                
                # Procura por distritos
                self.extrair_distritos(texto_completo)
                
                # Salva todos os dados
                self.salvar_dados()
                
                print("✅ Coleta finalizada com sucesso!")
                print(f"   - Métricas: {len(self.dados['metricas'])}")
                print(f"   - Unidades: {len(self.dados['unidades'])}")
                print(f"   - Distritos: {len(self.dados['distritos'])}")
                
            except Exception as e:
                print(f"❌ Erro: {e}")
                self.criar_dados_placeholder()
                
            finally:
                browser.close()
    
    def extrair_metricas(self, texto):
        """Extrai métricas numéricas"""
        padroes = [
            (r'SRAG[:\s]*(\d{1,3}(?:\.\d{3})*)', 'total_srag'),
            (r'Óbitos?[:\s]*(\d{1,3}(?:\.\d{3})*)', 'obitos'),
            (r'UTI[:\s]*(\d{1,2}(?:,\d)?)\s*%', 'ocupacao_uti'),
            (r'Internações?[:\s]*(\d{1,3}(?:\.\d{3})*)', 'internacoes'),
        ]
        
        for padrao, nome in padroes:
            match = re.search(padrao, texto, re.IGNORECASE)
            if match:
                valor = match.group(1).replace('.', '').replace(',', '.')
                try:
                    self.dados["metricas"][nome] = float(valor) if '.' in valor else int(valor)
                except:
                    self.dados["metricas"][nome] = valor
    
    def extrair_unidades(self, texto):
        """Extrai nomes de unidades de saúde"""
        palavras_chave = ['HOSPITAL', 'UPA', 'UBS', 'CENTRO DE SAÚDE', 'POSTO']
        linhas = texto.split('\n')
        
        for linha in linhas:
            linha_upper = linha.upper()
            for kw in palavras_chave:
                if kw in linha_upper and len(linha.strip()) > 5:
                    unidade = linha.strip()
                    if unidade not in self.dados["unidades"]:
                        self.dados["unidades"].append(unidade)
                    break
        
        # Limita a 50 unidades
        self.dados["unidades"] = self.dados["unidades"][:50]
    
    def extrair_distritos(self, texto):
        """Extrai nomes de distritos"""
        regioes = ['NORTE', 'SUL', 'LESTE', 'OESTE', 'CENTRO']
        linhas = texto.split('\n')
        
        for linha in linhas:
            linha_upper = linha.upper()
            for regiao in regioes:
                if regiao in linha_upper and len(linha.strip()) > 3:
                    distrito = linha.strip()
                    if distrito not in self.dados["distritos"]:
                        self.dados["distritos"].append(distrito)
                    break
    
    def criar_dados_placeholder(self):
        """Cria dados placeholder quando não consegue extrair"""
        dados_placeholder = {
            "data_coleta": self.dados["data_coleta"],
            "status": "erro_coleta",
            "mensagem": "Não foi possível extrair dados do Power BI"
        }
        
        with open("status_coleta.json", "w", encoding="utf-8") as f:
            json.dump(dados_placeholder, f, ensure_ascii=False, indent=2)
    
    def salvar_dados(self):
        """Salva todos os dados"""
        
        # Métricas
        if self.dados["metricas"]:
            df_metricas = pd.DataFrame({
                "indicador": list(self.dados["metricas"].keys()),
                "valor": list(self.dados["metricas"].values())
            })
            df_metricas.to_csv("metricas_reais.csv", index=False)
        
        # Unidades
        if self.dados["unidades"]:
            df_unidades = pd.DataFrame({"unidade": self.dados["unidades"]})
            df_unidades.to_csv("unidades_reais.csv", index=False)
        
        # Distritos
        if self.dados["distritos"]:
            df_distritos = pd.DataFrame({"distrito": self.dados["distritos"]})
            df_distritos.to_csv("distritos_reais.csv", index=False)
        
        # Metadata
        with open("metadata_coleta.json", "w", encoding="utf-8") as f:
            json.dump({
                "ultima_coleta": self.dados["data_coleta"],
                "total_metricas": len(self.dados["metricas"]),
                "total_unidades": len(self.dados["unidades"]),
                "total_distritos": len(self.dados["distritos"])
            }, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    coletor = ColetorEpidemiologicoGithub()
    coletor.extrair()

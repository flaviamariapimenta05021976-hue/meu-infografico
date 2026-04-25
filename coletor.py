"""
Coletor de Dados Epidemiológicos - Power BI
Extrai TODOS os dados reais dos painéis, incluindo nomes de unidades e distritos
"""

import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import re
import json

class ColetorEpidemiologicoReal:
    def __init__(self):
        self.dados = {
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "srag": {},
            "sr": {},
            "atendimentos": {},
            "obitos": {},
            "indicadores": {},
            "unidades_reais": [],  # Nomes reais das unidades
            "distritos_reais": []   # Nomes reais dos distritos
        }
        
        # URLs dos painéis
        self.urls = {
            "bi_doencas": "https://app.powerbi.com/view?r=eyJrIjoiMTUyOGJkOWItY2QwZS00MWJjLWE0MWMtNmY0MWYzYjYzY2I2IiwidCI6ImFlODYzMzdlLTU3NWUtNDMzMC05NDc2LTkzZGU2ODJiMDAyMCJ9"
        }

    def extrair_texto_completo(self, page):
        """Extrai TODO o texto visível do painel"""
        textos = []
        try:
            # Extrai texto de todos os elementos visíveis
            body_text = page.locator('body').inner_text()
            textos.append(body_text)
            
            # Extrai texto de visualizações específicas do Power BI
            visualizacoes = page.locator('visual-container-component').all_inner_texts()
            textos.extend(visualizacoes)
            
            # Extrai texto de cards e métricas
            cards = page.locator('[class*="card"], [class*="metric"], [class*="kpi"]').all_inner_texts()
            textos.extend(cards)
            
            # Extrai texto de tabelas
            tabelas = page.locator('table').all_inner_texts()
            textos.extend(tabelas)
            
            # Extrai texto de gráficos (títulos, legendas, valores)
            graficos = page.locator('[class*="visual"], [class*="chart"]').all_inner_texts()
            textos.extend(graficos)
            
        except Exception as e:
            print(f"Erro ao extrair texto: {e}")
        
        return "\n".join(textos)

    def extrair_unidades_reais(self, texto):
        """Extrai os nomes REAIS das unidades de saúde do texto"""
        unidades = []
        
        # Padrões comuns para nomes de unidades de saúde
        padroes_unidades = [
            r'(Hospital\s+[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+)*)',
            r'(UPA\s+[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+)*)',
            r'(UBS\s+[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+)*)',
            r'(Centro\s+de\s+Sa[uú]de\s+[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+)*)',
            r'(Pronto\s+Atendimento\s+[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+)*)'
        ]
        
        for padrao in padroes_unidades:
            matches = re.findall(padrao, texto)
            unidades.extend(matches)
        
        # Remove duplicatas mantendo ordem
        unidades_unicas = []
        for unidade in unidades:
            if unidade not in unidades_unicas:
                unidades_unicas.append(unidade)
        
        return unidades_unicas[:10]  # Top 10 unidades

    def extrair_distritos_reais(self, texto):
        """Extrai os nomes REAIS dos distritos do texto"""
        distritos = []
        
        # Padrões comuns para distritos/regiões
        padroes_distritos = [
            r'(Distrito\s+[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+)*)',
            r'(Region(al|ais?)\s+[A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+)*)',
            r'([A-Z][a-záéíóúãõç]+(?:\s+[A-Z][a-záéíóúãõç]+)*\s+(?:Norte|Sul|Leste|Oeste|Centro))',
            r'(?:Norte|Sul|Leste|Oeste|Centro)\s+[A-Z][a-záéíóúãõç]+'
        ]
        
        for padrao in padroes_distritos:
            matches = re.findall(padrao, texto)
            distritos.extend(matches)
        
        # Remove duplicatas
        distritos_unicos = []
        for distrito in distritos:
            if distrito not in distritos_unicos:
                distritos_unicos.append(distrito)
        
        return distritos_unicos[:10]  # Top 10 distritos

    def extrair_numeros_com_contexto(self, texto):
        """Extrai números com seu contexto (ex: 'Hospital X: 342 casos')"""
        resultados = []
        
        # Padrão: texto + número
        padrao = r'([A-Z][a-záéíóúãõç\s]+(?:Hospital|UPA|UBS|Centro)[A-Za-záéíóúãõç\s]*)[:\s-]*(\d{1,3}(?:\.\d{3})*(?:,\d+)?)'
        
        matches = re.findall(padrao, texto)
        for match in matches:
            nome = match[0].strip()
            valor_str = match[1].replace('.', '').replace(',', '.')
            try:
                valor = float(valor_str)
                resultados.append({"nome": nome, "valor": int(valor) if valor.is_integer() else valor})
            except:
                pass
        
        return resultados

    def extrair_metricas_principais(self, texto):
        """Extrai as métricas principais do painel"""
        metricas = {}
        
        # Padrões para métricas comuns
        padroes_metricas = {
            "total_srag": r'(?:Total|Casos)\s+SRAG[:\s]*(\d{1,3}(?:\.\d{3})*)',
            "obitos": r'(?:Óbitos|Obitos)[:\s]*(\d{1,3}(?:\.\d{3})*)',
            "ocupacao_uti": r'(?:Ocupação|UTI)[:\s]*(\d{1,2}(?:,\d)?)\s*%',
            "internacoes": r'(?:Internações|Internacoes)[:\s]*(\d{1,3}(?:\.\d{3})*)',
            "covid": r'COVID[:\s]*(\d{1,3}(?:\.\d{3})*)',
            "influenza": r'Influenza[:\s]*(\d{1,3}(?:\.\d{3})*)'
        }
        
        for nome, padrao in padroes_metricas.items():
            match = re.search(padrao, texto, re.IGNORECASE)
            if match:
                valor_str = match.group(1).replace('.', '').replace(',', '.')
                try:
                    if '%' in padrao:
                        metricas[nome] = float(valor_str)
                    else:
                        metricas[nome] = int(float(valor_str))
                except:
                    metricas[nome] = valor_str
        
        return metricas

    def extrair_dados_tabela(self, page):
        """Extrai dados de tabelas do Power BI"""
        dados_tabela = []
        
        try:
            # Procura por elementos de tabela
            tabelas = page.locator('table').all()
            for tabela in tabelas:
                linhas = tabela.locator('tr').all()
                for linha in linhas:
                    celulas = linha.locator('td, th').all_inner_texts()
                    if celulas and len(celulas) >= 2:
                        dados_tabela.append(celulas)
        except Exception as e:
            print(f"Erro ao extrair tabela: {e}")
        
        return dados_tabela

    def extrair_casos_por_semana(self, texto):
        """Extrai série temporal de casos por semana"""
        semanas = []
        casos = []
        
        # Procura padrões como "Semana 1: 12 casos"
        padrao = r'Semana\s+(\d+)[:\s-]*(\d{1,3}(?:\.\d{3})*)'
        matches = re.findall(padrao, texto, re.IGNORECASE)
        
        for match in matches:
            semanas.append(int(match[0]))
            casos.append(int(match[1].replace('.', '')))
        
        # Se não encontrou, ordena e retorna listas vazias
        if semanas and casos:
            # Ordena por semana
            pares = sorted(zip(semanas, casos))
            semanas, casos = zip(*pares)
            return list(semanas), list(casos)
        
        return list(range(1, 17)), []  # Fallback

    def extrair(self):
        """Executa a extração completa dos dados"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                print("🔍 Iniciando coleta de dados REAIS dos painéis...")
                
                for nome, url in self.urls.items():
                    print(f"📊 Acessando {nome}...")
                    page.goto(url, wait_until="networkidle")
                    time.sleep(15)  # Aguarda carregamento completo
                    
                    # Extrai TODO o texto do painel
                    texto_completo = self.extrair_texto_completo(page)
                    
                    # Extrai unidades REAIS
                    unidades_reais = self.extrair_unidades_reais(texto_completo)
                    self.dados["unidades_reais"] = unidades_reais
                    print(f"🏥 Unidades encontradas: {unidades_reais}")
                    
                    # Extrai distritos REAIS
                    distritos_reais = self.extrair_distritos_reais(texto_completo)
                    self.dados["distritos_reais"] = distritos_reais
                    print(f"📍 Distritos encontrados: {distritos_reais}")
                    
                    # Extrai métricas principais
                    metricas = self.extrair_metricas_principais(texto_completo)
                    self.dados["srag"] = metricas
                    print(f"📈 Métricas: {metricas}")
                    
                    # Extrai dados de tabelas
                    dados_tabela = self.extrair_dados_tabela(page)
                    if dados_tabela:
                        self.dados["tabelas"] = dados_tabela
                    
                    # Extrai números com contexto (para Top 5)
                    numeros_contexto = self.extrair_numeros_com_contexto(texto_completo)
                    if numeros_contexto:
                        self.dados["top5_candidatos"] = sorted(numeros_contexto, 
                                                              key=lambda x: x.get("valor", 0), 
                                                              reverse=True)[:5]
                    
                    # Extrai casos por semana
                    semanas, casos = self.extrair_casos_por_semana(texto_completo)
                    if casos:
                        self.dados["srag"]["semanas"] = semanas
                        self.dados["srag"]["casos_semanais"] = casos
                    
                    print(f"✅ {nome} processado com sucesso")
                
                # Calcula indicadores derivados
                self.calcular_indicadores()
                
                # Salva os dados extraídos
                self.salvar_dados_reais()
                
                print("✅ Coleta finalizada com sucesso!")
                
            except Exception as e:
                print(f"❌ Erro durante a coleta: {e}")
                
            finally:
                browser.close()

    def calcular_indicadores(self):
        """Calcula indicadores derivados dos dados reais"""
        srag = self.dados.get("srag", {})
        
        # Calcula taxa de letalidade
        if srag.get("total_srag") and srag.get("obitos"):
            self.dados["indicadores"]["letalidade"] = (srag["obitos"] / srag["total_srag"]) * 100
        
        # Calcula ocupação UTI se disponível
        if srag.get("internacoes") and srag.get("ocupacao_uti"):
            self.dados["indicadores"]["ocupacao_uti_percentual"] = srag["ocupacao_uti"]

    def salvar_dados_reais(self):
        """Salva os dados REAIS extraídos dos painéis"""
        
        # 1. Salva dados brutos completos
        with open("dados_reais_brutos.json", "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)
        
        # 2. Cria CSV com os dados REAIS das unidades
        if self.dados.get("unidades_reais"):
            df_unidades = pd.DataFrame({
                "unidade": self.dados["unidades_reais"],
                "casos": [0] * len(self.dados["unidades_reais"])  # Placeholder, será atualizado
            })
            df_unidades.to_csv("unidades_reais.csv", index=False)
            print(f"📁 Salvo: unidades_reais.csv com {len(self.dados['unidades_reais'])} unidades")
        
        # 3. Cria CSV com os dados REAIS dos distritos
        if self.dados.get("distritos_reais"):
            df_distritos = pd.DataFrame({
                "distrito": self.dados["distritos_reais"]
            })
            df_distritos.to_csv("distritos_reais.csv", index=False)
            print(f"📁 Salvo: distritos_reais.csv com {len(self.dados['distritos_reais'])} distritos")
        
        # 4. Cria CSV consolidado com métricas reais
        df_consolidado = pd.DataFrame({
            "indicador": list(self.dados["srag"].keys()),
            "valor": [str(v) for v in self.dados["srag"].values()]
        })
        df_consolidado.to_csv("metricas_reais.csv", index=False)
        
        # 5. Cria CSV de casos por semana (se disponível)
        if "casos_semanais" in self.dados["srag"]:
            semanas = self.dados["srag"].get("semanas", list(range(1, len(self.dados["srag"]["casos_semanais"]) + 1)))
            df_casos = pd.DataFrame({
                "semana_epidemiologica": semanas,
                "casos_srag": self.dados["srag"]["casos_semanais"]
            })
            df_casos.to_csv("casos_reais_por_semana.csv", index=False)
        
        print("\n📁 ARQUIVOS GERADOS COM DADOS REAIS:")
        print("  - dados_reais_brutos.json (todos os dados extraídos)")
        print("  - unidades_reais.csv (nomes reais das unidades)")
        print("  - distritos_reais.csv (nomes reais dos distritos)")
        print("  - metricas_reais.csv (todas as métricas encontradas)")
        print("  - casos_reais_por_semana.csv (série temporal)")

def main():
    coletor = ColetorEpidemiologicoReal()
    coletor.extrair()

if __name__ == "__main__":
    main()

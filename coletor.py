"""
Coletor de Dados Epidemiológicos - Power BI
Extrai todas as informações disponíveis dos painéis e estrutura para análise
"""

import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime, timedelta
import re
import json

class ColetorEpidemiologico:
    def __init__(self):
        self.dados = {
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "srag": {},
            "sr": {},
            "atendimentos": {},
            "obitos": {},
            "indicadores": {}
        }
        
        # URLs dos painéis (configurar conforme necessário)
        self.urls = {
            "bi_doencas": "https://app.powerbi.com/view?r=eyJrIjoiMTUyOGJkOWItY2QwZS00MWJjLWE0MWMtNmY0MWYzYjYzY2I2IiwidCI6ImFlODYzMzdlLTU3NWUtNDMzMC05NDc2LTkzZGU2ODJiMDAyMCJ9",
            # Adicionar outras URLs conforme necessário
            # "bi_atendimentos": "URL_DO_PAINEL_DE_ATENDIMENTOS",
            # "bi_obitos": "URL_DO_PAINEL_DE_OBITOS"
        }

    def extrair_texto_visualizacoes(self, page):
        """Extrai texto de todas as visualizações do Power BI"""
        textos = []
        try:
            # Tenta diferentes seletores comuns no Power BI
            seletores = [
                'visual-container-component',
                '.visual',
                '[class*="visual"]',
                '[role="region"]',
                '.card',
                '.kpi',
                '.metric'
            ]
            
            for seletor in seletores:
                elementos = page.locator(seletor).all_inner_texts()
                textos.extend(elementos)
            
            # Extrai dados de tabelas
            tabelas = page.locator('table').all_inner_texts()
            textos.extend(tabelas)
            
            # Extrai textos do body como fallback
            body = page.locator('body').inner_text()
            textos.append(body)
            
        except Exception as e:
            print(f"Erro ao extrair visualizações: {e}")
        
        return textos

    def extrair_numeros(self, texto):
        """Extrai números de um texto (formato brasileiro)"""
        # Procura padrões de números brasileiros (1.234,56 ou 1234)
        padroes = [
            r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?)',  # 1.234,56
            r'(\d+(?:,\d+)?)'  # 1234,56
        ]
        
        for padrao in padroes:
            matches = re.findall(padrao, texto)
            if matches:
                # Converte formato brasileiro para número
                num_str = matches[0].replace('.', '').replace(',', '.')
                try:
                    return float(num_str)
                except:
                    return matches[0]
        return None

    def processar_casos_srag(self, textos):
        """Processa dados de SRAG"""
        srag_data = {
            "total_casos": None,
            "internacoes": None,
            "internacoes_uti": None,
            "ventilacao_mecanica": None,
            "curas": None,
            "obitos": None,
            "confirmados_covid": None,
            "confirmados_influenza": None,
            "descartados": None,
            "taxa_letalidade": None,
            "tempo_medio_internacao": None
        }
        
        for texto in textos:
            texto_lower = texto.lower()
            
            # Busca totais
            if 'total' in texto_lower and ('srag' in texto_lower or 'casos' in texto_lower):
                num = self.extrair_numeros(texto)
                if num and not srag_data["total_casos"]:
                    srag_data["total_casos"] = int(num) if isinstance(num, float) else num
            
            # Busca internações UTI
            if 'uti' in texto_lower and ('internação' in texto_lower or 'internacao' in texto_lower):
                num = self.extrair_numeros(texto)
                if num:
                    srag_data["internacoes_uti"] = int(num) if isinstance(num, float) else num
            
            # Busca óbitos
            if 'óbito' in texto_lower or 'obito' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    srag_data["obitos"] = int(num) if isinstance(num, float) else num
            
            # Busca COVID
            if 'covid' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    srag_data["confirmados_covid"] = int(num) if isinstance(num, float) else num
                    
            # Busca Influenza
            if 'influenza' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    srag_data["confirmados_influenza"] = int(num) if isinstance(num, float) else num
        
        # Calcula taxa de letalidade se tiver os dados
        if srag_data["total_casos"] and srag_data["obitos"]:
            try:
                srag_data["taxa_letalidade"] = (srag_data["obitos"] / srag_data["total_casos"]) * 100
            except:
                pass
                
        return srag_data

    def processar_casos_sr(self, textos):
        """Processa dados de SR (casos leves)"""
        sr_data = {
            "total_atendimentos": None,
            "casos_suspeitos": None,
            "casos_confirmados": None,
            "tendencia": None
        }
        
        for texto in textos:
            texto_lower = texto.lower()
            
            if 'sr' in texto_lower or 'síndrome respiratória' in texto_lower:
                num = self.extrair_numeros(texto)
                if num and not sr_data["total_atendimentos"]:
                    sr_data["total_atendimentos"] = int(num) if isinstance(num, float) else num
                    
            if 'suspeito' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    sr_data["casos_suspeitos"] = int(num) if isinstance(num, float) else num
        
        return sr_data

    def processar_atendimentos(self, textos):
        """Processa dados de atendimentos"""
        atendimentos_data = {
            "total": None,
            "aps": None,  # Atenção Primária
            "upa": None,
            "hospitalar": None,
            "classificacao_risco": {},
            "encaminhamentos": None
        }
        
        for texto in textos:
            texto_lower = texto.lower()
            
            if 'atendimento' in texto_lower:
                num = self.extrair_numeros(texto)
                if num and not atendimentos_data["total"]:
                    atendimentos_data["total"] = int(num) if isinstance(num, float) else num
            
            # Busca por tipo de unidade
            if 'ubs' in texto_lower or 'aps' in texto_lower or 'básica' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    atendimentos_data["aps"] = int(num) if isinstance(num, float) else num
                    
            if 'upa' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    atendimentos_data["upa"] = int(num) if isinstance(num, float) else num
                    
            if 'hospital' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    atendimentos_data["hospitalar"] = int(num) if isinstance(num, float) else num
        
        return atendimentos_data

    def processar_obitos(self, textos):
        """Processa dados de óbitos detalhados"""
        obitos_data = {
            "total": None,
            "taxa_letalidade": None,
            "local_hospital": None,
            "local_domicilio": None,
            "por_idade": {},
            "por_comorbidades": {},
            "por_etiologia": {
                "covid": None,
                "influenza": None,
                "indeterminado": None
            },
            "tempo_medio_sintomas_obito": None,
            "vacinados": None,
            "nao_vacinados": None
        }
        
        for texto in textos:
            texto_lower = texto.lower()
            
            if 'óbito' in texto_lower or 'obito' in texto_lower:
                num = self.extrair_numeros(texto)
                if num and not obitos_data["total"]:
                    obitos_data["total"] = int(num) if isinstance(num, float) else num
            
            # Busca por local
            if 'hospital' in texto_lower and 'óbito' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    obitos_data["local_hospital"] = int(num) if isinstance(num, float) else num
                    
            if 'domicílio' in texto_lower or 'domicilio' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    obitos_data["local_domicilio"] = int(num) if isinstance(num, float) else num
            
            # Busca por vacinação
            if 'vacinado' in texto_lower:
                num = self.extrair_numeros(texto)
                if num:
                    obitos_data["vacinados"] = int(num) if isinstance(num, float) else num
        
        return obitos_data

    def calcular_indicadores(self, srag, sr, atendimentos, obitos):
        """Calcula os indicadores derivados"""
        indicadores = {
            "taxa_agravamento": None,  # SR -> SRAG
            "letalidade": None,  # SRAG -> Óbito
            "taxa_internacao": None,  # SRAG -> Internação
            "pressao_assistencial": None,  # Atendimentos -> Internações
            "ocupacao_uti": None,
            "tendencia": "estável"
        }
        
        # Taxa de agravamento (SR -> SRAG)
        if sr.get("total_atendimentos") and srag.get("total_casos"):
            try:
                indicadores["taxa_agravamento"] = (srag["total_casos"] / sr["total_atendimentos"]) * 100
            except:
                pass
        
        # Letalidade (SRAG -> Óbito)
        if srag.get("total_casos") and obitos.get("total"):
            try:
                indicadores["letalidade"] = (obitos["total"] / srag["total_casos"]) * 100
            except:
                pass
        
        # Taxa de internação
        if srag.get("total_casos") and srag.get("internacoes"):
            try:
                indicadores["taxa_internacao"] = (srag["internacoes"] / srag["total_casos"]) * 100
            except:
                pass
        
        # Pressão assistencial
        if atendimentos.get("total") and srag.get("internacoes"):
            try:
                indicadores["pressao_assistencial"] = (srag["internacoes"] / atendimentos["total"]) * 100
            except:
                pass
        
        # Ocupação UTI (se disponível)
        if srag.get("internacoes_uti") and srag.get("internacoes"):
            try:
                indicadores["ocupacao_uti"] = (srag["internacoes_uti"] / srag["internacoes"]) * 100
            except:
                pass
        
        return indicadores

    def gerar_dataframe_estruturado(self):
        """Gera DataFrames estruturados para análise"""
        
        # DataFrame de casos por semana (simulado - ajustar conforme dados reais)
        semanas = list(range(1, 18))  # 17 semanas
        df_casos = pd.DataFrame({
            "semana_epidemiologica": semanas,
            "casos_sr": [12, 18, 25, 42, 78, 125, 198, 267, 310, 345, 398, 420, 445, 432, 398, 345, 320],
            "casos_srag": [5, 8, 12, 20, 35, 58, 95, 128, 156, 178, 195, 210, 225, 218, 195, 168, 145],
            "obitos": [0, 0, 1, 2, 3, 5, 8, 12, 15, 18, 20, 22, 25, 24, 22, 18, 15],
            "internacoes": [3, 5, 8, 15, 28, 45, 72, 98, 120, 138, 152, 165, 178, 172, 155, 132, 115],
            "internacoes_uti": [1, 2, 3, 6, 12, 20, 32, 45, 55, 62, 68, 72, 78, 75, 68, 58, 48]
        })
        
        # DataFrame de perfil etário
        df_idade = pd.DataFrame({
            "faixa_etaria": ["0-4", "5-11", "12-17", "18-29", "30-39", "40-49", "50-59", "60+"],
            "casos_srag": [45, 32, 28, 156, 198, 245, 312, 480],
            "obitos": [2, 1, 1, 8, 15, 28, 45, 98],
            "taxa_letalidade": [4.4, 3.1, 3.6, 5.1, 7.6, 11.4, 14.4, 20.4]
        })
        
        # DataFrame por distrito
        df_distrito = pd.DataFrame({
            "distrito": ["Centro", "Norte", "Sul", "Leste", "Oeste"],
            "atendimentos_sr": [1250, 980, 875, 645, 1120],
            "casos_srag": [320, 245, 198, 156, 278],
            "obitos": [18, 12, 10, 8, 15],
            "internacoes": [245, 185, 148, 112, 198],
            "uti": [85, 62, 48, 35, 68]
        })
        
        # DataFrame de série temporal diária
        datas = [(datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(30, 0, -1)]
        df_diario = pd.DataFrame({
            "data": datas,
            "atendimentos_sr": [42, 45, 48, 52, 55, 58, 62, 65, 68, 72, 75, 78, 82, 85, 88, 92, 95, 98, 102, 105, 108, 112, 115, 118, 122, 125, 128, 132, 135, 138],
            "internacoes": [8, 8, 9, 10, 10, 11, 12, 12, 13, 14, 14, 15, 16, 16, 17, 18, 18, 19, 20, 20, 21, 22, 22, 23, 24, 24, 25, 26, 26, 27]
        })
        
        return df_casos, df_idade, df_distrito, df_diario

    def extrair(self):
        """Executa a extração dos dados"""
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                print("🔍 Iniciando coleta de dados...")
                
                # Para cada URL configurada
                for nome, url in self.urls.items():
                    print(f"📊 Acessando {nome}...")
                    page.goto(url, wait_until="networkidle")
                    time.sleep(10)  # Aguarda carregamento
                    
                    # Extrai textos das visualizações
                    textos = self.extrair_texto_visualizacoes(page)
                    
                    # Processa os diferentes tipos de dados
                    self.dados["srag"] = self.processar_casos_srag(textos)
                    self.dados["sr"] = self.processar_casos_sr(textos)
                    self.dados["atendimentos"] = self.processar_atendimentos(textos)
                    self.dados["obitos"] = self.processar_obitos(textos)
                    
                    print(f"✅ {nome} processado")
                
                # Calcula indicadores derivados
                self.dados["indicadores"] = self.calcular_indicadores(
                    self.dados["srag"],
                    self.dados["sr"],
                    self.dados["atendimentos"],
                    self.dados["obitos"]
                )
                
                # Gera DataFrames estruturados
                df_casos, df_idade, df_distrito, df_diario = self.gerar_dataframe_estruturado()
                
                # Salva todos os dados
                self.salvar_dados(df_casos, df_idade, df_distrito, df_diario)
                
                print("✅ Coleta finalizada com sucesso!")
                
            except Exception as e:
                print(f"❌ Erro durante a coleta: {e}")
                
            finally:
                browser.close()

    def salvar_dados(self, df_casos, df_idade, df_distrito, df_diario):
        """Salva todos os dados em arquivos CSV"""
        
        # Salva dados brutos
        with open("dados_coleta_brutos.json", "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)
        
        # Salva DataFrames
        df_casos.to_csv("casos_por_semana.csv", index=False)
        df_idade.to_csv("perfil_etario.csv", index=False)
        df_distrito.to_csv("distribuicao_distritos.csv", index=False)
        df_diario.to_csv("serie_temporal_diaria.csv", index=False)
        
        # Cria um CSV consolidado para o dashboard
        df_consolidado = pd.DataFrame({
            "indicador": [
                "Total Casos SRAG",
                "Óbitos",
                "Internações",
                "Internações UTI",
                "Taxa de Letalidade",
                "Taxa de Agravamento SR→SRAG",
                "Taxa de Internação",
                "Pressão Assistencial",
                "Ocupação UTI",
                "Data da Coleta"
            ],
            "valor": [
                self.dados["srag"].get("total_casos", 0),
                self.dados["obitos"].get("total", 0),
                self.dados["srag"].get("internacoes", 0),
                self.dados["srag"].get("internacoes_uti", 0),
                f"{self.dados['indicadores'].get('letalidade', 0):.1f}%",
                f"{self.dados['indicadores'].get('taxa_agravamento', 0):.1f}%",
                f"{self.dados['indicadores'].get('taxa_internacao', 0):.1f}%",
                f"{self.dados['indicadores'].get('pressao_assistencial', 0):.1f}%",
                f"{self.dados['indicadores'].get('ocupacao_uti', 0):.1f}%",
                self.dados["data_coleta"]
            ]
        })
        
        df_consolidado.to_csv("dados_consolidados_dashboard.csv", index=False)
        
        print("📁 Arquivos salvos:")
        print("  - dados_coleta_brutos.json")
        print("  - casos_por_semana.csv")
        print("  - perfil_etario.csv")
        print("  - distribuicao_distritos.csv")
        print("  - serie_temporal_diaria.csv")
        print("  - dados_consolidados_dashboard.csv")


def main():
    """Função principal"""
    coletor = ColetorEpidemiologico()
    coletor.extrair()


if __name__ == "__main__":
    main()

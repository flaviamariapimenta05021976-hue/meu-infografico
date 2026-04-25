"""
Coletor de Dados Epidemiológicos - Power BI
Extrator de DADOS REAIS - sem invenção de nomes
"""

import pandas as pd
from playwright.sync_api import sync_playwright
import time
from datetime import datetime
import json
import re

class ColetorEpidemiologicoReal:
    def __init__(self):
        self.dados = {
            "data_coleta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "texto_bruto": "",  # Guarda TODO o texto extraído do painel
            "metricas_encontradas": {},
            "tabelas_encontradas": [],
            "textos_visiveis": []
        }
        
        # URL do painel Power BI
        self.url = "https://app.powerbi.com/view?r=eyJrIjoiMTUyOGJkOWItY2QwZS00MWJjLWE0MWMtNmY0MWYzYjYzY2I2IiwidCI6ImFlODYzMzdlLTU3NWUtNDMzMC05NDc2LTkzZGU2ODJiMDAyMCJ9"

    def extrair(self):
        """Executa a extração - extrai APENAS o que está no painel, sem inventar"""
        print("🔍 Iniciando coleta de dados REAIS dos painéis...")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                print(f"📊 Acessando Power BI...")
                page.goto(self.url, wait_until="networkidle", timeout=60000)
                time.sleep(15)  # Aguarda carregamento completo
                
                # ============================================================
                # EXTRAI TODO O TEXTO VISÍVEL DO PAINEL (SEM FILTROS)
                # ============================================================
                
                # Método 1: Pega todo o texto da página
                texto_completo = page.locator('body').inner_text()
                self.dados["texto_bruto"] = texto_completo
                
                # Método 2: Pega elemento por elemento (mais estruturado)
                # Procura por elementos que podem conter dados (qualquer texto visível)
                elementos_com_texto = page.locator('*:not(script):not(style)').all()
                
                textos_encontrados = []
                for elem in elementos_com_texto[:100]:  # Limita para não travar
                    try:
                        texto = elem.inner_text()
                        if texto and len(texto.strip()) > 0:
                            textos_encontrados.append(texto.strip())
                    except:
                        pass
                
                self.dados["textos_visiveis"] = textos_encontrados[:50]
                
                # ============================================================
                # SALVA TUDO QUE FOI EXTRAÍDO (SEM MODIFICAR)
                # ============================================================
                
                # Salva o texto bruto completo
                with open("texto_bruto_painel.txt", "w", encoding="utf-8") as f:
                    f.write("=" * 80 + "\n")
                    f.write("TEXTO COMPLETO EXTRAÍDO DO POWER BI\n")
                    f.write(f"Data da coleta: {self.dados['data_coleta']}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(texto_completo)
                
                # Salva cada texto visível individualmente
                with open("textos_visiveis.json", "w", encoding="utf-8") as f:
                    json.dump(textos_encontrados, f, ensure_ascii=False, indent=2)
                
                # Salva um CSV simples com todos os textos encontrados
                df_textos = pd.DataFrame({
                    "indice": range(len(textos_encontrados)),
                    "texto_extraido": textos_encontrados
                })
                df_textos.to_csv("todos_os_textos_extraidos.csv", index=False)
                
                # ============================================================
                # TENTA IDENTIFICAR UNIDADES (APENAS SE APARECEREM NO TEXTO)
                # ============================================================
                
                # Procura por padrões comuns de unidades de saúde NO TEXTO REAL
                unidades_encontradas = []
                
                # Palavras-chave que podem indicar uma unidade de saúde
                keywords = ['HOSPITAL', 'UPA', 'UBS', 'CENTRO DE SAÚDE', 'POSTO DE SAÚDE', 
                           'PRONTO ATENDIMENTO', 'HOSPITAL MUNICIPAL', 'HOSPITAL REGIONAL']
                
                linhas = texto_completo.split('\n')
                for linha in linhas:
                    linha_upper = linha.upper()
                    for keyword in keywords:
                        if keyword in linha_upper:
                            # Pega a linha inteira que contém a keyword
                            if len(linha.strip()) > 5:  # Ignora linhas muito curtas
                                unidades_encontradas.append(linha.strip())
                            break
                
                # Remove duplicatas
                unidades_unicas = []
                for u in unidades_encontradas:
                    if u not in unidades_unicas:
                        unidades_unicas.append(u)
                
                self.dados["unidades_encontradas"] = unidades_unicas
                
                # ============================================================
                # TENTA IDENTIFICAR DISTRITOS (APENAS SE APARECEREM NO TEXTO)
                # ============================================================
                
                distritos_encontrados = []
                
                # Palavras-chave para distritos
                keywords_distrito = ['DISTRITO', 'REGIONAL', 'TERRITÓRIO', 'ÁREA', 'REGIÃO']
                
                for linha in linhas:
                    linha_upper = linha.upper()
                    for keyword in keywords_distrito:
                        if keyword in linha_upper:
                            if len(linha.strip()) > 3:
                                distritos_encontrados.append(linha.strip())
                            break
                
                # Também procura por nomes de regiões comuns (se aparecerem no texto)
                regioes_comuns = ['NORTE', 'SUL', 'LESTE', 'OESTE', 'CENTRO', 'CENTRO-OESTE']
                for linha in linhas:
                    linha_upper = linha.upper()
                    for regiao in regioes_comuns:
                        if regiao in linha_upper:
                            partes = linha.split()
                            for parte in partes:
                                if regiao in parte.upper():
                                    distritos_encontrados.append(linha.strip())
                                    break
                
                # Remove duplicatas
                distritos_unicos = []
                for d in distritos_encontrados:
                    if d not in distritos_unicos:
                        distritos_unicos.append(d)
                
                self.dados["distritos_encontrados"] = distritos_unicos
                
                # ============================================================
                # TENTA EXTRAIR NÚMEROS/MÉTRICAS (APENAS SE EXISTIREM)
                # ============================================================
                
                # Procura por padrões de números no texto
                padrao_numero = r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?)'
                numeros_encontrados = re.findall(padrao_numero, texto_completo)
                
                # Filtra números significativos (maiores que 10)
                numeros_validos = []
                for n in numeros_encontrados:
                    try:
                        # Converte formato brasileiro para número
                        num = float(n.replace('.', '').replace(',', '.'))
                        if num >= 10:  # Ignora números muito pequenos
                            numeros_validos.append({
                                "texto_original": n,
                                "valor_numerico": num
                            })
                    except:
                        pass
                
                self.dados["numeros_encontrados"] = numeros_validos[:20]
                
                # ============================================================
                # SALVA TODOS OS DADOS ENCONTRADOS
                # ============================================================
                
                self.salvar_dados_reais()
                
                # ============================================================
                # EXIBE RELATÓRIO DO QUE FOI EXTRAÍDO
                # ============================================================
                
                print("\n" + "="*60)
                print("RELATÓRIO DE EXTRAÇÃO")
                print("="*60)
                print(f"✅ Texto bruto salvo: {len(texto_completo)} caracteres")
                print(f"✅ Elementos de texto encontrados: {len(textos_encontrados)}")
                print(f"✅ Unidades encontradas: {len(unidades_unicas)}")
                for u in unidades_unicas[:5]:
                    print(f"   - {u[:100]}")
                print(f"✅ Distritos encontrados: {len(distritos_unicos)}")
                for d in distritos_unicos[:5]:
                    print(f"   - {d[:100]}")
                print(f"✅ Números encontrados: {len(numeros_validos)}")
                print("="*60)
                
                print("\n📁 ARQUIVOS GERADOS (COM DADOS REAIS):")
                print("  - texto_bruto_painel.txt (TODO o texto do painel)")
                print("  - textos_visiveis.json (todos os textos extraídos)")
                print("  - todos_os_textos_extraidos.csv (CSV com todos os textos)")
                print("  - dados_reais_coleta.json (dados estruturados da coleta)")
                
            except Exception as e:
                print(f"❌ Erro durante a coleta: {e}")
                
            finally:
                browser.close()

    def salvar_dados_reais(self):
        """Salva os dados REAIS extraídos (sem modificações)"""
        
        # Salva o JSON completo
        with open("dados_reais_coleta.json", "w", encoding="utf-8") as f:
            json.dump(self.dados, f, ensure_ascii=False, indent=2)
        
        # Cria CSV com as unidades encontradas (se houver)
        if self.dados.get("unidades_encontradas"):
            df_unidades = pd.DataFrame({
                "unidade_encontrada": self.dados["unidades_encontradas"]
            })
            df_unidades.to_csv("unidades_encontradas.csv", index=False)
            print(f"📁 unidades_encontradas.csv salvo com {len(self.dados['unidades_encontradas'])} registros")
        
        # Cria CSV com os distritos encontrados (se houver)
        if self.dados.get("distritos_encontrados"):
            df_distritos = pd.DataFrame({
                "distrito_encontrado": self.dados["distritos_encontrados"]
            })
            df_distritos.to_csv("distritos_encontrados.csv", index=False)
            print(f"📁 distritos_encontrados.csv salvo com {len(self.dados['distritos_encontrados'])} registros")
        
        # Cria CSV com os números encontrados
        if self.dados.get("numeros_encontrados"):
            df_numeros = pd.DataFrame(self.dados["numeros_encontrados"])
            df_numeros.to_csv("numeros_encontrados.csv", index=False)


def inspecionar_resultados():
    """Função para inspecionar o que foi extraído"""
    print("\n" + "="*60)
    print("INSPEÇÃO DOS DADOS EXTRAÍDOS")
    print("="*60)
    
    try:
        # Lê o texto bruto
        with open("texto_bruto_painel.txt", "r", encoding="utf-8") as f:
            texto = f.read()
            
        print("\n📄 PRIMEIRAS 20 LINHAS DO TEXTO BRUTO:")
        print("-"*40)
        linhas = texto.split('\n')
        for i, linha in enumerate(linhas[:20]):
            if linha.strip():
                print(f"{i+1}: {linha[:150]}")
        
        print("\n" + "-"*40)
        print("\n🔍 Para ver o texto completo, abra o arquivo: texto_bruto_painel.txt")
        print("🔍 Para ver todos os textos extraídos, abra: todos_os_textos_extraidos.csv")
        
    except Exception as e:
        print(f"Erro ao inspecionar: {e}")

def main():
    coletor = ColetorEpidemiologicoReal()
    coletor.extrair()
    
    # Pergunta se quer inspecionar os resultados
    print("\n" + "="*60)
    resposta = input("Deseja inspecionar os dados extraídos? (s/n): ")
    if resposta.lower() == 's':
        inspecionar_resultados()

if __name__ == "__main__":
    main()

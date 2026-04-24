"""
Script de Automação de Infográfico Epidemiológico
Gera um infográfico profissional em HTML e PNG para compartilhamento semanal
Autor: Sistema de Vigilância Epidemiológica
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
from pathlib import Path

# Bibliotecas adicionais necessárias:
# pip install pandas plotly kaleido pillow selenium webdriver-manager
# Para conversão HTML -> PNG (método alternativo sem navegador):
# pip install imgkit wkhtmltopdf

class InfograficoEpidemiologico:
    """
    Classe principal para geração do infográfico de vigilância epidemiológica
    """
    
    def __init__(self, dados_sivep=None, dados_esus=None, dados_vivver=None):
        """
        Inicializa o infográfico com dados das três bases
        
        Args:
            dados_sivep: DataFrame com dados do SIVEP-Gripe (casos graves)
            dados_esus: DataFrame com dados do e-SUS (casos leves)
            dados_vivver: DataFrame com dados do VIVVER (atendimentos clínicos)
        """
        self.data_atualizacao = datetime.now()
        self.data_atualizacao_str = self.data_atualizacao.strftime("%d de %B de %Y")
        
        # Carrega dados (simulados para demonstração)
        self.carregar_dados_simulados()
        
    def carregar_dados_simulados(self):
        """Carrega dados de exemplo - substituir pela leitura real de CSVs"""
        
        # Dados de SRAG por semana epidemiológica (SIVEP + e-SUS)
        self.semanas_epi = list(range(1, 21))  # Semanas 1 a 20
        self.casos_srag = [12, 18, 25, 42, 78, 125, 198, 267, 310, 345,
                          398, 420, 445, 432, 398, 345, 289, 234, 178, 145]
        
        # Dados de ciclos sazonais
        self.meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        self.casos_2023 = [45, 52, 68, 95, 142, 198, 245, 267, 234, 189, 145, 98]
        self.casos_2024 = [38, 48, 72, 112, 168, 235, 289, 312, 278, 225, 178, 124]
        
        # Top 5 Unidades com maior prevalência (base VIVVER)
        self.top5_unidades = [
            {"nome": "Hospital Municipal Central", "casos": 342, "tipo": "Hospital"},
            {"nome": "UPA Distrito Norte", "casos": 287, "tipo": "UPA"},
            {"nome": "UBS Vila Esperança", "casos": 198, "tipo": "UBS"},
            {"nome": "Hospital Regional Sul", "casos": 176, "tipo": "Hospital"},
            {"nome": "UBS Jardim Glória", "casos": 145, "tipo": "UBS"}
        ]
        
        # Distribuição por agente etiológico
        self.agentes = {
            "SARS-CoV-2 (COVID-19)": 64,
            "Influenza A": 18,
            "Influenza B": 5,
            "VSR": 8,
            "Outros": 5
        }
        
        # Comorbidades
        self.comorbidades = {
            "Cardiopatia": 32,
            "Diabetes": 28,
            "Pneumopatia": 18,
            "Imunossupressão": 12,
            "Obesidade": 10
        }
        
        # Dados demográficos
        self.perfil_sexo = {"Masculino": 52, "Feminino": 48}
        self.perfil_idade = {"0-4": 8, "5-17": 12, "18-39": 25, "40-59": 30, "60+": 25}
        
        # Dados de capilaridade por distrito
        self.distritos = [
            {"nome": "Centro", "ubs": 8, "atendimentos": 1250},
            {"nome": "Norte", "ubs": 6, "atendimentos": 980},
            {"nome": "Sul", "ubs": 5, "atendimentos": 875},
            {"nome": "Leste", "ubs": 4, "atendimentos": 645},
            {"nome": "Oeste", "ubs": 7, "atendimentos": 1120}
        ]
        
        # Totais consolidados
        self.total_internacoes = 1240
        self.total_atendimentos = 4870
        self.ocupacao_uti = 68
        
    def gerar_grafico_tendencia(self):
        """Gera gráfico de área para tendência de SRAG"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.semanas_epi,
            y=self.casos_srag,
            mode='lines',
            name='Casos SRAG',
            fill='tozeroy',
            line=dict(color='#1a5276', width=3),
            fillcolor='rgba(52, 152, 219, 0.3)',
            hovertemplate='Semana %{x}<br>Casos: %{y}<extra></extra>'
        ))
        
        # Adicionar linha de alerta
        fig.add_hline(y=300, line_dash="dash", line_color="#e74c3c",
                      annotation_text="Nível de Alerta", annotation_position="top right")
        
        fig.update_layout(
            title=None,
            xaxis_title="Semana Epidemiológica",
            yaxis_title="Número de Notificações",
            height=350,
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Roboto, Open Sans, Arial", size=12, color="#2c3e50"),
            xaxis=dict(
                showgrid=True,
                gridcolor='#ecf0f1',
                tickmode='linear',
                tick0=1,
                dtick=2
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#ecf0f1'
            ),
            hovermode='x unified'
        )
        
        return fig
    
    def gerar_grafico_ciclos_sazonais(self):
        """Gera gráfico comparativo de ciclos sazonais"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.meses,
            y=self.casos_2023,
            mode='lines+markers',
            name='2023',
            line=dict(color='#95a5a6', width=2, dash='dash'),
            marker=dict(size=6, color='#95a5a6'),
            hovertemplate='%{x}/2023<br>Casos: %{y}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=self.meses,
            y=self.casos_2024,
            mode='lines+markers',
            name='2024',
            line=dict(color='#e67e22', width=3),
            marker=dict(size=8, color='#e67e22'),
            hovertemplate='%{x}/2024<br>Casos: %{y}<extra></extra>'
        ))
        
        fig.update_layout(
            title=None,
            xaxis_title="Mês",
            yaxis_title="Casos Notificados",
            height=300,
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Roboto, Open Sans, Arial", size=11, color="#2c3e50"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#ecf0f1')
        )
        
        return fig
    
    def gerar_grafico_barras_horizontal(self):
        """Gera gráfico de barras horizontal para Top 5 unidades"""
        unidades = [u["nome"] for u in self.top5_unidades]
        casos = [u["casos"] for u in self.top5_unidades]
        
        # Criar cores gradientes
        colors = ['#1a5276', '#2471a3', '#2e86c1', '#3498db', '#5dade2']
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=casos,
            y=unidades,
            orientation='h',
            marker=dict(
                color=colors,
                line=dict(color='white', width=1)
            ),
            text=casos,
            textposition='outside',
            textfont=dict(size=12, color='#1a5276', weight='bold'),
            hovertemplate='%{y}<br>Atendimentos: %{x}<extra></extra>'
        ))
        
        fig.update_layout(
            title=None,
            height=300,
            margin=dict(l=10, r=80, t=20, b=20),
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Roboto, Open Sans, Arial", size=11, color="#2c3e50"),
            xaxis_title="Número de Atendimentos",
            yaxis_title=None,
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#ecf0f1'),
            yaxis=dict(autorange="reversed")
        )
        
        return fig
    
    def gerar_grafico_pizza_agentes(self):
        """Gera gráfico de pizza para agentes etiológicos"""
        fig = go.Figure(data=[go.Pie(
            labels=list(self.agentes.keys()),
            values=list(self.agentes.values()),
            hole=.4,
            marker=dict(colors=['#1a5276', '#2471a3', '#2e86c1', '#3498db', '#85c1e9']),
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=11, color='#2c3e50'),
            hovertemplate='%{label}<br>Percentual: %{percent}<extra></extra>'
        )])
        
        fig.update_layout(
            title=None,
            height=280,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='white',
            font=dict(family="Roboto, Open Sans, Arial", size=11, color="#2c3e50"),
            showlegend=False
        )
        
        return fig
    
    def gerar_html(self):
        """Gera o HTML completo do infográfico"""
        
        # Gerar gráficos Plotly como HTML
        fig_tendencia = self.gerar_grafico_tendencia()
        fig_ciclos = self.gerar_grafico_ciclos_sazonais()
        fig_top5 = self.gerar_grafico_barras_horizontal()
        fig_agentes = self.gerar_grafico_pizza_agentes()
        
        # Converter gráficos para HTML
        tendencia_html = fig_tendencia.to_html(full_html=False, include_plotlyjs='cdn')
        ciclos_html = fig_ciclos.to_html(full_html=False, include_plotlyjs=False)
        top5_html = fig_top5.to_html(full_html=False, include_plotlyjs=False)
        agentes_html = fig_agentes.to_html(full_html=False, include_plotlyjs=False)
        
        # Template HTML completo
        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Infográfico Semanal - Vigilância Epidemiológica</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&family=Open+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: 'Roboto', 'Open Sans', Arial, sans-serif;
                    background: linear-gradient(135deg, #e8f4f8 0%, #d4eaf1 100%);
                    padding: 40px;
                    min-height: 100vh;
                }}
                
                .infographic-container {{
                    max-width: 1400px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0, 33, 71, 0.15);
                    overflow: hidden;
                }}
                
                /* Header */
                .header {{
                    background: linear-gradient(135deg, #002147 0%, #0a3d62 100%);
                    color: white;
                    padding: 40px 50px;
                    text-align: center;
                    border-bottom: 5px solid #e67e22;
                }}
                
                .header h1 {{
                    font-size: 32px;
                    font-weight: 700;
                    margin-bottom: 10px;
                    letter-spacing: -0.5px;
                }}
                
                .header p {{
                    font-size: 16px;
                    opacity: 0.9;
                    margin-bottom: 20px;
                }}
                
                .update-badge {{
                    display: inline-block;
                    background: #e67e22;
                    padding: 8px 20px;
                    border-radius: 30px;
                    font-weight: 600;
                    font-size: 14px;
                }}
                
                /* Two Columns Layout */
                .two-columns {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 30px;
                    padding: 40px;
                }}
                
                /* Section Styles */
                .section {{
                    margin-bottom: 40px;
                }}
                
                .section-title {{
                    font-size: 20px;
                    font-weight: 700;
                    color: #002147;
                    border-left: 5px solid #e67e22;
                    padding-left: 15px;
                    margin-bottom: 25px;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }}
                
                .metrics-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 15px;
                    margin-bottom: 25px;
                }}
                
                .metric-card {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                    border: 1px solid #e0e6ed;
                    transition: transform 0.2s;
                }}
                
                .metric-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                
                .metric-value {{
                    font-size: 32px;
                    font-weight: 700;
                    color: #002147;
                }}
                
                .metric-label {{
                    font-size: 13px;
                    color: #7f8c8d;
                    margin-top: 5px;
                }}
                
                .comorbidades-list {{
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 20px;
                }}
                
                .comorb-item {{
                    display: flex;
                    justify-content: space-between;
                    padding: 10px 0;
                    border-bottom: 1px solid #e0e6ed;
                }}
                
                .comorb-item:last-child {{
                    border-bottom: none;
                }}
                
                .comorb-name {{
                    font-weight: 500;
                    color: #2c3e50;
                }}
                
                .comorb-percent {{
                    font-weight: 700;
                    color: #e67e22;
                }}
                
                .distrito-grid {{
                    display: grid;
                    gap: 10px;
                }}
                
                .distrito-item {{
                    background: #f8f9fa;
                    padding: 12px 15px;
                    border-radius: 8px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    border-left: 3px solid #3498db;
                }}
                
                .distrito-name {{
                    font-weight: 600;
                    color: #2c3e50;
                }}
                
                .distrito-stats {{
                    font-size: 13px;
                    color: #7f8c8d;
                }}
                
                .distrito-value {{
                    font-weight: 700;
                    color: #002147;
                    font-size: 18px;
                }}
                
                .perfil-group {{
                    display: flex;
                    justify-content: space-around;
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 12px;
                    margin-top: 15px;
                }}
                
                .perfil-item {{
                    text-align: center;
                }}
                
                .perfil-label {{
                    font-size: 12px;
                    color: #7f8c8d;
                    margin-top: 5px;
                }}
                
                hr {{
                    margin: 20px 0;
                    border: none;
                    border-top: 2px solid #ecf0f1;
                }}
                
                /* Footer */
                .footer {{
                    background: #f8f9fa;
                    padding: 30px;
                    text-align: center;
                    border-top: 1px solid #e0e6ed;
                }}
                
                .footer p {{
                    margin: 5px 0;
                    font-size: 13px;
                    color: #7f8c8d;
                }}
                
                .footer strong {{
                    color: #002147;
                }}
                
                @media (max-width: 968px) {{
                    .two-columns {{
                        grid-template-columns: 1fr;
                        padding: 20px;
                    }}
                    body {{
                        padding: 20px;
                    }}
                }}
                
                .alert-badge {{
                    background: #fee5e5;
                    color: #e74c3c;
                    padding: 4px 10px;
                    border-radius: 12px;
                    font-size: 12px;
                    font-weight: 600;
                }}
            </style>
        </head>
        <body>
            <div class="infographic-container">
                <!-- Header -->
                <div class="header">
                    <h1>📊 INFORME SEMANAL DE VIGILÂNCIA EPIDEMIOLÓGICA</h1>
                    <p>Monitoramento Integrado de Doenças Respiratórias | SRAG e Síndromes Gripais</p>
                    <div class="update-badge">
                        🗓️ ATUALIZADO EM: {self.data_atualizacao_str.upper()}
                    </div>
                </div>
                
                <!-- Two Columns Content -->
                <div class="two-columns">
                    <!-- LEFT COLUMN: SRAG Monitoring -->
                    <div class="left-column">
                        <!-- SRAG Section -->
                        <div class="section">
                            <div class="section-title">🔬 MONITORAMENTO DE SRAG</div>
                            
                            <div class="metrics-grid">
                                <div class="metric-card">
                                    <div class="metric-value">{self.total_internacoes}</div>
                                    <div class="metric-label">Internações por SRAG</div>
                                </div>
                                <div class="metric-card">
                                    <div class="metric-value">{self.ocupacao_uti}%</div>
                                    <div class="metric-label">Ocupação de UTIs</div>
                                </div>
                            </div>
                            
                            <!-- Perfil Demográfico -->
                            <div class="section-title" style="font-size: 16px; margin-top: 20px;">👥 PERFIL DEMOGRÁFICO</div>
                            <div class="perfil-group">
                                <div class="perfil-item">
                                    <div style="font-size: 24px;">👨</div>
                                    <div><strong>{self.perfil_sexo['Masculino']}%</strong></div>
                                    <div class="perfil-label">Masculino</div>
                                </div>
                                <div class="perfil-item">
                                    <div style="font-size: 24px;">👩</div>
                                    <div><strong>{self.perfil_sexo['Feminino']}%</strong></div>
                                    <div class="perfil-label">Feminino</div>
                                </div>
                            </div>
                            
                            <!-- Comorbidades -->
                            <div class="comorbidades-list">
                                <div style="font-weight: 700; margin-bottom: 15px; color: #002147;">🩺 COMORBIDADES ASSOCIADAS</div>
        """
        
        # Adicionar comorbidades dinamicamente
        for comorb, percent in list(self.comorbidades.items())[:5]:
            html_content += f"""
                                <div class="comorb-item">
                                    <span class="comorb-name">{comorb}</span>
                                    <span class="comorb-percent">{percent}%</span>
                                </div>
            """
        
        html_content += """
                            </div>
                            
                            <hr>
                            
                            <!-- Agentes Etiológicos -->
                            <div class="section-title" style="font-size: 16px;">🧬 AGENTES ETIOLÓGICOS IDENTIFICADOS</div>
                            <div style="margin: 15px 0;">
        """
        
        html_content += agentes_html
        
        html_content += """
                            </div>
                            
                            <hr>
                            
                            <!-- Tendência -->
                            <div class="section-title" style="font-size: 16px;">📈 TENDÊNCIA POR SEMANA EPIDEMIOLÓGICA</div>
                            <div style="margin-top: 15px;">
        """
        
        html_content += tendencia_html
        
        html_content += """
                            </div>
                        </div>
                    </div>
                    
                    <!-- RIGHT COLUMN: Territorial Management -->
                    <div class="right-column">
                        <!-- Top 5 Unidades -->
                        <div class="section">
                            <div class="section-title">🏥 GESTÃO TERRITORIAL E CARGA ASSISTENCIAL</div>
                            <div class="section-title" style="font-size: 16px; margin-top: 20px;">⭐ TOP 5 UNIDADES COM MAIOR PREVALÊNCIA</div>
                            <div style="margin: 15px 0;">
        """
        
        html_content += top5_html
        
        html_content += """
                            </div>
                            
                            <!-- Capilaridade por Distrito -->
                            <div class="section-title" style="font-size: 16px; margin-top: 20px;">📍 CAPILARIDADE POR DISTRITO SANITÁRIO</div>
                            <div class="distrito-grid">
        """
        
        for distrito in self.distritos:
            html_content += f"""
                                <div class="distrito-item">
                                    <div>
                                        <div class="distrito-name">{distrito['nome']}</div>
                                        <div class="distrito-stats">{distrito['ubs']} UBS | {distrito['atendimentos']} atendimentos</div>
                                    </div>
                                    <div class="distrito-value">{distrito['ubs']} 🏥</div>
                                </div>
            """
        
        html_content += """
                            </div>
                            
                            <hr>
                            
                            <!-- Ciclos Sazonais -->
                            <div class="section-title" style="font-size: 16px;">❄️ CICLOS SAZONAIS COMPARATIVOS</div>
                            <div style="margin: 15px 0;">
        """
        
        html_content += ciclos_html
        
        html_content += """
                            </div>
                            
                            <hr>
                            
                            <!-- Integração de Fluxos -->
                            <div style="background: #e8f5e9; padding: 20px; border-radius: 12px; text-align: center; margin-top: 20px;">
                                <div style="font-size: 24px; margin-bottom: 10px;">🔄</div>
                                <div style="font-weight: 700; color: #002147; margin-bottom: 5px;">INTEGRAÇÃO DE FLUXOS ASSISTENCIAIS</div>
                                <div style="font-size: 12px; color: #7f8c8d;">SIVEP-Gripe | e-SUS | VIVVER</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Footer -->
                <div class="footer">
                    <p><strong>📋 CRÉDITOS INSTITUCIONAIS</strong></p>
                    <p><strong>NIS</strong> (Núcleo de Informação em Saúde) | <strong>DIVEPI</strong> (Diretoria de Vigilância Epidemiológica) | <strong>CIEVS</strong> (Centro de Informações Estratégicas em Vigilância em Saúde)</p>
                    <p>📅 Relatório Automático Gerado para Subsecretaria de Saúde — {self.data_atualizacao.strftime('%d/%m/%Y %H:%M')}</p>
                    <p style="font-size: 10px; color: #bdc3c7;">Código Ref: Surveillance_V5_2026 | Dashboard Automatizado</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def salvar_html(self, output_path="infografico_epidemiologico.html"):
        """Salva o infográfico como arquivo HTML"""
        html_content = self.gerar_html()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML salvo em: {output_path}")
        return output_path
    
    def converter_para_png(self, html_path, png_path="infografico_epidemiologico.png"):
        """
        Converte HTML para PNG usando selenium (requer chromedriver)
        
        Alternativa mais simples: usar screenshot manual do navegador
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(f"file://{os.path.abspath(html_path)}")
            
            # Aguardar carregamento completo
            driver.implicitly_wait(5)
            
            # Tirar screenshot
            driver.save_screenshot(png_path)
            driver.quit()
            
            print(f"✅ PNG salvo em: {png_path}")
            return png_path
            
        except Exception as e:
            print(f"⚠️ Não foi possível converter automaticamente para PNG: {e}")
            print("💡 Dica: Abra o arquivo HTML no navegador e tire um screenshot manualmente")
            print("   Ou instale: pip install selenium webdriver-manager")
            return None


def main():
    """
    Função principal - Exemplo de uso do script
    """
    print("=" * 60)
    print("🚀 INICIANDO GERAÇÃO DO INFOGRÁFICO EPIDEMIOLÓGICO")
    print("=" * 60)
    
    # Criar instância do infográfico
    infografico = InfograficoEpidemiologico()
    
    # Salvar como HTML
    html_file = infografico.salvar_html("infografico_semanal.html")
    
    # Tentar converter para PNG
    print("\n📸 Tentando converter para PNG...")
    png_file = infografico.converter_para_png(html_file, "infografico_semanal.png")
    
    if png_file:
        print(f"\n✨ Arquivo final pronto para compartilhamento: {png_file}")
        print("📤 Envie por WhatsApp ou E-mail para os gestores")
    else:
        print(f"\n📄 Arquivo HTML gerado: {html_file}")
        print("🔧 Para obter um PNG de alta qualidade:")
        print("   1. Abra o arquivo HTML no Chrome/Edge")
        print("   2. Pressione Ctrl+Shift+I (Inspecionar)")
        print("   3. Ctrl+Shift+P -> Capture full size screenshot")
        print("   4. O PNG será baixado automaticamente")
    
    print("\n" + "=" * 60)
    print("✅ PROCESSO CONCLUÍDO")
    print("=" * 60)


if __name__ == "__main__":
    main()

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
from datetime import datetime
import pandas as pd

# Configuração de estilo profissional
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.titleweight'] = 'bold'

def criar_infografico():
    # Dados simulados (substituir pela leitura real dos CSVs)
    data_atual = datetime.now().strftime("%d de %B de %Y")
    
    # 1. Layout da figura (tamanho A4 paisagem - 3508x2480 pixels para alta resolução)
    fig = plt.figure(figsize=(19.2, 10.8), dpi=150, facecolor='white')
    
    # Cores institucionais
    cor_azul_marinho = '#002147'
    cor_azul_claro = '#3498db'
    cor_laranja = '#FF8C00'
    cor_cinza_claro = '#f8f9fa'
    cor_cinza_borda = '#e0e6ed'
    
    # =========================================================================
    # CABEÇALHO
    # =========================================================================
    ax_header = plt.axes([0, 0.92, 1, 0.08])
    ax_header.set_facecolor(cor_azul_marinho)
    ax_header.set_xlim(0, 1)
    ax_header.set_ylim(0, 1)
    ax_header.axis('off')
    
    # Título principal
    ax_header.text(0.5, 0.7, 'INFORME SEMANAL DE VIGILÂNCIA EPIDEMIOLÓGICA', 
                   transform=ax_header.transAxes, fontsize=20, fontweight='bold',
                   color='white', ha='center', va='center')
    ax_header.text(0.5, 0.4, 'Monitoramento Integrado de Doenças Respiratórias | SRAG e Síndromes Gripais',
                   transform=ax_header.transAxes, fontsize=12, color='white', 
                   ha='center', va='center', alpha=0.9)
    
    # Badge de atualização
    rect = FancyBboxPatch((0.42, 0.1), 0.16, 0.25, boxstyle="round,pad=0.02",
                          facecolor=cor_laranja, edgecolor='none', transform=ax_header.transAxes)
    ax_header.add_patch(rect)
    ax_header.text(0.5, 0.22, f'ATUALIZADO EM: {data_atual.upper()}', 
                   transform=ax_header.transAxes, fontsize=9, fontweight='bold',
                   color='white', ha='center', va='center')
    
    # =========================================================================
    # LADO ESQUERDO: MONITORAMENTO SRAG
    # =========================================================================
    ax_left = plt.axes([0.03, 0.05, 0.46, 0.85])
    ax_left.set_facecolor('white')
    ax_left.set_xlim(0, 1)
    ax_left.set_ylim(0, 1)
    ax_left.axis('off')
    
    # Título da seção
    ax_left.text(0.02, 0.97, '🔬 MONITORAMENTO DE SRAG', fontsize=16, fontweight='bold',
                color=cor_azul_marinho, transform=ax_left.transAxes)
    ax_left.plot([0.02, 0.3], [0.955, 0.955], color=cor_laranja, linewidth=3, transform=ax_left.transAxes)
    
    # Cards de métricas
    metricas = [
        {'valor': '1.247', 'label': 'Internações por SRAG', 'pos': (0.05, 0.88)},
        {'valor': '68%', 'label': 'Ocupação de UTIs', 'pos': (0.55, 0.88)},
        {'valor': '4.850', 'label': 'Atendimentos (7 dias)', 'pos': (0.05, 0.80)},
        {'valor': '38', 'label': 'Óbitos confirmados', 'pos': (0.55, 0.80)}
    ]
    
    for m in metricas:
        # Fundo do card
        rect = FancyBboxPatch((m['pos'][0], m['pos'][1]-0.03), 0.4, 0.07, 
                              boxstyle="round,pad=0.01", facecolor=cor_cinza_claro,
                              edgecolor=cor_cinza_borda, linewidth=1, transform=ax_left.transAxes)
        ax_left.add_patch(rect)
        ax_left.text(m['pos'][0]+0.2, m['pos'][1], m['valor'], fontsize=18, fontweight='bold',
                    color=cor_azul_marinho, ha='center', va='center', transform=ax_left.transAxes)
        ax_left.text(m['pos'][0]+0.2, m['pos'][1]-0.025, m['label'], fontsize=8,
                    color='#7f8c8d', ha='center', va='center', transform=ax_left.transAxes)
    
    # Subseção: Perfil Demográfico
    ax_left.text(0.02, 0.70, '👥 PERFIL DEMOGRÁFICO', fontsize=12, fontweight='bold',
                color=cor_azul_marinho, transform=ax_left.transAxes)
    
    # Sexo
    ax_left.text(0.05, 0.65, 'Sexo:', fontweight='bold', fontsize=10, transform=ax_left.transAxes)
    ax_left.text(0.05, 0.62, '👨 Masculino: 52%', fontsize=9, transform=ax_left.transAxes)
    ax_left.text(0.05, 0.59, '👩 Feminino: 48%', fontsize=9, transform=ax_left.transAxes)
    
    # Idade
    ax_left.text(0.55, 0.65, 'Distribuição etária:', fontweight='bold', fontsize=10, transform=ax_left.transAxes)
    idades = ['0-4: 8%', '5-17: 12%', '18-39: 25%', '40-59: 30%', '60+: 25%']
    for i, idade in enumerate(idades):
        ax_left.text(0.55, 0.62 - i*0.03, idade, fontsize=8, transform=ax_left.transAxes)
    
    # Comorbidades
    ax_left.text(0.02, 0.48, '🩺 COMORBIDADES ASSOCIADAS', fontsize=12, fontweight='bold',
                color=cor_azul_marinho, transform=ax_left.transAxes)
    
    comorbidades = {'Cardiopatia': 32, 'Diabetes': 28, 'Pneumopatia': 18, 
                    'Imunossupressão': 12, 'Obesidade': 10}
    
    y_start = 0.44
    for i, (nome, valor) in enumerate(comorbidades.items()):
        ax_left.text(0.05, y_start - i*0.035, nome, fontsize=9, transform=ax_left.transAxes)
        ax_left.text(0.45, y_start - i*0.035, f'{valor}%', fontsize=9, fontweight='bold',
                    color=cor_laranja, transform=ax_left.transAxes)
        # Barra de progresso
        rect = FancyBboxPatch((0.05, y_start - i*0.035 - 0.012), valor/100*0.35, 0.008,
                              facecolor=cor_azul_claro, edgecolor='none', transform=ax_left.transAxes)
        ax_left.add_patch(rect)
    
    # Gráfico de Tendência (simulado com matplotlib)
    ax_left.text(0.02, 0.26, '📈 TENDÊNCIA POR SEMANA EPIDEMIOLÓGICA', fontsize=12, fontweight='bold',
                color=cor_azul_marinho, transform=ax_left.transAxes)
    
    # Subplot para o gráfico de tendência dentro do lado esquerdo
    ax_trend = plt.axes([0.08, 0.05, 0.38, 0.18])
    semanas = list(range(1, 17))
    casos = [12, 18, 25, 42, 78, 125, 198, 267, 310, 345, 398, 420, 445, 432, 398, 345]
    
    ax_trend.fill_between(semanas, casos, alpha=0.3, color=cor_azul_claro)
    ax_trend.plot(semanas, casos, color=cor_azul_marinho, linewidth=2, marker='o', markersize=4)
    ax_trend.axhline(y=350, color='red', linestyle='--', linewidth=1, alpha=0.7, label='Alerta')
    ax_trend.set_xlabel('Semana Epidemiológica', fontsize=8)
    ax_trend.set_ylabel('Notificações', fontsize=8)
    ax_trend.tick_params(labelsize=7)
    ax_trend.grid(True, alpha=0.3, linestyle='--')
    ax_trend.legend(fontsize=7)
    
    # =========================================================================
    # LADO DIREITO: GESTÃO TERRITORIAL
    # =========================================================================
    ax_right = plt.axes([0.51, 0.05, 0.46, 0.85])
    ax_right.set_facecolor('white')
    ax_right.set_xlim(0, 1)
    ax_right.set_ylim(0, 1)
    ax_right.axis('off')
    
    # Título da seção
    ax_right.text(0.02, 0.97, '🏥 GESTÃO TERRITORIAL E CARGA ASSISTENCIAL', fontsize=16, fontweight='bold',
                 color=cor_azul_marinho, transform=ax_right.transAxes)
    ax_right.plot([0.02, 0.4], [0.955, 0.955], color=cor_laranja, linewidth=3, transform=ax_right.transAxes)
    
    # Top 5 Unidades
    ax_right.text(0.02, 0.91, '⭐ TOP 5 UNIDADES COM MAIOR PREVALÊNCIA', fontsize=12, fontweight='bold',
                 color=cor_azul_marinho, transform=ax_right.transAxes)
    
    top5 = [
        {'nome': 'Hospital Municipal Central', 'casos': 342, 'tipo': 'Hospital'},
        {'nome': 'UPA Distrito Norte', 'casos': 287, 'tipo': 'UPA'},
        {'nome': 'UBS Vila Esperança', 'casos': 198, 'tipo': 'UBS'},
        {'nome': 'Hospital Regional Sul', 'casos': 176, 'tipo': 'Hospital'},
        {'nome': 'UBS Jardim Glória', 'casos': 145, 'tipo': 'UBS'}
    ]
    
    for i, item in enumerate(top5):
        y_pos = 0.87 - i*0.045
        # Fundo do item
        rect = FancyBboxPatch((0.02, y_pos-0.02), 0.96, 0.04, boxstyle="round,pad=0.003",
                              facecolor=cor_cinza_claro, edgecolor=cor_cinza_borda, linewidth=0.5,
                              transform=ax_right.transAxes)
        ax_right.add_patch(rect)
        ax_right.text(0.05, y_pos, f"{i+1}º", fontsize=10, fontweight='bold',
                     color=cor_laranja, transform=ax_right.transAxes)
        ax_right.text(0.12, y_pos, item['nome'], fontsize=9, fontweight='bold',
                     transform=ax_right.transAxes)
        ax_right.text(0.12, y_pos-0.01, item['tipo'], fontsize=7, color='#7f8c8d',
                     transform=ax_right.transAxes)
        ax_right.text(0.85, y_pos, f"{item['casos']}", fontsize=12, fontweight='bold',
                     color=cor_azul_marinho, ha='right', transform=ax_right.transAxes)
        ax_right.text(0.85, y_pos-0.01, "atendimentos", fontsize=6, color='#7f8c8d',
                     ha='right', transform=ax_right.transAxes)
    
    # Capilaridade por Distrito
    ax_right.text(0.02, 0.62, '📍 CAPILARIDADE POR DISTRITO', fontsize=12, fontweight='bold',
                 color=cor_azul_marinho, transform=ax_right.transAxes)
    
    distritos = [
        {'nome': 'Centro', 'ubs': 8, 'atend': 1250, 'cov': 92},
        {'nome': 'Norte', 'ubs': 6, 'atend': 980, 'cov': 85},
        {'nome': 'Sul', 'ubs': 5, 'atend': 875, 'cov': 78},
        {'nome': 'Leste', 'ubs': 4, 'atend': 645, 'cov': 70},
        {'nome': 'Oeste', 'ubs': 7, 'atend': 1120, 'cov': 88}
    ]
    
    for i, d in enumerate(distritos):
        y_pos = 0.58 - i*0.035
        ax_right.text(0.05, y_pos, d['nome'], fontweight='bold', fontsize=9, transform=ax_right.transAxes)
        ax_right.text(0.25, y_pos, f"{d['ubs']} UBS", fontsize=8, transform=ax_right.transAxes)
        ax_right.text(0.45, y_pos, f"{d['atend']} atend.", fontsize=8, transform=ax_right.transAxes)
        ax_right.text(0.70, y_pos, f"Cobertura: {d['cov']}%", fontsize=8, transform=ax_right.transAxes)
        # Mini barra
        rect = FancyBboxPatch((0.70, y_pos-0.01), d['cov']/100*0.20, 0.006,
                              facecolor=cor_azul_claro, edgecolor='none', transform=ax_right.transAxes)
        ax_right.add_patch(rect)
    
    # Gráfico de Ciclos Sazonais
    ax_right.text(0.02, 0.38, '❄️ CICLOS SAZONAIS COMPARATIVOS', fontsize=12, fontweight='bold',
                 color=cor_azul_marinho, transform=ax_right.transAxes)
    
    # Subplot para o gráfico de ciclos
    ax_ciclos = plt.axes([0.56, 0.12, 0.40, 0.23])
    meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    casos_2023 = [45, 52, 68, 95, 142, 198, 245, 267, 234, 189, 145, 98]
    casos_2024 = [38, 48, 72, 112, 168, 235, 289, 312, 278, 225, 178, 124]
    
    ax_ciclos.plot(meses, casos_2023, color='#95a5a6', linewidth=2, marker='s', markersize=3, label='2023', linestyle='--')
    ax_ciclos.plot(meses, casos_2024, color=cor_laranja, linewidth=2.5, marker='o', markersize=4, label='2024')
    ax_ciclos.set_xlabel('Mês', fontsize=8)
    ax_ciclos.set_ylabel('Casos', fontsize=8)
    ax_ciclos.tick_params(labelsize=7)
    ax_ciclos.grid(True, alpha=0.3, linestyle='--')
    ax_ciclos.legend(fontsize=8, loc='upper left')
    ax_ciclos.set_ylim(bottom=0)
    
    # Integração de Fluxos
    rect_box = FancyBboxPatch((0.56, 0.04), 0.40, 0.06, boxstyle="round,pad=0.01",
                              facecolor='#e8f5e9', edgecolor='none', transform=ax_right.transAxes)
    ax_right.add_patch(rect_box)
    ax_right.text(0.76, 0.075, '🔄 INTEGRAÇÃO DE FLUXOS ASSISTENCIAIS', fontsize=9, fontweight='bold',
                 color=cor_azul_marinho, ha='center', transform=ax_right.transAxes)
    ax_right.text(0.76, 0.055, 'SIVEP-Gripe | e-SUS | VIVVER', fontsize=7, color='#2c3e50',
                 ha='center', transform=ax_right.transAxes)
    
    # =========================================================================
    # RODAPÉ INSTITUCIONAL
    # =========================================================================
    ax_footer = plt.axes([0, 0.01, 1, 0.03])
    ax_footer.set_facecolor(cor_cinza_claro)
    ax_footer.set_xlim(0, 1)
    ax_footer.set_ylim(0, 1)
    ax_footer.axis('off')
    
    ax_footer.text(0.5, 0.5, 'NIS (Núcleo de Informação em Saúde) | DIVEPI (Diretoria de Vigilância Epidemiológica) | CIEVS',
                   fontsize=8, color='#7f8c8d', ha='center', va='center', transform=ax_footer.transAxes)
    ax_footer.text(0.5, 0.2, f'Relatório Automático Gerado para Subsecretaria de Saúde — {data_atual}',
                   fontsize=7, color='#bdc3c7', ha='center', va='center', transform=ax_footer.transAxes)
    
    # Salvar imagem em alta resolução
    plt.savefig('infografico_srag.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.savefig('infografico_srag.jpg', dpi=300, bbox_inches='tight', facecolor='white', quality=95)
    print("✅ Infográfico gerado com sucesso!")
    print("📁 Arquivos salvos: infografico_srag.png e infografico_srag.jpg")
    
    plt.show()

if __name__ == "__main__":
    criar_infografico()

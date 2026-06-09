from pathlib import Path
import json
import sys

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.visualizations import main as generate_visualizations

REPORT = ROOT / 'report' / 'relatorio_final.pdf'
FIG = ROOT / 'report' / 'figures'


def ensure_report_inputs() -> None:
    """Gera resultados e figuras quando ainda nao existem."""
    required_files = [
        ROOT / 'data' / 'processed' / 'performance_results.json',
        FIG / 'grafo_mst_rs.png',
        FIG / 'bst_risco_rs.png',
        FIG / 'tempo_execucao_vs_n.png',
        FIG / 'gap_otimalidade.png',
        FIG / 'tabela_estruturas.png',
    ]
    if not all(path.exists() for path in required_files):
        generate_visualizations()


ensure_report_inputs()
DATA = json.loads((ROOT / 'data' / 'processed' / 'performance_results.json').read_text(encoding='utf-8'))['resultados']

# Use core fonts for portability.
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleGS', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=16, leading=19, spaceAfter=8))
styles.add(ParagraphStyle(name='H1GS', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=11, leading=13, spaceBefore=6, spaceAfter=4, textColor=colors.HexColor('#1f4e79')))
styles.add(ParagraphStyle(name='BodyGS', parent=styles['BodyText'], fontName='Helvetica', fontSize=8.2, leading=10.2, spaceAfter=3))
styles.add(ParagraphStyle(name='SmallGS', parent=styles['BodyText'], fontName='Helvetica', fontSize=7.2, leading=8.4, spaceAfter=2))
styles.add(ParagraphStyle(name='CaptionGS', parent=styles['BodyText'], fontName='Helvetica-Oblique', fontSize=7.0, leading=8.2, alignment=1, spaceAfter=2))


def p(text, style='BodyGS'):
    return Paragraph(text, styles[style])


def img(name, width_cm):
    path = FIG / name
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        w_px, h_px = im.size
    width = width_cm * cm
    height = width * (h_px / w_px)
    return Image(str(path), width=width, height=height)


def page_num(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 7)
    canvas.drawRightString(A4[0] - 1.5*cm, 0.9*cm, f'Pagina {doc.page}')
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(REPORT),
    pagesize=A4,
    rightMargin=1.25*cm,
    leftMargin=1.25*cm,
    topMargin=1.1*cm,
    bottomMargin=1.1*cm,
)

story = []
story.append(p('Global Solution 2026 - Monitoramento de Riscos Ambientais', 'TitleGS'))
story.append(p('Disciplina: Estruturas de Dados e Algoritmos - FIAP - Dynamic Programming', 'SmallGS'))
story.append(p('1. Identificacao do grupo e contextualizacao', 'H1GS'))
integrantes = [
    ['RM', 'Nome'],
    ['RM 565398', 'Cesar Aaron Herrera'],
    ['RM 562100', 'Kauê Soares Madarazzo'],
    ['RM 566290', 'Nicolas Mendes dos Santos'],
    ['RM 561993', 'Rafael Seiji Aoke Arakaki'],
    ['RM 563624', 'Rafael Yuji Nakaya'],
]
t = Table(integrantes, colWidths=[2.4*cm, 11.8*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#d9eaf7')),
    ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 7.8),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t)
story.append(Spacer(1, 0.15*cm))
story.append(p('O sistema modela municipios brasileiros como vertices de um grafo ponderado, onde as arestas representam rotas de atendimento e seus pesos representam tempo estimado de deslocamento em horas. Foram escolhidos dois cenarios: enchentes no Rio Grande do Sul e seca no MATOPIBA. A escolha privilegia relevancia social, aderencia aos ODS 2, 9, 11 e 13, e viabilidade tecnica dentro do escopo da disciplina.'))
story.append(p('<b>Hipoteses:</b> os dados sao sinteticos e justificados, inspirados em cenarios reais; o indice de risco varia de 0 a 1; a BST organiza municipios por risco; a Forca Bruta valida instancias pequenas; o Prim foi escolhido como Guloso por gerar MST de cobertura minima.'))

story.append(p('2. Modelagem das estruturas de dados', 'H1GS'))
story.append(p('Cada vertice e uma tupla imutavel: <i>(id_municipio, nome, indice_risco, custo_atendimento, populacao)</i>. O grafo usa dicionario de listas de adjacencia: <i>{id: [(vizinho, peso), ...]}</i>. Esta representacao foi escolhida porque, para redes municipais esparsas, consome O(V + E) espaco, enquanto matriz de adjacencia consumiria O(V^2). A consulta dos vizinhos de um municipio e direta e o Prim percorre principalmente arestas existentes.'))
story.append(p('A BST foi implementada do zero com as classes <i>Node</i> e <i>BinarySearchTree</i>. Ela suporta inserir, buscar por intervalo de risco, percurso in-order, altura e remocao por id. A chave logica e (risco, id), evitando conflito quando dois municipios tem o mesmo risco.'))

story.append(p('3. Complexidade teorica dos algoritmos', 'H1GS'))
complexity = [
    ['Algoritmo', 'Tempo', 'Espaco', 'Interpretacao'],
    ['Forca Bruta', 'Combinatoria: C(E, V-1)', 'O(V + E)', 'Enumera subarvores por backtracking; util apenas como oraculo em N <= 12.'],
    ['Prim com heapq', 'O(E log V)', 'O(V + E)', 'Escolhe a menor aresta da fronteira; viavel para instancias maiores.'],
    ['BST', 'Medio O(log V); pior O(V)', 'O(V)', 'Consulta municipios por faixas de risco e priorizacao.'],
]
t = Table(complexity, colWidths=[2.6*cm, 3.2*cm, 2.2*cm, 9.0*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eaf2f8')),
    ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 7.0),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t)

story.append(PageBreak())
story.append(p('4. Resultados e figuras obrigatorias', 'H1GS'))
# Two images side by side graph and BST
img_table = Table([[img('grafo_mst_rs.png', 8.0), img('bst_risco_rs.png', 8.0)]], colWidths=[8.5*cm, 8.5*cm])
img_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
story.append(img_table)
story.append(p('Figura 1 - Grafo do cenario RS com arestas da MST destacadas. Fonte: dados sinteticos do projeto. A MST reduz o custo total de cobertura, mantendo todos os municipios conectados. Em uma operacao real, isso representa uma malha minima para deslocamento inicial de equipes.', 'CaptionGS'))
story.append(p('Figura 2 - BST com municipios ordenados por indice de risco. Fonte: dados sinteticos do projeto. O percurso in-order retorna os municipios em ordem crescente de risco. A busca por intervalo permite selecionar rapidamente municipios de criticidade alta, por exemplo risco >= 0.80.', 'CaptionGS'))

story.append(Spacer(1, 0.15*cm))
img_table2 = Table([[img('tempo_execucao_vs_n.png', 8.0), img('gap_otimalidade.png', 7.7)]], colWidths=[8.5*cm, 8.5*cm])
img_table2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
story.append(img_table2)
story.append(p('Figura 3 - Tempo de execucao x N. Fonte: execucao local com time.perf_counter e tracemalloc. A curva da Forca Bruta cresce rapidamente e e interrompida para N > 12 por inviabilidade combinatoria. O Prim permanece estavel para N = 20, 50 e 100.', 'CaptionGS'))
story.append(p('Figura 4 - Gap de otimalidade. Fonte: comparacao entre Forca Bruta e Prim. Como Prim e correto para MST em grafo conectado ponderado, o gap observado nas instancias pequenas foi 0%. Isso valida a escolha gulosa para o problema de cobertura minima.', 'CaptionGS'))

story.append(img('tabela_estruturas.png', 16.5))
story.append(p('Figura 5 - Tabela de estruturas de dados utilizadas. Fonte: implementacao do projeto. As estruturas foram escolhidas pela adequacao ao problema: dict para grafo, list para adjacencia, tuple para vertices/arestas, set para visitados, heapq para fronteira gulosa e BST para risco.', 'CaptionGS'))

story.append(PageBreak())
story.append(p('5. Resultados numericos e escala de decisao', 'H1GS'))
perf_rows = [['N', 'Prim ms', 'FB ms', 'Gap %', 'Status FB']]
for r in DATA:
    n = str(r['n'])
    prim = str(r['greedy_prim']['tempo_ms'])
    fb = '-' if r['brute_force']['tempo_ms'] is None else str(r['brute_force']['tempo_ms'])
    gap = '-' if r['gap_percentual'] is None else str(r['gap_percentual'])
    status = r['brute_force'].get('status', '-')
    perf_rows.append([n, prim, fb, gap, status])

t = Table(perf_rows, colWidths=[1.6*cm, 2.3*cm, 2.3*cm, 2.0*cm, 6.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eaf2f8')),
    ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 7.0),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(t)
story.append(Spacer(1, 0.15*cm))
story.append(p('A Forca Bruta funciona como baseline porque testa todas as combinacoes candidatas de V-1 arestas por backtracking. Na pratica, o numero de combinacoes cresce rapidamente com E, por isso a execucao foi limitada a N <= 12. O cruzamento pratico ocorre antes de N = 20: a partir desse ponto, o custo da enumeracao deixa de ser aceitavel para uso operacional.'))

scale = [
    ['Nivel', 'Alternativa', 'Qualidade', 'Custo', 'Decisao'],
    ['1', 'Forca Bruta N pequeno', 'Otima', 'Alto', 'Boa para validar o projeto, ruim para operacao.'],
    ['2', 'Prim N pequeno', 'Otima para MST', 'Baixo', 'Serve para demonstracao e comparacao.'],
    ['3', 'Prim N medio/grande', 'Otima para MST', 'Baixo/medio', 'Melhor alternativa pratica.'],
    ['4', 'Forca Bruta N grande', 'Otima teorica', 'Inviavel', 'Nao recomendada.'],
]
t = Table(scale, colWidths=[1.4*cm, 4.1*cm, 3.0*cm, 2.3*cm, 6.2*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eaf2f8')),
    ('GRID', (0,0), (-1,-1), 0.25, colors.grey),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 7.0),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
]))
story.append(t)

story.append(p('6. Conclusao, recomendacao pratica e ODS', 'H1GS'))
story.append(p('A recomendacao pratica e usar BST para triagem por risco e Prim para construir a rede minima de cobertura. A Forca Bruta deve permanecer como ferramenta de validacao em instancias pequenas, nao como mecanismo operacional. A solucao e aderente aos ODS 2, 9, 11 e 13 por apoiar agricultura resiliente, infraestrutura, cidades sustentaveis e acao climatica.'))

story.append(p('7. Referencias', 'H1GS'))
story.append(p('FIAP - Global Solution 2026 - Dynamic Programming. Cormen et al., Introduction to Algorithms, 4th ed. Sedgewick & Wayne, Algorithms, 4th ed. Skiena, The Algorithm Design Manual, 3rd ed. Fontes sugeridas no enunciado: NASA Earthdata, INPE PRODES/DETER, ANA HidroWeb, INMET, IBGE, ANATEL e DNIT.', 'SmallGS'))

# Build
REPORT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story, onFirstPage=page_num, onLaterPages=page_num)
print(REPORT)

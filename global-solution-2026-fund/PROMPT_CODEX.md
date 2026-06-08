Você é o Codex trabalhando em um repositório público chamado `global-solution-2026-fund` para a FIAP - Global Solution 2026 - Dynamic Programming.

Objetivo: implementar e revisar um projeto em Python que cumpra fielmente o PDF da GS: monitoramento de riscos ambientais com grafo ponderado de municípios, BST, Força Bruta, algoritmo Guloso, análise de desempenho, visualizações, testes, README e relatório.

Integrantes obrigatórios no README e relatório:
- RM 565398 - Cesar Aaron Herrera
- RM 562100 - Kauê Soares Madarazzo
- RM 566290 - Nicolas Mendes dos Santos
- RM 561993 - Rafael Seiji Aoke Arakaki
- RM 563624 - Rafael Yuji Nakaya

Escopo técnico decidido:
1. Cenário A: rede de resposta a enchentes no Rio Grande do Sul.
2. Cenário B: triagem de risco de seca no MATOPIBA.
3. Dados sintéticos justificados, inspirados em contextos reais brasileiros.
4. Vertices como tuplas: `(id_municipio, nome, indice_risco, custo_atendimento, populacao)`.
5. Grafo como `dict[int, list[tuple[int, float]]]`, ou seja, lista de adjacência ponderada.
6. BST implementada do zero com classes `Node` e `BinarySearchTree`.
7. BST deve ter: `insert`, `search_range`, `in_order`, `height`, `remove`.
8. Força Bruta deve usar recursão/backtracking, contador de chamadas recursivas e soluções avaliadas, encontrando MST ótima em N <= 12.
9. Greedy escolhido: algoritmo de Prim com `heapq`, retornando custo total, arestas da MST, operações e passos/justificativas locais.
10. Performance deve medir N = 5, 8, 10, 12, 20, 50, 100 com `time.perf_counter()` e `tracemalloc`; para Força Bruta em N > 12, registrar inviável.
11. Visualizações obrigatórias: grafo com MST destacada, BST, tempo x N, tabela de estruturas, gap de otimalidade.
12. Testes com pytest.

Arquivos obrigatórios do PDF:
- README.md
- requirements.txt
- data/raw/
- data/processed/
- src/data_structures.py
- src/brute_force.py
- src/greedy.py
- src/performance_monitor.py
- src/visualizations.py
- notebooks/analise_resultados.ipynb
- tests/test_algorithms.py
- report/relatorio_final.pdf

Tarefas:
1. Revise se todos os arquivos existem.
2. Rode `pip install -r requirements.txt` se necessário.
3. Rode `python -m src.performance_monitor`.
4. Rode `python -m src.visualizations`.
5. Rode `pytest`.
6. Corrija bugs mantendo fidelidade ao enunciado.
7. Garanta que o README explique: cenário, hipóteses, estruturas, execução, módulos, escala de decisão e integrantes com RM.
8. Garanta que o relatório final siga as seções do PDF: identificação, cenário, modelagem, complexidade, resultados/figuras, escala de decisão, conclusão com ODS e referências.
9. Não substitua a implementação da BST, Força Bruta ou Prim por bibliotecas prontas. NetworkX é permitido apenas para visualização.
10. Faça commits pequenos e claros, distribuindo depois entre os integrantes quando possível.

Critério de aceite:
- `pytest` deve passar.
- `python -m src.performance_monitor` deve gerar `data/processed/performance_results.json`.
- `python -m src.visualizations` deve gerar as 5 figuras em `report/figures/`.
- O README deve estar em português.
- O projeto deve permanecer público no GitHub.

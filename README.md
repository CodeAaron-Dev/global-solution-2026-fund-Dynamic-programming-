# Global Solution 2026 - Dynamic Programming

Projeto público para a **FIAP - Global Solution 2026 - Dynamic Programming**, desenvolvido na disciplina de Estruturas de Dados e Algoritmos.

## Tema

Monitoramento de riscos ambientais em municípios brasileiros usando **grafo ponderado**, **árvore binária de busca (BST)**, **Força Bruta**, **algoritmo Guloso de Prim**, análise de desempenho, visualizações, testes automatizados e relatório final.

## Integrantes

| RM | Nome |
|---|---|
| RM 565398 | Cesar Aaron Herrera |
| RM 562100 | Kauê Soares Madarazzo |
| RM 566290 | Nicolas Mendes dos Santos |
| RM 561993 | Rafael Seiji Aoke Arakaki |
| RM 563624 | Rafael Yuji Nakaya |

## Cenários escolhidos

### Cenário A — rede de resposta a enchentes no Rio Grande do Sul

Municípios afetados ou estratégicos são modelados como vértices de um grafo ponderado. As arestas representam rotas de deslocamento entre municípios e seus pesos representam tempo estimado de deslocamento em horas. O objetivo é construir uma rede mínima de cobertura para orientar a resposta logística inicial a enchentes.

### Cenário B — triagem de risco de seca no MATOPIBA

Municípios da região MATOPIBA são organizados por índice de risco de seca. A BST permite consultar rapidamente municípios em faixas de criticidade, priorizando locais que exigem atenção operacional e análise de campo.

## Hipóteses e dados sintéticos

- Os dados são **sintéticos e justificados**, inspirados em contextos reais brasileiros, porque a integração completa de bases DNIT, INMET, NASA, IBGE e Defesa Civil exigiria tratamento geoespacial fora do escopo principal da disciplina.
- O peso de cada aresta representa **tempo estimado de deslocamento em horas**.
- O índice de risco varia de **0.0 a 1.0**, em que valores próximos de 1 indicam maior criticidade ambiental.
- O custo de atendimento e a população compõem a tupla do município para permitir análises futuras de priorização.
- A Força Bruta é usada como oráculo acadêmico somente em instâncias pequenas; para `N > 12`, ela é registrada como inviável.

## Modelagem e estruturas de dados

### Vértices

Cada município é representado exatamente como tupla:

```python
(id_municipio, nome, indice_risco, custo_atendimento, populacao)
```

### Grafo ponderado

O grafo usa lista de adjacência ponderada:

```python
dict[int, list[tuple[int, float]]]
```

### BST

A BST foi implementada do zero com as classes `Node` e `BinarySearchTree`. Ela ordena municípios por `(indice_risco, id_municipio)` para tratar empates e implementa:

- `insert`
- `search_range`
- `in_order`
- `height`
- `remove`

### Algoritmos

| Algoritmo | Implementação | Papel no projeto |
|---|---|---|
| Força Bruta | Recursão/backtracking, contador de chamadas recursivas e soluções avaliadas | Encontra a MST ótima em `N <= 12` para validar o Prim. |
| Guloso | Algoritmo de Prim com `heapq` | Retorna custo total, arestas da MST, operações e passos/justificativas locais. |

## Análise de desempenho

O módulo `src/performance_monitor.py` mede os tamanhos `N = 5, 8, 10, 12, 20, 50, 100` com:

- `time.perf_counter()` para tempo de execução;
- `tracemalloc` para memória;
- gap de otimalidade entre Força Bruta e Prim quando a Força Bruta é viável;
- status `inviavel` para Força Bruta em `N > 12`.

## Visualizações obrigatórias

O módulo `src/visualizations.py` gera as cinco figuras em `report/figures/`:

1. `grafo_mst_rs.png` — grafo do cenário RS com MST destacada;
2. `bst_risco_rs.png` — visualização da BST por índice de risco;
3. `tempo_execucao_vs_n.png` — tempo de execução por tamanho `N`;
4. `tabela_estruturas.png` — tabela das estruturas de dados utilizadas;
5. `gap_otimalidade.png` — gap de otimalidade entre Prim e Força Bruta.

## Estrutura do projeto

```text
global-solution-2026-fund/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data_structures.py
│   ├── brute_force.py
│   ├── greedy.py
│   ├── performance_monitor.py
│   └── visualizations.py
├── notebooks/
│   └── analise_resultados.ipynb
├── tests/
│   └── test_algorithms.py
└── report/
    ├── figures/
    └── relatorio_final.pdf
```

## Módulos

| Módulo | Descrição |
|---|---|
| `src/data_structures.py` | Define vértices, grafo, BST, geradores sintéticos e utilitários de serialização. |
| `src/brute_force.py` | Implementa enumeração por backtracking para encontrar MST ótima em grafos pequenos. |
| `src/greedy.py` | Implementa Prim com `heapq`, registrando operações e justificativas locais. |
| `src/performance_monitor.py` | Mede tempo, memória, operações e gap entre Força Bruta e Guloso. |
| `src/visualizations.py` | Gera as visualizações obrigatórias. |
| `scripts/build_report.py` | Regenera o PDF final com identificação, cenário, modelagem, complexidade, resultados, escala de decisão, conclusão/ODS e referências. |
| `tests/test_algorithms.py` | Testes automatizados com `pytest`. |

## Instalação

A partir da raiz do projeto:

```bash
pip install -r requirements.txt
```

## Como executar

A partir da raiz do projeto:

```bash
python -m src.performance_monitor
python -m src.visualizations
python scripts/build_report.py
pytest
```

Os principais artefatos gerados são:

```text
data/processed/performance_results.json
report/figures/
report/relatorio_final.pdf
```

## Escala de decisão resumida

| Nível | Solução | Qualidade | Custo computacional | Uso prático |
|---|---|---:|---:|---|
| 1 | Força Bruta em `N <= 12` | Ótima | Muito alto | Validação acadêmica e comparação com Prim. |
| 2 | Prim em grafo pequeno | Ótima para MST | Baixo | Demonstração e validação do modelo. |
| 3 | Prim em grafo médio/grande | Ótima para MST | Baixo/médio | Alternativa recomendada para operação real. |
| 4 | Força Bruta em `N > 12` | Ótima apenas em teoria | Inviável | Não recomendada operacionalmente. |

## Relatório final

O relatório `report/relatorio_final.pdf` segue as seções solicitadas no PDF da GS:

1. Identificação do grupo;
2. Cenário e problema ambiental;
3. Modelagem dos dados e estruturas;
4. Complexidade dos algoritmos;
5. Resultados e figuras;
6. Escala de decisão;
7. Conclusão com ODS e referências.

## Referências

- FIAP — Global Solution 2026 — Dynamic Programming.
- Cormen, T. et al. *Introduction to Algorithms*, 4th ed.
- Sedgewick, R. & Wayne, K. *Algorithms*, 4th ed.
- Skiena, S. *The Algorithm Design Manual*, 3rd ed.
- Fontes de dados citadas no enunciado: NASA Earthdata, INPE PRODES/DETER, ANA HidroWeb, INMET, IBGE, ANATEL e DNIT.

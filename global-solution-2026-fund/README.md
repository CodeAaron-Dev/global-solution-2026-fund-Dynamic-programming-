# Global Solution 2026 - Dynamic Programming

Projeto desenvolvido para a disciplina de Estruturas de Dados e Algoritmos - FIAP.

## Tema

Monitoramento de riscos ambientais em municipios brasileiros usando grafos ponderados, arvore binaria de busca (BST), Forca Bruta e algoritmo Guloso.

## Integrantes

| RM | Nome |
|---|---|
| RM 565398 | Cesar Aaron Herrera |
| RM 562100 | Kaue Soares Madarazzo |
| RM 566290 | Nicolas Mendes dos Santos |
| RM 561993 | Rafael Seiji Aoke Arakaki |
| RM 563624 | Rafael Yuji Nakaya |

## Cenarios escolhidos

O projeto instancia dois cenarios brasileiros, conforme permitido pelo enunciado:

1. **Cenario A - Rede de resposta a enchentes no Rio Grande do Sul**  
   Municipios afetados ou estrategicos sao modelados como vertices. As rotas entre municipios sao arestas ponderadas por tempo estimado de deslocamento em horas. O objetivo e construir uma rede minima de cobertura para orientar a resposta logistica.

2. **Cenario B - Triagem de risco de seca no MATOPIBA**  
   Municipios da regiao MATOPIBA sao modelados com indice sintetico de risco derivado conceitualmente de NDVI e precipitacao. A BST permite consultar rapidamente municipios em faixas de criticidade.

## Consideracoes e hipoteses

- Os dados sao **sinteticos e justificados**, inspirados em problemas reais brasileiros, porque a integracao completa de bases DNIT, INMET, NASA, IBGE e Defesa Civil exigiria tratamento geoespacial fora do escopo principal da disciplina.
- O peso de cada aresta representa **tempo estimado de deslocamento em horas**.
- O indice de risco varia de **0.0 a 1.0**, em que valores mais proximos de 1 indicam maior criticidade ambiental.
- A solucao Gulosa escolhida foi o **algoritmo de Prim**, pois ele construi uma **Arvore Geradora Minima (MST)** adequada para cobertura de municipios com menor custo total de rota.
- A Forca Bruta enumera arvores geradoras em instancias pequenas para validar o resultado do Prim.
- Para N maior que 12, a Forca Bruta e marcada como inviavel devido ao crescimento combinatorio.
- A BST e usada para priorizacao por risco, especialmente na consulta de municipios com risco alto.

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
    ├── figuras/
    └── relatorio_final.pdf
```

## Modulos

| Modulo | Descricao |
|---|---|
| `src/data_structures.py` | Define vertices, grafo, BST, geradores sinteticos e utilitarios de serializacao. |
| `src/brute_force.py` | Implementa enumeracao completa por backtracking para encontrar MST otima em grafos pequenos. |
| `src/greedy.py` | Implementa Prim com `heapq`, registrando operacoes e justificativas locais. |
| `src/performance_monitor.py` | Mede tempo, memoria, operacoes e gap entre Forca Bruta e Guloso. |
| `src/visualizations.py` | Gera as figuras obrigatorias: grafo com MST, BST, tempo x N, tabela de estruturas e gap. |
| `tests/test_algorithms.py` | Testes automatizados com `pytest`. |

## Dependencias

```bash
pip install -r requirements.txt
```

## Como executar

A partir da raiz do projeto:

```bash
python -m src.performance_monitor
python -m src.visualizations
pytest
```

Os resultados serao salvos em:

```text
data/processed/performance_results.json
report/figures/
```

## Execucao recomendada no Codex

1. Criar o repositorio publico com o nome `global-solution-2026-fund`.
2. Subir esta estrutura inicial.
3. Rodar `python -m src.performance_monitor`.
4. Rodar `python -m src.visualizations`.
5. Rodar `pytest`.
6. Conferir o README e o relatorio final.

## Escala de decisao resumida

| Nivel | Solucao | Qualidade | Custo computacional | Uso pratico |
|---|---|---:|---:|---|
| 1 | Forca Bruta em N pequeno | Otima | Muito alto | Validacao academica |
| 2 | Prim em grafo pequeno | Otima para MST | Baixo | Validacao e demonstracao |
| 3 | Prim em grafo medio/grande | Otima para MST | Baixo/medio | Recomendado para operacao real |
| 4 | Forca Bruta em N grande | Otima teorica | Inviavel | Nao recomendado |

## Referencias

- FIAP - Global Solution 2026 - Dynamic Programming.
- Cormen, T. et al. Introduction to Algorithms, 4th ed.
- Sedgewick, R. & Wayne, K. Algorithms, 4th ed.
- Skiena, S. The Algorithm Design Manual, 3rd ed.
- Fontes de dados citadas no enunciado: NASA Earthdata, INPE PRODES/DETER, ANA HidroWeb, INMET, IBGE, ANATEL e DNIT.

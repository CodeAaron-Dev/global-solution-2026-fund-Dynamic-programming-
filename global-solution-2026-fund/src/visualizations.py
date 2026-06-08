"""Geracao das figuras obrigatorias do relatorio."""

from __future__ import annotations

from pathlib import Path
import json
from typing import Dict, Tuple, List, Optional

import matplotlib.pyplot as plt
import networkx as nx

from .data_structures import create_rs_scenario, build_bst, BinarySearchTree, Node, Grafo
from .greedy import prim_mst
from .performance_monitor import main as run_performance_monitor

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / 'report' / 'figures'
PROCESSED_DIR = ROOT / 'data' / 'processed'


def _ensure_results() -> Path:
    path = PROCESSED_DIR / 'performance_results.json'
    if not path.exists():
        run_performance_monitor()
    return path


def plot_graph_with_mst() -> Path:
    vertices, grafo = create_rs_scenario()
    mst = prim_mst(grafo)
    mst_edges = {tuple(sorted((u, v))) for u, v, _ in mst['arestas']}

    g = nx.Graph()
    for municipio_id, municipio in vertices.items():
        g.add_node(municipio_id, label=municipio[1], risco=municipio[2])
    for u, neighbors in grafo.items():
        for v, peso in neighbors:
            if u < v:
                g.add_edge(u, v, weight=peso)

    pos = nx.spring_layout(g, seed=7)
    labels = {node: vertices[node][1].split()[0] for node in g.nodes}
    normal_edges = [(u, v) for u, v in g.edges if tuple(sorted((u, v))) not in mst_edges]
    highlight_edges = [(u, v) for u, v in g.edges if tuple(sorted((u, v))) in mst_edges]

    plt.figure(figsize=(10, 7))
    nx.draw_networkx_nodes(g, pos, node_size=800)
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=8)
    nx.draw_networkx_edges(g, pos, edgelist=normal_edges, width=1, alpha=0.45)
    nx.draw_networkx_edges(g, pos, edgelist=highlight_edges, width=3)
    nx.draw_networkx_edge_labels(
        g,
        pos,
        edge_labels={(u, v): f'{g[u][v]["weight"]:.2f}h' for u, v in g.edges},
        font_size=7,
    )
    plt.title('Cenario A - Grafo de municipios do RS com MST destacada')
    plt.axis('off')
    path = FIG_DIR / 'grafo_mst_rs.png'
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def _assign_tree_positions(node: Optional[Node], depth: int, x_counter: List[int], positions: Dict[Tuple[float, int], Tuple[float, float]], labels: Dict[Tuple[float, int], str]) -> None:
    if node is None:
        return
    _assign_tree_positions(node.left, depth + 1, x_counter, positions, labels)
    key = node.key
    positions[key] = (x_counter[0], -depth)
    labels[key] = f'{node.municipio[1][:10]}\n{node.municipio[2]:.2f}'
    x_counter[0] += 1
    _assign_tree_positions(node.right, depth + 1, x_counter, positions, labels)


def _collect_tree_edges(node: Optional[Node], edges: List[Tuple[Tuple[float, int], Tuple[float, int]]]) -> None:
    if node is None:
        return
    if node.left is not None:
        edges.append((node.key, node.left.key))
        _collect_tree_edges(node.left, edges)
    if node.right is not None:
        edges.append((node.key, node.right.key))
        _collect_tree_edges(node.right, edges)


def plot_bst() -> Path:
    vertices, _ = create_rs_scenario()
    bst = build_bst(vertices.values())
    positions: Dict[Tuple[float, int], Tuple[float, float]] = {}
    labels: Dict[Tuple[float, int], str] = {}
    edges: List[Tuple[Tuple[float, int], Tuple[float, int]]] = []
    _assign_tree_positions(bst.root, 0, [0], positions, labels)
    _collect_tree_edges(bst.root, edges)

    g = nx.DiGraph()
    for key in positions:
        g.add_node(key)
    g.add_edges_from(edges)

    plt.figure(figsize=(12, 6))
    nx.draw_networkx_edges(g, positions, arrows=False)
    nx.draw_networkx_nodes(g, positions, node_size=1400)
    nx.draw_networkx_labels(g, positions, labels=labels, font_size=8)
    plt.title('BST - Municipios ordenados por indice de risco')
    plt.axis('off')
    path = FIG_DIR / 'bst_risco_rs.png'
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def plot_performance() -> Path:
    data = json.loads(_ensure_results().read_text(encoding='utf-8'))['resultados']
    ns = [row['n'] for row in data]
    greedy_times = [row['greedy_prim']['tempo_ms'] for row in data]
    brute_times = [row['brute_force']['tempo_ms'] for row in data]

    plt.figure(figsize=(9, 5))
    plt.plot(ns, greedy_times, marker='o', label='Guloso - Prim')
    plt.plot(ns, brute_times, marker='o', label='Forca Bruta')
    plt.title('Tempo de execucao x N')
    plt.xlabel('Numero de vertices (N)')
    plt.ylabel('Tempo (ms)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    path = FIG_DIR / 'tempo_execucao_vs_n.png'
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def plot_gap() -> Path:
    data = json.loads(_ensure_results().read_text(encoding='utf-8'))['resultados']
    ns = [row['n'] for row in data if row['gap_percentual'] is not None]
    gaps = [row['gap_percentual'] for row in data if row['gap_percentual'] is not None]

    plt.figure(figsize=(8, 5))
    plt.plot(ns, gaps, marker='o')
    plt.title('Gap de otimalidade: Prim vs Forca Bruta')
    plt.xlabel('Numero de vertices (N)')
    plt.ylabel('Gap percentual (%)')
    plt.grid(True, alpha=0.3)
    path = FIG_DIR / 'gap_otimalidade.png'
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def plot_structures_table() -> Path:
    rows = [
        ['list', 'Adjacencia e caminhos', 'Guarda vizinhos e MST'],
        ['tuple', 'Vertices e arestas', '(id, nome, risco, custo, populacao)'],
        ['dict', 'Mapeamento por id', 'Grafo e metadados'],
        ['set', 'Visitados', 'Evita ciclos e repeticao'],
        ['heapq', 'Fronteira gulosa', 'Menor aresta no Prim'],
        ['BST', 'Busca por risco', 'Prioriza municipios criticos'],
        ['Grafo', 'Rede de rotas', 'Municipios e deslocamentos'],
    ]
    fig, ax = plt.subplots(figsize=(11, 4.2))
    ax.axis('off')
    table = ax.table(
        cellText=rows,
        colLabels=['Estrutura', 'Uso no sistema', 'Aplicacao concreta'],
        loc='center',
        cellLoc='left',
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)
    plt.title('Tabela de estruturas de dados utilizadas')
    path = FIG_DIR / 'tabela_estruturas.png'
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()
    return path


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    _ensure_results()
    paths = [
        plot_graph_with_mst(),
        plot_bst(),
        plot_performance(),
        plot_structures_table(),
        plot_gap(),
    ]
    print('Figuras geradas:')
    for path in paths:
        print(f'- {path}')


if __name__ == '__main__':
    main()

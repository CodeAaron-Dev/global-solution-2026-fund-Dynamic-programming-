"""Forca Bruta para validar MST em instancias pequenas."""

from __future__ import annotations

from typing import Dict, List, Tuple
import math

from .data_structures import Grafo, Aresta, get_unique_edges


class DisjointSet:
    """Union-Find simples usado apenas para verificar se um conjunto forma arvore."""

    def __init__(self, vertices: List[int]) -> None:
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> bool:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False
        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b
        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1
        return True


def is_spanning_tree(vertices: List[int], candidate_edges: List[Aresta]) -> bool:
    if len(candidate_edges) != len(vertices) - 1:
        return False
    ds = DisjointSet(vertices)
    for u, v, _ in candidate_edges:
        if not ds.union(u, v):
            return False
    root = ds.find(vertices[0])
    return all(ds.find(v) == root for v in vertices)


def brute_force_mst(grafo: Grafo, max_vertices: int = 12) -> Dict[str, object]:
    """Enumera todas as combinacoes de N-1 arestas por backtracking.

    Este algoritmo e intencionalmente caro. Ele serve como oraculo para validar o
    resultado do algoritmo Guloso em instancias pequenas.
    """
    vertices = list(grafo.keys())
    n = len(vertices)
    if n > max_vertices:
        return {
            'status': 'inviavel',
            'motivo': f'Forca Bruta limitada a N <= {max_vertices}; recebido N={n}',
            'custo_total': None,
            'arestas': [],
            'chamadas_recursivas': 0,
            'solucoes_avaliadas': 0,
        }

    edges = get_unique_edges(grafo)
    target_size = n - 1
    best_cost = math.inf
    best_edges: List[Aresta] = []
    calls = 0
    evaluated = 0

    def backtrack(index: int, chosen: List[Aresta], partial_cost: float) -> None:
        nonlocal best_cost, best_edges, calls, evaluated
        calls += 1

        if len(chosen) == target_size:
            evaluated += 1
            if partial_cost < best_cost and is_spanning_tree(vertices, chosen):
                best_cost = partial_cost
                best_edges = chosen.copy()
            return

        if index >= len(edges):
            return

        remaining_needed = target_size - len(chosen)
        remaining_available = len(edges) - index
        if remaining_available < remaining_needed:
            return

        if partial_cost >= best_cost:
            return

        # Escolhe a aresta atual.
        chosen.append(edges[index])
        backtrack(index + 1, chosen, partial_cost + edges[index][2])
        chosen.pop()

        # Nao escolhe a aresta atual.
        backtrack(index + 1, chosen, partial_cost)

    backtrack(0, [], 0.0)

    if best_cost == math.inf:
        return {
            'status': 'sem_solucao',
            'custo_total': None,
            'arestas': [],
            'chamadas_recursivas': calls,
            'solucoes_avaliadas': evaluated,
        }

    return {
        'status': 'otimo_encontrado',
        'custo_total': round(best_cost, 6),
        'arestas': best_edges,
        'chamadas_recursivas': calls,
        'solucoes_avaliadas': evaluated,
    }

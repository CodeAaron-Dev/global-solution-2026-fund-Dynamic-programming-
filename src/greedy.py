"""Algoritmo Guloso escolhido: Prim para Arvore Geradora Minima."""

from __future__ import annotations

from typing import Dict, List, Tuple, Set, Optional
import heapq

from .data_structures import Grafo, Aresta


def prim_mst(grafo: Grafo, start_id: Optional[int] = None) -> Dict[str, object]:
    """Calcula a MST usando Prim com heapq.

    Retorna custo total, arestas, quantidade de operacoes e justificativas locais.
    A decisao local do Prim e escolher a menor aresta da fronteira que conecta a
    arvore atual a um vertice ainda nao visitado.
    """
    if not grafo:
        return {
            'status': 'grafo_vazio',
            'custo_total': 0.0,
            'arestas': [],
            'operacoes': 0,
            'passos': [],
            'vertices_visitados': [],
        }

    if start_id is None:
        start_id = next(iter(grafo))
    if start_id not in grafo:
        raise ValueError('start_id nao pertence ao grafo')

    visited: Set[int] = {start_id}
    heap: List[Tuple[float, int, int]] = []
    mst_edges: List[Aresta] = []
    total_cost = 0.0
    operations = 0
    steps: List[str] = []

    for neighbor, weight in grafo[start_id]:
        heapq.heappush(heap, (weight, start_id, neighbor))
        operations += 1

    while heap and len(visited) < len(grafo):
        weight, u, v = heapq.heappop(heap)
        operations += 1
        if v in visited:
            continue

        visited.add(v)
        mst_edges.append((u, v, weight))
        total_cost += weight
        steps.append(
            f'Escolhida aresta ({u}, {v}) com peso {weight:.3f}, menor custo disponivel na fronteira.'
        )

        for neighbor, next_weight in grafo[v]:
            if neighbor not in visited:
                heapq.heappush(heap, (next_weight, v, neighbor))
                operations += 1

    if len(visited) != len(grafo):
        return {
            'status': 'grafo_desconectado',
            'motivo': 'Grafo desconectado: nao existe MST cobrindo todos os vertices.',
            'custo_total': None,
            'arestas': mst_edges,
            'operacoes': operations,
            'passos': steps,
            'vertices_visitados': sorted(visited),
        }

    return {
        'status': 'mst_encontrada',
        'custo_total': round(total_cost, 6),
        'arestas': mst_edges,
        'operacoes': operations,
        'passos': steps,
        'vertices_visitados': sorted(visited),
    }

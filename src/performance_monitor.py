"""Monitoramento de desempenho dos algoritmos."""

from __future__ import annotations

import json
from pathlib import Path
import time
import tracemalloc
from typing import Callable, Dict, Any, List

from .data_structures import (
    create_rs_scenario,
    create_matopiba_scenario,
    generate_connected_graph,
    serialize_scenario,
)
from .brute_force import brute_force_mst
from .greedy import prim_mst

ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT / 'data' / 'processed'


def measure(func: Callable[[], Dict[str, Any]]) -> Dict[str, Any]:
    """Mede tempo e memoria de uma funcao."""
    tracemalloc.start()
    start = time.perf_counter()
    result = func()
    elapsed_ms = (time.perf_counter() - start) * 1000
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    result['tempo_ms'] = round(elapsed_ms, 4)
    result['memoria_mb'] = round(peak / (1024 * 1024), 6)
    return result


def run_for_size(n: int) -> Dict[str, Any]:
    _, grafo = generate_connected_graph(n, seed=2026)

    greedy_result = measure(lambda: prim_mst(grafo))

    if n <= 12:
        brute_result = measure(lambda: brute_force_mst(grafo, max_vertices=12))
        if brute_result.get('custo_total') not in (None, 0):
            gap = ((greedy_result['custo_total'] - brute_result['custo_total']) / brute_result['custo_total']) * 100
        else:
            gap = None
    else:
        brute_result = {
            'status': 'inviavel',
            'motivo': 'Crescimento combinatorio torna a enumeracao completa impraticavel para N > 12.',
            'custo_total': None,
            'arestas': [],
            'chamadas_recursivas': None,
            'solucoes_avaliadas': None,
            'tempo_ms': None,
            'memoria_mb': None,
        }
        gap = None

    return {
        'n': n,
        'brute_force': brute_result,
        'greedy_prim': greedy_result,
        'gap_percentual': None if gap is None else round(gap, 6),
    }


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    rs_vertices, rs_grafo = create_rs_scenario()
    mt_vertices, mt_grafo = create_matopiba_scenario()
    serialize_scenario(rs_vertices, rs_grafo, PROCESSED_DIR / 'cenario_rs_enchentes.json')
    serialize_scenario(mt_vertices, mt_grafo, PROCESSED_DIR / 'cenario_matopiba_seca.json')

    sizes = [5, 8, 10, 12, 20, 50, 100]
    results: List[Dict[str, Any]] = [run_for_size(n) for n in sizes]

    output = {
        'hipoteses': [
            'Pesos representam tempo estimado de deslocamento em horas.',
            'Risco varia de 0 a 1.',
            'Forca Bruta roda somente ate N=12.',
            'Prim foi escolhido por gerar MST eficiente para cobertura minima de municipios.',
        ],
        'resultados': results,
    }
    (PROCESSED_DIR / 'performance_results.json').write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

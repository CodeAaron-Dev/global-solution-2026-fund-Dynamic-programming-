from src.data_structures import build_bst, create_graph, generate_connected_graph
from src.greedy import prim_mst
from src.brute_force import brute_force_mst, is_spanning_tree


def test_bst_in_order_sorted():
    vertices, _ = generate_connected_graph(8, seed=1)
    bst = build_bst(vertices.values())
    riscos = [municipio[2] for municipio in bst.in_order()]
    assert riscos == sorted(riscos)


def test_bst_search_range():
    vertices, _ = generate_connected_graph(8, seed=2)
    bst = build_bst(vertices.values())
    result = bst.search_range(0.60, 0.90)
    assert all(0.60 <= municipio[2] <= 0.90 for municipio in result)


def test_bst_remove():
    vertices, _ = generate_connected_graph(6, seed=3)
    bst = build_bst(vertices.values())
    first_id = next(iter(vertices))
    assert bst.remove(first_id) is True
    assert len(bst) == 5
    assert all(municipio[0] != first_id for municipio in bst.in_order())


def test_prim_matches_brute_force_small_graph():
    vertices, grafo = generate_connected_graph(6, seed=4)
    greedy = prim_mst(grafo)
    brute = brute_force_mst(grafo, max_vertices=12)
    assert brute['status'] == 'otimo_encontrado'
    assert abs(greedy['custo_total'] - brute['custo_total']) < 1e-9
    assert is_spanning_tree(list(vertices.keys()), greedy['arestas'])


def test_manual_graph_mst_cost():
    vertices = {
        1: (1, 'A', 0.5, 100.0, 1000),
        2: (2, 'B', 0.6, 100.0, 1000),
        3: (3, 'C', 0.7, 100.0, 1000),
        4: (4, 'D', 0.8, 100.0, 1000),
    }
    grafo = create_graph(vertices, [(1, 2, 1.0), (2, 3, 2.0), (3, 4, 1.0), (1, 4, 10.0), (1, 3, 4.0)])
    result = prim_mst(grafo, start_id=1)
    assert result['custo_total'] == 4.0


def test_prim_disconnected_graph_returns_status_dict():
    vertices = {
        1: (1, 'A', 0.5, 100.0, 1000),
        2: (2, 'B', 0.6, 100.0, 1000),
        3: (3, 'C', 0.7, 100.0, 1000),
    }
    grafo = create_graph(vertices, [(1, 2, 1.0)])

    result = prim_mst(grafo, start_id=1)

    assert result['status'] == 'grafo_desconectado'
    assert result['custo_total'] is None
    assert result['vertices_visitados'] == [1, 2]

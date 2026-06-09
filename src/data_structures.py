"""Estruturas de dados do projeto.

Este modulo centraliza as representacoes exigidas na Global Solution:
- Vertices como tuplas: (id_municipio, nome, indice_risco, custo_atendimento, populacao)
- Grafo como dicionario de listas de adjacencia
- BST implementada do zero com Node e BinarySearchTree
- Uso explicito de list, tuple, dict, set e heapq em conjunto com os algoritmos
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import csv
import json
import random

Municipio = Tuple[int, str, float, float, int]
Aresta = Tuple[int, int, float]
Grafo = Dict[int, List[Tuple[int, float]]]


@dataclass
class Node:
    """No da arvore binaria de busca.

    A chave primaria da BST e o indice de risco. Para evitar conflito quando dois
    municipios possuem o mesmo risco, a chave real e (risco, id_municipio).
    """

    municipio: Municipio
    left: Optional["Node"] = None
    right: Optional["Node"] = None

    @property
    def key(self) -> Tuple[float, int]:
        return (self.municipio[2], self.municipio[0])


class BinarySearchTree:
    """BST de municipios ordenada por indice de risco."""

    def __init__(self) -> None:
        self.root: Optional[Node] = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def insert(self, municipio: Municipio) -> None:
        """Insere um municipio mantendo a propriedade da BST."""
        new_node = Node(municipio)
        if self.root is None:
            self.root = new_node
            self._size += 1
            return

        current = self.root
        while current is not None:
            if new_node.key < current.key:
                if current.left is None:
                    current.left = new_node
                    self._size += 1
                    return
                current = current.left
            elif new_node.key > current.key:
                if current.right is None:
                    current.right = new_node
                    self._size += 1
                    return
                current = current.right
            else:
                # Mesmo id e mesmo risco: atualiza o registro.
                current.municipio = municipio
                return

    def search_range(self, r_min: float, r_max: float) -> List[Municipio]:
        """Retorna municipios com risco no intervalo [r_min, r_max]."""
        result: List[Municipio] = []

        def _search(node: Optional[Node]) -> None:
            if node is None:
                return
            risco = node.municipio[2]
            if risco >= r_min:
                _search(node.left)
            if r_min <= risco <= r_max:
                result.append(node.municipio)
            if risco <= r_max:
                _search(node.right)

        _search(self.root)
        return result

    def in_order(self) -> List[Municipio]:
        """Retorna os municipios em ordem crescente de risco."""
        result: List[Municipio] = []

        def _traverse(node: Optional[Node]) -> None:
            if node is None:
                return
            _traverse(node.left)
            result.append(node.municipio)
            _traverse(node.right)

        _traverse(self.root)
        return result

    def height(self) -> int:
        """Calcula a altura da BST.

        Uma arvore vazia tem altura 0. Uma arvore com apenas a raiz tem altura 1.
        """
        def _height(node: Optional[Node]) -> int:
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))

        return _height(self.root)

    def remove(self, id_municipio: int) -> bool:
        """Remove um municipio pelo id.

        Retorna True quando removeu e False quando o id nao foi encontrado.
        Como a BST e ordenada por (risco, id), e nao somente por id, localizar
        um id isolado exige percorrer potencialmente os dois lados da arvore.
        Por isso, esta etapa de busca por id tem custo O(n) no pior caso.
        """
        target = self._find_by_id(self.root, id_municipio)
        if target is None:
            return False
        self.root = self._remove_by_key(self.root, target.key)
        self._size -= 1
        return True

    def _find_by_id(self, node: Optional[Node], id_municipio: int) -> Optional[Node]:
        # A propriedade da BST usa a chave (risco, id). Sem conhecer o risco,
        # nao ha como decidir apenas um ramo; portanto a busca por id e linear.
        if node is None:
            return None
        if node.municipio[0] == id_municipio:
            return node
        return self._find_by_id(node.left, id_municipio) or self._find_by_id(node.right, id_municipio)

    def _remove_by_key(self, node: Optional[Node], key: Tuple[float, int]) -> Optional[Node]:
        if node is None:
            return None
        if key < node.key:
            node.left = self._remove_by_key(node.left, key)
        elif key > node.key:
            node.right = self._remove_by_key(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._min_node(node.right)
            node.municipio = successor.municipio
            node.right = self._remove_by_key(node.right, successor.key)
        return node

    def _min_node(self, node: Node) -> Node:
        current = node
        while current.left is not None:
            current = current.left
        return current


def load_vertices_from_csv(path: Path | str) -> Dict[int, Municipio]:
    """Carrega municipios de um CSV para um dicionario id -> tupla."""
    vertices: Dict[int, Municipio] = {}
    with Path(path).open(newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            municipio: Municipio = (
                int(row['id_municipio']),
                row['nome'],
                float(row['indice_risco']),
                float(row['custo_atendimento']),
                int(row['populacao']),
            )
            vertices[municipio[0]] = municipio
    return vertices


def build_bst(vertices: Iterable[Municipio]) -> BinarySearchTree:
    bst = BinarySearchTree()
    for municipio in vertices:
        bst.insert(municipio)
    return bst


def add_undirected_edge(grafo: Grafo, u: int, v: int, peso: float) -> None:
    """Adiciona aresta nao direcionada no formato dict de listas."""
    grafo.setdefault(u, []).append((v, float(peso)))
    grafo.setdefault(v, []).append((u, float(peso)))


def create_graph(vertices: Dict[int, Municipio], edges: Iterable[Aresta]) -> Grafo:
    grafo: Grafo = {id_municipio: [] for id_municipio in vertices}
    for u, v, peso in edges:
        add_undirected_edge(grafo, u, v, peso)
    return grafo


def get_unique_edges(grafo: Grafo) -> List[Aresta]:
    """Extrai arestas unicas de um grafo nao direcionado."""
    seen: set[Tuple[int, int]] = set()
    edges: List[Aresta] = []
    for u, neighbors in grafo.items():
        for v, peso in neighbors:
            a, b = sorted((u, v))
            if (a, b) not in seen:
                seen.add((a, b))
                edges.append((a, b, peso))
    return edges


def create_rs_scenario() -> Tuple[Dict[int, Municipio], Grafo]:
    """Cenario A - enchentes no RS, com dados sinteticos justificados."""
    vertices: Dict[int, Municipio] = {
        4314902: (4314902, 'Porto Alegre', 0.92, 1850.0, 1400000),
        4304606: (4304606, 'Canoas', 0.88, 1200.0, 348000),
        4318705: (4318705, 'Sao Leopoldo', 0.81, 980.0, 238000),
        4309209: (4309209, 'Gravatai', 0.74, 1100.0, 285000),
        4323002: (4323002, 'Viamão', 0.69, 900.0, 256000),
        4313409: (4313409, 'Novo Hamburgo', 0.77, 1050.0, 247000),
        4303103: (4303103, 'Cachoeirinha', 0.71, 860.0, 132000),
        4313375: (4313375, 'Nova Santa Rita', 0.84, 720.0, 30000),
        4300604: (4300604, 'Alvorada', 0.70, 760.0, 212000),
        4312401: (4312401, 'Montenegro', 0.73, 980.0, 65000),
        4319505: (4319505, 'Sapucaia do Sul', 0.82, 870.0, 140000),
        4306767: (4306767, 'Eldorado do Sul', 0.91, 700.0, 42000),
    }
    edges: List[Aresta] = [
        (4314902, 4304606, 0.45),
        (4314902, 4309209, 0.70),
        (4314902, 4323002, 0.85),
        (4314902, 4306767, 0.55),
        (4304606, 4313375, 0.40),
        (4304606, 4319505, 0.35),
        (4319505, 4318705, 0.30),
        (4318705, 4313409, 0.45),
        (4313375, 4312401, 0.95),
        (4303103, 4304606, 0.30),
        (4303103, 4309209, 0.40),
        (4300604, 4303103, 0.25),
        (4300604, 4323002, 0.60),
        (4312401, 4313409, 0.75),
        (4306767, 4313375, 0.65),
        (4309209, 4323002, 0.55),
    ]
    return vertices, create_graph(vertices, edges)


def create_matopiba_scenario() -> Tuple[Dict[int, Municipio], Grafo]:
    """Cenario B - seca no MATOPIBA, com dados sinteticos justificados."""
    vertices: Dict[int, Municipio] = {
        2111300: (2111300, 'Sao Luis', 0.61, 1500.0, 1100000),
        1721000: (1721000, 'Palmas', 0.76, 1300.0, 306000),
        2207702: (2207702, 'Parnaiba', 0.69, 900.0, 153000),
        2903201: (2903201, 'Barreiras', 0.83, 1250.0, 160000),
        2919553: (2919553, 'Luis Eduardo Magalhaes', 0.87, 1180.0, 93000),
        1702109: (1702109, 'Araguaina', 0.78, 1120.0, 183000),
        2105302: (2105302, 'Imperatriz', 0.72, 1000.0, 259000),
        2208007: (2208007, 'Picos', 0.80, 950.0, 78000),
        2903904: (2903904, 'Bom Jesus da Lapa', 0.75, 890.0, 70000),
        1718204: (1718204, 'Porto Nacional', 0.82, 820.0, 53000),
    }
    edges: List[Aresta] = [
        (2111300, 2105302, 5.20),
        (2105302, 1702109, 4.30),
        (1702109, 1721000, 5.10),
        (1721000, 1718204, 1.10),
        (1718204, 2903201, 6.90),
        (2903201, 2919553, 1.35),
        (2903201, 2903904, 3.80),
        (2207702, 2208007, 3.40),
        (2208007, 2903904, 6.20),
        (2105302, 2207702, 6.10),
        (1721000, 2903201, 7.40),
        (1702109, 2208007, 5.80),
    ]
    return vertices, create_graph(vertices, edges)


def generate_connected_graph(n: int, seed: int = 42) -> Tuple[Dict[int, Municipio], Grafo]:
    """Gera grafo conectado sintetico para testes de desempenho.

    O grafo tem uma cadeia base para garantir conectividade e algumas arestas extras
    para criar alternativas de escolha para Forca Bruta e Prim.
    """
    if n < 2:
        raise ValueError('n deve ser >= 2')
    rng = random.Random(seed + n)
    vertices: Dict[int, Municipio] = {}
    for i in range(n):
        municipio_id = 1000000 + i
        risco = round(0.25 + rng.random() * 0.70, 4)
        custo = round(500 + rng.random() * 2500, 2)
        populacao = rng.randint(8000, 1500000)
        vertices[municipio_id] = (municipio_id, f'Municipio {i + 1}', risco, custo, populacao)

    edge_set: set[Tuple[int, int]] = set()
    edges: List[Aresta] = []
    ids = list(vertices.keys())

    def add(u: int, v: int, peso: float) -> None:
        a, b = sorted((u, v))
        if a != b and (a, b) not in edge_set:
            edge_set.add((a, b))
            edges.append((a, b, round(peso, 3)))

    for i in range(n - 1):
        add(ids[i], ids[i + 1], rng.uniform(0.2, 5.0))

    # Poucas arestas extras para manter a Forca Bruta viavel em N pequeno.
    extra_edges = max(1, n // 3)
    attempts = 0
    while len(edges) < (n - 1 + extra_edges) and attempts < n * n:
        u, v = rng.sample(ids, 2)
        add(u, v, rng.uniform(0.2, 6.5))
        attempts += 1

    return vertices, create_graph(vertices, edges)


def serialize_scenario(vertices: Dict[int, Municipio], grafo: Grafo, output_path: Path | str) -> None:
    data = {
        'vertices': [list(v) for v in vertices.values()],
        'grafo': {str(k): [[v, peso] for v, peso in adj] for k, adj in grafo.items()},
    }
    Path(output_path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def load_scenario(path: Path | str) -> Tuple[Dict[int, Municipio], Grafo]:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    vertices: Dict[int, Municipio] = {
        int(row[0]): (int(row[0]), row[1], float(row[2]), float(row[3]), int(row[4]))
        for row in data['vertices']
    }
    grafo: Grafo = {
        int(k): [(int(v), float(peso)) for v, peso in adj]
        for k, adj in data['grafo'].items()
    }
    return vertices, grafo

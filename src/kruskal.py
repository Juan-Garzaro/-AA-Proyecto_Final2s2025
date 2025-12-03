"""Implementación
del algoritmo de Kruskal para la construcción del Árbol de Expansión Mínima
(MST).

Complejidad: O(E log E) debido al ordenamiento de las aristas,
donde E es el número de aristas. 
La operación Union-Find es casi O(1) en promedio (amortizada O(α(V))), 
lo que garantiza un rendimiento mucho mejor que los enfoques O(n³) para grafos densos.
"""
from typing import List, Tuple
from .utils import draw_graph_and_save_png, read_graph_csv

class UnionFind:
    """Estructura de datos Union-Find (Disjoint Set) con optimización por rango y compresión de caminos."""
    def __init__(self, nodes: List[str]):
        """
        Inicializa la estructura Union-Find.

        Cada nodo se inicializa como el representante de su propio conjunto.
        :param nodes: Lista de identificadores de nodos (cuerdas) en el grafo.
        """
        self.parent = {node: node for node in nodes}
        self.rank = {node: 0 for node in nodes}

    # Complejidad: Amortizada O(α(V)), donde α es la función inversa de Ackermann, que crece extremadamente lento (casi O(1)).
    def find(self, x: str) -> str:
        """
        Encuentra el representante (raíz) del conjunto al que pertenece x y realiza la compresión de caminos.

        :param x: Elemento cuyo representante se busca.
        :return: El representante (raíz) del conjunto.
        """
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Compresión de caminos
        return self.parent[x]

    # Complejidad: Amortizada O(α(V)), donde α es la función inversa de Ackermann (casi O(1)).
    def union(self, a: str, b: str) -> bool:
        """
        Une los conjuntos que contienen a y b utilizando la unión por rango.

        :param a: Elemento del primer conjunto.
        :param b: Elemento del segundo conjunto.
        :return: True si los conjuntos se unieron (la arista es parte del MST), 
                 False si ya estaban en el mismo conjunto (la arista forma un ciclo).
        """
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a != root_b:
            # Unión por rango
            if self.rank[root_a] < self.rank[root_b]:
                self.parent[root_a] = root_b
            elif self.rank[root_a] > self.rank[root_b]:
                self.parent[root_b] = root_a
            else:
                self.parent[root_b] = root_a
                self.rank[root_a] += 1
            return True
        return False

def kruskal(edges: List[Tuple[str, str, float]]) -> List[Tuple[str, str, float]]:
    """
    Calcula el Árbol de Expansión Mínima (MST) utilizando el algoritmo de Kruskal.

    :param edges: Lista de tuplas (u, v, peso) que representan las aristas del grafo.
    :return: Lista de aristas (u, v, peso) que forman el MST.
    """
    if not edges:
        return []

    # 1. Obtener lista de nodos únicos
    nodes = set()
    for u, v, _ in edges:
        nodes.add(u); nodes.add(v)
    
    # 2. Inicializar Union-Find
    uf = UnionFind(list(nodes))
    
    # 3. Ordenar las aristas por peso (ascendente)
    # Complejidad: O(E log E), la fase dominante del algoritmo.
    sorted_edges = sorted(edges, key=lambda item: item[2])

    mst = []
    # Complejidad del bucle: E iteraciones. Cada operación find/union es casi O(1).
    for u, v, w in sorted_edges:
        # 4. Intentar unir los conjuntos de u y v
        if uf.union(u, v):
            mst.append((u, v, w))
            if len(mst) == len(nodes) - 1:
                break # MST completado (V - 1 aristas)

    return mst

def run_kruskal(csv_path: str):
    """
    Ejecuta el algoritmo de Kruskal, muestra los resultados del MST y genera la imagen PNG obligatoria.

    :param csv_path: Ruta al archivo CSV que contiene las aristas del grafo.
    :return: Lista de aristas (u, v, peso) que forman el MST.
    """
    edges = read_graph_csv(csv_path)
    if not edges:
        print("❌ No se pudo leer el grafo para Kruskal.")
        return

    # 1. Procesar
    mst_edges = kruskal(edges)
    total_weight = sum(w for u, v, w in mst_edges)

    # 2. Mostrar salidas en consola
    print("\n--- Resultado Algoritmo de Kruskal ---")
    print(f"Peso Total del MST: {total_weight}")
    print("Aristas del MST (u, v, peso):")
    for u, v, w in mst_edges:
        print(f"  ({u} - {v}, peso: {w})")

    # 3. Generar imagen PNG obligatoria
    highlighted = [(u, v) for u, v, _ in mst_edges]
    draw_graph_and_save_png(
        edges=edges, 
        filename="kruskal_mst.png", 
        highlight_edges=highlighted,
        title=f"MST Kruskal (Peso Total: {total_weight})"
    )
    return mst_edges

if __name__ == '__main__':
    # Ejemplo de ejecución interna
    run_kruskal("../../data/grafos/ejemplo_grafo.csv")
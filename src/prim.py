"""Implementación del
algoritmo de Prim para la construcción del Árbol de Expansión Mínima (MST).

Complejidad: O(E log V) usando una cola de prioridad (heap), 
donde E es el número de aristas y V es el número de nodos.
Algoritmos de esta clase demuestran una escalabilidad superior a los métodos de triple anidamiento O(n³) para problemas de optimización.
"""
from typing import List, Tuple
import heapq
from collections import defaultdict
from .utils import draw_graph_and_save_png, read_graph_csv

def prim(edges: List[Tuple[str, str, float]], start_node: str = None) -> List[Tuple[str, str, float]]:
    """
    Calcula el Árbol de Expansión Mínima (MST) de un grafo no dirigido y ponderado utilizando Prim.

    :param edges: Lista de tuplas (u, v, peso) que representan las aristas del grafo.
    :param start_node: Nodo inicial opcional para comenzar el algoritmo. Si no se proporciona o no existe, se elige un nodo arbitrario.
    :return: Lista de aristas (u, v, peso) que forman el MST.
    """
    if not edges:
        return []

    # Construcción de la lista de adyacencia y conjunto de nodos
    adj = defaultdict(list)
    nodes = set()
    for u, v, w in edges:
        # Se guarda (peso, destino, origen) para la cola de prioridad
        adj[u].append((w, v, u))
        adj[v].append((w, u, v))
        nodes.add(u); nodes.add(v)

    # Determinar el nodo de inicio
    if start_node is None or start_node not in nodes:
        # Elije un nodo al azar si no se especifica uno válido
        start = next(iter(nodes))
    else:
        start = start_node

    # 1. Inicialización
    visited = set([start])
    # Cola de prioridad: almacena las aristas frontera (peso, u, v)
    heap = []
    
    # Inicializar la cola de prioridad con todas las aristas del nodo de inicio
    for w, v, u in adj[start]:
        heapq.heappush(heap, (w, u, v)) # (peso, u, v)

    mst = []
    # 2. Bucle principal
    # El bucle se detiene cuando el MST tiene V-1 aristas o la cola está vacía
    while heap and len(visited) < len(nodes):
        # Extrae la arista de menor peso que conecta un nodo visitado con uno no visitado
        weight, u, v = heapq.heappop(heap)

        if v not in visited:
            # 3. Incorporar el nuevo nodo al MST
            visited.add(v)
            # Asegura la arista se añade en el formato (u, v, weight)
            mst.append((u, v, weight))
            
            # 4. Actualizar la frontera: Añadir las nuevas aristas adyacentes al nodo 'v'
            for w_new, v_new, _ in adj[v]:
                if v_new not in visited:
                    heapq.heappush(heap, (w_new, v, v_new))

    return mst

def run_prim(csv_path: str, start_node: str = None):
    """
    Ejecuta el algoritmo de Prim, muestra los resultados del MST y genera la imagen PNG obligatoria.

    :param csv_path: Ruta al archivo CSV que contiene las aristas del grafo.
    :param start_node: Nodo inicial opcional para comenzar el algoritmo.
    :return: Lista de aristas (u, v, peso) que forman el MST.
    """
    edges = read_graph_csv(csv_path)
    if not edges:
        print("❌ No se pudo leer el grafo para Prim.")
        return

    # 1. Procesar
    mst_edges = prim(edges, start_node)
    total_weight = sum(w for u, v, w in mst_edges)

    # 2. Mostrar salidas en consola
    print("\n--- Resultado Algoritmo de Prim ---")
    print(f"Peso Total del MST: {total_weight}")
    print("Aristas del MST (u, v, peso):")
    for u, v, w in mst_edges:
        print(f"  ({u} - {v}, peso: {w})")

    # 3. Generar imagen PNG obligatoria
    highlighted = [(u, v) for u, v, _ in mst_edges]
    draw_graph_and_save_png(
        edges=edges, 
        filename="prim_mst.png", 
        highlight_edges=highlighted,
        title=f"MST Prim (Peso Total: {total_weight})"
    )
    return mst_edges

if __name__ == '__main__':
    # Ejemplo de ejecución interna
    run_prim("../../data/grafos/ejemplo_grafo.csv")
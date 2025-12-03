"""Implementación del
algoritmo de Dijkstra para encontrar las rutas más cortas desde un origen.

Complejidad: O(E log V) con una cola de prioridad (heap), 
donde E es el número de aristas y V es el número de nodos. 
Esta eficiencia contrasta fuertemente con algoritmos de fuerza bruta de O(n³) o superior.
"""
from typing import List, Tuple, Dict, Optional
import heapq
from collections import defaultdict
from .utils import draw_graph_and_save_png, read_graph_csv

def dijkstra(edges: List[Tuple[str, str, float]], source: str) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    """
    Calcula la distancia mínima y el predecesor para cada nodo desde un nodo fuente.

    :param edges: Lista de tuplas (u, v, peso) que representan las aristas del grafo.
    :param source: Nodo origen desde donde se calcula la ruta más corta.
    :return: Una tupla que contiene: 
             - distancias (Dict[str, float]): Distancia mínima del origen a cada nodo.
             - predecesores (Dict[str, Optional[str]]): Predecesor de cada nodo en el camino más corto.
    """
    # Inicialización
    adj = defaultdict(list)
    nodes = set()
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w)) # Grafo no dirigido (asumido)
        nodes.add(u); nodes.add(v)

    if source not in nodes:
        print(f"❌ Error: El nodo origen '{source}' no existe en el grafo.")
        return {}, {}

    dist = {n: float('inf') for n in nodes}
    prev = {n: None for n in nodes}
    dist[source] = 0
    
    # Cola de prioridad: (distancia_actual, nodo)
    pq = [(0, source)]

    # Algoritmo principal
    while pq:
        d, u = heapq.heappop(pq)

        # Si ya encontramos una ruta más corta, ignorar
        if d > dist[u]:
            continue

        # Recorrer vecinos
        for v, weight in adj[u]:
            new_distance = d + weight
            
            # Relajación
            if new_distance < dist[v]:
                dist[v] = new_distance
                prev[v] = u
                heapq.heappush(pq, (new_distance, v))

    return dist, prev

def reconstruct_path(prev: Dict[str, Optional[str]], target: str) -> List[str]:
    """
    Reconstruye el camino desde el origen hasta el nodo objetivo usando el mapa de predecesores.

    :param prev: Diccionario de predecesores (nodo actual -> nodo anterior).
    :param target: Nodo objetivo al que se quiere llegar desde el origen.
    :return: Lista de nodos que forman la ruta más corta (origen al destino).
    """
    path = []
    at = target
    while at is not None:
        path.append(at)
        at = prev.get(at)
    path.reverse()
    return path if path[0] == target or len(path) > 1 else []

def run_dijkstra(csv_path: str, source: str):
    """
    Ejecuta el algoritmo de Dijkstra, muestra los resultados en consola y genera la imagen PNG obligatoria.

    :param csv_path: Ruta al archivo CSV que contiene las aristas del grafo.
    :param source: Nodo origen para el cálculo de rutas.
    :return: None
    """
    edges = read_graph_csv(csv_path)
    if not edges:
        print("❌ No se pudo leer el grafo para Dijkstra.")
        return

    # Procesar
    dist, prev = dijkstra(edges, source)
    
    if not dist:
        return

    # Mostrar salidas en consola
    print(f"\n--- Resultado Algoritmo de Dijkstra (Origen: {source}) ---")
    highlighted_edges = []
    
    for target, d in sorted(dist.items()):
        if d == float('inf'):
            print(f"Ruta a {target}: NO ALCANZABLE")
        else:
            path = reconstruct_path(prev, target)
            print(f"Ruta a {target} (Distancia: {d}): {' -> '.join(path)}")
            
            # Colectar aristas del camino más corto
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                highlighted_edges.append((u, v))

    # Generar imagen PNG obligatoria
    highlighted_edges = list(set([tuple(sorted(e)) for e in highlighted_edges]))
    
    draw_graph_and_save_png(
        edges=edges, 
        filename="dijkstra_paths.png", 
        highlight_edges=highlighted_edges,
        title=f"Rutas más Cortas (Dijkstra) desde {source}"
    )

if __name__ == '__main__':
    # Ejemplo de ejecución interna
    run_dijkstra("../../data/grafos/ejemplo_grafo.csv", "A")
"""Módulo de utilidades para lectura de archivos y dibujo de grafos.

Incluye funciones para leer archivos de entrada (CSV y TXT) y para generar visualizaciones 
de grafos y árboles (MST, rutas, Árbol de Huffman) utilizando NetworkX y Matplotlib.

Complejidad: Las funciones en este módulo son principalmente de utilidad y visualización. 
Su complejidad es dominada por operaciones de I/O (lectura de archivos) y por la rutina de dibujo de grafos 
(que es típicamente O(V+E) o superior dependiendo del layout, pero no está ligada directamente al análisis asintótico de los algoritmos principales).
"""
from typing import List, Tuple, Dict, Any
import csv
import networkx as nx
import matplotlib.pyplot as plt
import os

# ----------------------------------------------------
# DEFINICIÓN DE LA RUTA DE SALIDA
# ----------------------------------------------------
OUTPUT_DIR = os.path.join("docs", "evidencias")
# ----------------------------------------------------

# Intenta importar pygraphviz para layout (dependencia externa para mejor visualización)
try:
    import pygraphviz
    HAS_GRAPHVIZ = True
except ImportError:
    HAS_GRAPHVIZ = False
    print("ADVERTENCIA: pygraphviz no encontrado. Usando layout 'spring' como fallback.")

def read_graph_csv(path: str) -> List[Tuple[str, str, float]]:
    """
    Lee un archivo CSV con formato origen, destino, peso y retorna una lista de aristas.

    :param path: Ruta al archivo CSV.
    :return: Lista de tuplas (u, v, peso) que representan las aristas del grafo.
    """
    edges = []
    try:
        # Complejidad: O(L), donde L es el número de líneas (aristas) en el archivo.
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Asume que la primera fila es un encabezado y la salta.
            next(reader, None) 
            for row in reader:
                if len(row) >= 3:
                    try:
                        u, v, w = row[0].strip(), row[1].strip(), float(row[2])
                        edges.append((u, v, w))
                    except ValueError:
                        print(f"❌ Error al convertir peso '{row[2]}' a número en fila: {row}")
    except FileNotFoundError:
        print(f"❌ Archivo CSV no encontrado en: {path}")
    return edges

def read_text_file(path: str) -> str:
    """
    Lee un archivo de texto para el algoritmo de Huffman.

    :param path: Ruta al archivo TXT.
    :return: Contenido completo del archivo como un string.
    """
    try:
        # Complejidad: O(C), donde C es el número total de caracteres en el archivo.
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Archivo de texto no encontrado en: {path}")
        return ""

def draw_graph_and_save_png(
    edges: List[Tuple[str, str, float]],
    filename: str,
    highlight_edges: List[Tuple[str, str]] = None,
    title: str = ""
):
    """
    Dibuja un grafo a PNG, resaltando aristas específicas (MST o ruta más corta).

    Utiliza NetworkX para la manipulación y Matplotlib para la salida. 
    Usa Graphviz para el layout si está disponible para una mejor estética.

    :param edges: Lista de aristas (u, v, peso) del grafo completo.
    :param filename: Nombre del archivo PNG de salida (ej. prim_mst.png).
    :param highlight_edges: Lista de aristas (u, v) a resaltar (e.g., MST o ruta).
    :param title: Título para el gráfico.
    :return: None
    """
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    
    # 1. Determinar el layout (Graphviz o fallback)
    # La complejidad de la generación del layout varía; Graphviz es más lento (polinomial en V+E) 
    # pero produce mejores resultados que 'spring_layout' (típicamente O(V^3) o O(V+E) dependiendo de la implementación).
    pos = None
    if HAS_GRAPHVIZ:
        try:
            pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        except Exception as e:
            print(f"❌ Graphviz layout falló ({e}). Usando layout 'spring'.")
            pos = nx.spring_layout(G)
    else:
        pos = nx.spring_layout(G)

    plt.figure(figsize=(10, 7))

    # 2. Dibujar nodos y aristas
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')

    all_edges = [(u, v) for u, v, _ in edges]
    highlight_set = set(tuple(sorted(e)) for e in (highlight_edges or []))
    
    default_edges = []
    highlight_list = []

    for u, v in all_edges:
        edge = tuple(sorted((u, v)))
        if edge in highlight_set:
            highlight_list.append((u, v))
        else:
            default_edges.append((u, v))

    # Dibujar aristas no resaltadas (gris claro)
    nx.draw_networkx_edges(G, pos, edgelist=default_edges, edge_color='gray', width=1.0)
    
    # Dibujar aristas resaltadas (rojo/azul y más gruesas)
    nx.draw_networkx_edges(G, pos, edgelist=highlight_list, edge_color='red', width=2.5)

    # 3. Etiquetas de peso
    edge_labels = nx.get_edge_attributes(G, 'weight')
    labels_to_show = edge_labels
    if highlight_edges:
        # Mostrar peso solo para las aristas que forman parte del resultado
        labels_to_show = {
            (u, v): w 
            for (u, v), w in edge_labels.items() 
            if tuple(sorted((u,v))) in highlight_set
        }

    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels_to_show, font_color='darkgreen', font_size=10)

    # 4. Guardar archivo
    plt.title(title)
    plt.tight_layout()
    
    # LÓGICA DE GUARDADO
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    full_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(full_path, dpi=300)
    plt.close()
    print(f"✅ Imagen generada: {full_path}")

def draw_huffman_tree_and_save_png(root: Any, filename: str):
    """
    Dibuja el árbol de Huffman (dirigido) a PNG.

    :param root: Nodo raíz del árbol de Huffman.
    :param filename: Nombre del archivo PNG de salida (huffman_tree.png).
    :return: None
    """
    if root is None:
        return
        
    G = nx.DiGraph()
    pos = {}
    
    def add_nodes(node, parent=None, edge_label=None, level=0, x_coord=0):
        """Función recursiva para construir el grafo. Complejidad: O(n), n=símbolos únicos."""
        node_id = id(node)
        label = f"{node.symbol if node.symbol else 'N'}\n({node.freq})"
        G.add_node(node_id, label=label, freq=node.freq, is_leaf=node.is_leaf())
        
        if parent is not None:
            G.add_edge(parent, node_id, label=edge_label)
        
        # Simple cálculo de posición jerárquica para el layout
        pos[node_id] = (x_coord, -level)

        if node.left:
            add_nodes(node.left, node_id, '0', level + 1, x_coord - 2**(4-level))
        if node.right:
            add_nodes(node.right, node_id, '1', level + 1, x_coord + 2**(4-level))
            
    # Asume que el nodo raíz es 'root' del módulo huffman.py
    add_nodes(root, x_coord=0, level=0) 

    plt.figure(figsize=(12, 8))
    
    # Ajustar el layout: Graphviz es preferido para árboles
    if HAS_GRAPHVIZ:
        try:
            pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
        except Exception:
            pass # Si falla, usa el layout simple creado

    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')
    leaf_nodes = [n for n, data in G.nodes(data=True) if data.get('is_leaf', False)]
    internal_nodes = [n for n in G.nodes() if n not in leaf_nodes]

    nx.draw_networkx_nodes(G, pos, nodelist=internal_nodes, node_color='lightgreen', node_size=800, alpha=0.9)
    nx.draw_networkx_nodes(G, pos, nodelist=leaf_nodes, node_color='skyblue', node_size=800, alpha=0.9)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=10)
    nx.draw_networkx_edges(G, pos, arrows=True, width=1.5)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=12)

    plt.title("Árbol de Huffman")
    plt.tight_layout()
    
    # LÓGICA DE GUARDADO
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    full_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(full_path, dpi=300)
    plt.close()
    print(f"✅ Imagen generada: {full_path}")

def draw_frequency_png(freqs: Dict[str, int], filename: str):
    """
    Genera una gráfica de barras con las frecuencias de los símbolos.

    :param freqs: Diccionario de frecuencias (símbolo: frecuencia).
    :param filename: Nombre del archivo PNG de salida (huffman_freq.png).
    :return: None
    """
    if not freqs:
        print("❌ No hay datos para generar el gráfico de frecuencias.")
        return

    # Preparar datos (ordenar por frecuencia)
    # Complejidad: O(n log n), donde n es el número de símbolos únicos, debido a la ordenación.
    sorted_items = sorted(freqs.items(), key=lambda item: item[1], reverse=True)
    symbols = [item[0] if item[0] != '\n' else 'NL' for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    plt.figure(figsize=(12, 6))
    plt.bar(symbols, counts, color='teal')
    plt.xlabel('Símbolo')
    plt.ylabel('Frecuencia')
    plt.title('Gráfica de Frecuencias de Símbolos (Huffman)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # LÓGICA DE GUARDADO
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    full_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(full_path, dpi=300)
    plt.close()
    print(f"✅ Imagen generada: {full_path}")
    
    #PR TEST
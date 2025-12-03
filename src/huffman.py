"""Implementación del
algoritmo de Huffman para codificación óptima.

Complejidad: O(n log n) donde n es el número de símbolos únicos,
debido a la construcción del árbol mediante la cola de prioridad.
Esta eficiencia es similar a la ordenación por comparación y es ideal para conjuntos de datos grandes, superando a las soluciones polinomiales de alto grado.
"""
from typing import Dict, Tuple, Optional, List, Any
import heapq
from .utils import draw_huffman_tree_and_save_png, draw_frequency_png, read_text_file

class Node:
    """Nodo del Árbol de Huffman."""
    def __init__(self, freq: int, symbol: Optional[str] = None, left: Any = None, right: Any = None):
        """
        Inicializa un nodo del Árbol de Huffman.

        :param freq: Frecuencia (peso) del símbolo o subárbol.
        :param symbol: Símbolo (carácter) si es un nodo hoja; None si es un nodo interno.
        :param left: Hijo izquierdo (corresponde al código '0').
        :param right: Hijo derecho (corresponde al código '1').
        """
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def is_leaf(self) -> bool:
        """
        Verifica si el nodo es una hoja (contiene un símbolo).

        :return: True si es un nodo hoja, False si es un nodo interno.
        """
        return self.symbol is not None

    def __lt__(self, other):
        """
        Define el orden de prioridad para el heap (comparación por frecuencia).

        :param other: El otro objeto Node con el que comparar.
        :return: True si la frecuencia de este nodo es menor que la del otro.
        """
        return self.freq < other.freq

def huffman_frequencies(text: str) -> Dict[str, int]:
    """
    Calcula las frecuencias de aparición de cada carácter en un texto.

    :param text: El string de entrada a analizar.
    :return: Diccionario donde la clave es el símbolo (carácter) y el valor es su frecuencia.
    """
    freqs = {}
    for ch in text:
        freqs[ch] = freqs.get(ch, 0) + 1
    return freqs

def build_huffman_tree(freqs: Dict[str, int]) -> Optional[Node]:
    """
    Construye el árbol de Huffman óptimo a partir de las frecuencias de los símbolos.

    :param freqs: Diccionario de frecuencias de los símbolos.
    :return: El nodo raíz del Árbol de Huffman o None si la lista de frecuencias está vacía.
    """
    if not freqs:
        return None
        
    # Crear una lista de nodos hoja e insertarlos en una cola de prioridad
    # Complejidad: O(n) para crear los nodos + O(n) para heapify. Total: O(n).
    heap = [Node(freq, symbol=s) for s, freq in freqs.items()]
    heapq.heapify(heap)

    # Combinar los dos nodos de menor frecuencia hasta que solo quede la raíz
    # Complejidad: O(n log n). El bucle corre n-1 veces. Cada heappop/heappush es O(log n).
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        
        # Crear un nuevo nodo interno
        combined_freq = left.freq + right.freq
        new_node = Node(combined_freq, left=left, right=right)
        
        heapq.heappush(heap, new_node)

    return heap[0] # Retorna la raíz

def generate_codes(root: Node) -> Dict[str, str]:
    """
    Genera la tabla de códigos de Huffman (símbolo a código binario) recorriendo el árbol.

    :param root: El nodo raíz del Árbol de Huffman.
    :return: Diccionario donde la clave es el símbolo y el valor es su código binario de longitud variable.
    """
    codes = {}
    
    def walk(node: Node, current_code: str):
        """
        Recorrido recursivo del árbol: '0' para izquierda, '1' para derecha.
        """
        if node.is_leaf():
            codes[node.symbol] = current_code
            return
        
        if node.left:
            walk(node.left, current_code + '0')
        if node.right:
            walk(node.right, current_code + '1')

    # Caso especial para texto con un solo símbolo
    if root.is_leaf():
        codes[root.symbol] = '0'

    elif root:
        # Complejidad: O(n * L_max), donde n es el número de símbolos únicos y L_max es la longitud máxima del código. 
        # En la práctica, es O(n) para generar todos los códigos.
        walk(root, "")
    
    return codes

def run_huffman(txt_path: str):
    """
    Ejecuta el algoritmo de Huffman, muestra la tabla de códigos y genera las imágenes PNG obligatorias 
    del árbol y la gráfica de frecuencias.

    :param txt_path: Ruta al archivo de texto a codificar.
    :return: Una tupla que contiene los códigos generados y el nodo raíz del árbol (codes, tree_root).
    """
    text = read_text_file(txt_path)
    if not text:
        print("❌ El archivo de texto está vacío o no se pudo leer para Huffman.")
        return

    # 1. Procesar
    freqs = huffman_frequencies(text)
    tree_root = build_huffman_tree(freqs)
    
    if not tree_root:
        return

    codes = generate_codes(tree_root)
    
    # 2. Mostrar salidas en consola
    print("\n--- Resultado Algoritmo de Huffman ---")
    
    # Tabla completa de códigos
    print("\nTabla de Códigos de Huffman (Símbolo: Código Binario):")
    sorted_codes = sorted(codes.items(), key=lambda item: freqs[item[0]], reverse=True)
    for symbol, code in sorted_codes:
        # Reemplazar caracteres invisibles o especiales para mejor visualización
        display_symbol = repr(symbol) if len(symbol) > 1 or symbol == ' ' or symbol == '\n' else symbol
        print(f"  {display_symbol:<5} (Frecuencia: {freqs[symbol]:>3}): {code}")

    # Representación textual del árbol (Simplificada, usando la raíz y códigos)
    print("\nRepresentación textual del Árbol (Raíz y Códigos):")
    print(f"Raíz del Árbol (Frecuencia Total): {tree_root.freq}")
    print("El árbol binario se genera visualmente en huffman_tree.png")

    # 3. Generar imágenes PNG obligatorias
    
    # Imagen PNG del árbol (huffman_tree.png)
    draw_huffman_tree_and_save_png(tree_root, "huffman_tree.png")
    
    # Imagen PNG adicional de frecuencias (huffman_freq.png)
    draw_frequency_png(freqs, "huffman_freq.png")
    
    return codes, tree_root

if __name__ == '__main__':
    # Ejemplo de ejecución interna
    run_huffman("../../data/textos/ejemplo_texto.txt")
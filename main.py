"""
Módulo principal: Menú interactivo y punto de entrada para el Proyecto Final de
Algoritmos Avanzados.

Implementa el flujo para ejecutar Prim, Kruskal, Dijkstra y Huffman, 
leyendo archivos de datos y generando los PNG de salida obligatorios. 
Este módulo maneja la interfaz de usuario y la orquestación de las funciones 'run'
de cada algoritmo.

Complejidad: La complejidad de este módulo es O(1) ya que solo maneja la interfaz de usuario
(input/output en consola) y delega el procesamiento pesado a las funciones importadas 
(O(E log V) o O(n log n)).
"""
import os
import sys

# Ajustar el PATH para permitir importaciones modulares
# Esto asegura que los módulos dentro de src puedan importarse correctamente, especialmente cuando
# el script se ejecuta desde la raíz del proyecto.
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importar las funciones run de cada algoritmo
try:
    from src.prim import run_prim
    from src.kruskal import run_kruskal
    from src.dijkstra import run_dijkstra
    from src.huffman import run_huffman
except ImportError as e:
    print(f"❌ Error al importar módulos de src/: {e}")
    print("Asegúrate de que 'src/utils.py' y los demás archivos estén creados correctamente en la carpeta 'src'.")
    sys.exit(1)


# Rutas de archivos obligatorias
GRAPH_PATH = os.path.join('data', 'grafos', 'ejemplo_grafo.csv')
TEXT_PATH = os.path.join('data', 'textos', 'ejemplo_texto.txt')


def display_menu():
    """
    Muestra el menú interactivo con las opciones de ejecución disponibles en consola (estilo PEP-257).
    """
    print("\n" + "="*50)
    print("   PROYECTO FINAL: ALGORITMOS AVANZADOS")
    print("="*50)
    print("1. Ejecutar Prim (MST)")
    print("2. Ejecutar Kruskal (MST)")
    print("3. Ejecutar Dijkstra (Rutas más cortas)")
    print("4. Ejecutar Huffman (Codificación óptima)")
    print("0. Salir")
    print("-" * 50)


def get_user_choice() -> str:
    """
    Solicita la opción al usuario.

    :return: La opción ingresada por el usuario como string.
    """
    return input("Elige una opción: ").strip()


def handle_dijkstra():
    """
    Maneja la ejecución de Dijkstra.

    Solicita el nodo origen al usuario antes de invocar la función de procesamiento.
    """
    source_node = input(f"Ingrese el nodo origen para Dijkstra (ej: A, B, C): ").strip().upper()
    if source_node:
        # Delega la complejidad O(E log V) a la función run_dijkstra
        run_dijkstra(GRAPH_PATH, source_node)
    else:
        print("❌ Nodo origen no puede estar vacío.")


def main():
    """
    Función principal que gestiona el bucle de ejecución del menú interactivo.

    Permite al usuario seleccionar qué algoritmo ejecutar hasta que elige la opción de Salir (0).
    """
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == '0':
            print("Saliendo del programa. ¡Hasta luego!")
            break
        elif choice == '1':
            print(f"\nEjecutando Prim desde: {GRAPH_PATH}...")
            # Delega la complejidad O(E log V)
            run_prim(GRAPH_PATH)
        elif choice == '2':
            print(f"\nEjecutando Kruskal desde: {GRAPH_PATH}...")
            # Delega la complejidad O(E log E)
            run_kruskal(GRAPH_PATH)
        elif choice == '3':
            print(f"\nEjecutando Dijkstra desde: {GRAPH_PATH}...")
            # Delega la complejidad O(E log V)
            handle_dijkstra()
        elif choice == '4':
            print(f"\nEjecutando Huffman desde: {TEXT_PATH}...")
            # Delega la complejidad O(n log n)
            run_huffman(TEXT_PATH)
        else:
            print("Opción no válida. Por favor, elige un número del 0 al 4.")

# Bloque de ejecución principal
if __name__ == '__main__':
    main()
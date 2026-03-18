import random
from grafo import Grafo
import os
import json
from collections import deque
import time

def coordinates_to_vertex(row, column, columns):    
    """
    Función que convierte las coordenadas de un vértice a su índice en la matriz de adyacencia.
    :param row: Fila del vértice
    :param column: Columna del vértice
    :param columns: Número de columnas de la matriz
    """
    return row * columns + column

def vertex_to_coordinates(vertex, columns):
    """
    Función que convierte el índice de un vértice en la matriz de adyacencia a sus coordenadas.
    :param vertex: Índice del vértice
    :param columns: Número de columnas de la matriz
    """
    row = vertex // columns
    column = vertex % columns
    return row, column

def init_maze(ROWS, COLUMNS):
    """
    Función que inicializa el grafo con todos los vertices desconectados (con paredes entre todos los vertices).
    :param rows: Número de filas del laberinto
    :param columns: Número de columnas del laberinto
    """
    grafo = Grafo()

    for i in range(ROWS * COLUMNS):
                # Aristas horizontales
                vertex_o = i
                vertex_i = i + 1
                if vertex_i % COLUMNS != 0:
                    grafo.add_edge(vertex_o, vertex_i, 1)
                # Aristas verticales
                vertex_i = i + COLUMNS
                if vertex_i < ROWS * COLUMNS:
                    grafo.add_edge(vertex_o, vertex_i, 1)
    
    return grafo

def space(ROWS, COLUMNS):
    """
    Función que agrega obstaculos al espacio de trabajo.
    :param grafo: Grafo que representa el espacio de trabajo.
    """
    grafo = init_maze(ROWS, COLUMNS)        # Inicializa el grafo con todos los vertices desconectados
    Q = set(grafo.V.keys())     # Conjunto de vértices no visitados
    n = int(len(Q) * random.uniform(0.05, 0.3))  # Número de obstáculos entre 1% y 20%
    
    obstacles = random.sample(sorted(Q), n) # Selecciona n vértices al azar

    # Elimina las aristas que conectan los obstáculos
    for vertex in obstacles:

        # Obtiene las coordenadas del vértice
        row, column = vertex_to_coordinates(vertex, COLUMNS)
        
        # Obtiene los vecinos del vértice
        neighboors = [(row-1, column) if row-1 >= 0 else None,
                      (row+1, column) if row+1 < ROWS else None,
                      (row, column-1) if column-1 >= 0 else None,
                      (row, column+1) if column+1 < COLUMNS else None]
        
        # Elimina las aristas entre el vértice y sus vecinos
        for neighboor in neighboors:
            
            if neighboor is not None:

                neighboor = coordinates_to_vertex(neighboor[0], neighboor[1], COLUMNS)

                if f"({vertex}, {neighboor})" in grafo.E:
                    grafo.E[f"({vertex}, {neighboor})"] = 0

                if f"({neighboor}, {vertex})" in grafo.E:
                    grafo.E[f"({neighboor}, {vertex})"] = 0

    return grafo, obstacles

def dijkstra_algorithm(graph, init_point, end_point):
    """
    Función que implementa el algoritmo de Dijkstra para encontrar la ruta más corta entre dos puntos en un grafo.
    :param graph: Grafo en el que se busca la ruta
    :param init_point: Nodo de inicio
    :param end_point: Nodo final
    """

    # Inicializamos las distancias. Usamos infinito (inf) para los nodos no visitados
    distances = {node: float('inf') for node in graph.V.keys()}
    distances[init_point] = 0  # La distancia al nodo de inicio es 0

    # Inicializamos la tabla de predecesores (quién nos lleva a cada nodo)
    predecessors = {node: None for node in graph.V.keys()}  # No hay predecesores al principio
    
    # Usamos una cola para procesar los nodos en orden de proximidad
    queue = deque([init_point])  # Cola para BFS
    
    while queue:
        current_node = queue.popleft()  # Extraemos el primer nodo de la cola
        
        # Recorremos los vecinos del nodo actual
        for neighbor in graph.V[current_node]:
            # neighbor = str(neighbor)  # Aseguramos que el vecino sea un string

            # Si existe una arista entre el nodo actual y su vecino
            if f"({neighbor}, {current_node})" in graph.E and graph.E[f"({neighbor}, {current_node})"] > 0:
                # Si el vecino no ha sido visitado, actualizamos su distancia
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[current_node] + 1
                    predecessors[neighbor] = current_node  # Guardamos quién nos lleva a este vecino
                    queue.append(neighbor)  # Añadimos el vecino a la cola

            # Verificar reciprocidad de la arista
            if f"({current_node}, {neighbor})" in graph.E and graph.E[f"({current_node}, {neighbor})"] > 0:
                # Si el vecino no ha sido visitado, actualizamos su distancia
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[current_node] + 1
                    predecessors[neighbor] = current_node  # Guardamos quién nos lleva a este vecino
                    queue.append(neighbor)  # Añadimos el vecino a la cola

    # Reconstrucción del camino desde el vértice final
    path = [end_point]
    while predecessors[path[-1]] is not None:  # Mientras no lleguemos al vértice inicial
        path.append(predecessors[path[-1]])

    # Invertir el camino para obtener el orden correcto (de inicio a fin)
    path.reverse()

    return path

def paths(grafo, obstacles):
    """
    Función que genera rutas con el algoritmo de Dijkstra para diferentes pares de puntos en el grafo
    :param grafo: Grafo en el que se buscan las rutas
    :param obstacles: Lista de obstáculos en el grafo
    """

    turtle_init = {}                # Diccionario para almacenar la posición inicial de las tortugas
    turtle_paths = {}               # Diccionario para almacenar las rutas de cada tortuga
    Q = set(grafo.V.keys())         # Convierte Q a conjunto si no lo es
    obstacles = set(obstacles)      # Lista de obstáculos convertida a conjunto
    Q = Q - obstacles               # Elimina los elementos de Q que están en obstacles

    # Selecciona la cantidad de agentes
    N = random.randint(1, 5)

    # Inicializa los agentes en puntos aleatorios a partir de los elementos de Q
    for i in range(N):
        init_point = random.choice(list(Q))
        Q.remove(init_point)
        turtle_init[str(i)] = init_point             # Guarda la posición inicial de la tortuga

        # Selecciona un punto final aleatorio (diferente de la posición inicial)
        end_point = random.choice(list(Q))
        Q.remove(end_point)

        # Obtiene la ruta usando el algoritmo de Dijkstra
        path = dijkstra_algorithm(grafo, init_point, end_point)

        # Guarda la ruta en el diccionario
        turtle_paths[str(i)] = path

    return turtle_paths

def send(ROWS, COLUMNS):
    """
    Función que envía la información del grafo a la interfaz gráfica para su visualización.
    :param ROWS: Número de filas del laberinto
    :param COLUMNS: Número de columnas del laberinto
    """

    # Inicializa el grafo y agrega obstáculos
    grafo, obstacles = space(ROWS, COLUMNS)

    # Obtiene las rutas de las tortugas
    turtle_paths = paths(grafo, obstacles)

    # Diccionario para almacenar los colores de los nodos
    colors = {}

    # Iterar sobre cada grupo en el diccionario original para asignar colores a los nodos
    for group in turtle_paths.values():
        # Para cada grupo, asignar 'blue' al inicio de cada ruta
        colors[str(group[0])] = "blue"
        # Asignar 'red' al último número de cada ruta
        colors[str(group[-1])] = "red"

    grafo.colors = colors       # Asigna los colores al grafo

    # Para cada tortuga en el diccionario de rutas
    for tortuga, ruta in turtle_paths.items():
        for i in range(len(ruta) - 1):
            # Aquí se actualiza la posición de la tortuga con el par de nodos consecutivos
            grafo.turtle = {ruta[i]: ruta[i + 1]}
            grafo.send_graph()

            time.sleep(0.2)
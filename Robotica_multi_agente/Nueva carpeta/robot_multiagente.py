"""
Generación de un mapa (grafo) con obstaculos (nodos inalcanzables) y la utilizacion del algoritmo de Dijkstra para que robots "tortugas" encuentren el camino mas corto
hasta una tarea determinada (nodo objetivo).

Leonardo López Ortiz
Metodos y Modelos Computacionales
Maestría en Ingeniería Eléctrica
UTP - Pereira, Colombia 2024.
"""

import random
from grafo import Grafo
from collections import deque
import time
from labyrinth import Labyrinth
import threading

# Parametros iniciales (se pueden cambiar en cualquier momento)
ROWS = 15
COLUMNS = 15

def coor_to_vertex(row, column, columns):
    """
    Convierte coordenadas de los vertices a los indices de la matriz de adyacencia.
    """
    return row * columns + column

def vertex_to_coor(vertex, columns):
    """
    Convierte los indices de la matriz de adyacencia a las coordenadas del vertice.
    """
    row = vertex // columns
    column = vertex % columns
    return row, column

def maze(rows, columns):
    """
    Inicializacion del grafo con todos sus nodos conectados
    """
    graph = Grafo()

    for i in range(rows * columns):
        # Horizontal edges
        vertex_o = i
        vertex_i = i + 1
        if vertex_i % columns != 0:
            graph.add_edge(vertex_o, vertex_i, 1)
        # Vertical edges
        vertex_i = i + columns
        if vertex_i < rows * columns:
            graph.add_edge(vertex_o, vertex_i, 1)

    return graph

def obstacle(rows, columns):
    """
    Se agregan obstaculos en la interzfaz.
    """
    graph = maze(rows, columns)
    q = set(graph.V.keys())
    n = int(len(q) * random.uniform(0.1, 0.7)) #10% a 70% de obstaculos

    obstacles = random.sample(sorted(q), n)

    for vertex in obstacles:
        row, column = vertex_to_coor(vertex, columns)

        neighbors = [
            (row - 1, column) if row - 1 >= 0 else None,
            (row + 1, column) if row + 1 < rows else None,
            (row, column - 1) if column - 1 >= 0 else None,
            (row, column + 1) if column + 1 < columns else None
        ]

        for neighbor in neighbors:
            if neighbor is not None:
                neighbor = coor_to_vertex(neighbor[0], neighbor[1], columns)

                if f"({vertex}, {neighbor})" in graph.E:
                    graph.E[f"({vertex}, {neighbor})"] = 0

                if f"({neighbor}, {vertex})" in graph.E:
                    graph.E[f"({neighbor}, {vertex})"] = 0

    return graph, obstacles

def dijkstra(graph, init_point, end_point):
    """
    Se utiliza la implementacion del algoritmo de Dijkstra ya que es el que mejor funciona para encontrar el camino mas corto entre dos puntos de un grafo.
    """
    distances = {node: float('inf') for node in graph.V.keys()}
    distances[init_point] = 0

    predecessors = {node: None for node in graph.V.keys()}
    queue = deque([init_point])

    while queue:
        current_node = queue.popleft()

        for neighbor in graph.V[current_node]:
            if f"({neighbor}, {current_node})" in graph.E and graph.E[f"({neighbor}, {current_node})"] > 0:
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[current_node] + 1
                    predecessors[neighbor] = current_node
                    queue.append(neighbor)

            if f"({current_node}, {neighbor})" in graph.E and graph.E[f"({current_node}, {neighbor})"] > 0:
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = distances[current_node] + 1
                    predecessors[neighbor] = current_node
                    queue.append(neighbor)

    path = [end_point]
    while predecessors[path[-1]] is not None:
        path.append(predecessors[path[-1]])

    path.reverse()
    return path

def paths(graph, obstacles):
    """
    Generacion de rutas en diferentes partes del grafo utiliando el algoritmo de Dijkstra.
    """
    turtle_init = {}
    turtle_paths = {}
    q = set(graph.V.keys())
    obstacles = set(obstacles)
    q = q - obstacles

    n = random.randint(2, 5)  # Generación aleatoria de tortugas

    for i in range(n):
        init_point = random.choice(list(q))
        q.remove(init_point)
        turtle_init[str(i)] = init_point

        end_point = random.choice(list(q))
        q.remove(end_point)

        path = dijkstra(graph, init_point, end_point)
        turtle_paths[str(i)] = path

    return turtle_paths

def enviar(rows, columns):
    """
    Envia la estrutura de grafo generada a la interfaz grafica.
    """
    graph, obstacles = obstacle(rows, columns)
    turtle_paths = paths(graph, obstacles)

    colors = {}
    available_colors = ["blue", "green", "purple", "orange", "yellow"] # colores donde comienza una tortuga aleatoriamente o sea el grafo.

    for idx, (turtle, path) in enumerate(turtle_paths.items()):
        color = available_colors[idx % len(available_colors)]
        colors[str(path[0])] = color  # nodo inicial
        colors[str(path[-1])] = "red"  # nodo final

    graph.colors = colors

    for step in range(max(len(path) for path in turtle_paths.values())):
        for turtle, path in turtle_paths.items():
            if step < len(path) - 1:
                graph.turtle = {path[step]: path[step + 1]}
                graph.send_graph()

        time.sleep(0.8)

def create_labyrinth():
    maze = Labyrinth(ROWS, COLUMNS)
    maze.start()

def create_graph():
    enviar(ROWS, COLUMNS)

if __name__ == '__main__':
    thread1 = threading.Thread(target=create_labyrinth)
    thread1.start()

    thread2 = threading.Thread(target=create_graph)
    thread2.start()

    thread2.join()
    thread1.join()

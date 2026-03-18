"""
This is an example of multi-threading execution
Front-end and Back-end modules are running in different threads
Inter-thread comm is implemented with a Queue and a mutex lock

Eduardo Martinez Duque
Nathalia Arias Santa
UTP - Pereira, Colombia 2024.
"""

from labyrinth import Labyrinth
import threading
from robot_movement import send

# input parameters
ROWS = 15
COLUMNS = 20


def create_labyrinth():
    """
    Esta función crea un objeto Laberinto con el número especificado de filas y columnas, e inicia el bucle de eventos Tkinter.

    La función utiliza las constantes globales FILAS y COLUMNAS para determinar el tamaño del laberinto. A continuación, el laberinto
    se muestra en la pantalla llamando al método start de la clase Labyrinth.

    :return: None
    """
    maze = Labyrinth(ROWS, COLUMNS)
    maze.start()


def create_graph():
    """
    Esta función implementa el  problema de PLANEACIÓN DE MOVIMIENTO EN ROBÓTICA MULTI-AGENTE.

    :return: None
    """
    send(ROWS, COLUMNS)


if __name__ == '__main__':
    # Crear dos hilos para ejecutar las funciones create_labyrinth y create_graph concurrentemente
    
    hilo1 = threading.Thread(target=create_labyrinth)
    hilo1.start()  

    hilo2 = threading.Thread(target=create_graph)
    hilo2.start()

    # Esperar a que los hilos terminen
    hilo2.join()
    hilo1.join()
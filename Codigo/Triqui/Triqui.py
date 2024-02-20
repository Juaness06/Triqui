# Importación de librerías necesarias para el juego
import copy  # Para copiar el estado del tablero
import random  # Para generar movimientos aleatorios
import sys  # Para cerrar el programa
import pygame  # Para la interfaz gráfica del juego
import numpy as np  # Para manejar el tablero como una matriz
from constantes import *  # Importa las constantes definidas en otro archivo, como dimensiones de la ventana, colores, etc.


# Inicialización de Pygame y configuración de la ventana de visualización
pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption('TRIQUI MOVIL')
screen.fill(FONDO_COLOR)

# Definición de la clase Tablero, que gestiona el estado del juego
class Tablero:

    def __init__(self):
        # Inicializa un tablero 3x3 vacío
        self.cuadrados = np.zeros((FILAS, COLUMNAS))
        self.cuadradosMarcados = 0  # Contador para los cuadrados ocupados

    # Método para evaluar el estado del tablero y determinar si hay un ganador
    def estadoFinal(self, show=False):
        # Revisa todas las posibles líneas de victoria (filas, columnas, diagonales)
        for columnas in range(COLUMNAS):
            if self.cuadrados[0][columnas] == self.cuadrados[1][columnas] == self.cuadrados[2][columnas] != 0:
                return self.cuadrados[0][columnas]

        for filas in range(FILAS):
            if self.cuadrados[filas][0] == self.cuadrados[filas][1] == self.cuadrados[filas][2] != 0:
                return self.cuadrados[filas][0]

        if self.cuadrados[0][0] == self.cuadrados[1][1] == self.cuadrados[2][2] != 0:
            return self.cuadrados[1][1]

        if self.cuadrados[2][0] == self.cuadrados[1][1] == self.cuadrados[0][2] != 0:
            return self.cuadrados[1][1]

        return 0  # Retorna 0 si no hay ganador

    # Método para colocar una ficha en el tablero
    def ponerFicha(self, fila, columna, jugador):
        self.cuadrados[fila][columna] = jugador
        self.cuadradosMarcados += 1

    # Verifica si una posición del tablero está vacía
    def cuadradoVacio(self, fila, columna):
        return self.cuadrados[fila][columna] == 0

    # Devuelve una lista de todas las posiciones vacías en el tablero
    def obtenerVacios(self):
        cuadradosVacios = []
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                if self.cuadradoVacio(fila, columna):
                    cuadradosVacios.append((fila, columna))
        return cuadradosVacios

    # Verifica si el tablero está completamente lleno
    def lleno(self):
        return self.cuadradosMarcados == 9

# Clase Maquina: representa la IA del juego
class Maquina:

    def __init__(self, nivel=1, jugador=2):
        self.nivel = nivel  # Dificultad de la IA
        self.jugador = jugador  # Identificador del jugador máquina

    # Método para seleccionar una posición aleatoria (usado en dificultad baja)
    def aleatorio(self, tablero):
        cuadradosVacios = tablero.obtenerVacios()
        indiceAleatorio = random.randrange(0, len(cuadradosVacios))
        return cuadradosVacios[indiceAleatorio]

    # Implementación del algoritmo Minimax para determinar la mejor jugada
    def minimax(self, tablero, maximizar):
        caso = tablero.estadoFinal()
        if caso == 1:
            return 1, None  # Victoria para el jugador 1
        if caso == 2:
            return -1, None  # Victoria para el jugador 2
        elif tablero.lleno():
            return 0, None  # Empate

        if maximizar:
            maximaEvaluacion = -100
            mejorJugada = None
            for (fila, columna) in tablero.obtenerVacios():
                tableroTemporal = copy.deepcopy(tablero)
                tableroTemporal.ponerFicha(fila, columna, 1)
                evaluacion = self.minimax(tableroTemporal, False)[0]
                if evaluacion > maximaEvaluacion:
                    maximaEvaluacion = evaluacion
                    mejorJugada = (fila, columna)
            return maximaEvaluacion, mejorJugada
        else:
            minimaEvaluacion = 100
            mejorJugada = None
            for (fila, columna) in tablero.obtenerVacios():
                tableroTemporal = copy.deepcopy(tablero)
                tableroTemporal.ponerFicha(fila, columna, self.jugador)
                evaluacion = self.minimax(tableroTemporal, True)[0]
                if evaluacion < minimaEvaluacion:
                    minimaEvaluacion = evaluacion
                    mejorJugada = (fila, columna)
            return minimaEvaluacion, mejorJugada

    # Método que decide la jugada de la IA basándose en el nivel de dificultad
    def evaluar(self, tableroPrincipal):
        if self.nivel == 0:
            jugada = self.aleatorio(tableroPrincipal)
        else:
            _, jugada = self.minimax(tableroPrincipal, False)
        print(f'La máquina ha escogido la posición {jugada}')
        return jugada

# Clase Juego: gestiona el flujo principal del juego
class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.maquina = Maquina()
        self.jugador = 1  # El jugador humano inicia como jugador 1
        self.modoJuego = 'maquina'
        self.enJuego = True
        self.dibujarFiguras()

    # Dibuja las líneas del tablero en la pantalla
    def dibujarFiguras(self):
        screen.fill(FONDO_COLOR)
        for fila in range(1, FILAS):
            pygame.draw.line(screen, LINEA_COLOR, (0, fila * TAMANO_CUADRO), (ANCHO, fila * TAMANO_CUADRO), LINEA_ANCHO)
        for columna in range(1, COLUMNAS):
            pygame.draw.line(screen, LINEA_COLOR, (columna * TAMANO_CUADRO, 0), (columna * TAMANO_CUADRO, ALTURA), LINEA_ANCHO)

    # Dibuja las fichas de los jugadores en el tablero
    def dibujar(self, fila, columna):
        if self.jugador == 1:
            # Dibuja una 'X' para el jugador 1
            inicio_desc = (columna * TAMANO_CUADRO + OFFSET, fila * TAMANO_CUADRO + OFFSET)
            fin_desc = (columna * TAMANO_CUADRO + TAMANO_CUADRO - OFFSET, fila * TAMANO_CUADRO + TAMANO_CUADRO - OFFSET)
            pygame.draw.line(screen, COLOR_X, inicio_desc, fin_desc, ANCHO_X)
            inicio_asc = (columna * TAMANO_CUADRO + OFFSET, fila * TAMANO_CUADRO + TAMANO_CUADRO - OFFSET)
            fin_asc = (columna * TAMANO_CUADRO + TAMANO_CUADRO - OFFSET, fila * TAMANO_CUADRO + OFFSET)
            pygame.draw.line(screen, COLOR_X, inicio_asc, fin_asc, ANCHO_X)
        elif self.jugador == 2:
            # Dibuja un círculo para el jugador 2
            centro = (columna * TAMANO_CUADRO + TAMANO_CUADRO // 2, fila * TAMANO_CUADRO + TAMANO_CUADRO // 2)
            pygame.draw.circle(screen, COLOR_CIRCULO, centro, RADIO_CIRCULO, ANCHO_CIRCULO)

    # Realiza una jugada en el tablero y cambia el turno
    def hacerJuagada(self, fila, columna):
        self.tablero.ponerFicha(fila, columna, self.jugador)
        self.dibujar(fila, columna)
        self.turno()

    # Cambia el turno entre los jugadores
    def turno(self):
        self.jugador = self.jugador % 2 + 1

    # Verifica si el juego ha terminado
    def acabarJuego(self):
        return self.tablero.estadoFinal(show=True) != 0 or self.tablero.lleno()

    # Reinicia el juego a su estado inicial
    def reiniciar(self):
        self.__init__()

# Función principal que inicia y controla el flujo del juego
def main():
    juego = Juego()

    # Bucle principal del juego
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Salir del juego
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Reiniciar juego o cambiar nivel de IA
                if event.key == pygame.K_r:
                    juego.reiniciar()
                if event.key == pygame.K_0:
                    juego.maquina.nivel = 0
                if event.key == pygame.K_1:
                    juego.maquina.nivel = 1
            if event.type == pygame.MOUSEBUTTONDOWN:  # Manejar jugadas del usuario
                pos = event.pos
                fila = pos[1] // TAMANO_CUADRO
                columna = pos[0] // TAMANO_CUADRO
                if juego.tablero.cuadradoVacio(fila, columna) and juego.enJuego:
                    juego.hacerJuagada(fila, columna)
                    if juego.acabarJuego():
                        juego.enJuego = False
        if juego.modoJuego == 'maquina' and juego.jugador == juego.maquina.jugador and juego.enJuego:
            fila, columna = juego.maquina.evaluar(juego.tablero)
            juego.hacerJuagada(fila, columna)
            if juego.acabarJuego():
                juego.enJuego = False
        pygame.display.update()

main()  # Ejecuta el juego
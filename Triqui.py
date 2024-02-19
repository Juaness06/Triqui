import copy
import random
import sys
import pygame
import numpy as np
from constantes import *


pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTURA))
pygame.display.set_caption('TRIQUI MOVIL')
screen.fill(FONDO_COLOR)

# clase tablero
class Tablero:

    def __init__(self):
        self.cuadrados = np.zeros((FILAS, COLUMNAS)) # matriz de 3x3
        self.cuadradosVacios = self.cuadrados
        self.cuadradosMarcados = 0

    def estadoFinal(self, show=False): # retorna 0 si no hay ganador, 1 si gana el jugador 1, 2 si gana el jugador 2

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

        return 0

    def ponerFicha(self, fila, columna, jugador): # pone la ficha en el tablero
        self.cuadrados[fila][columna] = jugador
        self.cuadradosMarcados += 1

    def cuadradoVacio(self, fila, columna): # retorna si el cuadrado esta vacio
        return self.cuadrados[fila][columna] == 0

    def obtenerVacios(self):
        cuadradosVacios = []
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                if self.cuadradoVacio(fila, columna):
                    cuadradosVacios.append((fila, columna))

        return cuadradosVacios

    def lleno(self):
        return self.cuadradosMarcados == 9

    def esVacio(self):
        return self.cuadradosMarcados == 0


class Maquina:

    def __init__(self, nivel=1, jugador=2):

        self.nivel = nivel # nivel es la dificultad de la maquina
        self.jugador = jugador

    def aleatorio(self, tablero):
        cuadradosVacios = tablero.obtenerVacios()
        indiceAleatorio = random.randrange(0, len(cuadradosVacios))

        return cuadradosVacios[indiceAleatorio]

    def minimax(self, tablero, maximizar): # algoritmo minimax
        caso = tablero.estadoFinal()
        if caso == 1:

            return 1, None

        if caso == 2:

            return -1, None

        elif tablero.lleno():
            return 0, None

        if maximizar: # si maximizar es verdadero

            maximaEvaluacion = -100
            mejorJugada = None
            cuadradosVacios = tablero.obtenerVacios()
            for (fila, columna) in cuadradosVacios:
                tableroTemporal = copy.deepcopy(tablero)
                tableroTemporal.ponerFicha(fila, columna, 1)
                eval = self.minimax(tableroTemporal, False)[0]
                if eval > maximaEvaluacion:
                    maximaEvaluacion = eval
                    mejorJugada = (fila, columna)

            return maximaEvaluacion, mejorJugada

        else: # si maximizar es falso

            minimaEvaluacion = 100
            mejorJugada = None
            cuadradosVacios = tablero.obtenerVacios()
            for (fila, columna) in cuadradosVacios:
                tableroTemporal = copy.deepcopy(tablero)
                tableroTemporal.ponerFicha(fila, columna, self.jugador)
                eval = self.minimax(tableroTemporal, True)[0]
                if eval < minimaEvaluacion:
                    minimaEvaluacion = eval
                    mejorJugada = (fila, columna)

            return minimaEvaluacion, mejorJugada

    def evaluar(self, tableroPrincipal): # aqui es donde la maquina evaluara el tablero y escogera la mejor jugada
        if self.nivel == 0:
            eval = 'aleatorio'
            mover = self.aleatorio(tableroPrincipal)
        else:
            eval, mover = self.minimax(tableroPrincipal, False)
        print(f'la maquina ha escogido la posicion {mover} con un puntaje de {eval}')

        return mover


class Juego:
    def __init__(self):
        self.tablero = Tablero()
        self.maquina = Maquina()
        self.jugador = 1
        self.modoJuego = 'maquina'
        self.enJuego = True
        self.dibujarFiguras()


    def dibujarFiguras(self):
        screen.fill(FONDO_COLOR)
        for fila in range(1, FILAS):
            pygame.draw.line(screen, LINEA_COLOR, (0, fila * TAMANO_CUADRO), (ANCHO, fila * TAMANO_CUADRO), LINEA_ANCHO)
        for columna in range(1, COLUMNAS):
            pygame.draw.line(screen, LINEA_COLOR, (columna * TAMANO_CUADRO, 0), (columna * TAMANO_CUADRO, ALTURA),
                             LINEA_ANCHO)

    def dibujar(self, fila, columna):
        if self.jugador == 1:
            inicio_desc = (columna * TAMANO_CUADRO + OFFSET, fila * TAMANO_CUADRO + OFFSET)
            fin_desc = (columna * TAMANO_CUADRO + TAMANO_CUADRO - OFFSET, fila * TAMANO_CUADRO + TAMANO_CUADRO - OFFSET)
            pygame.draw.line(screen, COLOR_X, inicio_desc, fin_desc, ANCHO_X)
            inicio_asc = (columna * TAMANO_CUADRO + OFFSET, fila * TAMANO_CUADRO + TAMANO_CUADRO - OFFSET)
            fin_asc = (columna * TAMANO_CUADRO + TAMANO_CUADRO - OFFSET, fila * TAMANO_CUADRO + OFFSET)
            pygame.draw.line(screen, COLOR_X, inicio_asc, fin_asc, ANCHO_X)
        elif self.jugador == 2:
            centro = (columna * TAMANO_CUADRO + TAMANO_CUADRO // 2, fila * TAMANO_CUADRO + TAMANO_CUADRO // 2)
            pygame.draw.circle(screen, COLOR_CIRCULO, centro, RADIO_CIRCULO, ANCHO_CIRCULO)

    def hacerJuagada(self, fila, columna):
        self.tablero.ponerFicha(fila, columna, self.jugador)
        self.dibujar(fila, columna)
        self.turno()

    def turno(self):
        self.jugador = self.jugador % 2 + 1

    def acabarJuego(self):
        return self.tablero.estadoFinal(show=True) != 0 or self.tablero.lleno()

    def reiniciar(self):
        self.__init__()


def main():
    juego = Juego()
    tablero = juego.tablero
    maquina = juego.maquina

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    juego.reiniciar()
                    tablero = juego.tablero
                    maquina = juego.maquina
                if event.key == pygame.K_0:
                    maquina.nivel = 0
                if event.key == pygame.K_1:
                    maquina.nivel = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                fila = pos[1] // TAMANO_CUADRO
                columna = pos[0] // TAMANO_CUADRO
                if tablero.cuadradoVacio(fila, columna) and juego.enJuego:
                    juego.hacerJuagada(fila, columna)
                    if juego.acabarJuego():
                        juego.enJuego = False
        if juego.modoJuego == 'maquina' and juego.jugador == maquina.jugador and juego.enJuego:
            pygame.display.update()
            fila, columna = maquina.evaluar(tablero)
            juego.hacerJuagada(fila, columna)
            if juego.acabarJuego():
                juego.enJuego = False
        pygame.display.update()


main()

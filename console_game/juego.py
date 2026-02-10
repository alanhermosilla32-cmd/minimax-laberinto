import os
from collections import deque
import msvcrt
import random
import time

# Constantes del Juego (Emojis)
MURO = "🟦"
CAMINO = "  "
RITMO = "🐭"  # Ratón
GATO = "🐱"
QUESO = "🧀"
JUGADOR = RITMO
ENEMIGO = GATO
META = QUESO

# Mapa del laberinto (1 = Muro, 0 = Camino)
# Un laberinto simple de 10x10 para empezar
MAPA_DISEÑO = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class JuegoLaberinto:
    def __init__(self):
        self.mapa = [fila[:] for fila in MAPA_DISEÑO]  # Copia del mapa
        self.filas = len(self.mapa)
        self.columnas = len(self.mapa[0])
        self.jugador_pos = [1, 1]
        self.enemigo_pos = [9, 13]
        self.meta_pos = [5, 7]
        self.juego_terminado = False
        self.mensaje_final = ""

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def dibujar_mapa(self):
        self.limpiar_pantalla()
        print("🎮 ¡Juego del Laberinto: Ratón vs Gato! 🎮")
        print("Usa WASD para moverte. Llega al Queso 🧀. ¡Cuidado con el Gato 🐱!\n")
        
        buffer_pantalla = ""
        for y in range(self.filas):
            linea = ""
            for x in range(self.columnas):
                if y == self.jugador_pos[0] and x == self.jugador_pos[1]:
                    linea += JUGADOR
                elif y == self.enemigo_pos[0] and x == self.enemigo_pos[1]:
                    linea += ENEMIGO
                elif y == self.meta_pos[0] and x == self.meta_pos[1]:
                    linea += META
                elif self.mapa[y][x] == 1:
                    linea += MURO
                else:
                    linea += CAMINO
            buffer_pantalla += linea + "\n"
        print(buffer_pantalla)
        
        if self.juego_terminado:
            print(self.mensaje_final)

    def mover_jugador(self, dy, dx):
        nueva_y = self.jugador_pos[0] + dy
        nueva_x = self.jugador_pos[1] + dx

        if self.mapa[nueva_y][nueva_x] != 1:
            self.jugador_pos = [nueva_y, nueva_x]
            self.verificar_victoria()
            self.mover_enemigo()
            self.verificar_derrota()

    def mover_enemigo(self):
        # IA mejorada: Usar BFS para perseguir al jugador
        camino = self.bfs_buscar_camino(self.enemigo_pos, self.jugador_pos)
        
        if camino:
            # El primer paso del camino es a donde debemos ir
            siguiente_paso = camino[0]
            # Calcular delta
            dy = siguiente_paso[0] - self.enemigo_pos[0]
            dx = siguiente_paso[1] - self.enemigo_pos[1]
            
            nueva_y = self.enemigo_pos[0] + dy
            nueva_x = self.enemigo_pos[1] + dx
            
            # Verificar si choca con el muro (aunque BFS ya lo evita, doble check)
            if self.mapa[nueva_y][nueva_x] != 1:
                self.enemigo_pos = [nueva_y, nueva_x]
        else:
             # Si no hay camino directo, quedarse quieto o mover aleatorio (opcional)
             pass

    def verificar_victoria(self):
        if self.jugador_pos == self.meta_pos:
            self.juego_terminado = True
            self.mensaje_final = "\n🎉 ¡Felicidades! ¡El ratón consiguió el queso! 🧀🎉"

    def verificar_derrota(self):
         if self.jugador_pos == self.enemigo_pos:
            self.juego_terminado = True
            self.mensaje_final = "\n💀 ¡Oh no! ¡El gato te atrapó! 💀"

    def mover_raton_automatico(self):
        # Usar BFS para encontrar el camino más corto al queso
        camino = self.bfs_buscar_camino(self.jugador_pos, self.meta_pos)
        
        if camino:
            # El primer paso del camino es a donde debemos ir
            siguiente_paso = camino[0]
            # Calcular delta para mover_jugador
            dy = siguiente_paso[0] - self.jugador_pos[0]
            dx = siguiente_paso[1] - self.jugador_pos[1]
            self.mover_jugador(dy, dx)
        else:
            # Si no hay camino (bloqueado), moverse aleatoriamente (fallback)
            direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(direcciones)
            for d_y, d_x in direcciones:
                 nueva_y = self.jugador_pos[0] + d_y
                 nueva_x = self.jugador_pos[1] + d_x
                 if self.mapa[nueva_y][nueva_x] != 1:
                     self.mover_jugador(d_y, d_x)
                     break

    def bfs_buscar_camino(self, inicio, meta):
        # BFS para encontrar el camino más corto
        # inicio y meta son listas o tuplas [y, x]
        inicio = tuple(inicio)
        meta = tuple(meta)
        
        cola = deque([(inicio, [])]) # (posicion_actual, camino_recorrido)
        visitados = set([inicio])
        
        while cola:
            (y, x), camino = cola.popleft()
            
            if (y, x) == meta:
                return camino # Retorna la lista de pasos para llegar a la meta
            
            direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(direcciones) # Para variar si hay múltiples caminos iguales
            
            for dy, dx in direcciones:
                ny, nx = y + dy, x + dx
                
                # Verificar límites y muros
                if 0 <= ny < self.filas and 0 <= nx < self.columnas:
                    if self.mapa[ny][nx] != 1 and (ny, nx) not in visitados:
                        visitados.add((ny, nx))
                        nuevo_camino = camino + [[ny, nx]]
                        cola.append(((ny, nx), nuevo_camino))
        
        return None # No se encontró camino

    def iniciar(self):
        print("Iniciando modo automático inteligente (BFS)...")
        time.sleep(1)
        while not self.juego_terminado:
            self.dibujar_mapa()
            
            # Movimiento automático
            time.sleep(0.2) # Un poco más rápido
            
            self.mover_raton_automatico()
            if not self.juego_terminado:
                 pass

            # Salida de emergencia
            if msvcrt.kbhit():
                tecla = msvcrt.getch().decode('utf-8').lower()
                if tecla == 'q':
                    print("\nSaliendo del juego...")
                    break
        
        self.dibujar_mapa()
        print(self.mensaje_final)
        input("\nPresiona Enter para salir...")

if __name__ == "__main__":
    juego = JuegoLaberinto()
    juego.iniciar()

import random
import time
import os
import math
import sys

# Intentar importar pygame, salir si falla (aunque ya debiera estar instalado)
try:
    import pygame
except ImportError:
    print("Error: Pygame no está instalado. Ejecuta 'pip install pygame'")
    sys.exit(1)

# Constantes de Lógica
EMPTY = '.'
OBSTACLE = '#'
MOUSE = 'M'
CAT = 'C'
CHEESE = 'Q'

# Constantes de Pygame
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40 # Tamaño base de celda
FPS = 60

# Colores (Tema Neon/Cyberpunk)
COLOR_BG = (10, 10, 20)          # Azul oscuro casi negro
COLOR_GRID = (40, 40, 80)        # Grid sutil
COLOR_OBSTACLE = (30, 30, 50)    # Bloque oscuro
COLOR_OBSTACLE_BORDER = (60, 60, 100)
COLOR_MOUSE = (0, 255, 255)      # Cyan Neon
COLOR_CAT = (255, 0, 100)        # Rosa Neon
COLOR_CHEESE = (255, 255, 0)     # Amarillo Neon
COLOR_TEXT = (200, 200, 255)
COLOR_UI_BG = (20, 20, 40, 200)

# --- CLASES LÓGICAS (MODELO) ---

class Board:
    def __init__(self, width=21, height=15): # Ajustado a impar para mejor laberinto
        self.width = width
        self.height = height
        self.grid = [[OBSTACLE for _ in range(width)] for _ in range(height)]
        self.obstacles = set()
        self.cheese_pos = None
        
        self._generate_maze()
        self._place_cheese()
        self._update_obstacles_set()

    def _generate_maze(self):
        # Algoritmo Recursive Backtracker
        # 1. Empezar con todo muros (ya hecho en __init__)
        # 2. Elegir celda inicial impar (1,1)
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = EMPTY
        stack = [(start_x, start_y)]
        
        while stack:
            cx, cy = stack[-1]
            # Buscar vecinos no visitados (distancia 2)
            neighbors = []
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if self.grid[ny][nx] == OBSTACLE:
                        neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                # Abrir muro intermedio
                self.grid[cy + dy//2][cx + dx//2] = EMPTY
                # Abrir nueva celda
                self.grid[ny][nx] = EMPTY
                stack.append((nx, ny))
            else:
                stack.pop()
        
        # Abrir algunas paredes extra para no hacerlo tan lineal (loops)
        for _ in range(int(self.width * self.height * 0.05)):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.grid[y][x] == OBSTACLE:
                 # Chequear si conecta dos pasillos
                 if (self.grid[y+1][x] == EMPTY and self.grid[y-1][x] == EMPTY) or \
                    (self.grid[y][x+1] == EMPTY and self.grid[y][x-1] == EMPTY):
                        self.grid[y][x] = EMPTY

    def _update_obstacles_set(self):
        self.obstacles.clear()
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == OBSTACLE:
                    self.obstacles.add((x, y))

    def _place_cheese(self):
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.grid[y][x] == EMPTY:
                self.cheese_pos = (x, y)
                self.grid[y][x] = CHEESE
                break

    def is_valid(self, pos):
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            if self.grid[y][x] != OBSTACLE:
                return True
        return False

    def get_neighbors(self, pos):
        x, y = pos
        # Movimiento en 4 direcciones para respetar el laberinto mejor
        # (Con 8 direcciones se pueden "saltar" esquinas de muros)
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1)
        ]
        valid_moves = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid((nx, ny)):
                valid_moves.append((nx, ny))
        return valid_moves

# --- ALGORITMO MINIMAX ---

def chebyshev_distance(pos1, pos2):
    return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))

def evaluate_state(board, cat_pos, mouse_pos):
    if cat_pos == mouse_pos:
        return -math.inf
    if mouse_pos == board.cheese_pos:
        return math.inf
    
    dist_cat = chebyshev_distance(cat_pos, mouse_pos)
    dist_cheese = chebyshev_distance(mouse_pos, board.cheese_pos)
    
    # Heurística ponderada
    security_score = dist_cat
    goal_score = -dist_cheese 
    return (security_score * 1.0) + (goal_score * 1.5)

def minimax(board, depth, is_maximizing, cat_pos, mouse_pos, alpha, beta):
    current_eval = evaluate_state(board, cat_pos, mouse_pos)
    if depth == 0 or current_eval == -math.inf or current_eval == math.inf:
        return current_eval, None

    if is_maximizing: # Turno Ratón
        max_eval = -math.inf
        # default move: stay
        best_move = mouse_pos 
        possible_moves = board.get_neighbors(mouse_pos)
        possible_moves.sort(key=lambda m: evaluate_state(board, cat_pos, m), reverse=True)

        if not possible_moves: return -math.inf, mouse_pos

        for move in possible_moves:
            eval_score, _ = minimax(board, depth - 1, False, cat_pos, move, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha: break
        return max_eval, best_move

    else: # Turno Gato
        min_eval = math.inf
        best_move = cat_pos
        possible_moves = board.get_neighbors(cat_pos)
        possible_moves.sort(key=lambda m: evaluate_state(board, m, mouse_pos))

        if not possible_moves: return math.inf, cat_pos

        for move in possible_moves:
            if move == mouse_pos: return -math.inf, move
            eval_score, _ = minimax(board, depth - 1, True, move, mouse_pos, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha: break
        return min_eval, best_move

# --- AGENTES ---

class Agent:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

    def get_move(self, board, my_pos, opponent_pos, events=None):
        raise NotImplementedError 

class RandomMouse(Agent):
    def __init__(self):
        super().__init__("Ratón Aleatorio", MOUSE)

    def get_move(self, board, my_pos, opponent_pos, events=None):
        moves = board.get_neighbors(my_pos)
        if not moves: return my_pos
        return random.choice(moves)

class PygameHumanAgent(Agent):
    def __init__(self, name, symbol):
        super().__init__(name, symbol)
    
    def get_move(self, board, my_pos, opponent_pos, events=None):
        if events is None: return None
        
        # Mapeo de teclas
        dx, dy = 0, 0
        move_chosen = False
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w: dy = -1; move_chosen = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s: dy = 1; move_chosen = True
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a: dx = -1; move_chosen = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d: dx = 1; move_chosen = True
                elif event.key == pygame.K_q: dx, dy = -1, -1; move_chosen = True
                elif event.key == pygame.K_e: dx, dy = 1, -1; move_chosen = True
                elif event.key == pygame.K_z: dx, dy = -1, 1; move_chosen = True
                elif event.key == pygame.K_c: dx, dy = 1, 1; move_chosen = True
                elif event.key == pygame.K_SPACE: dx, dy = 0, 0; move_chosen = True # Esperar

        if move_chosen:
            nx, ny = my_pos[0] + dx, my_pos[1] + dy
            if board.is_valid((nx, ny)):
                return (nx, ny)
        
        return None

class SmartMouse(Agent):
    def __init__(self, depth=3):
        super().__init__("Ratón Inteligente", MOUSE)
        self.depth = depth

    def get_move(self, board, my_pos, opponent_pos, events=None):
        score, move = minimax(board, self.depth, True, opponent_pos, my_pos, -math.inf, math.inf)
        return move

class SmartCat(Agent):
    def __init__(self, depth=3):
        super().__init__("Gato Inteligente", CAT)
        self.depth = depth

    def get_move(self, board, my_pos, opponent_pos, events=None):
        score, move = minimax(board, self.depth, False, my_pos, opponent_pos, -math.inf, math.inf)
        return move

# --- CLASE RENDERER (VISTA) ---

class Renderer:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size + 100)) # +100 para UI abajo
        pygame.display.set_caption("Laberinto Minimax: Neon Chase")
        self.font = pygame.font.SysFont("consolas", 20)
        self.title_font = pygame.font.SysFont("impact", 40)
        
        # Estado de animación
        self.vis_cat_pos = (-100, -100) # Inicial fuera de pantalla
        self.vis_mouse_pos = (-100, -100)

    def grid_to_screen(self, grid_pos):
        return (grid_pos[0] * self.cell_size, grid_pos[1] * self.cell_size)

    def draw_glow_circle(self, surface, color, pos, radius, glow_radius):
        # Dibujar núcleo
        pygame.draw.circle(surface, color, pos, radius)
        # Dibujar brillo
        glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, 100), (glow_radius, glow_radius), glow_radius)
        surface.blit(glow_surf, (pos[0]-glow_radius, pos[1]-glow_radius), special_flags=pygame.BLEND_ADD)

    def draw_cat_skin(self, surface, pos, size):
        # Base con brillo suave
        self.draw_glow_circle(surface, COLOR_CAT, pos, size//2 - 4, 25)
        
        # Orejas (Poligonos) - estilo Gato
        ear_offset_x = 10
        ear_offset_y = 12
        left_ear = [(pos[0] - ear_offset_x, pos[1] - 5), (pos[0] - 16, pos[1] - 18), (pos[0] - 4, pos[1] - 12)]
        right_ear = [(pos[0] + ear_offset_x, pos[1] - 5), (pos[0] + 16, pos[1] - 18), (pos[0] + 4, pos[1] - 12)]
        pygame.draw.polygon(surface, COLOR_CAT, left_ear)
        pygame.draw.polygon(surface, COLOR_CAT, right_ear)
        
        # Ojos "Malvados"
        eye_color = (255, 200, 200)
        pygame.draw.line(surface, eye_color, (pos[0]-8, pos[1]-2), (pos[0]-3, pos[1]+3), 2)
        pygame.draw.line(surface, eye_color, (pos[0]+8, pos[1]-2), (pos[0]+3, pos[1]+3), 2)

    def draw_mouse_skin(self, surface, pos, size):
         # Cuerpo
        self.draw_glow_circle(surface, COLOR_MOUSE, pos, size//2 - 6, 20)
        
        # Orejas Redondas Grandes
        ear_radius = 8
        pygame.draw.circle(surface, COLOR_MOUSE, (int(pos[0] - 10), int(pos[1] - 10)), ear_radius)
        pygame.draw.circle(surface, COLOR_MOUSE, (int(pos[0] + 10), int(pos[1] - 10)), ear_radius)
        
        # Nariz
        pygame.draw.circle(surface, (255, 100, 150), pos, 3)
        
        # Cola (Curva simple)
        start = (pos[0], pos[1]+10)
        end = (pos[0]+10, pos[1]+15)
        pygame.draw.line(surface, COLOR_MOUSE, start, end, 2)

    def draw_cheese_skin(self, surface, pos, size):
        # Brillo pulsante (recalculado aqui o pasado, usaremos estatico + glow)
        self.draw_glow_circle(surface, COLOR_CHEESE, pos, size//3, 20)
        
        # Forma de Cuña (Triangulo)
        # Puntos relativos al centro pos
        off = size // 3
        p1 = (pos[0], pos[1] - off + 2)          # Arriba
        p2 = (pos[0] - off + 2, pos[1] + off - 2) # Abajo Izq
        p3 = (pos[0] + off - 2, pos[1] + off - 2) # Abajo Der
        pygame.draw.polygon(surface, COLOR_CHEESE, [p1, p2, p3])
        
        # Agujeros (Detalles)
        hole_color = (200, 150, 0)
        pygame.draw.circle(surface, hole_color, (int(pos[0]), int(pos[1] + 4)), 3)
        pygame.draw.circle(surface, hole_color, (int(pos[0] - 5), int(pos[1] + 8)), 2)

    def render_game(self, board, cat_pos, mouse_pos, turn, message="", game_over=False):
        self.screen.fill(COLOR_BG)
        
        # Dibujar Grid y Obstáculos
        for y in range(board.height):
            for x in range(board.width):
                rect = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1) # Borde grid
                
                if (x, y) in board.obstacles:
                    # Obstáculo estilo "Cyber Bloque"
                    pygame.draw.rect(self.screen, COLOR_OBSTACLE, rect)
                    pygame.draw.rect(self.screen, COLOR_OBSTACLE_BORDER, rect, 2)
                    # Detalle interno
                    pygame.draw.line(self.screen, COLOR_OBSTACLE_BORDER, (rect.left, rect.top), (rect.right, rect.bottom), 1)
                    
                elif (x, y) == board.cheese_pos:
                    # Queso Skin
                    center = (int(x*self.cell_size + self.cell_size//2), int(y*self.cell_size + self.cell_size//2))
                    self.draw_cheese_skin(self.screen, center, self.cell_size)

        # Actualizar posiciones visuales (interpolación lineal si animando)
        target_cat = self.grid_to_screen(cat_pos)
        target_mouse = self.grid_to_screen(mouse_pos)

        
        # Lógica simple de suavizado (Lerp)
        dt = 0.15 # Un poco más rápido para que se sienta responsive
        
        # Inicializar si es la primera vez (para evitar lerp desde el origen)
        if self.vis_cat_pos == (-100, -100): self.vis_cat_pos = target_cat
        if self.vis_mouse_pos == (-100, -100): self.vis_mouse_pos = target_mouse

        cx, cy = self.vis_cat_pos
        tx, ty = target_cat
        self.vis_cat_pos = (cx + (tx-cx)*dt, cy + (ty-cy)*dt)
        
        mx, my = self.vis_mouse_pos
        tx, ty = target_mouse
        self.vis_mouse_pos = (mx + (tx-mx)*dt, my + (ty-my)*dt)

        # Si la distancia es muy pequeña, ajustar a posición final
        if abs(cx - target_cat[0]) < 1 and abs(cy - target_cat[1]) < 1: self.vis_cat_pos = target_cat
        if abs(mx - target_mouse[0]) < 1 and abs(my - target_mouse[1]) < 1: self.vis_mouse_pos = target_mouse

        # Dibujar Agentes (SKINS)
        cat_center = (int(self.vis_cat_pos[0] + self.cell_size/2), int(self.vis_cat_pos[1] + self.cell_size/2))
        mouse_center = (int(self.vis_mouse_pos[0] + self.cell_size/2), int(self.vis_mouse_pos[1] + self.cell_size/2))

        # Llamar a funciones de Skin
        self.draw_cat_skin(self.screen, cat_center, self.cell_size)
        self.draw_mouse_skin(self.screen, mouse_center, self.cell_size)
        
        # UI Panel Inferior
        ui_rect = pygame.Rect(0, self.height * self.cell_size, self.width * self.cell_size, 100)
        pygame.draw.rect(self.screen, (20, 20, 30), ui_rect)
        pygame.draw.line(self.screen, COLOR_GRID, (0, ui_rect.top), (ui_rect.width, ui_rect.top), 2)
        
        info_text = f"Turno: {turn} | {message}"
        text_surf = self.font.render(info_text, True, COLOR_TEXT)
        self.screen.blit(text_surf, (20, ui_rect.top + 20))
        
        controls = "Controles: WASD (Mover) | ESPACIO (Esperar)"
        controls_surf = self.font.render(controls, True, (150, 150, 150))
        self.screen.blit(controls_surf, (20, ui_rect.top + 50))

        pygame.display.flip()

    def show_menu(self):
        running = True
        options = ["IA vs IA", "Jugar como Raton", "Jugar como Gato", "Salir"]
        selected = 0
        
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(COLOR_BG)
            
            # Título Neon animado color
            hue = (time.time() * 50) % 360
            title_color = pygame.Color(0)
            title_color.hsla = (hue, 100, 50, 100)
            
            title = self.title_font.render("NEON CHASE: MINIMAX", True, title_color)
            # Efecto sombra
            title_shadow = self.title_font.render("NEON CHASE: MINIMAX", True, (0, 50, 50))
            self.screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 4, 100 + 4))
            self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            
            # Opciones
            for i, opt in enumerate(options):
                color = COLOR_CAT if i == selected else (100, 100, 100)
                text = self.font.render(opt, True, color)
                rect = text.get_rect(center=(SCREEN_WIDTH//2, 250 + i * 50))
                self.screen.blit(text, rect)
                
                if i == selected:
                    # Flechas selectoras
                    arrow = self.font.render(">", True, COLOR_CAT)
                    self.screen.blit(arrow, (rect.left - 30, rect.top))
            
            # Dibujar preview de skins en el menú
            self.draw_cat_skin(self.screen, (100, 500), 60)
            self.draw_mouse_skin(self.screen, (700, 500), 60)
            
            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: selected = (selected - 1) % len(options)
                    elif event.key == pygame.K_DOWN: selected = (selected + 1) % len(options)
                    elif event.key == pygame.K_RETURN:
                        return selected

# --- JUEGO PRINCIPAL ---

class Game:
    def __init__(self):
        pygame.init()
        self.width = 20
        self.height = 15
        self.cell_size = 40
        
        self.renderer = Renderer(self.width, self.height, self.cell_size)
        self.board = None
        self.cat_agent = None
        self.mouse_agent = None
        
        self.cat_pos = None
        self.mouse_pos = None
        self.turn = 1
        self.turn_limit = 100

    def setup_game(self, mode):
        self.board = Board(self.width, self.height)
        if mode == 0: # IA vs IA
            self.cat_agent = SmartCat(depth=4)
            self.mouse_agent = SmartMouse(depth=4)
        elif mode == 1: # Human Mouse
            self.cat_agent = SmartCat(depth=4)
            self.mouse_agent = PygameHumanAgent("Tú (Ratón)", MOUSE)
        elif mode == 2: # Human Cat
            self.cat_agent = PygameHumanAgent("Tú (Gato)", CAT)
            self.mouse_agent = SmartMouse(depth=4)
        else:
            pygame.quit()
            sys.exit()

        self.cat_pos = self._get_random_start_pos()
        self.mouse_pos = self._get_random_start_pos(exclude=[self.cat_pos])
        
        # Init renderer positions
        self.renderer.vis_cat_pos = self.renderer.grid_to_screen(self.cat_pos)
        self.renderer.vis_mouse_pos = self.renderer.grid_to_screen(self.mouse_pos)
        
        self.turn = 1 # Reset turnos

    def _get_random_start_pos(self, exclude=None):
        if exclude is None: exclude = []
        while True:
            x = random.randint(0, self.board.width - 1)
            y = random.randint(0, self.board.height - 1)
            pos = (x, y)
            if self.board.is_valid(pos) and pos not in exclude and pos != self.board.cheese_pos:
                return pos

    def run(self):
        while True:
            choice = self.renderer.show_menu()
            if choice == 3: break
            
            self.setup_game(choice)
            self.game_loop()

    def game_loop(self):
        clock = pygame.time.Clock()
        running = True
        game_over = False
        winner = None
        
        # Control de turnos
        turn_state = 0 # 0: Mouse Start, 1: Mouse Moving, 2: Cat Start, 3: Cat Moving
        action_delay = 0 
        
        mouse_think_time = 0
        cat_think_time = 0

        while running:
            dt = clock.tick(FPS) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if game_over and event.type == pygame.KEYDOWN:
                    running = False # Salir al menú con cualquier tecla

            if not game_over:
                # Lógica de Turnos
                if turn_state == 0: # Turno Ratón (Pensar/Input)
                    if not isinstance(self.mouse_agent, PygameHumanAgent):
                         # Pequeño delay artificial para ver "pensar" a la IA
                         mouse_think_time += dt
                         if mouse_think_time < 0.2: 
                             self.renderer.render_game(self.board, self.cat_pos, self.mouse_pos, self.turn, "Ratón pensando...")
                             pygame.display.flip()
                             continue
                    
                    move = self.mouse_agent.get_move(self.board, self.mouse_pos, self.cat_pos, events)
                    if move:
                        self.mouse_pos = move
                        turn_state = 1
                        action_delay = 0.2 
                        mouse_think_time = 0

                elif turn_state == 1: # Ratón Post-Movimiento (Animación/Delay)
                    action_delay -= dt
                    if action_delay <= 0:
                        # Chequeos
                        if self.mouse_pos == self.board.cheese_pos:
                            winner = "Raton (Queso)"
                            game_over = True
                        elif self.mouse_pos == self.cat_pos:
                            winner = "Gato (Suicidio)"
                            game_over = True
                        else:
                            turn_state = 2 # Pase a gato

                elif turn_state == 2: # Turno Gato
                     if not isinstance(self.cat_agent, PygameHumanAgent):
                         cat_think_time += dt
                         if cat_think_time < 0.2:
                             self.renderer.render_game(self.board, self.cat_pos, self.mouse_pos, self.turn, "Gato pensando...")
                             pygame.display.flip()
                             continue

                     move = self.cat_agent.get_move(self.board, self.cat_pos, self.mouse_pos, events)
                     if move:
                        self.cat_pos = move
                        turn_state = 3
                        action_delay = 0.2
                        cat_think_time = 0

                elif turn_state == 3: # Gato Post-Movimiento
                    action_delay -= dt
                    if action_delay <= 0:
                        if self.cat_pos == self.mouse_pos:
                            winner = "Gato (Atrapado)"
                            game_over = True
                        else:
                            self.turn += 1
                            if self.turn > self.turn_limit:
                                winner = "Raton (Tiempo)"
                                game_over = True
                            turn_state = 0 # Volver a ratón

            # Renderizar
            msg = f"Ganador: {winner} - Presiona Tecla" if game_over else f"Turno de: {'Gato' if turn_state >= 2 else 'Ratón'}"
            self.renderer.render_game(self.board, self.cat_pos, self.mouse_pos, self.turn, msg, game_over)

if __name__ == "__main__":
    game = Game()
    game.run()

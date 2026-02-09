# 🎓 Guía de Desarrollo: Neon Chase Minimax

¡Bienvenido, futuro desarrollador! 👋
Este documento es un recorrido guiado por el código fuente de **Neon Chase**. Nuestro objetivo es que entiendas no solo *qué* hace el código, sino *por qué* está hecho así.

---

## 🏗️ Arquitectura del Proyecto
El juego sigue un patrón de diseño simplificado llamado **MVC (Modelo-Vista-Controlador)**, aunque adaptado a juegos.

1.  **Modelo (Lógica)**: Reglas, tablero, posiciones. No sabe nada de gráficos.
    *   Clases: `Board`, `Agent`, `SmartCat`, `SmartMouse`.
2.  **Vista (Renderer)**: Dibuja cosas en la pantalla. No decide reglas.
    *   Clase: `Renderer`.
3.  **Controlador (Game)**: Une todo. Recibe teclas y actualiza el juego.
    *   Clase: `Game`.

---

## 🧠 1. El Cerebro: Algoritmo Minimax
La "Magia" de la IA está en la función `minimax` y `evaluate_state`.

### ¿Cómo piensa el Gato/Ratón?
Imagina un árbol de decisiones:
*   "Si me muevo arriba, el gato podría moverse abajo o izquierda..."
*   "Si el gato mueve abajo, yo pierdo."
*   "Si el gato mueve izquierda, yo sigo vivo."

El **Minimax** explora estas ramas hasta cierta profundidad (`depth=4` pasos en el futuro).

```python
def minimax(..., is_maximizing, ...):
    # Condición de Parada (Caso Base)
    if depth == 0 or game_over:
        return puntuacion_tablero
    
    if is_maximizing (Turno del Ratón):
        # Busca la jugada con MAYOR puntaje
        max_eval = -infinito
        for movimiento in movimientos_posibles:
            eval = minimax(..., depth-1, False, ...) # Llama recursivamente
            max_eval = max(max_eval, eval)
        return max_eval

    else (Turno del Gato):
        # Busca la jugada con MENOR puntaje (para perjudicar al ratón)
        min_eval = +infinito
        # ... lógica similar pero buscando min ...
        return min_eval
```

### La Poda Alpha-Beta
Es una optimización. Si encontramos una jugada "muy mala" en una rama, dejamos de investigar esa rama inmediatamente. Ahorra tiempo de cómputo.

---

## 🧩 2. El Mundo: Generación de Laberintos
Usamos el algoritmo **Recursive Backtracker** en la clase `Board`.

1.  Empezamos con un tablero lleno de muros (`#`).
2.  Elegimos una celda y "cavamos" caminos.
3.  Nos movemos 2 pasos en una dirección aleatoria y rompemos el muro intermedio.
4.  Si nos quedamos atascados, **retrocedemos** (backtrack) hasta encontrar un camino nuevo.

Esto garantiza un laberinto **perfecto** (todo está conectado, sin áreas inalcanzables).

---

## 🎨 3. Los Gráficos: Pygame y Skins
La clase `Renderer` maneja la ventana.

### Skins Procedurales
En lugar de cargar imágenes `.png` (que podrían perderse), dibujamos los personajes usando código geométrico.

**Ejemplo: Dibujar al Gato**
```python
def draw_cat_skin(self, surface, pos, size):
    # Dibujar círculo base (cabeza)
    pygame.draw.circle(...)
    
    # Dibujar orejas (Triángulos/Polígonos)
    left_ear = [(x1,y1), (x2,y2), (x3,y3)]
    pygame.draw.polygon(surface, color, left_ear)
    
    # Dibujar ojos (Líneas)
    pygame.draw.line(...)
```
¡Así es como logramos que el gato se vea "malo" y el ratón "tierno" solo con figuras básicas!

---

## 🔄 4. El Bucle de Juego (Game Loop)
Es el corazón de cualquier videojuego. Ocurre 60 veces por segundo (`FPS=60`).

1.  **Input**: ¿El usuario presionó una tecla? (`pygame.event.get()`)
2.  **Update**: 
    *   Si es turno de la IA, calcula su movimiento.
    *   Si hay animaciones, actualiza las posiciones `x, y` suavemente (interpolación).
3.  **Render**: Borra la pantalla, dibuja el tablero, dibuja los personajes en sus nuevas posiciones, muestra el resultado en pantalla.

---

## 💡 Retos para ti
¿Quieres mejorar el juego? Intenta esto:
1.  **Cambiar colores**: Busca `COLOR_GRID` o `COLOR_NEON` y pon tus favoritos.
2.  **Aumentar dificultad**: Cambia `depth=4` a `depth=6` en `setup_game`. ¡La IA será mas lista (y lenta)!
3.  **Más obstáculos**: Modifica `_generate_maze` para que rompa menos muros.

¡Felicidades por llegar hasta aquí! El código es tuyo para experimentar. 🚀

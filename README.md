# 🐱 NEON CHASE: Minimax Laberinto 🐭🧀

Bienvenido a la evolución Cyberpunk del clásico juego del Gato y el Ratón.

## 🌟 Novedades v2.0
-   **Laberinto Real**: Generación procedural (DFS) de laberintos complejos y conectados. ¡Ya no son solo bloques aleatorios!
-   **Interfaz Gráfica Neon**: Adiós a la consola aburrida. Hola a los gráficos vectoriales minimalistas.
-   **Animaciones Suaves**: Movimiento interpolado para una experiencia fluida.
-   **Efectos Visuales**: El queso pulsa con energía, los agentes brillan.
-   **Menú Principal**: Navegación intuitiva con teclado.
-   **Listo para Monetizar**: Estructura preparada para compilar a `.exe` y distribuir.

## 🚀 Cómo Jugar

### Opción Rápida (Launcher)
Doble clic en **`jugar.bat`** para lanzar el juego automáticamente.

### Opción Manual
```bash
python minimax_lab.py
```

### Controles
-   **Flechas / WASD**: Moverse en el menú y en el juego.
-   **Espacio**: Esperar un turno (útil para estrategias).
-   **Enter**: Seleccionar opción en el menú.
-   **Q, E, Z, C**: Movimiento diagonal (como en el teclado numérico).

## 🛠️ Cómo Crear Ejecutable (.exe)
Si quieres vender o compartir tu juego como un profesional:

1.  Ejecuta el archivo **`build.bat`**.
2.  Espera a que termine el proceso (instalará `pyinstaller` si es necesario).
3.  Busca tu ejecutable en la carpeta `dist/`.

## 🧠 Inteligencia Artificial
El núcleo sigue siendo el poderoso algoritmo **Minimax con Poda Alpha-Beta**, ahora visualizado en todo su esplendor.
-   **Profundidad**: 4 niveles de anticipación.
-   **Heurística**: Distancia Chebyshev ponderada (Seguridad vs Objetivo).

---
*Creado con Python y Pygame.*

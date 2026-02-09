@echo off
title Laberinto Minimax Launcher
echo ==========================================
echo    INICIANDO JUEGO LABERINTO MINIMAX
echo ==========================================
echo.

REM 1. Intentar con 'py' launcher (comun en Windows)
echo [1] Intentando con 'py'...
py "c:\Users\alan.hermosilla\Desktop\LABERINTO MINIMAX\minimax_lab.py"
if %errorlevel% EQU 0 goto end

REM 2. Intentar con 'python' en el PATH
echo [2] Intentando con 'python' del sistema...
python "c:\Users\alan.hermosilla\Desktop\LABERINTO MINIMAX\minimax_lab.py"
if %errorlevel% EQU 0 goto end

REM 3. Intentar con ruta absoluta especifica (Python 3.11 User Install)
echo [3] Intentando con ruta absoluta C:\Users\alan.hermosilla\AppData\Local\Programs\Python\Python311\python.exe...
"C:\Users\alan.hermosilla\AppData\Local\Programs\Python\Python311\python.exe" "c:\Users\alan.hermosilla\Desktop\LABERINTO MINIMAX\minimax_lab.py"
if %errorlevel% EQU 0 goto end

REM 4. Fallo total
echo.
echo [ERROR CRITICO] No se pudo encontrar Python.
echo Por favor, asegurate de que Python este instalado.
echo Intenta reinstalar desde python.org o la Microsoft Store.
echo.
pause
exit /b 1

:end
echo.
echo Juego terminado correctamente.
pause

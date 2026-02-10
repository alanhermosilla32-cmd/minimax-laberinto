@echo off
title Juego del Laberinto
chcp 65001 > nul
cls
echo Iniciando el juego...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] No se detecto Python instalado o no esta en el PATH.
    echo Por favor instala Python desde https://www.python.org/
    pause
    exit /b
)
python juego.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] El juego se cerro inesperadamente.
    echo Revisa el mensaje de error arriba.
)
pause

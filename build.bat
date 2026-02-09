@echo off
echo ==========================================
echo    CONSTRUCTOR DE EJECUTABLE (EXE)
echo ==========================================
echo.

echo [1] Verificando PyInstaller...
py -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller no encontrado. Instalando...
    py -m pip install pyinstaller
)

echo [2] Creando ejecutable...
echo Esto puede tardar unos minutos...
py -m PyInstaller --onefile --noconsole --name "NeonChase_Minimax" "c:\Users\alan.hermosilla\Desktop\LABERINTO MINIMAX\minimax_lab.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Fallo al crear el ejecutable.
    pause
    exit /b 1
)

echo.
echo [EXITO] Ejecutable creado en la carpeta 'dist'.
echo Puedes distribuir el archivo 'NeonChase_Minimax.exe' sin necesidad de Python.
echo.
pause

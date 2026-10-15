@echo off
TITLE Lunar Lander Challenge
COLOR 0A

echo ========================================================
echo         LUNAR LANDER CHALLENGE - HUMAN PLAYER MODE
echo ========================================================
echo.
echo Checking: Is Python installed?
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found!
    echo Please install it from python.org and make sure to check: "Add Python to PATH"
    pause
    exit
)

echo.
echo [1/2] Checking required packages...
echo (This may take a while only on the first run)
pip install gymnasium[box2d] pygame numpy >nul 2>&1

echo.
echo [2/2] Starting game... Good luck!
echo.
python lunar_lander.py

echo.
echo Press any key to exit...
pause

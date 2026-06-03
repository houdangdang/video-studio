@echo off
:: VideoForge — 双击启动（Windows）
cd /d "%~dp0"
echo Starting VideoForge server...
echo.
python server.py
if errorlevel 1 (
    echo.
    echo Python not found! Make sure you have Python 3 installed.
    echo Download: https://www.python.org/downloads/
    pause
)

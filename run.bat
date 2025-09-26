@echo off
title Brainfuck Translator
color 0A

:: Python check
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo Python not found. Please install Python 3.x.
    pause
    exit /b
)

:: Virtual environment setup (optional)
:: python -m venv venv
:: call venv\Scripts\activate

:: Install colorama if not present
pip show colorama >nul 2>&1
IF ERRORLEVEL 1 (
    echo Installing required module: colorama
    pip install colorama
)

:: Run Python script
python brainfucktranslator.py

pause

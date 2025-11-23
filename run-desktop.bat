@echo off
chcp 65001 >nul
title Guia de Alter - Desktop Application

echo.
echo ╔═══════════════════════════════════════════════╗
echo ║   🌴 GUIA DE ALTER - DESKTOP LAUNCHER         ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Verifica se o ambiente virtual existe
if not exist ".venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual não encontrado!
    echo 📦 Criando ambiente virtual...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Erro ao criar ambiente virtual
        pause
        exit /b 1
    )
)

REM Ativa o ambiente virtual
echo 🔧 Ativando ambiente virtual...
call .venv\Scripts\activate.bat

REM Instala/atualiza dependências
echo 📦 Instalando dependências...
pip install -r requirements.txt --quiet --disable-pip-version-check

if errorlevel 1 (
    echo ❌ Erro ao instalar dependências
    pause
    exit /b 1
)

REM Executa a aplicação desktop
echo.
echo 🚀 Iniciando aplicação desktop...
echo.
python run_desktop.py

REM Se houver erro
if errorlevel 1 (
    echo.
    echo ❌ A aplicação foi encerrada com erro
    pause
)

deactivate

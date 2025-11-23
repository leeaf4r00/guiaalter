@echo off
echo ========================================
echo   Guia de Alter - Servidor + Tunnel
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Instale Python em: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Verifica se cloudflared está instalado
cloudflared --version >nul 2>&1
if errorlevel 1 (
    echo AVISO: Cloudflared nao encontrado!
    echo.
    echo Instalando via winget...
    winget install --id Cloudflare.cloudflared -e --accept-source-agreements --accept-package-agreements
    
    REM Verifica novamente
    cloudflared --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ERRO: Falha na instalacao do cloudflared.
        echo Instale manualmente: https://github.com/cloudflare/cloudflared/releases
        pause
        exit /b 1
    )
)

echo [1/2] Iniciando servidor Flask...
start "Guia Alter Server" cmd /k "python run.py"

echo [2/2] Aguardando servidor iniciar...
timeout /t 5 /nobreak >nul

echo.
echo ========================================
echo   Cloudflare Tunnel Iniciando...
echo ========================================
echo.
echo IMPORTANTE: Copie a URL que aparecer abaixo!
echo Exemplo: https://abc-123-xyz.trycloudflare.com
echo.
echo Acesse no celular:
echo   [URL]/mobile-admin/login
echo.
echo Pressione Ctrl+C para parar o tunnel
echo ========================================
echo.

cloudflared tunnel --url http://localhost:5000

pause

@echo off
REM Script de inicio rápido para Docker (Windows)
REM Uso: start-docker.bat [dev|prod]

setlocal enabledelayedexpansion

set MODE=%1
if "%MODE%"=="" set MODE=prod

echo 🐳 Iniciando Registro Físico con Docker
echo =====================================

REM Crear directorio de datos si no existe
if not exist "data" mkdir data

if "%MODE%"=="dev" (
    echo 🔧 Modo: Desarrollo
    docker-compose --profile dev up -d
    echo ✅ Aplicación iniciada en modo desarrollo
    echo 🌐 URL: http://localhost:5001
) else if "%MODE%"=="prod" (
    echo 🚀 Modo: Producción
    docker-compose up -d
    echo ✅ Aplicación iniciada en modo producción
    echo 🌐 URL: http://localhost:5000
) else (
    echo ❌ Modo no válido. Usa: dev o prod
    exit /b 1
)

echo.
echo 📋 Comandos útiles:
echo   Ver logs: docker-compose logs -f
echo   Detener:  docker-compose down
echo   Estado:   docker-compose ps

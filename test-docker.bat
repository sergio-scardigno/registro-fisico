@echo off
REM Script para probar la aplicación Docker (Windows)
REM Uso: test-docker.bat

setlocal enabledelayedexpansion

echo 🐳 Probando aplicación Docker
echo ============================

REM Crear directorio de datos si no existe
echo 📁 Creando directorio de datos...
if not exist "data" mkdir data

REM Detener contenedores existentes
echo 🛑 Deteniendo contenedores existentes...
docker-compose down 2>nul

REM Construir y ejecutar
echo 🔨 Construyendo imagen...
docker-compose build

echo 🚀 Ejecutando aplicación...
docker-compose up -d

REM Esperar a que la aplicación esté lista
echo ⏳ Esperando a que la aplicación esté lista...
timeout /t 10 /nobreak >nul

REM Verificar que la aplicación esté funcionando
echo 🔍 Verificando estado de la aplicación...
curl -f http://localhost:5000/ >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: La aplicación no está respondiendo
    echo 📋 Logs del contenedor:
    docker-compose logs
    exit /b 1
) else (
    echo ✅ Aplicación funcionando correctamente
    echo 🌐 URL: http://localhost:5000
)

echo.
echo 🎉 ¡Prueba completada exitosamente!
echo 📋 Comandos útiles:
echo   Ver logs: docker-compose logs -f
echo   Detener:  docker-compose down
echo   Estado:   docker-compose ps

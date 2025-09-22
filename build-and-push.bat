@echo off
REM Script para construir y subir la imagen a Docker Hub (Windows)
REM Uso: build-and-push.bat [version] [username]

setlocal enabledelayedexpansion

REM Configuración
set IMAGE_NAME=registro-fisico
set DEFAULT_VERSION=latest
set DEFAULT_USERNAME=sergioscardigno82

REM Obtener parámetros
set VERSION=%1
if "%VERSION%"=="" set VERSION=%DEFAULT_VERSION%

set USERNAME=%2
if "%USERNAME%"=="" set USERNAME=%DEFAULT_USERNAME%

echo 🐳 Construyendo y subiendo imagen Docker
echo =======================================
echo Imagen: %USERNAME%/%IMAGE_NAME%:%VERSION%
echo.

REM Verificar que Docker esté ejecutándose
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Docker no está ejecutándose
    exit /b 1
)

REM Verificar login en Docker Hub
docker info | findstr "Username:" >nul
if errorlevel 1 (
    echo ⚠️  Verificando login en Docker Hub...
    docker info >nul 2>&1
    if errorlevel 1 (
        echo ❌ Error: Docker no está ejecutándose correctamente
        exit /b 1
    ) else (
        echo ✅ Docker está funcionando, continuando con el build...
    )
)

REM Construir la imagen
echo 🔨 Construyendo imagen...
docker build -t %USERNAME%/%IMAGE_NAME%:%VERSION% .

if errorlevel 1 (
    echo ❌ Error al construir la imagen
    exit /b 1
) else (
    echo ✅ Imagen construida exitosamente
)

REM Crear tag latest si no es la versión por defecto
if not "%VERSION%"=="latest" (
    echo 🏷️  Creando tag latest...
    docker tag %USERNAME%/%IMAGE_NAME%:%VERSION% %USERNAME%/%IMAGE_NAME%:latest
)

REM Subir la imagen
echo 📤 Subiendo imagen a Docker Hub...
docker push %USERNAME%/%IMAGE_NAME%:%VERSION%

if errorlevel 1 (
    echo ❌ Error al subir la imagen
    exit /b 1
) else (
    echo ✅ Imagen subida exitosamente
)

REM Subir tag latest si aplica
if not "%VERSION%"=="latest" (
    echo 📤 Subiendo tag latest...
    docker push %USERNAME%/%IMAGE_NAME%:latest
)

echo.
echo 🎉 ¡Proceso completado exitosamente!
echo Imagen disponible en: https://hub.docker.com/r/%USERNAME%/%IMAGE_NAME%
echo.
echo Para usar la imagen:
echo docker run -p 5000:5000 -v %cd%\data:/app/instance %USERNAME%/%IMAGE_NAME%:%VERSION%

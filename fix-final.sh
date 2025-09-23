#!/bin/bash

# Script definitivo para solucionar el problema
echo "🔧 Solución definitiva para el problema de permisos..."

# Detener contenedores
echo "🛑 Deteniendo contenedores..."
docker compose down

# Limpiar completamente
echo "🧹 Limpiando sistema Docker..."
docker system prune -af
docker volume prune -f

# Crear directorio de datos
echo "📁 Creando directorio de datos..."
mkdir -p data
chmod 755 data

# Reconstruir imagen desde cero
echo "🔨 Reconstruyendo imagen desde cero..."
docker compose build --no-cache --pull

# Ejecutar
echo "🚀 Ejecutando aplicación..."
docker compose up -d

# Esperar
echo "⏳ Esperando a que la aplicación esté lista..."
sleep 30

# Verificar
echo "📋 Estado de contenedores:"
docker ps

echo "📋 Logs:"
docker logs registro-fisico-app --tail 25

# Verificar conectividad
echo "🌐 Verificando conectividad..."
if curl -f http://localhost:5000/ >/dev/null 2>&1; then
    echo "✅ ¡Aplicación funcionando correctamente!"
    echo "🌐 URL: http://localhost:5000"
else
    echo "❌ Error: La aplicación no está respondiendo"
    echo "📋 Logs completos:"
    docker logs registro-fisico-app
fi

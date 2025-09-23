#!/bin/bash

# Script de solución rápida para permisos
echo "🔧 Solucionando problema de permisos..."

# Detener contenedores
docker compose down

# Limpiar
docker system prune -f

# Crear directorio de datos
mkdir -p data
chmod 755 data

# Reconstruir imagen
docker compose build --no-cache

# Ejecutar
docker compose up -d

# Esperar
sleep 15

# Verificar
echo "📋 Estado de contenedores:"
docker ps

echo "📋 Logs:"
docker logs registro-fisico-app --tail 10

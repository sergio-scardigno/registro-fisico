#!/bin/bash

# Script para solucionar problemas de Docker en Linux
# Uso: ./fix-linux-docker.sh

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Solucionando problemas de Docker en Linux${NC}"
echo -e "${BLUE}===========================================${NC}"

# Detener contenedores existentes
echo -e "${YELLOW}🛑 Deteniendo contenedores existentes...${NC}"
sudo docker compose down 2>/dev/null || true

# Crear directorio de datos con permisos correctos
echo -e "${YELLOW}📁 Creando directorio de datos...${NC}"
mkdir -p data
chmod 755 data

# Verificar permisos
echo -e "${YELLOW}🔍 Verificando permisos...${NC}"
ls -la data

# Limpiar imágenes y contenedores antiguos
echo -e "${YELLOW}🧹 Limpiando imágenes antiguas...${NC}"
sudo docker system prune -f

# Reconstruir la imagen
echo -e "${YELLOW}🔨 Reconstruyendo imagen...${NC}"
sudo docker compose build --no-cache

# Ejecutar la aplicación
echo -e "${YELLOW}🚀 Ejecutando aplicación...${NC}"
sudo docker compose up -d

# Esperar a que la aplicación esté lista
echo -e "${YELLOW}⏳ Esperando a que la aplicación esté lista...${NC}"
sleep 15

# Verificar estado
echo -e "${YELLOW}🔍 Verificando estado...${NC}"
sudo docker ps

# Verificar logs
echo -e "${YELLOW}📋 Últimos logs:${NC}"
sudo docker logs registro-fisico-app --tail 20

# Verificar si la aplicación está funcionando
echo -e "${YELLOW}🌐 Verificando conectividad...${NC}"
if curl -f http://localhost:5000/ >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Aplicación funcionando correctamente${NC}"
    echo -e "${BLUE}🌐 URL: http://localhost:5000${NC}"
else
    echo -e "${RED}❌ Error: La aplicación no está respondiendo${NC}"
    echo -e "${YELLOW}📋 Logs completos:${NC}"
    sudo docker logs registro-fisico-app
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 ¡Problema solucionado!${NC}"
echo -e "${BLUE}📋 Comandos útiles:${NC}"
echo -e "  Ver logs: ${YELLOW}sudo docker logs registro-fisico-app -f${NC}"
echo -e "  Detener:  ${YELLOW}sudo docker compose down${NC}"
echo -e "  Estado:   ${YELLOW}sudo docker ps${NC}"


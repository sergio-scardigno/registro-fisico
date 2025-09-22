#!/bin/bash

# Script para probar la aplicación Docker
# Uso: ./test-docker.sh

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Probando aplicación Docker${NC}"
echo -e "${BLUE}============================${NC}"

# Crear directorio de datos si no existe
echo -e "${YELLOW}📁 Creando directorio de datos...${NC}"
mkdir -p data

# Detener contenedores existentes
echo -e "${YELLOW}🛑 Deteniendo contenedores existentes...${NC}"
docker-compose down 2>/dev/null || true

# Construir y ejecutar
echo -e "${YELLOW}🔨 Construyendo imagen...${NC}"
docker-compose build

echo -e "${YELLOW}🚀 Ejecutando aplicación...${NC}"
docker-compose up -d

# Esperar a que la aplicación esté lista
echo -e "${YELLOW}⏳ Esperando a que la aplicación esté lista...${NC}"
sleep 10

# Verificar que la aplicación esté funcionando
echo -e "${YELLOW}🔍 Verificando estado de la aplicación...${NC}"
if curl -f http://localhost:5000/ >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Aplicación funcionando correctamente${NC}"
    echo -e "${BLUE}🌐 URL: http://localhost:5000${NC}"
else
    echo -e "${RED}❌ Error: La aplicación no está respondiendo${NC}"
    echo -e "${YELLOW}📋 Logs del contenedor:${NC}"
    docker-compose logs
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 ¡Prueba completada exitosamente!${NC}"
echo -e "${BLUE}📋 Comandos útiles:${NC}"
echo -e "  Ver logs: ${YELLOW}docker-compose logs -f${NC}"
echo -e "  Detener:  ${YELLOW}docker-compose down${NC}"
echo -e "  Estado:   ${YELLOW}docker-compose ps${NC}"

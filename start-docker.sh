#!/bin/bash

# Script de inicio rápido para Docker
# Uso: ./start-docker.sh [dev|prod]

set -e

MODE=${1:-prod}

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Iniciando Registro Físico con Docker${NC}"
echo -e "${BLUE}=====================================${NC}"

# Crear directorio de datos si no existe
mkdir -p data

if [ "$MODE" = "dev" ]; then
    echo -e "${YELLOW}🔧 Modo: Desarrollo${NC}"
    docker-compose --profile dev up -d
    echo -e "${GREEN}✅ Aplicación iniciada en modo desarrollo${NC}"
    echo -e "${BLUE}🌐 URL: http://localhost:5001${NC}"
elif [ "$MODE" = "prod" ]; then
    echo -e "${YELLOW}🚀 Modo: Producción${NC}"
    docker-compose up -d
    echo -e "${GREEN}✅ Aplicación iniciada en modo producción${NC}"
    echo -e "${BLUE}🌐 URL: http://localhost:5000${NC}"
else
    echo -e "❌ Modo no válido. Usa: dev o prod"
    exit 1
fi

echo ""
echo -e "${BLUE}📋 Comandos útiles:${NC}"
echo -e "  Ver logs: ${YELLOW}docker-compose logs -f${NC}"
echo -e "  Detener:  ${YELLOW}docker-compose down${NC}"
echo -e "  Estado:   ${YELLOW}docker-compose ps${NC}"

#!/bin/bash

# Script para construir y subir la imagen a Docker Hub
# Uso: ./build-and-push.sh [version] [username]

set -e

# Configuración
IMAGE_NAME="registro-fisico"
DEFAULT_VERSION="latest"
DEFAULT_USERNAME="tu-usuario-dockerhub"

# Obtener parámetros
VERSION=${1:-$DEFAULT_VERSION}
USERNAME=${2:-$DEFAULT_USERNAME}

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐳 Construyendo y subiendo imagen Docker${NC}"
echo -e "${BLUE}=======================================${NC}"
echo -e "Imagen: ${YELLOW}${USERNAME}/${IMAGE_NAME}:${VERSION}${NC}"
echo ""

# Verificar que Docker esté ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Docker no está ejecutándose${NC}"
    exit 1
fi

# Verificar login en Docker Hub
if ! docker info | grep -q "Username:"; then
    echo -e "${YELLOW}⚠️  No estás logueado en Docker Hub${NC}"
    echo -e "Ejecuta: ${BLUE}docker login${NC}"
    exit 1
fi

# Construir la imagen
echo -e "${BLUE}🔨 Construyendo imagen...${NC}"
docker build -t ${USERNAME}/${IMAGE_NAME}:${VERSION} .

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Imagen construida exitosamente${NC}"
else
    echo -e "${RED}❌ Error al construir la imagen${NC}"
    exit 1
fi

# Crear tag latest si no es la versión por defecto
if [ "$VERSION" != "latest" ]; then
    echo -e "${BLUE}🏷️  Creando tag latest...${NC}"
    docker tag ${USERNAME}/${IMAGE_NAME}:${VERSION} ${USERNAME}/${IMAGE_NAME}:latest
fi

# Subir la imagen
echo -e "${BLUE}📤 Subiendo imagen a Docker Hub...${NC}"
docker push ${USERNAME}/${IMAGE_NAME}:${VERSION}

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Imagen subida exitosamente${NC}"
else
    echo -e "${RED}❌ Error al subir la imagen${NC}"
    exit 1
fi

# Subir tag latest si aplica
if [ "$VERSION" != "latest" ]; then
    echo -e "${BLUE}📤 Subiendo tag latest...${NC}"
    docker push ${USERNAME}/${IMAGE_NAME}:latest
fi

echo ""
echo -e "${GREEN}🎉 ¡Proceso completado exitosamente!${NC}"
echo -e "Imagen disponible en: ${YELLOW}https://hub.docker.com/r/${USERNAME}/${IMAGE_NAME}${NC}"
echo ""
echo -e "${BLUE}Para usar la imagen:${NC}"
echo -e "docker run -p 5000:5000 -v \$(pwd)/data:/app/instance ${USERNAME}/${IMAGE_NAME}:${VERSION}"

#!/bin/bash

# Script de despliegue para servidor Linux/Ubuntu
# Uso: ./deploy-server.sh [comando]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_message() {
    echo -e "${2}${1}${NC}"
}

# Función para verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_message "❌ Docker no está instalado" $RED
        print_message "📦 Instalando Docker..." $YELLOW
        
        # Instalar Docker
        sudo apt update
        sudo apt install -y docker.io docker-compose-plugin
        sudo systemctl start docker
        sudo systemctl enable docker
        
        # Agregar usuario al grupo docker
        sudo usermod -aG docker $USER
        print_message "✅ Docker instalado. Reinicia la sesión y ejecuta 'newgrp docker'" $GREEN
        exit 1
    fi
    
    if ! docker compose version &> /dev/null; then
        print_message "❌ Docker Compose no está instalado" $RED
        print_message "📦 Instalando Docker Compose..." $YELLOW
        sudo apt install -y docker-compose-plugin
    fi
}

# Función para configurar directorios y permisos
setup_directories() {
    print_message "📁 Configurando directorios y permisos..." $YELLOW
    
    # Crear directorio de datos
    mkdir -p ./data
    
    # Configurar permisos
    sudo chown -R $USER:$USER ./data
    chmod -R 775 ./data
    
    # Crear directorio instance en el contenedor
    mkdir -p /app/instance
    
    print_message "✅ Directorios configurados correctamente" $GREEN
}

# Función para descargar la imagen
pull_image() {
    print_message "📥 Descargando imagen más reciente..." $YELLOW
    docker pull sergioscardigno82/registro-fisico:latest
    print_message "✅ Imagen descargada" $GREEN
}

# Función para iniciar la aplicación
start_app() {
    print_message "🚀 Iniciando aplicación..." $YELLOW
    
    # Detener contenedores existentes si los hay
    docker compose -f docker-compose.prod.yml down 2>/dev/null || true
    
    # Iniciar aplicación
    docker compose -f docker-compose.prod.yml up -d
    
    # Esperar a que la aplicación esté lista
    print_message "⏳ Esperando a que la aplicación esté lista..." $YELLOW
    sleep 10
    
    # Verificar que esté funcionando
    if curl -f http://localhost:5000 > /dev/null 2>&1; then
        print_message "✅ Aplicación iniciada correctamente en http://localhost:5000" $GREEN
    else
        print_message "⚠️ La aplicación puede estar iniciando. Verifica con: docker logs registro-fisico-app" $YELLOW
    fi
}

# Función para mostrar estado
show_status() {
    print_message "📊 Estado de la aplicación:" $BLUE
    echo ""
    docker ps | grep registro-fisico || print_message "❌ No hay contenedores en ejecución" $RED
    echo ""
    
    if docker ps | grep registro-fisico > /dev/null; then
        print_message "📋 Logs recientes:" $BLUE
        docker logs --tail 10 registro-fisico-app
    fi
}

# Función para detener la aplicación
stop_app() {
    print_message "🛑 Deteniendo aplicación..." $YELLOW
    docker compose -f docker-compose.prod.yml down
    print_message "✅ Aplicación detenida" $GREEN
}

# Función para reiniciar la aplicación
restart_app() {
    print_message "🔄 Reiniciando aplicación..." $YELLOW
    docker compose -f docker-compose.prod.yml restart
    print_message "✅ Aplicación reiniciada" $GREEN
}

# Función para actualizar la aplicación
update_app() {
    print_message "🔄 Actualizando aplicación..." $YELLOW
    pull_image
    docker compose -f docker-compose.prod.yml down
    docker compose -f docker-compose.prod.yml up -d
    print_message "✅ Aplicación actualizada" $GREEN
}

# Función para respaldar datos
backup_data() {
    print_message "💾 Creando respaldo de datos..." $YELLOW
    BACKUP_FILE="backup-$(date +%Y%m%d_%H%M%S).tar.gz"
    tar -czf "$BACKUP_FILE" ./data/
    print_message "✅ Respaldo creado: $BACKUP_FILE" $GREEN
}

# Función para mostrar ayuda
show_help() {
    print_message "🐳 Script de Despliegue - Registro Físico" $BLUE
    print_message "=========================================" $BLUE
    echo ""
    print_message "📖 Comandos disponibles:" $YELLOW
    echo ""
    print_message "  install    - Instalar Docker y configurar entorno" $GREEN
    print_message "  setup      - Configurar directorios y permisos" $GREEN
    print_message "  start      - Iniciar la aplicación" $GREEN
    print_message "  stop       - Detener la aplicación" $GREEN
    print_message "  restart    - Reiniciar la aplicación" $GREEN
    print_message "  status     - Ver estado de la aplicación" $GREEN
    print_message "  update     - Actualizar a la última versión" $GREEN
    print_message "  backup     - Crear respaldo de datos" $GREEN
    print_message "  logs       - Ver logs en tiempo real" $GREEN
    print_message "  help       - Mostrar esta ayuda" $GREEN
    echo ""
    print_message "📝 Ejemplos:" $BLUE
    print_message "  ./deploy-server.sh install" $GREEN
    print_message "  ./deploy-server.sh start" $GREEN
    print_message "  ./deploy-server.sh status" $GREEN
}

# Función para ver logs
show_logs() {
    print_message "📋 Mostrando logs en tiempo real (Ctrl+C para salir)..." $YELLOW
    docker compose -f docker-compose.prod.yml logs -f
}

# Función principal
main() {
    case "${1:-help}" in
        "install")
            check_docker
            setup_directories
            ;;
        "setup")
            setup_directories
            ;;
        "start")
            check_docker
            setup_directories
            pull_image
            start_app
            ;;
        "stop")
            stop_app
            ;;
        "restart")
            restart_app
            ;;
        "status")
            show_status
            ;;
        "update")
            update_app
            ;;
        "backup")
            backup_data
            ;;
        "logs")
            show_logs
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Ejecutar función principal
main "$@"

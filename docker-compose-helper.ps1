# Script helper para Docker Compose
# Uso: .\docker-compose-helper.ps1 [comando] [ambiente]

param(
    [string]$comando = "help",
    [string]$ambiente = "prod"
)

Write-Host "🐳 Docker Compose Helper - Registro Físico" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

switch ($comando.ToLower()) {
    "start" {
        if ($ambiente -eq "dev") {
            Write-Host "🚀 Iniciando en modo DESARROLLO..." -ForegroundColor Yellow
            docker compose -f docker-compose.dev.yml up -d
            Write-Host "✅ Aplicación iniciada en: http://localhost:5001" -ForegroundColor Green
        } else {
            Write-Host "🚀 Iniciando en modo PRODUCCIÓN..." -ForegroundColor Yellow
            docker compose -f docker-compose.prod.yml up -d
            Write-Host "✅ Aplicación iniciada en: http://localhost:5000" -ForegroundColor Green
        }
    }
    
    "stop" {
        if ($ambiente -eq "dev") {
            Write-Host "🛑 Deteniendo modo DESARROLLO..." -ForegroundColor Yellow
            docker compose -f docker-compose.dev.yml down
        } else {
            Write-Host "🛑 Deteniendo modo PRODUCCIÓN..." -ForegroundColor Yellow
            docker compose -f docker-compose.prod.yml down
        }
        Write-Host "✅ Aplicación detenida" -ForegroundColor Green
    }
    
    "restart" {
        if ($ambiente -eq "dev") {
            Write-Host "🔄 Reiniciando modo DESARROLLO..." -ForegroundColor Yellow
            docker compose -f docker-compose.dev.yml restart
            Write-Host "✅ Aplicación reiniciada en: http://localhost:5001" -ForegroundColor Green
        } else {
            Write-Host "🔄 Reiniciando modo PRODUCCIÓN..." -ForegroundColor Yellow
            docker compose -f docker-compose.prod.yml restart
            Write-Host "✅ Aplicación reiniciada en: http://localhost:5000" -ForegroundColor Green
        }
    }
    
    "logs" {
        if ($ambiente -eq "dev") {
            Write-Host "📋 Mostrando logs de DESARROLLO..." -ForegroundColor Yellow
            docker compose -f docker-compose.dev.yml logs -f
        } else {
            Write-Host "📋 Mostrando logs de PRODUCCIÓN..." -ForegroundColor Yellow
            docker compose -f docker-compose.prod.yml logs -f
        }
    }
    
    "status" {
        Write-Host "📊 Estado de contenedores:" -ForegroundColor Yellow
        docker ps | findstr registro-fisico
    }
    
    "pull" {
        Write-Host "📥 Descargando última imagen..." -ForegroundColor Yellow
        docker pull sergioscardigno82/registro-fisico:latest
        Write-Host "✅ Imagen actualizada" -ForegroundColor Green
    }
    
    "clean" {
        Write-Host "🧹 Limpiando contenedores y volúmenes..." -ForegroundColor Yellow
        docker-compose -f docker-compose.prod.yml down -v
        docker-compose -f docker-compose.dev.yml down -v
        docker system prune -f
        Write-Host "✅ Limpieza completada" -ForegroundColor Green
    }
    
    "help" {
        Write-Host "📖 Comandos disponibles:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  start [prod|dev]    - Iniciar la aplicación" -ForegroundColor White
        Write-Host "  stop [prod|dev]     - Detener la aplicación" -ForegroundColor White
        Write-Host "  restart [prod|dev]  - Reiniciar la aplicación" -ForegroundColor White
        Write-Host "  logs [prod|dev]     - Ver logs en tiempo real" -ForegroundColor White
        Write-Host "  status              - Ver estado de contenedores" -ForegroundColor White
        Write-Host "  pull                - Actualizar imagen" -ForegroundColor White
        Write-Host "  clean               - Limpiar contenedores y volúmenes" -ForegroundColor White
        Write-Host "  help                - Mostrar esta ayuda" -ForegroundColor White
        Write-Host ""
        Write-Host "📝 Ejemplos:" -ForegroundColor Cyan
        Write-Host "  .\docker-compose-helper.ps1 start prod" -ForegroundColor Gray
        Write-Host "  .\docker-compose-helper.ps1 start dev" -ForegroundColor Gray
        Write-Host "  .\docker-compose-helper.ps1 logs prod" -ForegroundColor Gray
        Write-Host "  .\docker-compose-helper.ps1 status" -ForegroundColor Gray
    }
    
    default {
        Write-Host "❌ Comando no reconocido: $comando" -ForegroundColor Red
        Write-Host "💡 Usa 'help' para ver comandos disponibles" -ForegroundColor Yellow
    }
}

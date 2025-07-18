#!/bin/bash

# Script de lanzamiento para FastAPI SOAP Service

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Iniciando FastAPI SOAP Service${NC}"

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ No se encontró el entorno virtual. Créalo primero con: python -m venv venv${NC}"
    exit 1
fi

# Activar el entorno virtual
echo -e "${YELLOW}📦 Activando entorno virtual...${NC}"
source venv/bin/activate

# Verificar si las dependencias están instaladas
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}📥 Instalando dependencias...${NC}"
    pip install -r requirements.txt
fi

# Crear directorio de logs si no existe
mkdir -p logs

# Verificar si existe archivo .env
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No se encontró archivo .env. Copiando desde env.example...${NC}"
    cp env.example .env
fi

# Lanzar la aplicación
echo -e "${GREEN}🎯 Iniciando servidor en http://localhost:8000${NC}"
echo -e "${GREEN}📚 Documentación disponible en: http://localhost:8000/docs${NC}"
echo -e "${GREEN}❤️  Health check: http://localhost:8000/api/v1/health${NC}"
echo ""

# Lanzar con uvicorn en modo desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 
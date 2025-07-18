"""
Aplicación principal FastAPI
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger

from app.config.settings import settings
from app.config.logging import setup_logging
from app.middleware.error_handler import ErrorHandlerMiddleware
from app.api.v1 import health


# Configurar logging
setup_logging()

# Crear directorio de logs si no existe
os.makedirs("logs", exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestión del ciclo de vida de la aplicación
    """
    # Startup
    logger.info(f"Iniciando {settings.app_name} v{settings.app_version}")
    logger.info(f"Modo debug: {settings.debug}")
    logger.info(f"Servidor configurado en {settings.host}:{settings.port}")
    
    yield
    
    # Shutdown
    logger.info(f"Cerrando {settings.app_name}")


# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    API REST que sirve como capa intermedia para servicios SOAP.
    
    Esta API proporciona endpoints REST que facilitan la integración
    con servicios SOAP existentes, ofreciendo una interfaz moderna
    y fácil de usar.
    
    ## Características
    
    - Endpoints REST para servicios SOAP
    - Documentación automática con OpenAPI
    - Manejo de errores uniforme
    - Logging estructurado
    - Configuración mediante variables de entorno
    - Preparado para contenedores Docker
    """,
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

# Agregar middleware de manejo de errores
app.add_middleware(ErrorHandlerMiddleware)

# Incluir routers
app.include_router(health.router, prefix="/api/v1")

# Importar y agregar router de identificación
from app.api.v1 import identificacion
app.include_router(identificacion.router, prefix="/api/v1")

# Importar y agregar router de registro
from app.api.v1 import registro
app.include_router(registro.router, prefix="/api/v1")

# Importar y agregar router de consulta registro civil
from app.api.v1 import consulta_rc
app.include_router(consulta_rc.router, prefix="/api/v1")


# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requests"""
    start_time = time.time()
    
    # Log del request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Procesar el request
    response = await call_next(request)
    
    # Log del response
    process_time = time.time() - start_time
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"Status: {response.status_code} "
        f"Time: {process_time:.4f}s"
    )
    
    return response


# Endpoint raíz
@app.get(
    "/",
    summary="Información de la API",
    description="Endpoint raíz que proporciona información básica de la API"
)
async def root():
    """Endpoint raíz"""
    return {
        "message": f"Bienvenido a {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json",
        "health": "/api/v1/health"
    }


# Endpoint de información de la API
@app.get(
    "/info",
    summary="Información detallada de la API",
    description="Proporciona información detallada sobre la configuración de la API"
)
async def info():
    """Información detallada de la API"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "debug": settings.debug,
        "environment": os.getenv("ENVIRONMENT", "development"),
        "python_version": os.sys.version,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "openapi_url": "/openapi.json"
    }


# Importar time para el middleware
import time

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=True
    ) 
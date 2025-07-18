"""
Endpoints de salud de la aplicación
"""
from datetime import datetime
from fastapi import APIRouter, status
from loguru import logger
from app.models.responses import HealthResponse
from app.config.settings import settings
import time


router = APIRouter(
    prefix="/health",
    tags=["Health"],
    responses={
        status.HTTP_200_OK: {"description": "Servicio funcionando correctamente"},
        status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Servicio no disponible"}
    }
)

# Variable para almacenar el tiempo de inicio
start_time = time.time()


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Verificar estado de la aplicación",
    description="Endpoint para verificar que la aplicación está funcionando correctamente"
)
async def health_check():
    """
    Endpoint de verificación de salud.
    
    Retorna:
        - Status: ok si la aplicación está funcionando
        - Timestamp: momento de la verificación
        - Version: versión de la aplicación
        - Uptime: tiempo que lleva funcionando la aplicación
    """
    try:
        # Calcular uptime
        uptime_seconds = time.time() - start_time
        uptime_str = str(datetime.fromtimestamp(uptime_seconds) - datetime.fromtimestamp(0))
        
        logger.info("Health check requested")
        
        return HealthResponse(
            status="ok",
            timestamp=datetime.now(),
            version=settings.app_version,
            uptime=uptime_str
        )
        
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        raise


@router.get(
    "/ready",
    summary="Verificar si la aplicación está lista",
    description="Endpoint para verificar que la aplicación está lista para recibir tráfico"
)
async def readiness_check():
    """
    Endpoint de verificación de preparación.
    
    Verifica que todos los servicios dependientes estén disponibles.
    """
    try:
        # Aquí puedes agregar verificaciones adicionales:
        # - Conexión a base de datos
        # - Servicios externos
        # - Etc.
        
        logger.info("Readiness check requested")
        
        return {
            "status": "ready",
            "timestamp": datetime.now(),
            "checks": {
                "database": "ok",  # Placeholder para futuras verificaciones
                "soap_services": "ok",  # Placeholder para futuras verificaciones
                "external_apis": "ok"  # Placeholder para futuras verificaciones
            }
        }
        
    except Exception as e:
        logger.error(f"Error en readiness check: {str(e)}")
        raise


@router.get(
    "/live",
    summary="Verificar si la aplicación está viva",
    description="Endpoint simple para verificar que la aplicación responde"
)
async def liveness_check():
    """
    Endpoint de verificación de vida.
    
    Respuesta simple para verificar que la aplicación está respondiendo.
    """
    logger.info("Liveness check requested")
    
    return {
        "status": "alive",
        "timestamp": datetime.now()
    } 
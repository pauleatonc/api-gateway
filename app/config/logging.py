"""
Configuración de logging estructurado con loguru
"""
import sys
from loguru import logger
from .settings import settings


def setup_logging():
    """Configurar el sistema de logging"""
    
    # Remover el handler por defecto de loguru
    logger.remove()
    
    # Configurar handler para stdout
    logger.add(
        sys.stdout,
        format=settings.log_format,
        level=settings.log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # Configurar handler para archivos (opcional)
    logger.add(
        "logs/app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    # Configurar logging para uvicorn
    logger.add(
        "logs/access.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
        level="INFO",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        filter=lambda record: "access" in record["name"].lower(),
    )
    
    return logger


# Instancia global del logger
app_logger = setup_logging() 
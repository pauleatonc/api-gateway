"""
Configuración de logging estructurado con loguru
"""
import sys
import os
from pathlib import Path
from loguru import logger
from .settings import settings


def setup_logging():
    """Configurar el sistema de logging"""
    
    # Remover el handler por defecto de loguru
    logger.remove()
    
    # Configurar handler para stdout (siempre activo)
    logger.add(
        sys.stdout,
        format=settings.log_format,
        level=settings.log_level,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # Configurar handler para archivos (opcional, solo si el directorio existe y hay permisos)
    try:
        # Crear directorio de logs si no existe
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Verificar permisos de escritura
        test_file = log_dir / ".test_write"
        test_file.touch()
        test_file.unlink()
        
        # Si llegamos aquí, tenemos permisos, configurar logs en archivo
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
        
        logger.add(
            "logs/access.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
            level="INFO",
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            filter=lambda record: "access" in record["name"].lower(),
        )
        
        logger.info("Logs en archivo habilitados en directorio 'logs/'")
        
    except (PermissionError, OSError) as e:
        # Si no hay permisos o el directorio no se puede crear, solo usar stdout
        logger.warning(f"No se pueden crear logs en archivo: {e}. Usando solo stdout.")
    
    return logger


# Instancia global del logger
app_logger = setup_logging() 
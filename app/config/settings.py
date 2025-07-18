"""
Configuración de la aplicación usando pydantic-settings
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Configuración de la aplicación
    app_name: str = Field(default="FastAPI SOAP Service", description="Nombre de la aplicación")
    app_version: str = Field(default="1.0.0", description="Versión de la aplicación")
    debug: bool = Field(default=False, description="Modo debug")
    environment: str = Field(default="development", description="Entorno de ejecución")
    
    # Configuración del servidor
    host: str = Field(default="0.0.0.0", description="Host del servidor")
    port: int = Field(default=8000, description="Puerto del servidor")
    
    # Configuración de logging
    log_level: str = Field(default="INFO", description="Nivel de logging")
    log_format: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        description="Formato de logging"
    )
    
    # Configuración de CORS
    allow_origins: list[str] = Field(default=["*"], description="Orígenes permitidos para CORS")
    allow_methods: list[str] = Field(default=["*"], description="Métodos HTTP permitidos")
    allow_headers: list[str] = Field(default=["*"], description="Headers permitidos")
    
    # Configuración de base de datos (para uso futuro)
    database_url: Optional[str] = Field(default=None, description="URL de conexión a la base de datos")
    
    # Configuración para servicios SOAP
    soap_timeout: int = Field(default=30, description="Timeout para llamadas SOAP en segundos")
    soap_retry_attempts: int = Field(default=3, description="Número de intentos de reintento para SOAP")
    
    # Configuración específica para SENCE
    sence_wsdl_url: str = Field(
        default="https://wsdesa.sence.cl/WsComponentes/WsIdentificacion.asmx?wsdl",
        description="URL del WSDL de SENCE"
    )
    use_soap_mocks: bool = Field(default=True, description="Usar mocks en lugar del servicio SOAP real")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instancia global de configuración
settings = Settings() 
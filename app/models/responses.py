"""
Modelos de respuesta usando pydantic
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime


class HealthResponse(BaseModel):
    """Modelo de respuesta para el endpoint de salud"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "timestamp": "2024-01-01T12:00:00Z",
                "version": "1.0.0",
                "uptime": "0:05:30.123456"
            }
        }
    )
    
    status: str = Field(description="Estado de la aplicación")
    timestamp: datetime = Field(description="Timestamp de la respuesta")
    version: str = Field(description="Versión de la aplicación")
    uptime: Optional[str] = Field(default=None, description="Tiempo de funcionamiento")


class ErrorResponse(BaseModel):
    """Modelo de respuesta para errores"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "Bad Request",
                "message": "El parámetro 'id' es requerido",
                "code": "VALIDATION_ERROR",
                "details": {
                    "field": "id",
                    "value": None
                }
            }
        }
    )
    
    error: str = Field(description="Tipo de error")
    message: str = Field(description="Mensaje descriptivo del error")
    code: str = Field(description="Código de error")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Detalles adicionales del error")


class SuccessResponse(BaseModel):
    """Modelo de respuesta genérica exitosa"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Operación completada exitosamente",
                "data": {
                    "id": "123",
                    "status": "processed"
                }
            }
        }
    )
    
    success: bool = Field(default=True, description="Indica si la operación fue exitosa")
    message: str = Field(description="Mensaje descriptivo")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Datos de respuesta")


class PaginatedResponse(BaseModel):
    """Modelo de respuesta paginada"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {"id": "1", "name": "Item 1"},
                    {"id": "2", "name": "Item 2"}
                ],
                "total": 100,
                "page": 1,
                "size": 10,
                "pages": 10
            }
        }
    )
    
    items: List[Dict[str, Any]] = Field(description="Lista de elementos")
    total: int = Field(description="Total de elementos")
    page: int = Field(description="Página actual")
    size: int = Field(description="Tamaño de página")
    pages: int = Field(description="Total de páginas")


class SOAPServiceResponse(BaseModel):
    """Modelo de respuesta para servicios SOAP"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "service_name": "RegistroCivil",
                "operation": "consultarRUT",
                "success": True,
                "response_data": {
                    "rut": "12345678-9",
                    "nombre": "Juan Pérez",
                    "estado": "activo"
                },
                "error_message": None,
                "execution_time": 0.25
            }
        }
    )
    
    service_name: str = Field(description="Nombre del servicio SOAP")
    operation: str = Field(description="Operación ejecutada")
    success: bool = Field(description="Indica si la operación fue exitosa")
    response_data: Optional[Dict[str, Any]] = Field(default=None, description="Datos de respuesta del servicio")
    error_message: Optional[str] = Field(default=None, description="Mensaje de error si aplica")
    execution_time: Optional[float] = Field(default=None, description="Tiempo de ejecución en segundos") 
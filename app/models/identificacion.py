"""
Modelos Pydantic para el servicio de Identificación de SENCE
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Modelos para IniciarSesion
class IniciarSesionRequest(BaseModel):
    """Modelo para la petición de IniciarSesion"""
    usuario: str = Field(..., description="Usuario para iniciar sesión")
    clave: str = Field(..., description="Clave del usuario", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "usuario": "usuario_ejemplo",
                "clave": "clave_ejemplo"
            }
        }


class IniciarSesionResponse(BaseModel):
    """Modelo para la respuesta de IniciarSesion"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    token: Optional[str] = Field(None, description="Token de sesión generado")
    guid: Optional[str] = Field(None, description="GUID de sesión")
    mensaje: Optional[str] = Field(None, description="Mensaje de respuesta")
    codigo_error: Optional[str] = Field(None, description="Código de error si existe")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "token": "abc123token",
                "guid": "550e8400-e29b-41d4-a716-446655440000",
                "mensaje": "Sesión iniciada correctamente",
                "codigo_error": None
            }
        }


# Modelos para IniciarSesionPorGuid
class IniciarSesionPorGuidRequest(BaseModel):
    """Modelo para la petición de IniciarSesionPorGuid"""
    guid: str = Field(..., description="GUID de sesión", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "guid": "550e8400-e29b-41d4-a716-446655440000"
            }
        }


class IniciarSesionPorGuidResponse(BaseModel):
    """Modelo para la respuesta de IniciarSesionPorGuid"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    token: Optional[str] = Field(None, description="Token de sesión generado")
    mensaje: Optional[str] = Field(None, description="Mensaje de respuesta")
    codigo_error: Optional[str] = Field(None, description="Código de error si existe")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "token": "abc123token",
                "mensaje": "Sesión iniciada correctamente por GUID",
                "codigo_error": None
            }
        }


# Modelos para IniciarSesionToken
class IniciarSesionTokenRequest(BaseModel):
    """Modelo para la petición de IniciarSesionToken"""
    token: str = Field(..., description="Token de sesión", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "abc123token"
            }
        }


class IniciarSesionTokenResponse(BaseModel):
    """Modelo para la respuesta de IniciarSesionToken"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    usuario: Optional[str] = Field(None, description="Usuario asociado al token")
    mensaje: Optional[str] = Field(None, description="Mensaje de respuesta")
    codigo_error: Optional[str] = Field(None, description="Código de error si existe")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "usuario": "usuario_ejemplo",
                "mensaje": "Token válido",
                "codigo_error": None
            }
        }


# Modelos para ObtenerListadoURLporRut
class UrlSistema(BaseModel):
    """Modelo para un sistema/URL"""
    nombre: str = Field(..., description="Nombre del sistema")
    url: str = Field(..., description="URL del sistema")
    descripcion: Optional[str] = Field(None, description="Descripción del sistema")
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Sistema Ejemplo",
                "url": "https://ejemplo.sence.cl",
                "descripcion": "Sistema de ejemplo para pruebas"
            }
        }


class ObtenerListadoURLporRutResponse(BaseModel):
    """Modelo para la respuesta de ObtenerListadoURLporRut"""
    success: bool = Field(..., description="Indica si la operación fue exitosa")
    sistemas: List[UrlSistema] = Field(default_factory=list, description="Lista de sistemas disponibles")
    mensaje: Optional[str] = Field(None, description="Mensaje de respuesta")
    codigo_error: Optional[str] = Field(None, description="Código de error si existe")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "sistemas": [
                    {
                        "nombre": "Sistema Ejemplo",
                        "url": "https://ejemplo.sence.cl",
                        "descripcion": "Sistema de ejemplo para pruebas"
                    }
                ],
                "mensaje": "Listado obtenido correctamente",
                "codigo_error": None
            }
        }


# Modelo genérico para errores
class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    success: bool = Field(default=False, description="Indica que la operación falló")
    mensaje: str = Field(..., description="Mensaje de error")
    codigo_error: Optional[str] = Field(None, description="Código de error específico")
    detalle: Optional[str] = Field(None, description="Detalle adicional del error")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "mensaje": "Error al conectar con el servicio SOAP",
                "codigo_error": "SOAP_ERROR",
                "detalle": "Timeout al conectar con el servidor"
            }
        } 
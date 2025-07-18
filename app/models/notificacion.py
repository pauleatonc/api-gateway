"""
Modelos Pydantic para el servicio de Notificación de SENCE
"""
from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
import base64


# Enumeración del WSDL
class ETipoEstado(str, Enum):
    """Enumeración para eTipoEstado"""
    NULO = "Nulo"
    CORRECTO = "CORRECTO"
    INCORRECTO = "INCORRECTO"
    PROCESAR = "PROCESAR"
    ERROR = "ERROR"
    EXCEPCION = "EXCEPCION"


# Modelos de respuesta
class RespuestaProcesoBe(BaseModel):
    """Modelo para RespuestaProcesoBe"""
    estadoProceso: ETipoEstado = Field(..., description="Estado del proceso")
    respuestaProceso: Optional[str] = Field(None, description="Respuesta del proceso")


class RespuestaMailBe(BaseModel):
    """Modelo para RespuestaMailBe"""
    estado: Optional[RespuestaProcesoBe] = Field(None, description="Estado del proceso")
    mailsNoInsertados: Optional[List[str]] = Field(None, description="Lista de mails que no se pudieron insertar")


# Modelos de request para SMS
class EnviarSMSRequest(BaseModel):
    """Modelo para request de EnviarSMS"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    ambiente: Optional[str] = Field(None, description="Ambiente (desarrollo/producción)", example="desarrollo")
    celular: int = Field(..., description="Número de celular", example=987654321)
    mensaje: Optional[str] = Field(None, description="Mensaje SMS", example="Hola, este es un mensaje de prueba")

    @validator('celular')
    def validate_celular(cls, v):
        if not (100000000 <= v <= 999999999):
            raise ValueError('El número de celular debe tener 9 dígitos')
        return v


# Modelos de request para correos públicos
class EnviarCorreoPublicoRequest(BaseModel):
    """Modelo para request de EnviarCorreoPublico"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    ambiente: Optional[str] = Field(None, description="Ambiente", example="desarrollo")
    mail: Optional[str] = Field(None, description="Dirección de email", example="usuario@ejemplo.com")
    asunto: Optional[str] = Field(None, description="Asunto del correo", example="Notificación importante")
    mensaje: Optional[str] = Field(None, description="Mensaje del correo", example="Este es el contenido del correo")

    @validator('mail')
    def validate_mail(cls, v):
        if v and '@' not in v:
            raise ValueError('El email debe tener un formato válido')
        return v


class EnviarListaCorreoPublicoRequest(BaseModel):
    """Modelo para request de EnviarListaCorreoPublico"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    ambiente: Optional[str] = Field(None, description="Ambiente", example="desarrollo")
    lstMails: Optional[List[str]] = Field(None, description="Lista de emails", example=["usuario1@ejemplo.com", "usuario2@ejemplo.com"])
    asunto: Optional[str] = Field(None, description="Asunto del correo", example="Notificación masiva")
    mensaje: Optional[str] = Field(None, description="Mensaje del correo", example="Este es el contenido del correo masivo")

    @validator('lstMails')
    def validate_mails(cls, v):
        if v:
            for mail in v:
                if '@' not in mail:
                    raise ValueError(f'El email {mail} debe tener un formato válido')
        return v


class EnviarCorreoPublicoRmRequest(BaseModel):
    """Modelo para request de EnviarCorreoPublicoRm"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    ambiente: Optional[str] = Field(None, description="Ambiente", example="desarrollo")
    mail: Optional[str] = Field(None, description="Dirección de email", example="usuario@ejemplo.com")
    asunto: Optional[str] = Field(None, description="Asunto del correo", example="Notificación con respuesta")
    mensaje: Optional[str] = Field(None, description="Mensaje del correo", example="Este correo retorna estado")

    @validator('mail')
    def validate_mail(cls, v):
        if v and '@' not in v:
            raise ValueError('El email debe tener un formato válido')
        return v


# Modelos de respuesta genéricos
class EnvioExitosoResponse(BaseModel):
    """Modelo para respuestas exitosas de envío"""
    success: bool = Field(default=True, description="Indica si el envío fue exitoso")
    mensaje: str = Field(default="Envío realizado correctamente", description="Mensaje de confirmación")


class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    success: bool = Field(default=False, description="Indica si la operación falló")
    mensaje: str = Field(..., description="Mensaje de error")
    codigo_error: Optional[str] = Field(None, description="Código de error específico")
    detalle: Optional[str] = Field(None, description="Detalle adicional del error")

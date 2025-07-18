"""
Modelos Pydantic simplificados para el servicio de Registro de SENCE (WsRegistroCUS)
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# Enumeraciones
class TipoEstado(str, Enum):
    """Enumeración para eTipoEstado"""
    NULO = "NULO"
    CORRECTO = "CORRECTO"
    INCORRECTO = "INCORRECTO"
    PROCESAR = "PROCESAR"
    ERROR = "ERROR"
    EXCEPCION = "EXCEPCION"


class TipoEmpresa(str, Enum):
    """Enumeración para eTipoEmpresa"""
    EMPRESA = "EMPRESA"
    OTEC = "OTEC"
    OTIC = "OTIC"


# Modelos base para respuestas
class RespuestaProcesoBe(BaseModel):
    """Modelo para RespuestaProcesoBe"""
    estadoProceso: TipoEstado = Field(..., description="Estado del proceso")
    codigoProceso: int = Field(..., description="Código del proceso")
    respuestaProceso: Optional[str] = Field(None, description="Respuesta del proceso")
    
    class Config:
        json_schema_extra = {
            "example": {
                "estadoProceso": "CORRECTO",
                "codigoProceso": 200,
                "respuestaProceso": "Registro exitoso"
            }
        }


# Modelos para datos de personas (simplificados)
class DatosPersona(BaseModel):
    """Modelo para DatosPersona"""
    Rut: int = Field(..., description="RUT de la persona (sin dígito verificador)")
    Dv: Optional[str] = Field(None, description="Dígito verificador")
    ApellidoPaterno: Optional[str] = Field(None, description="Apellido paterno")
    ApellidoMaterno: Optional[str] = Field(None, description="Apellido materno")
    Nombres: Optional[str] = Field(None, description="Nombres")
    NroSerie: Optional[str] = Field(None, description="Número de serie")
    CodigoCelular: Optional[str] = Field(None, description="Código del celular")
    NumeroCelular: int = Field(..., description="Número de celular")
    Mail: Optional[str] = Field(None, description="Correo electrónico")
    FechaNacimiento: datetime = Field(..., description="Fecha de nacimiento")
    FechaDefuncion: Optional[datetime] = Field(None, description="Fecha de defunción")
    IdNacionalidad: int = Field(..., description="ID de nacionalidad")
    Comuna: int = Field(..., description="ID de comuna")
    Direccion: Optional[str] = Field(None, description="Dirección")
    NroDireccion: Optional[str] = Field(None, description="Número de dirección")
    IdSexo: int = Field(..., description="ID del sexo")


class DatosContacto(BaseModel):
    """Modelo para DatosContacto"""
    Direccion: Optional[str] = Field(None, description="Dirección")
    NroDireccion: Optional[str] = Field(None, description="Número de dirección")
    NroDepartamento: Optional[str] = Field(None, description="Número de departamento")
    IdComuna: int = Field(..., description="ID de comuna")
    Email: Optional[str] = Field(None, description="Correo electrónico")
    CodigoCelular: Optional[str] = Field(None, description="Código del celular")
    NumeroCelular: int = Field(..., description="Número de celular")
    CodigoTelefonoFijo: int = Field(..., description="Código del teléfono fijo")
    TelefonoFijo: int = Field(..., description="Número de teléfono fijo")


class DatosPersonaCrm(BaseModel):
    """Modelo para DatosPersonaCrm"""
    Rut: int = Field(..., description="RUT de la persona (sin dígito verificador)")
    Dv: Optional[str] = Field(None, description="Dígito verificador")
    Contacto: Optional[DatosContacto] = Field(None, description="Datos de contacto")


class DatosContactoSO(BaseModel):
    """Modelo para DatosContactoSO (SIAC-OIRS)"""
    Direccion: Optional[str] = Field(None, description="Dirección")
    NroDireccion: Optional[str] = Field(None, description="Número de dirección")
    NroDepartamento: Optional[str] = Field(None, description="Número de departamento")
    IdComuna: int = Field(..., description="ID de comuna")
    Email: Optional[str] = Field(None, description="Correo electrónico")
    CodigoCelular: Optional[str] = Field(None, description="Código del celular")
    NumeroCelular: Optional[str] = Field(None, description="Número de celular (string)")
    CodigoTelefonoFijo: Optional[str] = Field(None, description="Código del teléfono fijo (string)")
    TelefonoFijo: Optional[str] = Field(None, description="Número de teléfono fijo (string)")


class DatosPersonaSiacOirs(BaseModel):
    """Modelo para DatosPersonaSiacOirs"""
    Rut: int = Field(..., description="RUT de la persona (sin dígito verificador)")
    Dv: Optional[str] = Field(None, description="Dígito verificador")
    Contacto: Optional[DatosContactoSO] = Field(None, description="Datos de contacto SIAC-OIRS")


# Modelos para datos de empresas
class DatosEmpresa(BaseModel):
    """Modelo para DatosEmpresa"""
    RutEmpresa: int = Field(..., description="RUT de la empresa (sin dígito verificador)")
    DvEmpresa: Optional[str] = Field(None, description="Dígito verificador de la empresa")
    TipoEmpresa: int = Field(..., description="Tipo de empresa")
    IdComuna: int = Field(..., description="ID de comuna")
    DireccionCalle: Optional[str] = Field(None, description="Dirección - calle")
    DireccionNumero: Optional[str] = Field(None, description="Dirección - número")
    NumeroCelular: int = Field(..., description="Número de celular")
    CodigoCelular: Optional[str] = Field(None, description="Código del celular")
    MailEmpresa: Optional[str] = Field(None, description="Correo electrónico de la empresa")
    IdPreguntaSecreta: int = Field(..., description="ID de pregunta secreta")
    RespuestaSecreta: Optional[str] = Field(None, description="Respuesta secreta")
    RutRepresentante: int = Field(..., description="RUT del representante")
    DvRepresentante: Optional[str] = Field(None, description="Dígito verificador del representante")
    MailRepresentante: Optional[str] = Field(None, description="Correo del representante")
    NumeroCelularRepresentante: int = Field(..., description="Celular del representante")
    CodigoCelularRepresentante: Optional[str] = Field(None, description="Código celular del representante")
    Cus: Optional[str] = Field(None, description="Código CUS")


class DatosEmpresaRudo(BaseModel):
    """Modelo para DatosEmpresaRudo (ActualizarEmpresa)"""
    RutEmpresa: int = Field(..., description="RUT de la empresa (sin dígito verificador)")
    DvEmpresa: Optional[str] = Field(None, description="Dígito verificador de la empresa")
    TipoEmpresa: int = Field(..., description="Tipo de empresa")
    IdComuna: int = Field(..., description="ID de comuna")
    DireccionCalle: Optional[str] = Field(None, description="Dirección - calle")
    DireccionNumero: Optional[str] = Field(None, description="Dirección - número")
    Telefono: int = Field(..., description="Número de teléfono")
    MailEmpresa: Optional[str] = Field(None, description="Correo electrónico de la empresa")


# Modelos para Oracle (simplificados usando Dict)
class DatosEmpresaOracle(BaseModel):
    """Modelo simplificado para DatosEmpresaOracle"""
    PerJur: Optional[Dict[str, Any]] = Field(None, description="Datos empresa Oracle")
    PreguntaRespuesta: Optional[Dict[str, Any]] = Field(None, description="Pregunta respuesta")
    PerNat: Optional[Dict[str, Any]] = Field(None, description="Persona natural")
    AdhesionOracle: Optional[Dict[str, Any]] = Field(None, description="Adhesión Oracle")
    UsuarioOracle: Optional[Dict[str, Any]] = Field(None, description="Usuario Oracle")


# Modelos para requests
class RegistroPersonaRequest(BaseModel):
    """Modelo para request de RegistroPersona"""
    idSistema: int = Field(..., description="ID del sistema")
    datosPersona: DatosPersona = Field(..., description="Datos de la persona")


class RegistroPersonaCrmRequest(BaseModel):
    """Modelo para request de RegistroPersonaCrm"""
    idSistema: int = Field(..., description="ID del sistema")
    datosPersona: DatosPersonaCrm = Field(..., description="Datos de la persona CRM")


class RegistrarPersonaSiacOirsRequest(BaseModel):
    """Modelo para request de RegistrarPersonaSiacOirs"""
    idSistema: int = Field(..., description="ID del sistema")
    datosPersona: DatosPersonaSiacOirs = Field(..., description="Datos de la persona SIAC-OIRS")


class RegistroEmpresaRequest(BaseModel):
    """Modelo para request de RegistroEmpresa"""
    idSistema: int = Field(..., description="ID del sistema")
    datosEmpresa: DatosEmpresa = Field(..., description="Datos de la empresa")


class ActualizarEmpresaRequest(BaseModel):
    """Modelo para request de ActualizarEmpresa"""
    idSistema: int = Field(..., description="ID del sistema")
    datosEmpresa: DatosEmpresaRudo = Field(..., description="Datos de la empresa")


class ActualizarRazonSocialRequest(BaseModel):
    """Modelo para request de ActualizarRazonSocial"""
    idSistema: int = Field(..., description="ID del sistema")
    rutEmpresa: int = Field(..., description="RUT de la empresa")
    dvEmpresa: Optional[str] = Field(None, description="DV de la empresa")


class ActualizarRepLegalesRequest(BaseModel):
    """Modelo para request de ActualizarRepLegales"""
    idSistema: int = Field(..., description="ID del sistema")
    rutEmpresa: int = Field(..., description="RUT de la empresa")
    dvEmpresa: Optional[str] = Field(None, description="DV de la empresa")


class ActualizarTipoEntidadRequest(BaseModel):
    """Modelo para request de ActualizarTipoEntidad"""
    idSistema: int = Field(..., description="ID del sistema")
    rutEmpresa: int = Field(..., description="RUT de la empresa")
    dvEmpresa: Optional[str] = Field(None, description="DV de la empresa")
    tipoEntidad: TipoEmpresa = Field(..., description="Tipo de entidad")


class CambioCusEmpresaRequest(BaseModel):
    """Modelo para request de CambioCusEmpresa"""
    idSistema: int = Field(..., description="ID del sistema")
    rutEmpresa: int = Field(..., description="RUT de la empresa")
    dvRutEmpresa: Optional[str] = Field(None, description="DV de la empresa")
    cusActual: Optional[str] = Field(None, description="CUS actual")
    nuevaCus: Optional[str] = Field(None, description="Nueva CUS")


class RegistroEmpresaOracleRequest(BaseModel):
    """Modelo para request de RegistroEmpresaOracle"""
    idSistema: int = Field(..., description="ID del sistema")
    datosEmpresa: DatosEmpresaOracle = Field(..., description="Datos de la empresa Oracle")


# Modelo genérico para errores
class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    success: bool = Field(default=False, description="Indica que la operación falló")
    mensaje: str = Field(..., description="Mensaje de error")
    codigo_error: Optional[str] = Field(None, description="Código de error específico")
    detalle: Optional[str] = Field(None, description="Detalle adicional del error") 
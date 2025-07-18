"""
Modelos Pydantic simplificados para el servicio de Consulta Registro Civil de SENCE
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# Enumeraciones simplificadas
class TipoEstado(str, Enum):
    """Enumeración para eTipoEstado"""
    NULO = "NULO"
    CORRECTO = "CORRECTO"
    INCORRECTO = "INCORRECTO"
    PROCESAR = "PROCESAR"
    ERROR = "ERROR"
    EXCEPCION = "EXCEPCION"


class TipoDocumento(str, Enum):
    """Enumeración para eTipoDocumento"""
    C = "C"  # Cédula
    P = "P"  # Pasaporte
    S = "S"  # Salvoconducto
    T = "T"  # Título de viaje
    D = "D"  # Documento de viaje


# Modelos base
class RespuestaProcesoBe(BaseModel):
    """Modelo para RespuestaProcesoBe"""
    estadoProceso: TipoEstado = Field(..., description="Estado del proceso")
    respuestaProceso: Optional[str] = Field(None, description="Respuesta del proceso")
    codigoProceso: int = Field(..., description="Código del proceso")


# Modelos para ConsultaRun
class ConsultaRunBe(BaseModel):
    """Modelo para ConsultaRunBe"""
    rut: int = Field(..., description="RUT de la persona")
    dv: Optional[str] = Field(None, description="Dígito verificador")
    nombres: Optional[str] = Field(None, description="Nombres")
    apellidoPaterno: Optional[str] = Field(None, description="Apellido paterno")
    apellidoMaterno: Optional[str] = Field(None, description="Apellido materno")
    fechaNacimiento: Optional[datetime] = Field(None, description="Fecha de nacimiento")
    fechaDefuncion: Optional[datetime] = Field(None, description="Fecha de defunción")
    sexo: Optional[str] = Field(None, description="Sexo")
    nacionalidad: Optional[str] = Field(None, description="Nacionalidad")
    estadoCivil: Optional[str] = Field(None, description="Estado civil")
    cantidadHijos: int = Field(..., description="Cantidad de hijos")
    fechaNacTruncada: Optional[str] = Field(None, description="Fecha de nacimiento truncada")
    fechaDefTruncada: Optional[str] = Field(None, description="Fecha de defunción truncada")


class RespuestaConsultaRunBe(BaseModel):
    """Modelo para RespuestaConsultaRunBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[ConsultaRunBe] = Field(None, description="Datos de la consulta")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


# Modelos para ConsultaNroSerieNroDocumento (simplificados)
class DatosRespuestaNroSerieNroDocBe(BaseModel):
    """Modelo simplificado para DatosRespuestaNroSerieNroDocBe"""
    EstadoRespuesta: str = Field(..., description="Estado de la respuesta")
    Rut: int = Field(..., description="RUT")
    Dv: Optional[str] = Field(None, description="Dígito verificador")
    CodigoTipoDocumento: str = Field(..., description="Código tipo documento")
    CodigoClaseDocumento: str = Field(..., description="Código clase documento")
    NumeroDocumento: Optional[str] = Field(None, description="Número de documento")
    NumeroSerie: Optional[str] = Field(None, description="Número de serie")
    IndicadorVigencia: str = Field(..., description="Indicador de vigencia")
    FechaVencimiento: datetime = Field(..., description="Fecha de vencimiento")
    IndicadorBloqueo: str = Field(..., description="Indicador de bloqueo")


class RespuestaConsultaNroSerieNroDocBe(BaseModel):
    """Modelo para RespuestaConsultaNroSerieNroDocBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[DatosRespuestaNroSerieNroDocBe] = Field(None, description="Datos de la consulta")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


# Modelos para ConsultaCertificadoNacimiento
class ConsultaCertNacBe(BaseModel):
    """Modelo para ConsultaCertNacBe"""
    rut: int = Field(..., description="RUT")
    dv: Optional[str] = Field(None, description="Dígito verificador")
    circunscripcion: Optional[str] = Field(None, description="Circunscripción")
    numeroInscripcionNacimiento: Optional[str] = Field(None, description="Número inscripción nacimiento")
    registroInscripcionNacimiento: Optional[str] = Field(None, description="Registro inscripción nacimiento")
    anioInscripcionNacimiento: Optional[str] = Field(None, description="Año inscripción nacimiento")
    nombreCompleto: Optional[str] = Field(None, description="Nombre completo")
    fechaNacimiento: Optional[datetime] = Field(None, description="Fecha de nacimiento")
    sexo: Optional[str] = Field(None, description="Sexo")
    lugarNacimiento: Optional[str] = Field(None, description="Lugar de nacimiento")
    nacionalidadNacimiento: Optional[str] = Field(None, description="Nacionalidad al nacer")
    nombrePadre: Optional[str] = Field(None, description="Nombre del padre")
    runPadre: Optional[str] = Field(None, description="RUN del padre")
    nombreMadre: Optional[str] = Field(None, description="Nombre de la madre")
    runMadre: Optional[str] = Field(None, description="RUN de la madre")
    subInscripcionNacimiento: Optional[str] = Field(None, description="Sub inscripción nacimiento")


class RespuestaConsultaCertNacimientoBe(BaseModel):
    """Modelo para RespuestaConsultaCertNacimientoBe"""
    Cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    Respuesta: Optional[ConsultaCertNacBe] = Field(None, description="Datos del certificado")
    XmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


# Modelos para ConsultaDiscapacidad (simplificados)
class ConsultaDiscapacidadBe(BaseModel):
    """Modelo para ConsultaDiscapacidadBe"""
    Run: int = Field(..., description="RUN")
    Dv: Optional[str] = Field(None, description="Dígito verificador")
    ApareceEnRND: Optional[str] = Field(None, description="Aparece en RND")
    Discapacidad: Optional[Dict[str, Any]] = Field(None, description="Datos de discapacidad")
    DiscapacidadRn: Optional[Dict[str, Any]] = Field(None, description="Datos discapacidad RN")


class RespuestaConsultaDiscapacidadBe(BaseModel):
    """Modelo para RespuestaConsultaDiscapacidadBe"""
    Cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    Respuesta: Optional[ConsultaDiscapacidadBe] = Field(None, description="Datos de discapacidad")
    XmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


# Modelos para Verify
class VerifyRequest(BaseModel):
    """Modelo para request de Verify"""
    xmlparamin: Optional[str] = Field(None, description="XML de entrada")


class VerifyResponse(BaseModel):
    """Modelo para respuesta de Verify"""
    VerifyResult: int = Field(..., description="Resultado de verificación")
    xmlparamout: Optional[str] = Field(None, description="XML de salida")


# Modelos para VerificarHuellaDactilar
class HuellaDactilarBe(BaseModel):
    """Modelo para HuellaDactilarBe"""
    RutEmpresa: int = Field(..., description="RUT de la empresa")
    IdTransaccion: int = Field(..., description="ID de transacción")
    Ip: Optional[str] = Field(None, description="IP del cliente")
    UsuarioFinal: Optional[str] = Field(None, description="Usuario final")
    RutPersona: int = Field(..., description="RUT de la persona")
    NumeroDedo: int = Field(..., description="Número del dedo")
    Formato: int = Field(..., description="Formato de la huella")
    ImagenBase64: Optional[str] = Field(None, description="Imagen en Base64")


class RespuestaHuellaDactilarBe(BaseModel):
    """Modelo para RespuestaHuellaDactilarBe"""
    Puntaje: int = Field(..., description="Puntaje de la verificación")
    RespuestaAFIS: str = Field(..., description="Respuesta AFIS")


class RespuestaBeOfRespuestaHuellaDactilarBe(BaseModel):
    """Modelo para RespuestaBeOfRespuestaHuellaDactilarBe"""
    decision: bool = Field(..., description="Decisión de la verificación")
    mensaje: Optional[str] = Field(None, description="Mensaje")
    mensajeDetalle: Optional[str] = Field(None, description="Mensaje detallado")
    estructuraDatos: Optional[RespuestaHuellaDactilarBe] = Field(None, description="Estructura de datos")
    TipoRespuesta: str = Field(..., description="Tipo de respuesta")


# Modelos para requests de endpoints
class ConsultaRunRequest(BaseModel):
    """Modelo para request de ConsultaRun"""
    idSistema: int = Field(..., description="ID del sistema")
    rut: int = Field(..., description="RUT")
    dv: Optional[str] = Field(None, description="Dígito verificador")


class ConsultaNroSerieNroDocumentoRequest(BaseModel):
    """Modelo para request de ConsultaNroSerieNroDocumento"""
    idSistema: int = Field(..., description="ID del sistema")
    rut: int = Field(..., description="RUT")
    dv: Optional[str] = Field(None, description="Dígito verificador")
    nroSerieDoc: Optional[str] = Field(None, description="Número de serie del documento")
    tipoDocumento: TipoDocumento = Field(..., description="Tipo de documento")


class ConsultaCertificadoNacimientoRequest(BaseModel):
    """Modelo para request de ConsultaCertificadoNacimiento"""
    idSistema: int = Field(..., description="ID del sistema")
    rut: int = Field(..., description="RUT")
    dv: Optional[str] = Field(None, description="Dígito verificador")


class ConsultaDiscapacidadRequest(BaseModel):
    """Modelo para request de ConsultaDiscapacidad"""
    idSistema: int = Field(..., description="ID del sistema")
    run: int = Field(..., description="RUN")
    dv: Optional[str] = Field(None, description="Dígito verificador")


class VerificarHuellaDactilarRequest(BaseModel):
    """Modelo para request de VerificarHuellaDactilar"""
    IdSistema: int = Field(..., description="ID del sistema")
    Datos: HuellaDactilarBe = Field(..., description="Datos de la huella dactilar")


# Modelo genérico para errores
class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    success: bool = Field(default=False, description="Indica que la operación falló")
    mensaje: str = Field(..., description="Mensaje de error")
    codigo_error: Optional[str] = Field(None, description="Código de error específico")
    detalle: Optional[str] = Field(None, description="Detalle adicional del error") 
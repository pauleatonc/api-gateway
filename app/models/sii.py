"""
Modelos Pydantic para el servicio SII (Servicio de Impuestos Internos)
"""
from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, Field, validator
from enum import Enum


# Enumeración del WSDL
class ETipoEstado(str, Enum):
    """Enumeración para eTipoEstado"""
    NULO = "NULO"
    CORRECTO = "CORRECTO"
    INCORRECTO = "INCORRECTO"
    PROCESAR = "PROCESAR"
    ERROR = "ERROR"
    EXCEPCION = "EXCEPCION"


# Modelos de respuesta base
class RespuestaProcesoBe(BaseModel):
    """Modelo para RespuestaProcesoBe"""
    estadoProceso: ETipoEstado = Field(..., description="Estado del proceso")
    respuestaProceso: Optional[str] = Field(None, description="Respuesta del proceso")
    codigoProceso: int = Field(..., description="Código del proceso")


# Modelos específicos para cada consulta
class RepresentanteLegalSii(BaseModel):
    """Modelo para RepresentanteLegalSii"""
    rut: int = Field(..., description="RUT del representante legal")
    dv: Optional[str] = Field(None, description="Dígito verificador")
    fechaInicio: Optional[str] = Field(None, description="Fecha de inicio")


class RespuestaSiiDatosGlosa(BaseModel):
    """Modelo para RespuestaSiiDatosGlosa"""
    fechaInicioActividad: datetime = Field(..., description="Fecha de inicio de actividad")
    glosa: Optional[str] = Field(None, description="Glosa")
    estado: Optional[str] = Field(None, description="Estado")


class RepresentanteLegalSiiBe(BaseModel):
    """Modelo para RepresentanteLegalSiiBe"""
    representantes: Optional[List[RepresentanteLegalSii]] = Field(None, description="Lista de representantes legales")
    datosGenerales: Optional[RespuestaSiiDatosGlosa] = Field(None, description="Datos generales")


class RespuestaSiiRepresentanteLegalBe(BaseModel):
    """Modelo para RespuestaSiiRepresentanteLegalBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[RepresentanteLegalSiiBe] = Field(None, description="Respuesta específica")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


class RespuestaSiiConsIvaBe(BaseModel):
    """Modelo para RespuestaSiiConsIvaBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[RespuestaSiiDatosGlosa] = Field(None, description="Respuesta específica")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


class ConsultaSiiNumeroEmpleadosBe(BaseModel):
    """Modelo para ConsultaSiiNumeroEmpleadosBe"""
    fechaInicioActividad: datetime = Field(..., description="Fecha de inicio de actividad")
    glosa: Optional[str] = Field(None, description="Glosa")
    estado: Optional[str] = Field(None, description="Estado")
    numeroEmpleados: Optional[str] = Field(None, description="Número de empleados")


class RespuestaSiiNumeroEmpleadosBe(BaseModel):
    """Modelo para RespuestaSiiNumeroEmpleadosBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[ConsultaSiiNumeroEmpleadosBe] = Field(None, description="Respuesta específica")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


class ConsultaSiiCatEmpBe(BaseModel):
    """Modelo para ConsultaSiiCatEmpBe"""
    fechaInicioActividad: datetime = Field(..., description="Fecha de inicio de actividad")
    glosa: Optional[str] = Field(None, description="Glosa")
    estado: Optional[str] = Field(None, description="Estado")
    tipo: Optional[str] = Field(None, description="Tipo")
    glosaTipo: Optional[str] = Field(None, description="Glosa del tipo")
    cantPeriodo: Optional[str] = Field(None, description="Cantidad de período")


class RespuestaSiiCatEmpBe(BaseModel):
    """Modelo para RespuestaSiiCatEmpBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[ConsultaSiiCatEmpBe] = Field(None, description="Respuesta específica")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


class RespuestaSiiDatosGenerales(BaseModel):
    """Modelo para RespuestaSiiDatosGenerales"""
    estado: Optional[str] = Field(None, description="Estado")
    glosa: Optional[str] = Field(None, description="Glosa")
    razonSocial: Optional[str] = Field(None, description="Razón social")
    nombre: Optional[str] = Field(None, description="Nombre")
    apPaterno: Optional[str] = Field(None, description="Apellido paterno")
    apMaterno: Optional[str] = Field(None, description="Apellido materno")
    xml: Optional[str] = Field(None, description="XML")


class RespuestaSiiDatosContribuyenteBe(BaseModel):
    """Modelo para RespuestaSiiDatosContribuyenteBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[RespuestaSiiDatosGenerales] = Field(None, description="Respuesta específica")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


class ActEconomicaBe(BaseModel):
    """Modelo para ActEconomicaBe"""
    actividad: int = Field(..., description="Código de actividad")
    categoria: int = Field(..., description="Categoría")
    descripcion: Optional[str] = Field(None, description="Descripción")
    fechaInic: datetime = Field(..., description="Fecha de inicio")


class RespuestaSiiActEconomicaBe(BaseModel):
    """Modelo para RespuestaSiiActEconomicaBe"""
    fechaInicioActividad: datetime = Field(..., description="Fecha de inicio de actividad")
    glosa: Optional[str] = Field(None, description="Glosa")
    estado: Optional[str] = Field(None, description="Estado")
    actividadEconomica: Optional[List[ActEconomicaBe]] = Field(None, description="Lista de actividades económicas")


class RespuestaSiiActividadEconomicaBe(BaseModel):
    """Modelo para RespuestaSiiActividadEconomicaBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[RespuestaSiiActEconomicaBe] = Field(None, description="Respuesta específica")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


class RespuestaSiiEstadoGiroBe(BaseModel):
    """Modelo para RespuestaSiiEstadoGiroBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[RespuestaSiiDatosGlosa] = Field(None, description="Respuesta específica")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


class RespuestaSiiFecIniActBe(BaseModel):
    """Modelo para RespuestaSiiFecIniActBe"""
    cabecera: Optional[RespuestaProcesoBe] = Field(None, description="Cabecera de respuesta")
    respuesta: Optional[RespuestaSiiDatosGlosa] = Field(None, description="Respuesta específica")
    xmlRespuesta: Optional[str] = Field(None, description="XML de respuesta")


# Modelos de request para cada operación
class ConsultaRepresentanteLegalRequest(BaseModel):
    """Modelo para request de ConsultaRepresentanteLegal"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rut: Optional[str] = Field(None, description="RUT del contribuyente", example="12345678")
    dv: Optional[str] = Field(None, description="Dígito verificador", example="9")

    @validator('rut')
    def validate_rut(cls, v):
        if v and not v.isdigit():
            raise ValueError('El RUT debe contener solo números')
        return v

    @validator('dv')
    def validate_dv(cls, v):
        if v and len(v) != 1:
            raise ValueError('El dígito verificador debe ser un solo carácter')
        return v


class ConsultaRelacionContribuyenteEmpresaRequest(BaseModel):
    """Modelo para request de ConsultaRelacionContribuyenteEmpresa"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rutEmp: int = Field(..., description="RUT de la empresa", example=12345678)
    dvEmp: Optional[str] = Field(None, description="Dígito verificador de la empresa", example="9")
    rutSoc: int = Field(..., description="RUT del socio", example=87654321)
    dvSoc: Optional[str] = Field(None, description="Dígito verificador del socio", example="0")

    @validator('rutEmp', 'rutSoc')
    def validate_rut(cls, v):
        if v and not (10000000 <= v <= 99999999):
            raise ValueError('El RUT debe tener entre 7 y 8 dígitos')
        return v


class ConsultaMovimientoContribuyenteRequest(BaseModel):
    """Modelo para request de ConsultaMovimientoContribuyente"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rutCont: int = Field(..., description="RUT del contribuyente", example=12345678)
    dvCont: Optional[str] = Field(None, description="Dígito verificador del contribuyente", example="9")
    periodoTrib: Optional[str] = Field(None, description="Período tributario", example="202312")

    @validator('rutCont')
    def validate_rut(cls, v):
        if v and not (10000000 <= v <= 99999999):
            raise ValueError('El RUT debe tener entre 7 y 8 dígitos')
        return v


class ConsultaNumeroEmpleadosRequest(BaseModel):
    """Modelo para request de ConsultaNumeroEmpleados"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rut: int = Field(..., description="RUT de la empresa", example=12345678)
    dv: Optional[str] = Field(None, description="Dígito verificador", example="9")
    periodo: int = Field(..., description="Período", example=202312)

    @validator('rut')
    def validate_rut(cls, v):
        if v and not (10000000 <= v <= 99999999):
            raise ValueError('El RUT debe tener entre 7 y 8 dígitos')
        return v

    @validator('periodo')
    def validate_periodo(cls, v):
        if v and not (200001 <= v <= 999912):
            raise ValueError('El período debe tener formato AAAAMM')
        return v


class ConsultaCategoriaEmpresaRequest(BaseModel):
    """Modelo para request de ConsultaCategoriaEmpresa"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rut: int = Field(..., description="RUT de la empresa", example=12345678)
    dv: Optional[str] = Field(None, description="Dígito verificador", example="9")
    fecha: datetime = Field(..., description="Fecha de consulta", example="2023-12-01T00:00:00")
    tipoConsulta: int = Field(..., description="Tipo de consulta (1-4)", example=1)

    @validator('rut')
    def validate_rut(cls, v):
        if v and not (10000000 <= v <= 99999999):
            raise ValueError('El RUT debe tener entre 7 y 8 dígitos')
        return v

    @validator('tipoConsulta')
    def validate_tipo_consulta(cls, v):
        if v not in [1, 2, 3, 4]:
            raise ValueError('El tipo de consulta debe ser 1, 2, 3 o 4')
        return v


class ConsultaDatosContribuyenteRequest(BaseModel):
    """Modelo para request de ConsultaDatosContribuyente"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rut: int = Field(..., description="RUT del contribuyente", example=12345678)
    dv: Optional[str] = Field(None, description="Dígito verificador", example="9")

    @validator('rut')
    def validate_rut(cls, v):
        if v and not (10000000 <= v <= 99999999):
            raise ValueError('El RUT debe tener entre 7 y 8 dígitos')
        return v


class ConsultaActividadEconomicaRequest(BaseModel):
    """Modelo para request de ConsultaActividadEconomica"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rut: int = Field(..., description="RUT del contribuyente", example=12345678)
    dv: Optional[str] = Field(None, description="Dígito verificador", example="9")

    @validator('rut')
    def validate_rut(cls, v):
        if v and not (10000000 <= v <= 99999999):
            raise ValueError('El RUT debe tener entre 7 y 8 dígitos')
        return v


class ConsultaEstadoGiroRequest(BaseModel):
    """Modelo para request de ConsultaEstadoGiro"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rut: int = Field(..., description="RUT del contribuyente", example=12345678)
    dv: Optional[str] = Field(None, description="Dígito verificador", example="9")

    @validator('rut')
    def validate_rut(cls, v):
        if v and not (10000000 <= v <= 99999999):
            raise ValueError('El RUT debe tener entre 7 y 8 dígitos')
        return v


class ConsultaFechaInicioActividadRequest(BaseModel):
    """Modelo para request de ConsultaFechaInicioActividad"""
    idSistema: int = Field(..., description="ID del sistema", example=1)
    rut: int = Field(..., description="RUT del contribuyente", example=12345678)
    dv: Optional[str] = Field(None, description="Dígito verificador", example="9")

    @validator('rut')
    def validate_rut(cls, v):
        if v and not (10000000 <= v <= 99999999):
            raise ValueError('El RUT debe tener entre 7 y 8 dígitos')
        return v


# Modelo de respuesta de error
class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    success: bool = Field(default=False, description="Indica si la operación falló")
    mensaje: str = Field(..., description="Mensaje de error")
    codigo_error: Optional[str] = Field(None, description="Código de error específico")
    detalle: Optional[str] = Field(None, description="Detalle adicional del error")

"""
Modelos Pydantic para el servicio de Perfiles de SENCE
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


# Enumeraciones del WSDL
class EstadoAcceso(str, Enum):
    """Enumeración para EstadoAcceso"""
    NO_AUTORIZADO = "NoAutorizado"
    AUTORIZADO = "Autorizado"


class ETipoPersona(str, Enum):
    """Enumeración para eTipoPersona"""
    PERSONA_NATURAL = "PersonaNatural"
    PERSONA_JURIDICA = "PersonaJuridica"
    PERSONA_EXTRANJERA = "PersonaExtranjera"
    OTRA = "Otra"


class EEstado(str, Enum):
    """Enumeración para eEstado"""
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"


class ETipoPerfil(str, Enum):
    """Enumeración para eTipoPerfil"""
    NORMAL = "Normal"
    ADMINISTRADOR = "Administrador"
    ARQUITECTO_TI = "ArquitectoTi"
    SENCE = "Sence"


class ERegion(str, Enum):
    """Enumeración para eRegion"""
    REGION_DE_TARAPACA = "Region_de_Tarapaca"
    REGION_DE_ANTOFAGASTA = "Region_de_Antofagasta"
    REGION_DE_ATACAMA = "Region_de_Atacama"
    REGION_DE_COQUIMBO = "Region_de_Coquimbo"
    REGION_DE_VALPARAISO = "Region_de_Valparaiso"
    REGION_DEL_LIB_GEN_BER_OHIG = "Region_del_Lib_Gen_Ber_Ohig"
    REGION_DEL_MAULE = "Region_del_Maule"
    REGION_DEL_BIO_BIO = "Region_del_Bio_Bio"
    REGION_DE_LA_ARAUCANIA = "Region_de_la_Araucania"
    REGION_DE_LOS_LAGOS = "Region_de_los_Lagos"
    REGION_DE_AYSEN_DEL_GEN_CARLOS_IC = "Region_de_Aysen_del_Gen_Carlos_IC"
    REGION_DE_MAGALLANES_Y_LA_ANT_CHILENA = "Region_de_Magallanes_y_la_Ant_Chilena"
    REGION_METROPOLITANA_DE_SANTIAGO = "Region_Metropolitana_de_Santiago"
    REGION_DE_LOS_RIOS = "Region_de_los_Rios"
    REGION_DE_ARICA_Y_PARINACOTA = "Region_de_Arica_y_Parinacota"
    REGION_DE_NUBLE = "Region_de_Nuble"
    EXTRANJERO = "Extranjero"


# Modelos base
class AutorizacionBe(BaseModel):
    """Modelo para AutorizacionBe"""
    acceso: str = Field(..., description="Estado de acceso")
    codigo: int = Field(..., description="Código de autorización")
    descripcion: Optional[str] = Field(None, description="Descripción del acceso")


class UsuarioBe(BaseModel):
    """Modelo para UsuarioBe"""
    idUsuario: int = Field(..., description="ID del usuario")
    nombre: Optional[str] = Field(None, description="Nombre del usuario")
    apellidoPaterno: Optional[str] = Field(None, description="Apellido paterno")
    apellidoMaterno: Optional[str] = Field(None, description="Apellido materno")
    tipoPersona: str = Field(..., description="Tipo de persona")


class FuncionBe(BaseModel):
    """Modelo para FuncionBe"""
    idFuncion: int = Field(..., description="ID de la función")
    nombreFuncion: Optional[str] = Field(None, description="Nombre de la función")
    obligatorio: bool = Field(..., description="Es obligatoria")
    denegado: bool = Field(..., description="Está denegada")
    estado: str = Field(..., description="Estado de la función")


class PerfilBe(BaseModel):
    """Modelo para PerfilBe"""
    idPerfil: int = Field(..., description="ID del perfil")
    nombrePerfil: Optional[str] = Field(None, description="Nombre del perfil")
    estado: str = Field(..., description="Estado del perfil")
    tipoPerfil: str = Field(..., description="Tipo de perfil")
    region: Optional[str] = Field(None, description="Región asociada")
    funcion: Optional[List[FuncionBe]] = Field(None, description="Lista de funciones")


class PerfilSistemaBe(BaseModel):
    """Modelo para PerfilSistemaBe"""
    idSistema: int = Field(..., description="ID del sistema")
    nombreSistema: Optional[str] = Field(None, description="Nombre del sistema")
    perfil: Optional[List[PerfilBe]] = Field(None, description="Lista de perfiles")


class UsuarioEmpresaBe(BaseModel):
    """Modelo para UsuarioEmpresaBe"""
    idUsuarioEmpresa: int = Field(..., description="ID del usuario empresa")
    razonSocial: Optional[str] = Field(None, description="Razón social")
    tipoEmpresa: Optional[str] = Field(None, description="Tipo de empresa")
    tipoPersona: str = Field(..., description="Tipo de persona")


class RespuestaPerfilesBe(BaseModel):
    """Modelo para RespuestaPerfilesBe"""
    autorizacion: Optional[AutorizacionBe] = Field(None, description="Datos de autorización")
    usuario: Optional[List[UsuarioBe]] = Field(None, description="Lista de usuarios")
    perfil: Optional[PerfilSistemaBe] = Field(None, description="Perfil del sistema")
    funcion: Optional[List[FuncionBe]] = Field(None, description="Lista de funciones")
    usuarioEmpresa: Optional[List[UsuarioEmpresaBe]] = Field(None, description="Lista de usuarios empresa")


# Modelos para requests POST
class SolicitarPerfilUsuarioRequest(BaseModel):
    """Modelo para request de SolicitarPerfilUsuario"""
    idSistema: int = Field(..., description="ID del sistema")
    idPerfil: int = Field(..., description="ID del perfil")
    rutUsuario: int = Field(..., description="RUT del usuario")
    motivoSolicitud: Optional[str] = Field(None, description="Motivo de la solicitud")
    idRegion: int = Field(..., description="ID de la región")
    tipoPersona: str = Field(..., description="Tipo de persona")
    rutUsrUpdate: int = Field(..., description="RUT del usuario que actualiza")


class BloquearPerfilRequest(BaseModel):
    """Modelo para request de BloquearPerfilSistemaUsuarioPorRut"""
    idSistema: int = Field(..., description="ID del sistema")
    idPerfil: int = Field(..., description="ID del perfil")
    rutUsuario: int = Field(..., description="RUT del usuario")
    tipoPersona: str = Field(..., description="Tipo de persona")
    rutUsrUpdate: int = Field(..., description="RUT del usuario que actualiza")


class AsignarPerfilRequest(BaseModel):
    """Modelo para request de AsignarPerfilSistemaUsuarioPorRut"""
    idSistema: int = Field(..., description="ID del sistema")
    idPerfil: int = Field(..., description="ID del perfil")
    region: str = Field(..., description="Región")
    rutUsuario: int = Field(..., description="RUT del usuario")
    tipoPersona: str = Field(..., description="Tipo de persona")
    rutUsrUpdate: int = Field(..., description="RUT del usuario que actualiza")


# Modelo para errores
class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    success: bool = Field(default=False, description="Indica si la operación fue exitosa")
    mensaje: str = Field(..., description="Mensaje de error")
    codigo_error: Optional[str] = Field(None, description="Código de error específico")
    detalle: Optional[str] = Field(None, description="Detalle adicional del error") 
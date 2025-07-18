"""
Router REST para el servicio de Perfiles de SENCE
"""
from typing import Union
from fastapi import APIRouter, Depends, Query, Path, status
from fastapi.responses import JSONResponse
from zeep.exceptions import Fault
from loguru import logger

from app.models.perfiles import (
    RespuestaPerfilesBe, SolicitarPerfilUsuarioRequest, BloquearPerfilRequest,
    AsignarPerfilRequest, ErrorResponse, ETipoPersona, ERegion
)
from app.services.perfiles_soap_client import PerfilesSoapClientService, perfiles_soap_client

router = APIRouter(
    prefix="/perfiles",
    tags=["Perfiles SENCE"],
    responses={
        502: {
            "model": ErrorResponse,
            "description": "Error del servicio SOAP"
        }
    }
)


def get_perfiles_soap_client() -> PerfilesSoapClientService:
    """Dependency injection para el cliente SOAP de Perfiles"""
    return perfiles_soap_client


@router.get(
    "/usuarios",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar usuarios por perfil y sistema",
    description="Obtiene una lista de usuarios (Naturales) consultando por el identificador del sistema y el identificador del perfil.",
    responses={
        200: {
            "description": "Lista de usuarios obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Acceso autorizado"
                        },
                        "usuario": [
                            {
                                "idUsuario": 1,
                                "nombre": "Juan Carlos",
                                "apellidoPaterno": "Pérez",
                                "apellidoMaterno": "González",
                                "tipoPersona": "PersonaNatural"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def consulta_usuarios_por_perfil_sistema(
    id_sistema: int = Query(..., description="ID del sistema", example=1),
    id_perfil: int = Query(..., description="ID del perfil", example=1),
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Consulta usuarios por perfil y sistema"""
    try:
        response = await soap_client.consulta_usuarios_por_perfil_sistema(
            id_sistema=id_sistema,
            id_perfil=id_perfil
        )
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_usuarios_por_perfil_sistema: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_usuarios_por_perfil_sistema: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


@router.get(
    "/usuarios/{rut}",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar perfil de usuario por RUT",
    description="Obtiene todos los perfiles que posee un usuario según su RUT de un sistema particular. Incluye perfiles no asignados.",
    responses={
        200: {
            "description": "Perfil de usuario obtenido exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Acceso autorizado"
                        },
                        "perfil": {
                            "idSistema": 1,
                            "nombreSistema": "Sistema de Pruebas",
                            "perfil": [
                                {
                                    "idPerfil": 1,
                                    "nombrePerfil": "Administrador",
                                    "estado": "Activo",
                                    "tipoPerfil": "Administrador"
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
)
async def consulta_perfil_usuario_sistema_por_rut(
    rut: int = Path(..., description="RUT de la persona", example=12345678),
    id_sistema: int = Query(..., description="ID del sistema", example=1),
    tipo_persona: ETipoPersona = Query(..., description="Tipo de persona", example=ETipoPersona.PERSONA_NATURAL),
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Consulta perfil de usuario por RUT"""
    try:
        response = await soap_client.consulta_perfil_usuario_sistema_por_rut(
            rut_persona=rut,
            id_sistema=id_sistema,
            tipo_persona=tipo_persona.value
        )
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_perfil_usuario_sistema_por_rut: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_perfil_usuario_sistema_por_rut: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


@router.get(
    "/perfiles",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar perfiles por sistema",
    description="Obtiene una lista de perfiles asociados a un sistema.",
    responses={
        200: {
            "description": "Lista de perfiles obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Acceso autorizado"
                        },
                        "perfil": {
                            "idSistema": 1,
                            "nombreSistema": "Sistema de Pruebas",
                            "perfil": [
                                {
                                    "idPerfil": 1,
                                    "nombrePerfil": "Administrador",
                                    "estado": "Activo",
                                    "tipoPerfil": "Administrador"
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
)
async def consulta_perfil_por_sistema(
    id_sistema: int = Query(..., description="ID del sistema", example=1),
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Consulta perfiles por sistema"""
    try:
        response = await soap_client.consulta_perfil_por_sistema(id_sistema=id_sistema)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_perfil_por_sistema: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_perfil_por_sistema: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


@router.get(
    "/funciones",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar funciones por sistema",
    description="Obtiene un listado de funciones disponibles de un sistema.",
    responses={
        200: {
            "description": "Lista de funciones obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Acceso autorizado"
                        },
                        "funcion": [
                            {
                                "idFuncion": 1,
                                "nombreFuncion": "Consultar datos",
                                "obligatorio": True,
                                "denegado": False,
                                "estado": "Activo"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def consulta_funciones_por_sistema(
    id_sistema: int = Query(..., description="ID del sistema", example=1),
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Consulta funciones por sistema"""
    try:
        response = await soap_client.consulta_funciones_por_sistema(id_sistema=id_sistema)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_funciones_por_sistema: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_funciones_por_sistema: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


@router.get(
    "/funciones/por-perfil",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar funciones por perfil y sistema",
    description="Obtiene un listado de funciones que tiene un perfil asociado a un sistema.",
    responses={
        200: {
            "description": "Lista de funciones por perfil obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Acceso autorizado"
                        },
                        "funcion": [
                            {
                                "idFuncion": 1,
                                "nombreFuncion": "Consultar datos",
                                "obligatorio": True,
                                "denegado": False,
                                "estado": "Activo"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def consulta_funciones_por_perfil_sistema(
    id_perfil: int = Query(..., description="ID del perfil", example=1),
    id_sistema: int = Query(..., description="ID del sistema", example=1),
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Consulta funciones por perfil y sistema"""
    try:
        response = await soap_client.consulta_funciones_por_perfil_sistema(
            id_perfil=id_perfil,
            id_sistema=id_sistema
        )
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_funciones_por_perfil_sistema: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_funciones_por_perfil_sistema: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


@router.get(
    "/empresas",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar empresas por perfil y sistema",
    description="Obtiene una lista de usuarios (Jurídicos) consultando por el identificador del sistema y el identificador del perfil.",
    responses={
        200: {
            "description": "Lista de empresas obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Acceso autorizado"
                        },
                        "usuarioEmpresa": [
                            {
                                "idUsuarioEmpresa": 1,
                                "razonSocial": "Empresa de Pruebas S.A.",
                                "tipoEmpresa": "Sociedad Anónima",
                                "tipoPersona": "PersonaJuridica"
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def consulta_empresas_por_perfil_sistema(
    id_sistema: int = Query(..., description="ID del sistema", example=1),
    id_perfil: int = Query(..., description="ID del perfil", example=1),
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Consulta empresas por perfil y sistema"""
    try:
        response = await soap_client.consulta_empresas_por_perfil_sistema(
            id_sistema=id_sistema,
            id_perfil=id_perfil
        )
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_empresas_por_perfil_sistema: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_empresas_por_perfil_sistema: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


@router.post(
    "/solicitar",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Solicitar perfil para usuario",
    description="Solicita la asignación de un perfil para un usuario de un sistema particular.",
    responses={
        200: {
            "description": "Solicitud de perfil procesada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Solicitud procesada correctamente"
                        }
                    }
                }
            }
        }
    }
)
async def solicitar_perfil_usuario(
    request: SolicitarPerfilUsuarioRequest,
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Solicita perfil para usuario"""
    try:
        response = await soap_client.solicitar_perfil_usuario(request=request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en solicitar_perfil_usuario: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en solicitar_perfil_usuario: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


@router.post(
    "/bloquear",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Bloquear perfil de usuario",
    description="Bloquea el perfil de un usuario en un sistema.",
    responses={
        200: {
            "description": "Bloqueo de perfil procesado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Perfil bloqueado correctamente"
                        }
                    }
                }
            }
        }
    }
)
async def bloquear_perfil_sistema_usuario_por_rut(
    request: BloquearPerfilRequest,
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Bloquea perfil de usuario"""
    try:
        response = await soap_client.bloquear_perfil_sistema_usuario_por_rut(request=request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en bloquear_perfil_sistema_usuario_por_rut: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en bloquear_perfil_sistema_usuario_por_rut: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


@router.post(
    "/asignar",
    response_model=RespuestaPerfilesBe,
    status_code=status.HTTP_200_OK,
    summary="Asignar perfil a usuario",
    description="Asigna un perfil a un usuario en un sistema.",
    responses={
        200: {
            "description": "Asignación de perfil procesada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "autorizacion": {
                            "acceso": "Autorizado",
                            "codigo": 200,
                            "descripcion": "Perfil asignado correctamente"
                        }
                    }
                }
            }
        }
    }
)
async def asignar_perfil_sistema_usuario_por_rut(
    request: AsignarPerfilRequest,
    soap_client: PerfilesSoapClientService = Depends(get_perfiles_soap_client)
) -> Union[RespuestaPerfilesBe, JSONResponse]:
    """Asigna perfil a usuario"""
    try:
        response = await soap_client.asignar_perfil_sistema_usuario_por_rut(request=request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en asignar_perfil_sistema_usuario_por_rut: {fault}")
        error_response = ErrorResponse(
            mensaje=f"Error en el servicio SOAP: {str(fault)}",
            codigo_error="SOAP_FAULT",
            detalle=f"Fault code: {fault.code if hasattr(fault, 'code') else 'Unknown'}"
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en asignar_perfil_sistema_usuario_por_rut: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        ) 
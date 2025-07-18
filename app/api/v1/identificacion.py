"""
Endpoints REST para el servicio de Identificación de SENCE
"""
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from loguru import logger

from app.models.identificacion import (
    IniciarSesionRequest,
    IniciarSesionResponse,
    IniciarSesionPorGuidRequest, 
    IniciarSesionPorGuidResponse,
    IniciarSesionTokenRequest,
    IniciarSesionTokenResponse,
    ObtenerListadoURLporRutResponse,
    ErrorResponse
)
from app.services.soap_client import SoapClientService, soap_client


# Crear router
router = APIRouter(
    prefix="/auth",
    tags=["Identificación SENCE"],
    responses={
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)


def get_soap_client() -> SoapClientService:
    """Dependencia para obtener el cliente SOAP"""
    return soap_client


@router.post(
    "/login",
    response_model=IniciarSesionResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión con usuario y clave",
    description="Inicia sesión usando usuario y contraseña en el servicio SENCE",
    responses={
        200: {"model": IniciarSesionResponse, "description": "Sesión iniciada correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def iniciar_sesion(
    request: IniciarSesionRequest,
    soap_client: SoapClientService = Depends(get_soap_client)
) -> Union[IniciarSesionResponse, JSONResponse]:
    """
    Inicia sesión con usuario y contraseña.
    
    - **usuario**: Nombre de usuario para autenticación
    - **clave**: Contraseña del usuario
    
    Retorna información de sesión incluyendo token y GUID si es exitoso.
    """
    try:
        logger.info(f"Iniciando sesión para usuario: {request.usuario}")
        
        response = await soap_client.iniciar_sesion(
            usuario=request.usuario,
            clave=request.clave
        )
        
        # Si hay un error en el servicio SOAP, devolver 502
        if not response.success and response.codigo_error in ["SOAP_FAULT", "CONNECTION_ERROR"]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.mensaje,
                    codigo_error=response.codigo_error,
                    detalle=f"Error al comunicarse con el servicio SOAP de SENCE"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en iniciar_sesion: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/login/guid",
    response_model=IniciarSesionPorGuidResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión con GUID",
    description="Inicia sesión usando un GUID de sesión en el servicio SENCE",
    responses={
        200: {"model": IniciarSesionPorGuidResponse, "description": "Sesión iniciada correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def iniciar_sesion_por_guid(
    request: IniciarSesionPorGuidRequest,
    soap_client: SoapClientService = Depends(get_soap_client)
) -> Union[IniciarSesionPorGuidResponse, JSONResponse]:
    """
    Inicia sesión con un GUID de sesión.
    
    - **guid**: GUID de sesión válido
    
    Retorna información de sesión incluyendo token si es exitoso.
    """
    try:
        logger.info(f"Iniciando sesión por GUID: {request.guid}")
        
        response = await soap_client.iniciar_sesion_por_guid(guid=request.guid)
        
        # Si hay un error en el servicio SOAP, devolver 502
        if not response.success and response.codigo_error in ["SOAP_FAULT", "CONNECTION_ERROR"]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.mensaje,
                    codigo_error=response.codigo_error,
                    detalle=f"Error al comunicarse con el servicio SOAP de SENCE"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en iniciar_sesion_por_guid: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/login/token",
    response_model=IniciarSesionTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Validar token de sesión",
    description="Valida un token de sesión existente en el servicio SENCE",
    responses={
        200: {"model": IniciarSesionTokenResponse, "description": "Token validado correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def iniciar_sesion_token(
    request: IniciarSesionTokenRequest,
    soap_client: SoapClientService = Depends(get_soap_client)
) -> Union[IniciarSesionTokenResponse, JSONResponse]:
    """
    Valida un token de sesión.
    
    - **token**: Token de sesión a validar
    
    Retorna información del usuario asociado al token si es válido.
    """
    try:
        logger.info(f"Validando token de sesión: {request.token[:10]}...")
        
        response = await soap_client.iniciar_sesion_token(token=request.token)
        
        # Si hay un error en el servicio SOAP, devolver 502
        if not response.success and response.codigo_error in ["SOAP_FAULT", "CONNECTION_ERROR"]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.mensaje,
                    codigo_error=response.codigo_error,
                    detalle=f"Error al comunicarse con el servicio SOAP de SENCE"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en iniciar_sesion_token: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.get(
    "/systems/{rut}",
    response_model=ObtenerListadoURLporRutResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener sistemas disponibles por RUT",
    description="Obtiene la lista de sistemas/URLs disponibles para un RUT específico",
    responses={
        200: {"model": ObtenerListadoURLporRutResponse, "description": "Listado obtenido correctamente"},
        400: {"description": "RUT inválido"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def obtener_listado_url_por_rut(
    rut: str = Path(..., description="RUT del usuario (formato: 12345678-9)", min_length=9, max_length=12),
    soap_client: SoapClientService = Depends(get_soap_client)
) -> Union[ObtenerListadoURLporRutResponse, JSONResponse]:
    """
    Obtiene la lista de sistemas/URLs disponibles para un RUT específico.
    
    - **rut**: RUT del usuario en formato 12345678-9
    
    Retorna una lista de sistemas disponibles para el RUT especificado.
    """
    try:
        logger.info(f"Obteniendo listado de URLs para RUT: {rut}")
        
        response = await soap_client.obtener_listado_url_por_rut(rut=rut)
        
        # Si hay un error en el servicio SOAP, devolver 502
        if not response.success and response.codigo_error in ["SOAP_FAULT", "CONNECTION_ERROR"]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.mensaje,
                    codigo_error=response.codigo_error,
                    detalle=f"Error al comunicarse con el servicio SOAP de SENCE"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en obtener_listado_url_por_rut: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        ) 
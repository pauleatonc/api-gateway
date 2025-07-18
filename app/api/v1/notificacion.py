"""
Router REST para el servicio de Notificación de SENCE
"""
from typing import Union
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from zeep.exceptions import Fault
from loguru import logger

from app.models.notificacion import (
    # Requests
    EnviarSMSRequest, EnviarCorreoPublicoRequest, EnviarListaCorreoPublicoRequest,
    EnviarCorreoPublicoRmRequest,
    # Responses
    EnvioExitosoResponse, RespuestaMailBe, ErrorResponse
)
from app.services.notificacion_soap_client import NotificacionSoapClientService, notificacion_soap_client

router = APIRouter(
    prefix="/notificacion",
    tags=["Notificación SENCE"],
    responses={
        502: {
            "model": ErrorResponse,
            "description": "Error del servicio SOAP"
        }
    }
)


def get_notificacion_soap_client() -> NotificacionSoapClientService:
    """Dependency injection para el cliente SOAP de Notificación"""
    return notificacion_soap_client


@router.post(
    "/sms",
    response_model=EnvioExitosoResponse,
    status_code=status.HTTP_200_OK,
    summary="Enviar SMS",
    description="Envía un mensaje SMS a un número de celular.",
    responses={
        200: {
            "description": "SMS enviado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "mensaje": "SMS enviado correctamente"
                    }
                }
            }
        }
    }
)
async def enviar_sms(
    request: EnviarSMSRequest,
    soap_client: NotificacionSoapClientService = Depends(get_notificacion_soap_client)
) -> Union[EnvioExitosoResponse, JSONResponse]:
    """Envía SMS a un número de celular"""
    try:
        response = await soap_client.enviar_sms(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en enviar_sms: {fault}")
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
        logger.error(f"Error inesperado en enviar_sms: {str(e)}")
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
    "/correo/publico",
    response_model=EnvioExitosoResponse,
    status_code=status.HTTP_200_OK,
    summary="Enviar correo público",
    description="Envía un correo electrónico a una cuenta externa (Gmail, Hotmail, etc.).",
    responses={
        200: {
            "description": "Correo enviado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "mensaje": "Correo público enviado correctamente"
                    }
                }
            }
        }
    }
)
async def enviar_correo_publico(
    request: EnviarCorreoPublicoRequest,
    soap_client: NotificacionSoapClientService = Depends(get_notificacion_soap_client)
) -> Union[EnvioExitosoResponse, JSONResponse]:
    """Envía correo público a una cuenta externa"""
    try:
        response = await soap_client.enviar_correo_publico(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en enviar_correo_publico: {fault}")
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
        logger.error(f"Error inesperado en enviar_correo_publico: {str(e)}")
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
    "/correo/publico/lista",
    response_model=EnvioExitosoResponse,
    status_code=status.HTTP_200_OK,
    summary="Enviar lista de correos públicos",
    description="Envía un correo electrónico a múltiples cuentas externas.",
    responses={
        200: {
            "description": "Lista de correos enviada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "mensaje": "Lista de correos públicos enviada correctamente"
                    }
                }
            }
        }
    }
)
async def enviar_lista_correo_publico(
    request: EnviarListaCorreoPublicoRequest,
    soap_client: NotificacionSoapClientService = Depends(get_notificacion_soap_client)
) -> Union[EnvioExitosoResponse, JSONResponse]:
    """Envía correo público a múltiples cuentas externas"""
    try:
        response = await soap_client.enviar_lista_correo_publico(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en enviar_lista_correo_publico: {fault}")
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
        logger.error(f"Error inesperado en enviar_lista_correo_publico: {str(e)}")
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
    "/correo/publico/rm",
    response_model=RespuestaMailBe,
    status_code=status.HTTP_200_OK,
    summary="Enviar correo público con respuesta",
    description="Envía un correo electrónico a una cuenta externa y retorna el estado del envío.",
    responses={
        200: {
            "description": "Correo enviado exitosamente con respuesta",
            "content": {
                "application/json": {
                    "example": {
                        "estado": {
                            "estadoProceso": "CORRECTO",
                            "respuestaProceso": "Correo enviado correctamente"
                        },
                        "mailsNoInsertados": []
                    }
                }
            }
        }
    }
)
async def enviar_correo_publico_rm(
    request: EnviarCorreoPublicoRmRequest,
    soap_client: NotificacionSoapClientService = Depends(get_notificacion_soap_client)
) -> Union[RespuestaMailBe, JSONResponse]:
    """Envía correo público con respuesta detallada"""
    try:
        response = await soap_client.enviar_correo_publico_rm(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en enviar_correo_publico_rm: {fault}")
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
        logger.error(f"Error inesperado en enviar_correo_publico_rm: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )

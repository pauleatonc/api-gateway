"""
Router REST para el servicio de Firma Desatendida de SENCE
"""
from typing import Union
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from zeep.exceptions import Fault
from loguru import logger

from app.models.firma import (
    FirmaDesatendidaRequest,
    FirmaDesatendidaResponse,
    ErrorResponse
)
from app.services.firma_soap_client import FirmaSoapClientService, firma_soap_client

router = APIRouter(
    prefix="/firma",
    tags=["Firma Desatendida SENCE"],
    responses={
        502: {
            "model": ErrorResponse,
            "description": "Error del servicio SOAP"
        }
    }
)


def get_firma_soap_client() -> FirmaSoapClientService:
    """Dependency injection para el cliente SOAP de Firma"""
    return firma_soap_client


@router.post(
    "/desatendida",
    response_model=FirmaDesatendidaResponse,
    status_code=status.HTTP_200_OK,
    summary="Firma Desatendida de Documentos",
    description="""
    Realiza la firma desatendida de uno o más documentos.
    
    Este servicio permite firmar documentos de forma automática sin intervención del usuario,
    utilizando el sistema de firma electrónica de SENCE.
    
    **Parámetros:**
    - **documentos**: Lista de documentos a firmar (en formato Base64)
    - **proposito**: Propósito de la firma (Firmar, Visar, Aprobar)
    - **runFirmante**: RUN del firmante autorizado
    
    **Nota:** El contenido del documento debe estar codificado en Base64 y el checksum
    debe calcularse usando SHA256 sobre el contenido original del archivo.
    """,
    responses={
        200: {
            "description": "Documentos firmados exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "mensaje": "Documentos firmados exitosamente",
                        "documentosFirmados": [
                            {
                                "folio": 1619,
                                "nombre": "resolucion.pdf",
                                "estado": "FIRMADO"
                            }
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Solicitud inválida",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "mensaje": "Error de validación",
                        "codigo_error": "VALIDATION_ERROR",
                        "detalle": "El checksum debe tener 64 caracteres"
                    }
                }
            }
        },
        502: {
            "description": "Error del servicio SOAP",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "mensaje": "Error en el servicio SOAP",
                        "codigo_error": "SOAP_FAULT",
                        "detalle": "Error de comunicación con el servicio"
                    }
                }
            }
        }
    }
)
async def firma_desatendida(
    request: FirmaDesatendidaRequest,
    soap_client: FirmaSoapClientService = Depends(get_firma_soap_client)
) -> Union[FirmaDesatendidaResponse, JSONResponse]:
    """
    Realiza la firma desatendida de documentos
    
    Este endpoint permite firmar uno o más documentos de forma automática
    utilizando el sistema de firma electrónica de SENCE.
    """
    try:
        logger.info(f"Procesando firma desatendida - RUN: {request.runFirmante}, Documentos: {len(request.documentos)}")
        
        response = await soap_client.firma_desatendida(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en firma_desatendida: {fault}")
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
        logger.error(f"Error inesperado en firma_desatendida: {str(e)}")
        error_response = ErrorResponse(
            mensaje="Error interno del servidor",
            codigo_error="INTERNAL_ERROR",
            detalle=str(e)
        )
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=error_response.model_dump()
        )


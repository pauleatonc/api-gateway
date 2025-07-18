"""
Endpoints REST para el servicio de Consulta Registro Civil de SENCE
"""
from typing import Union, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from zeep.exceptions import Fault
from loguru import logger

from app.models.consulta_rc import (
    # Response models
    RespuestaConsultaRunBe,
    RespuestaConsultaNroSerieNroDocBe,
    RespuestaConsultaCertNacimientoBe,
    RespuestaConsultaDiscapacidadBe,
    VerifyResponse,
    RespuestaBeOfRespuestaHuellaDactilarBe,
    # Request models
    VerifyRequest,
    VerificarHuellaDactilarRequest,
    # Enums
    TipoDocumento,
    # Error model
    ErrorResponse
)
from app.services.consulta_rc_soap_client import ConsultaRcSoapClientService, consulta_rc_soap_client


# Crear router
router = APIRouter(
    prefix="/rc",
    tags=["Consulta Registro Civil"],
    responses={
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)


def get_consulta_rc_soap_client() -> ConsultaRcSoapClientService:
    """Dependencia para obtener el cliente SOAP de consulta RC"""
    return consulta_rc_soap_client


@router.get(
    "/run",
    response_model=RespuestaConsultaRunBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar RUN",
    description="Verifica el RUN de una persona en el Registro Civil",
    responses={
        200: {"model": RespuestaConsultaRunBe, "description": "Información del RUN obtenida correctamente"},
        400: {"description": "Parámetros inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def consulta_run(
    id_sistema: int = Query(..., description="ID del sistema que realiza la consulta"),
    rut: int = Query(..., description="RUT de la persona a consultar"),
    dv: Optional[str] = Query(None, description="Dígito verificador del RUT"),
    soap_client: ConsultaRcSoapClientService = Depends(get_consulta_rc_soap_client)
) -> Union[RespuestaConsultaRunBe, JSONResponse]:
    """
    Consulta información de un RUN en el Registro Civil.
    
    - **id_sistema**: ID del sistema que realiza la consulta
    - **rut**: RUT de la persona a consultar
    - **dv**: Dígito verificador del RUT (opcional)
    
    Retorna información completa de la persona si el RUN existe.
    """
    try:
        logger.info(f"Consultando RUN: {rut}")
        
        response = await soap_client.consulta_run(
            id_sistema=id_sistema,
            rut=rut,
            dv=dv
        )
        
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_run: {fault}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error en el servicio SOAP",
                codigo_error="SOAP_FAULT",
                detalle=str(fault)
            ).model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_run: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.get(
    "/run/documento",
    response_model=RespuestaConsultaNroSerieNroDocBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar número de serie o documento",
    description="Verifica el número de serie o número de documento del RUN",
    responses={
        200: {"model": RespuestaConsultaNroSerieNroDocBe, "description": "Información del documento obtenida correctamente"},
        400: {"description": "Parámetros inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def consulta_nro_serie_nro_documento(
    id_sistema: int = Query(..., description="ID del sistema que realiza la consulta"),
    rut: int = Query(..., description="RUT de la persona"),
    dv: Optional[str] = Query(None, description="Dígito verificador del RUT"),
    nro_serie_doc: Optional[str] = Query(None, description="Número de serie del documento"),
    tipo_documento: TipoDocumento = Query(TipoDocumento.C, description="Tipo de documento"),
    soap_client: ConsultaRcSoapClientService = Depends(get_consulta_rc_soap_client)
) -> Union[RespuestaConsultaNroSerieNroDocBe, JSONResponse]:
    """
    Consulta el número de serie o número de documento del RUN.
    
    - **id_sistema**: ID del sistema que realiza la consulta
    - **rut**: RUT de la persona
    - **dv**: Dígito verificador del RUT (opcional)
    - **nro_serie_doc**: Número de serie del documento (opcional)
    - **tipo_documento**: Tipo de documento (C=Cédula, P=Pasaporte, etc.)
    
    Retorna información del documento y su vigencia.
    """
    try:
        logger.info(f"Consultando documento para RUT: {rut}, tipo: {tipo_documento}")
        
        response = await soap_client.consulta_nro_serie_nro_documento(
            id_sistema=id_sistema,
            rut=rut,
            dv=dv,
            nro_serie_doc=nro_serie_doc,
            tipo_documento=tipo_documento
        )
        
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_nro_serie_nro_documento: {fault}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error en el servicio SOAP",
                codigo_error="SOAP_FAULT",
                detalle=str(fault)
            ).model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_nro_serie_nro_documento: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.get(
    "/cert-nac",
    response_model=RespuestaConsultaCertNacimientoBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar certificado de nacimiento",
    description="Obtiene información del certificado de nacimiento",
    responses={
        200: {"model": RespuestaConsultaCertNacimientoBe, "description": "Información del certificado obtenida correctamente"},
        400: {"description": "Parámetros inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def consulta_certificado_nacimiento(
    id_sistema: int = Query(..., description="ID del sistema que realiza la consulta"),
    rut: int = Query(..., description="RUT de la persona"),
    dv: Optional[str] = Query(None, description="Dígito verificador del RUT"),
    soap_client: ConsultaRcSoapClientService = Depends(get_consulta_rc_soap_client)
) -> Union[RespuestaConsultaCertNacimientoBe, JSONResponse]:
    """
    Consulta información del certificado de nacimiento.
    
    - **id_sistema**: ID del sistema que realiza la consulta
    - **rut**: RUT de la persona
    - **dv**: Dígito verificador del RUT (opcional)
    
    Retorna información completa del certificado de nacimiento incluyendo datos de los padres.
    """
    try:
        logger.info(f"Consultando certificado de nacimiento para RUT: {rut}")
        
        response = await soap_client.consulta_certificado_nacimiento(
            id_sistema=id_sistema,
            rut=rut,
            dv=dv
        )
        
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_certificado_nacimiento: {fault}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error en el servicio SOAP",
                codigo_error="SOAP_FAULT",
                detalle=str(fault)
            ).model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_certificado_nacimiento: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.get(
    "/discapacidad",
    response_model=RespuestaConsultaDiscapacidadBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar discapacidad",
    description="Consulta si una persona tiene alguna discapacidad registrada",
    responses={
        200: {"model": RespuestaConsultaDiscapacidadBe, "description": "Información de discapacidad obtenida correctamente"},
        400: {"description": "Parámetros inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def consulta_discapacidad(
    id_sistema: int = Query(..., description="ID del sistema que realiza la consulta"),
    run: int = Query(..., description="RUN de la persona"),
    dv: Optional[str] = Query(None, description="Dígito verificador del RUN"),
    soap_client: ConsultaRcSoapClientService = Depends(get_consulta_rc_soap_client)
) -> Union[RespuestaConsultaDiscapacidadBe, JSONResponse]:
    """
    Consulta información sobre discapacidad de una persona.
    
    - **id_sistema**: ID del sistema que realiza la consulta
    - **run**: RUN de la persona
    - **dv**: Dígito verificador del RUN (opcional)
    
    Retorna información sobre las discapacidades registradas y sus grados.
    """
    try:
        logger.info(f"Consultando discapacidad para RUN: {run}")
        
        response = await soap_client.consulta_discapacidad(
            id_sistema=id_sistema,
            run=run,
            dv=dv
        )
        
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consulta_discapacidad: {fault}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error en el servicio SOAP",
                codigo_error="SOAP_FAULT",
                detalle=str(fault)
            ).model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en consulta_discapacidad: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/verify",
    response_model=VerifyResponse,
    status_code=status.HTTP_200_OK,
    summary="Verificar huella dactilar (BATCH)",
    description="Verifica la huella dactilar mediante proceso BATCH de BioPortal",
    responses={
        200: {"model": VerifyResponse, "description": "Verificación realizada correctamente"},
        400: {"description": "Datos inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def verify(
    request: VerifyRequest,
    soap_client: ConsultaRcSoapClientService = Depends(get_consulta_rc_soap_client)
) -> Union[VerifyResponse, JSONResponse]:
    """
    Verifica la huella dactilar mediante proceso BATCH de BioPortal.
    
    - **xmlparamin**: XML con los datos de la huella a verificar
    
    Retorna el resultado de la verificación y el XML de respuesta.
    """
    try:
        logger.info(f"Verificando huella dactilar mediante BATCH")
        
        response = await soap_client.verify(xml_param_in=request.xmlparamin)
        
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en verify: {fault}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error en el servicio SOAP",
                codigo_error="SOAP_FAULT",
                detalle=str(fault)
            ).model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en verify: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/huella",
    response_model=RespuestaBeOfRespuestaHuellaDactilarBe,
    status_code=status.HTTP_200_OK,
    summary="Verificar huella dactilar",
    description="Verifica la huella dactilar de una persona",
    responses={
        200: {"model": RespuestaBeOfRespuestaHuellaDactilarBe, "description": "Verificación realizada correctamente"},
        400: {"description": "Datos inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def verificar_huella_dactilar(
    request: VerificarHuellaDactilarRequest,
    soap_client: ConsultaRcSoapClientService = Depends(get_consulta_rc_soap_client)
) -> Union[RespuestaBeOfRespuestaHuellaDactilarBe, JSONResponse]:
    """
    Verifica la huella dactilar de una persona.
    
    - **IdSistema**: ID del sistema que realiza la verificación
    - **Datos**: Datos de la huella dactilar a verificar
    
    Retorna el resultado de la verificación con el puntaje y la respuesta AFIS.
    """
    try:
        logger.info(f"Verificando huella dactilar para RUT: {request.Datos.RutPersona}")
        
        response = await soap_client.verificar_huella_dactilar(
            id_sistema=request.IdSistema,
            datos=request.Datos
        )
        
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en verificar_huella_dactilar: {fault}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error en el servicio SOAP",
                codigo_error="SOAP_FAULT",
                detalle=str(fault)
            ).model_dump()
        )
    except Exception as e:
        logger.error(f"Error inesperado en verificar_huella_dactilar: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        ) 
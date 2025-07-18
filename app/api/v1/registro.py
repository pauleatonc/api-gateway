"""
Endpoints REST para el servicio de Registro de SENCE (WsRegistroCUS)
"""
from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from loguru import logger

from app.models.registro import (
    # Request models
    RegistroPersonaRequest,
    RegistroPersonaCrmRequest,
    RegistrarPersonaSiacOirsRequest,
    RegistroEmpresaRequest,
    ActualizarEmpresaRequest,
    ActualizarRazonSocialRequest,
    ActualizarRepLegalesRequest,
    ActualizarTipoEntidadRequest,
    CambioCusEmpresaRequest,
    RegistroEmpresaOracleRequest,
    # Response models
    RespuestaProcesoBe,
    ErrorResponse,
    TipoEstado
)
from app.services.registro_soap_client import RegistroSoapClientService, registro_soap_client


# Crear router
router = APIRouter(
    prefix="/registro",
    tags=["Registro SENCE"],
    responses={
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)


def get_registro_soap_client() -> RegistroSoapClientService:
    """Dependencia para obtener el cliente SOAP de registro"""
    return registro_soap_client


@router.post(
    "/persona",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Registrar persona",
    description="Registra una persona en el sistema SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Persona registrada correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def registro_persona(
    request: RegistroPersonaRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Registra una persona en el sistema SENCE.
    
    - **idSistema**: ID del sistema que realiza el registro
    - **datosPersona**: Datos completos de la persona a registrar
    
    Retorna el resultado del proceso de registro.
    """
    try:
        logger.info(f"Registrando persona con RUT: {request.datosPersona.Rut}")
        
        response = await soap_client.registro_persona(
            id_sistema=request.idSistema,
            datos_persona=request.datosPersona
        )
        
        # Si hay error de conexión SOAP, devolver 502
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en registro_persona: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/persona/crm",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Registrar persona en CRM",
    description="Registra una persona en el sistema CRM de SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Persona registrada en CRM correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def registro_persona_crm(
    request: RegistroPersonaCrmRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Registra una persona en el sistema CRM de SENCE.
    
    - **idSistema**: ID del sistema que realiza el registro
    - **datosPersona**: Datos de la persona para CRM (incluye datos de contacto)
    
    Retorna el resultado del proceso de registro.
    """
    try:
        logger.info(f"Registrando persona en CRM con RUT: {request.datosPersona.Rut}")
        
        response = await soap_client.registro_persona_crm(
            id_sistema=request.idSistema,
            datos_persona=request.datosPersona
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en registro_persona_crm: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/persona/siac",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Registrar persona en SIAC-OIRS",
    description="Registra una persona en el sistema SIAC-OIRS de SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Persona registrada en SIAC-OIRS correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def registrar_persona_siac_oirs(
    request: RegistrarPersonaSiacOirsRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Registra una persona en el sistema SIAC-OIRS de SENCE.
    
    - **idSistema**: ID del sistema que realiza el registro
    - **datosPersona**: Datos de la persona para SIAC-OIRS
    
    Retorna el resultado del proceso de registro.
    """
    try:
        logger.info(f"Registrando persona en SIAC-OIRS con RUT: {request.datosPersona.Rut}")
        
        response = await soap_client.registrar_persona_siac_oirs(
            id_sistema=request.idSistema,
            datos_persona=request.datosPersona
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en registrar_persona_siac_oirs: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/empresa",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Registrar empresa",
    description="Registra una empresa en el sistema SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Empresa registrada correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def registro_empresa(
    request: RegistroEmpresaRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Registra una empresa en el sistema SENCE.
    
    - **idSistema**: ID del sistema que realiza el registro
    - **datosEmpresa**: Datos completos de la empresa a registrar
    
    Retorna el resultado del proceso de registro.
    """
    try:
        logger.info(f"Registrando empresa con RUT: {request.datosEmpresa.RutEmpresa}")
        
        response = await soap_client.registro_empresa(
            id_sistema=request.idSistema,
            datos_empresa=request.datosEmpresa
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en registro_empresa: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.put(
    "/empresa",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Actualizar empresa",
    description="Actualiza los datos de una empresa en el sistema SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Empresa actualizada correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def actualizar_empresa(
    request: ActualizarEmpresaRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Actualiza los datos de una empresa en el sistema SENCE.
    
    - **idSistema**: ID del sistema que realiza la actualización
    - **datosEmpresa**: Datos actualizados de la empresa
    
    Retorna el resultado del proceso de actualización.
    """
    try:
        logger.info(f"Actualizando empresa con RUT: {request.datosEmpresa.RutEmpresa}")
        
        response = await soap_client.actualizar_empresa(
            id_sistema=request.idSistema,
            datos_empresa=request.datosEmpresa
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en actualizar_empresa: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.patch(
    "/empresa/razon",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Actualizar razón social",
    description="Actualiza la razón social de una empresa en el sistema SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Razón social actualizada correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def actualizar_razon_social(
    request: ActualizarRazonSocialRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Actualiza la razón social de una empresa en el sistema SENCE.
    
    - **idSistema**: ID del sistema que realiza la actualización
    - **rutEmpresa**: RUT de la empresa
    - **dvEmpresa**: Dígito verificador de la empresa
    
    Retorna el resultado del proceso de actualización.
    """
    try:
        logger.info(f"Actualizando razón social para empresa con RUT: {request.rutEmpresa}")
        
        response = await soap_client.actualizar_razon_social(
            id_sistema=request.idSistema,
            rut_empresa=request.rutEmpresa,
            dv_empresa=request.dvEmpresa
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en actualizar_razon_social: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.patch(
    "/empresa/rep-legal",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Actualizar representantes legales",
    description="Actualiza los representantes legales de una empresa en el sistema SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Representantes legales actualizados correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def actualizar_rep_legales(
    request: ActualizarRepLegalesRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Actualiza los representantes legales de una empresa en el sistema SENCE.
    
    - **idSistema**: ID del sistema que realiza la actualización
    - **rutEmpresa**: RUT de la empresa
    - **dvEmpresa**: Dígito verificador de la empresa
    
    Retorna el resultado del proceso de actualización.
    """
    try:
        logger.info(f"Actualizando representantes legales para empresa con RUT: {request.rutEmpresa}")
        
        response = await soap_client.actualizar_rep_legales(
            id_sistema=request.idSistema,
            rut_empresa=request.rutEmpresa,
            dv_empresa=request.dvEmpresa
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en actualizar_rep_legales: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.patch(
    "/empresa/tipo",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Actualizar tipo de entidad",
    description="Actualiza el tipo de entidad de una empresa en el sistema SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Tipo de entidad actualizado correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def actualizar_tipo_entidad(
    request: ActualizarTipoEntidadRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Actualiza el tipo de entidad de una empresa en el sistema SENCE.
    
    - **idSistema**: ID del sistema que realiza la actualización
    - **rutEmpresa**: RUT de la empresa
    - **dvEmpresa**: Dígito verificador de la empresa
    - **tipoEntidad**: Nuevo tipo de entidad (EMPRESA, OTEC, OTIC)
    
    Retorna el resultado del proceso de actualización.
    """
    try:
        logger.info(f"Actualizando tipo de entidad para empresa con RUT: {request.rutEmpresa}")
        
        response = await soap_client.actualizar_tipo_entidad(
            id_sistema=request.idSistema,
            rut_empresa=request.rutEmpresa,
            dv_empresa=request.dvEmpresa,
            tipo_entidad=request.tipoEntidad
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en actualizar_tipo_entidad: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/empresa/con-cus",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Registrar empresa con CUS",
    description="Registra una empresa con código CUS en el sistema SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Empresa registrada con CUS correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def registro_empresa_con_cus(
    request: RegistroEmpresaRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Registra una empresa con código CUS en el sistema SENCE.
    
    - **idSistema**: ID del sistema que realiza el registro
    - **datosEmpresa**: Datos completos de la empresa (incluyendo CUS)
    
    Retorna el resultado del proceso de registro.
    """
    try:
        logger.info(f"Registrando empresa con CUS, RUT: {request.datosEmpresa.RutEmpresa}")
        
        response = await soap_client.registro_empresa_con_cus(
            id_sistema=request.idSistema,
            datos_empresa=request.datosEmpresa
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en registro_empresa_con_cus: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.patch(
    "/empresa/cambio-cus",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Cambiar CUS de empresa",
    description="Cambia el código CUS de una empresa en el sistema SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "CUS cambiado correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def cambio_cus_empresa(
    request: CambioCusEmpresaRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Cambia el código CUS de una empresa en el sistema SENCE.
    
    - **idSistema**: ID del sistema que realiza el cambio
    - **rutEmpresa**: RUT de la empresa
    - **dvRutEmpresa**: Dígito verificador de la empresa
    - **cusActual**: Código CUS actual
    - **nuevaCus**: Nuevo código CUS
    
    Retorna el resultado del proceso de cambio.
    """
    try:
        logger.info(f"Cambiando CUS para empresa con RUT: {request.rutEmpresa}")
        
        response = await soap_client.cambio_cus_empresa(
            id_sistema=request.idSistema,
            rut_empresa=request.rutEmpresa,
            dv_rut_empresa=request.dvRutEmpresa,
            cus_actual=request.cusActual,
            nueva_cus=request.nuevaCus
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en cambio_cus_empresa: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        )


@router.post(
    "/empresa/oracle",
    response_model=RespuestaProcesoBe,
    status_code=status.HTTP_200_OK,
    summary="Registrar empresa en Oracle",
    description="Registra una empresa en el sistema Oracle de SENCE",
    responses={
        200: {"model": RespuestaProcesoBe, "description": "Empresa registrada en Oracle correctamente"},
        400: {"description": "Datos de entrada inválidos"},
        502: {"model": ErrorResponse, "description": "Error del servicio SOAP"}
    }
)
async def registro_empresa_oracle(
    request: RegistroEmpresaOracleRequest,
    soap_client: RegistroSoapClientService = Depends(get_registro_soap_client)
) -> Union[RespuestaProcesoBe, JSONResponse]:
    """
    Registra una empresa en el sistema Oracle de SENCE.
    
    - **idSistema**: ID del sistema que realiza el registro
    - **datosEmpresa**: Datos completos de la empresa para Oracle
    
    Retorna el resultado del proceso de registro.
    """
    try:
        logger.info(f"Registrando empresa en Oracle")
        
        response = await soap_client.registro_empresa_oracle(
            id_sistema=request.idSistema,
            datos_empresa=request.datosEmpresa
        )
        
        if response.estadoProceso in [TipoEstado.ERROR, TipoEstado.EXCEPCION] and response.codigoProceso in [500, 502]:
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content=ErrorResponse(
                    mensaje=response.respuestaProceso,
                    codigo_error="SOAP_ERROR",
                    detalle="Error al comunicarse con el servicio SOAP de registro"
                ).model_dump()
            )
        
        return response
        
    except Exception as e:
        logger.error(f"Error inesperado en registro_empresa_oracle: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                mensaje="Error interno del servidor",
                codigo_error="INTERNAL_ERROR",
                detalle=str(e)
            ).model_dump()
        ) 
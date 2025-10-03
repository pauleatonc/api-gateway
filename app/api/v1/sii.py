"""
Router REST para el servicio SII (Servicio de Impuestos Internos)
"""
from typing import Union
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from zeep.exceptions import Fault
from loguru import logger

from app.models.sii import *
from app.services.sii_soap_client import SiiSoapClientService, sii_soap_client

router = APIRouter(
    prefix="/sii",
    tags=["SII - Servicio de Impuestos Internos"],
    responses={
        502: {
            "model": ErrorResponse,
            "description": "Error del servicio SOAP"
        }
    }
)


def get_sii_soap_client() -> SiiSoapClientService:
    """Dependency injection para el cliente SOAP de SII"""
    return sii_soap_client


@router.post(
    "/representante-legal",
    response_model=RespuestaSiiRepresentanteLegalBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar representante legal",
    description="Entrega el representante legal vigente de un RUT.",
)
async def consultar_representante_legal(
    request: ConsultaRepresentanteLegalRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiRepresentanteLegalBe, JSONResponse]:
    """Consulta representante legal de un RUT"""
    try:
        response = await soap_client.consulta_representante_legal(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_representante_legal: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_representante_legal: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )


@router.post(
    "/relacion-empresa",
    response_model=RespuestaSiiConsIvaBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar relación contribuyente-empresa",
    description="Permite verificar si un contribuyente es o no socio de una empresa.",
)
async def consultar_relacion_contribuyente_empresa(
    request: ConsultaRelacionContribuyenteEmpresaRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiConsIvaBe, JSONResponse]:
    """Consulta relación entre contribuyente y empresa"""
    try:
        response = await soap_client.consulta_relacion_contribuyente_empresa(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_relacion_contribuyente_empresa: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_relacion_contribuyente_empresa: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )


@router.post(
    "/movimiento-contribuyente",
    response_model=RespuestaSiiConsIvaBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar movimiento contribuyente",
    description="Permite verificar si un contribuyente presenta o no movimiento.",
)
async def consultar_movimiento_contribuyente(
    request: ConsultaMovimientoContribuyenteRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiConsIvaBe, JSONResponse]:
    """Consulta movimiento de un contribuyente"""
    try:
        response = await soap_client.consulta_movimiento_contribuyente(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_movimiento_contribuyente: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_movimiento_contribuyente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )


@router.post(
    "/numero-empleados",
    response_model=RespuestaSiiNumeroEmpleadosBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar número de empleados",
    description="Consulta la cantidad de empleados de la empresa.",
)
async def consultar_numero_empleados(
    request: ConsultaNumeroEmpleadosRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiNumeroEmpleadosBe, JSONResponse]:
    """Consulta número de empleados de una empresa"""
    try:
        response = await soap_client.consulta_numero_empleados(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_numero_empleados: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_numero_empleados: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )


@router.post(
    "/categoria-empresa",
    response_model=RespuestaSiiCatEmpBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar categoría empresa",
    description="Consulta la categorización de las empresas según el monto de sus ventas.",
)
async def consultar_categoria_empresa(
    request: ConsultaCategoriaEmpresaRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiCatEmpBe, JSONResponse]:
    """Consulta categoría de una empresa"""
    try:
        response = await soap_client.consulta_categoria_empresa(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_categoria_empresa: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_categoria_empresa: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )


@router.post(
    "/datos-contribuyente",
    response_model=RespuestaSiiDatosContribuyenteBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar datos contribuyente",
    description="Obtiene los datos personales del contribuyente (Persona Natural o Jurídica).",
)
async def consultar_datos_contribuyente(
    request: ConsultaDatosContribuyenteRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiDatosContribuyenteBe, JSONResponse]:
    """Consulta datos personales de un contribuyente"""
    try:
        response = await soap_client.consulta_datos_contribuyente(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_datos_contribuyente: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_datos_contribuyente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )


@router.post(
    "/actividad-economica",
    response_model=RespuestaSiiActividadEconomicaBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar actividad económica",
    description="Informa las actividades económicas asociadas a un contribuyente.",
)
async def consultar_actividad_economica(
    request: ConsultaActividadEconomicaRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiActividadEconomicaBe, JSONResponse]:
    """Consulta actividades económicas de un contribuyente"""
    try:
        response = await soap_client.consulta_actividad_economica(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_actividad_economica: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_actividad_economica: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )


@router.post(
    "/estado-giro",
    response_model=RespuestaSiiEstadoGiroBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar estado giro",
    description="Consulta el estado del giro de un contribuyente.",
)
async def consultar_estado_giro(
    request: ConsultaEstadoGiroRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiEstadoGiroBe, JSONResponse]:
    """Consulta estado del giro de un contribuyente"""
    try:
        response = await soap_client.consulta_estado_giro(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_estado_giro: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_estado_giro: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )


@router.post(
    "/fecha-inicio-actividad",
    response_model=RespuestaSiiFecIniActBe,
    status_code=status.HTTP_200_OK,
    summary="Consultar fecha inicio actividad",
    description="Entrega la fecha de inicio de actividad de un contribuyente.",
)
async def consultar_fecha_inicio_actividad(
    request: ConsultaFechaInicioActividadRequest,
    soap_client: SiiSoapClientService = Depends(get_sii_soap_client)
) -> Union[RespuestaSiiFecIniActBe, JSONResponse]:
    """Consulta fecha de inicio de actividad de un contribuyente"""
    try:
        response = await soap_client.consulta_fecha_inicio_actividad(request)
        return response
        
    except Fault as fault:
        logger.error(f"Error SOAP en consultar_fecha_inicio_actividad: {fault}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(fault)
        )
    except Exception as e:
        logger.error(f"Error inesperado en consultar_fecha_inicio_actividad: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Error interno del servidor"
        )

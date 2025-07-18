"""
Cliente SOAP para el servicio de Identificación de SENCE
"""
from typing import Optional, List, Dict, Any
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from requests import Session
from loguru import logger

from app.config.settings import settings
from app.models.identificacion import (
    IniciarSesionResponse, 
    IniciarSesionPorGuidResponse, 
    IniciarSesionTokenResponse,
    ObtenerListadoURLporRutResponse,
    UrlSistema,
    ErrorResponse
)


class SoapClientService:
    """Cliente SOAP para el servicio de Identificación de SENCE"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.use_mocks = settings.use_soap_mocks
        
        if not self.use_mocks:
            self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente SOAP con configuración optimizada para XML grandes"""
        try:
            # Configurar sesión con timeouts y configuraciones para XML grandes
            session = Session()
            session.verify = True
            
            # Configurar transporte con timeouts y configuraciones para XML grandes
            transport = Transport(
                session=session,
                timeout=settings.soap_timeout,
                operation_timeout=settings.soap_timeout,
                # Configuraciones para manejar XML grandes
                cache=None,  # Desactivar cache para XML grandes
            )
            
            # Crear cliente SOAP
            self.client = Client(
                wsdl=settings.sence_wsdl_url,
                transport=transport,
            )
            
            # Configurar settings para árboles XML grandes
            self.client.settings.strict = False
            self.client.settings.xml_huge_tree = True
            
            logger.info(f"Cliente SOAP inicializado correctamente para: {settings.sence_wsdl_url}")
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente SOAP: {str(e)}")
            raise
    
    def _get_mock_iniciar_sesion(self, usuario: str, clave: str) -> IniciarSesionResponse:
        """Mock para IniciarSesion"""
        if usuario == "test_user" and clave == "test_pass":
            return IniciarSesionResponse(
                success=True,
                token="mock_token_123",
                guid="550e8400-e29b-41d4-a716-446655440000",
                mensaje="Sesión iniciada correctamente (MOCK)",
                codigo_error=None
            )
        else:
            return IniciarSesionResponse(
                success=False,
                token=None,
                guid=None,
                mensaje="Credenciales inválidas (MOCK)",
                codigo_error="AUTH_ERROR"
            )
    
    def _get_mock_iniciar_sesion_por_guid(self, guid: str) -> IniciarSesionPorGuidResponse:
        """Mock para IniciarSesionPorGuid"""
        if guid == "550e8400-e29b-41d4-a716-446655440000":
            return IniciarSesionPorGuidResponse(
                success=True,
                token="mock_token_from_guid_123",
                mensaje="Sesión iniciada correctamente por GUID (MOCK)",
                codigo_error=None
            )
        else:
            return IniciarSesionPorGuidResponse(
                success=False,
                token=None,
                mensaje="GUID inválido (MOCK)",
                codigo_error="GUID_ERROR"
            )
    
    def _get_mock_iniciar_sesion_token(self, token: str) -> IniciarSesionTokenResponse:
        """Mock para IniciarSesionToken"""
        if token in ["mock_token_123", "mock_token_from_guid_123"]:
            return IniciarSesionTokenResponse(
                success=True,
                usuario="test_user",
                mensaje="Token válido (MOCK)",
                codigo_error=None
            )
        else:
            return IniciarSesionTokenResponse(
                success=False,
                usuario=None,
                mensaje="Token inválido (MOCK)",
                codigo_error="TOKEN_ERROR"
            )
    
    def _get_mock_obtener_listado_url_por_rut(self, rut: str) -> ObtenerListadoURLporRutResponse:
        """Mock para ObtenerListadoURLporRut"""
        if rut == "12345678-9":
            return ObtenerListadoURLporRutResponse(
                success=True,
                sistemas=[
                    UrlSistema(
                        nombre="Sistema de Capacitación",
                        url="https://capacitacion.sence.cl",
                        descripcion="Sistema para gestión de capacitaciones"
                    ),
                    UrlSistema(
                        nombre="Sistema de Reportes",
                        url="https://reportes.sence.cl",
                        descripcion="Sistema de generación de reportes"
                    )
                ],
                mensaje="Listado obtenido correctamente (MOCK)",
                codigo_error=None
            )
        else:
            return ObtenerListadoURLporRutResponse(
                success=False,
                sistemas=[],
                mensaje="RUT no encontrado (MOCK)",
                codigo_error="RUT_NOT_FOUND"
            )
    
    async def iniciar_sesion(self, usuario: str, clave: str) -> IniciarSesionResponse:
        """Iniciar sesión con usuario y clave"""
        if self.use_mocks:
            logger.info(f"Usando mock para IniciarSesion con usuario: {usuario}")
            return self._get_mock_iniciar_sesion(usuario, clave)
        
        try:
            logger.info(f"Llamando a IniciarSesion SOAP para usuario: {usuario}")
            result = self.client.service.IniciarSesion(
                usuario=usuario,
                clave=clave
            )
            
            return IniciarSesionResponse(
                success=True,
                token=getattr(result, 'token', None),
                guid=getattr(result, 'guid', None),
                mensaje=getattr(result, 'mensaje', 'Sesión iniciada correctamente'),
                codigo_error=None
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en IniciarSesion: {fault}")
            return IniciarSesionResponse(
                success=False,
                token=None,
                guid=None,
                mensaje=str(fault),
                codigo_error="SOAP_FAULT"
            )
        except Exception as e:
            logger.error(f"Error general en IniciarSesion: {str(e)}")
            return IniciarSesionResponse(
                success=False,
                token=None,
                guid=None,
                mensaje=f"Error de conexión: {str(e)}",
                codigo_error="CONNECTION_ERROR"
            )
    
    async def iniciar_sesion_por_guid(self, guid: str) -> IniciarSesionPorGuidResponse:
        """Iniciar sesión con GUID"""
        if self.use_mocks:
            logger.info(f"Usando mock para IniciarSesionPorGuid con GUID: {guid}")
            return self._get_mock_iniciar_sesion_por_guid(guid)
        
        try:
            logger.info(f"Llamando a IniciarSesionPorGuid SOAP para GUID: {guid}")
            result = self.client.service.IniciarSesionPorGuid(guid=guid)
            
            return IniciarSesionPorGuidResponse(
                success=True,
                token=getattr(result, 'token', None),
                mensaje=getattr(result, 'mensaje', 'Sesión iniciada correctamente'),
                codigo_error=None
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en IniciarSesionPorGuid: {fault}")
            return IniciarSesionPorGuidResponse(
                success=False,
                token=None,
                mensaje=str(fault),
                codigo_error="SOAP_FAULT"
            )
        except Exception as e:
            logger.error(f"Error general en IniciarSesionPorGuid: {str(e)}")
            return IniciarSesionPorGuidResponse(
                success=False,
                token=None,
                mensaje=f"Error de conexión: {str(e)}",
                codigo_error="CONNECTION_ERROR"
            )
    
    async def iniciar_sesion_token(self, token: str) -> IniciarSesionTokenResponse:
        """Validar token de sesión"""
        if self.use_mocks:
            logger.info(f"Usando mock para IniciarSesionToken con token: {token[:10]}...")
            return self._get_mock_iniciar_sesion_token(token)
        
        try:
            logger.info(f"Llamando a IniciarSesionToken SOAP para token: {token[:10]}...")
            result = self.client.service.IniciarSesionToken(token=token)
            
            return IniciarSesionTokenResponse(
                success=True,
                usuario=getattr(result, 'usuario', None),
                mensaje=getattr(result, 'mensaje', 'Token válido'),
                codigo_error=None
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en IniciarSesionToken: {fault}")
            return IniciarSesionTokenResponse(
                success=False,
                usuario=None,
                mensaje=str(fault),
                codigo_error="SOAP_FAULT"
            )
        except Exception as e:
            logger.error(f"Error general en IniciarSesionToken: {str(e)}")
            return IniciarSesionTokenResponse(
                success=False,
                usuario=None,
                mensaje=f"Error de conexión: {str(e)}",
                codigo_error="CONNECTION_ERROR"
            )
    
    async def obtener_listado_url_por_rut(self, rut: str) -> ObtenerListadoURLporRutResponse:
        """Obtener listado de URLs por RUT"""
        if self.use_mocks:
            logger.info(f"Usando mock para ObtenerListadoURLporRut con RUT: {rut}")
            return self._get_mock_obtener_listado_url_por_rut(rut)
        
        try:
            logger.info(f"Llamando a ObtenerListadoURLporRut SOAP para RUT: {rut}")
            result = self.client.service.ObtenerListadoURLporRut(rut=rut)
            
            # Procesar la respuesta del SOAP
            sistemas = []
            if hasattr(result, 'sistemas') and result.sistemas:
                for sistema in result.sistemas:
                    sistemas.append(UrlSistema(
                        nombre=getattr(sistema, 'nombre', ''),
                        url=getattr(sistema, 'url', ''),
                        descripcion=getattr(sistema, 'descripcion', None)
                    ))
            
            return ObtenerListadoURLporRutResponse(
                success=True,
                sistemas=sistemas,
                mensaje=getattr(result, 'mensaje', 'Listado obtenido correctamente'),
                codigo_error=None
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en ObtenerListadoURLporRut: {fault}")
            return ObtenerListadoURLporRutResponse(
                success=False,
                sistemas=[],
                mensaje=str(fault),
                codigo_error="SOAP_FAULT"
            )
        except Exception as e:
            logger.error(f"Error general en ObtenerListadoURLporRut: {str(e)}")
            return ObtenerListadoURLporRutResponse(
                success=False,
                sistemas=[],
                mensaje=f"Error de conexión: {str(e)}",
                codigo_error="CONNECTION_ERROR"
            )


# Instancia global del cliente SOAP
soap_client = SoapClientService() 
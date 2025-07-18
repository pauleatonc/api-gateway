"""
Cliente SOAP para el servicio de Notificación de SENCE
"""
from typing import Optional, List, Union
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.settings import Settings
from requests import Session
from loguru import logger
import base64

from app.config.settings import settings
from app.models.notificacion import (
    RespuestaMailBe, RespuestaProcesoBe, ETipoEstado, EnvioExitosoResponse,
    EnviarSMSRequest, EnviarCorreoPublicoRequest, EnviarListaCorreoPublicoRequest,
    EnviarCorreoPublicoRmRequest
)


class NotificacionSoapClientService:
    """Servicio cliente SOAP para Notificación de SENCE"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.use_mocks = settings.use_soap_mocks
        self.wsdl_url = "https://wsdesa.sence.cl/wscomponentes/wsnotificacion.asmx?wsdl"
        
        if not self.use_mocks:
            self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente SOAP con zeep"""
        try:
            session = Session()
            session.timeout = settings.soap_timeout
            transport = Transport(session=session)
            
            soap_settings = Settings(
                strict=False,
                xml_huge_tree=True
            )
            
            self.client = Client(
                wsdl=self.wsdl_url,
                transport=transport,
                settings=soap_settings
            )
            
            logger.info(f"Cliente SOAP Notificación inicializado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente SOAP Notificación: {str(e)}")
            raise
    
    def _get_mock_response_exitoso(self, tipo_operacion: str) -> EnvioExitosoResponse:
        """Genera respuesta mock exitosa para operaciones simples"""
        return EnvioExitosoResponse(
            success=True,
            mensaje=f"Mock: {tipo_operacion} enviado correctamente"
        )
    
    def _get_mock_response_mail_be(self, tipo_operacion: str) -> RespuestaMailBe:
        """Genera respuesta mock para operaciones que retornan RespuestaMailBe"""
        return RespuestaMailBe(
            estado=RespuestaProcesoBe(
                estadoProceso=ETipoEstado.CORRECTO,
                respuestaProceso=f"Mock: {tipo_operacion} procesado correctamente"
            ),
            mailsNoInsertados=[]
        )
    
    # Métodos para SMS
    async def enviar_sms(self, request: EnviarSMSRequest) -> EnvioExitosoResponse:
        """Envía SMS"""
        if self.use_mocks:
            logger.info(f"Usando mock para EnviarSMS - Celular: {request.celular}")
            return self._get_mock_response_exitoso("SMS")
        
        try:
            result = self.client.service.EnviarSMS(
                idSistema=request.idSistema,
                ambiente=request.ambiente,
                celular=request.celular,
                mensaje=request.mensaje
            )
            
            logger.info(f"SMS enviado exitosamente a {request.celular}")
            return EnvioExitosoResponse(
                success=True,
                mensaje="SMS enviado correctamente"
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en EnviarSMS: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en EnviarSMS: {str(e)}")
            raise
    
    # Métodos para correos públicos
    async def enviar_correo_publico(self, request: EnviarCorreoPublicoRequest) -> EnvioExitosoResponse:
        """Envía correo público"""
        if self.use_mocks:
            logger.info(f"Usando mock para EnviarCorreoPublico - Email: {request.mail}")
            return self._get_mock_response_exitoso("Correo público")
        
        try:
            result = self.client.service.EnviarCorreoPublico(
                idSistema=request.idSistema,
                ambiente=request.ambiente,
                mail=request.mail,
                asunto=request.asunto,
                mensaje=request.mensaje
            )
            
            logger.info(f"Correo público enviado exitosamente a {request.mail}")
            return EnvioExitosoResponse(
                success=True,
                mensaje="Correo público enviado correctamente"
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en EnviarCorreoPublico: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en EnviarCorreoPublico: {str(e)}")
            raise
    
    async def enviar_lista_correo_publico(self, request: EnviarListaCorreoPublicoRequest) -> EnvioExitosoResponse:
        """Envía lista de correos públicos"""
        if self.use_mocks:
            logger.info(f"Usando mock para EnviarListaCorreoPublico - {len(request.lstMails or [])} emails")
            return self._get_mock_response_exitoso("Lista de correos públicos")
        
        try:
            result = self.client.service.EnviarListaCorreoPublico(
                idSistema=request.idSistema,
                ambiente=request.ambiente,
                lstMails=request.lstMails,
                asunto=request.asunto,
                mensaje=request.mensaje
            )
            
            logger.info(f"Lista de correos públicos enviada exitosamente")
            return EnvioExitosoResponse(
                success=True,
                mensaje="Lista de correos públicos enviada correctamente"
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en EnviarListaCorreoPublico: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en EnviarListaCorreoPublico: {str(e)}")
            raise
    
    async def enviar_correo_publico_rm(self, request: EnviarCorreoPublicoRmRequest) -> RespuestaMailBe:
        """Envía correo público con respuesta"""
        if self.use_mocks:
            logger.info(f"Usando mock para EnviarCorreoPublicoRm - Email: {request.mail}")
            return self._get_mock_response_mail_be("Correo público RM")
        
        try:
            result = self.client.service.EnviarCorreoPublicoRm(
                idSistema=request.idSistema,
                ambiente=request.ambiente,
                mail=request.mail,
                asunto=request.asunto,
                mensaje=request.mensaje
            )
            
            logger.info(f"Correo público RM enviado exitosamente a {request.mail}")
            return RespuestaMailBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en EnviarCorreoPublicoRm: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en EnviarCorreoPublicoRm: {str(e)}")
            raise


# Instancia global del cliente
notificacion_soap_client = NotificacionSoapClientService()

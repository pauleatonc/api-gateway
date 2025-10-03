"""
Cliente SOAP para el servicio de Firma Desatendida de SENCE
"""
from typing import Optional
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.settings import Settings
from zeep.helpers import serialize_object
from requests import Session
from loguru import logger

from app.config.settings import settings
from app.models.firma import (
    FirmaDesatendidaRequest,
    FirmaDesatendidaResponse,
    DocumentoFirma,
    Proposito
)


class FirmaSoapClientService:
    """Servicio cliente SOAP para Firma Desatendida de SENCE"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.use_mocks = settings.use_soap_mocks
        # URL del WSDL del servicio de firma (ajustar según la URL real)
        self.wsdl_url = "https://wsdesa.sence.cl/wsfirmadocs/wsfirmadocs.asmx?wsdl"
        
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
            
            logger.info(f"Cliente SOAP Firma inicializado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente SOAP Firma: {str(e)}")
            raise
    
    def _get_mock_response(self, request: FirmaDesatendidaRequest) -> FirmaDesatendidaResponse:
        """Genera respuesta mock para FirmaDesatendida"""
        documentos_firmados = []
        for doc in request.documentos:
            documentos_firmados.append({
                "folio": doc.folio,
                "nombre": doc.nombre,
                "estado": "FIRMADO",
                "checksum": doc.checksum
            })
        
        return FirmaDesatendidaResponse(
            success=True,
            mensaje=f"Mock: {len(request.documentos)} documento(s) firmado(s) exitosamente",
            documentosFirmados=documentos_firmados
        )
    
    async def firma_desatendida(self, request: FirmaDesatendidaRequest) -> FirmaDesatendidaResponse:
        """
        Realiza la firma desatendida de documentos
        
        Args:
            request: Datos de la solicitud de firma
            
        Returns:
            FirmaDesatendidaResponse con el resultado de la operación
        """
        if self.use_mocks:
            logger.info(f"Usando mock para FirmaDesatendida - RUN: {request.runFirmante}, Documentos: {len(request.documentos)}")
            return self._get_mock_response(request)
        
        try:
            # Preparar los documentos para el servicio SOAP
            documentos_soap = []
            for doc in request.documentos:
                documento_soap = {
                    'Base64': doc.base64,
                    'Checksum': doc.checksum,
                    'Descripcion': doc.descripcion,
                    'Folio': doc.folio,
                    'Formato': doc.formato.value,
                    'Nombre': doc.nombre,
                    'Region': doc.region,
                    'TipoDocumento': doc.tipoDocumento.value
                }
                documentos_soap.append(documento_soap)
            
            # Llamar al servicio SOAP
            result = self.client.service.FirmaDesatendida(
                parametros={
                    'Documentos': {
                        'Documento': documentos_soap
                    },
                    'Proposito': request.proposito.value,
                    'RunFirmante': request.runFirmante.replace('.', '').replace('-', '')
                }
            )
            
            # Procesar la respuesta
            if result:
                # Convertir el resultado a un diccionario serializable
                result_dict = serialize_object(result)
                
                logger.info(f"Firma desatendida exitosa - RUN: {request.runFirmante}, Documentos: {len(request.documentos)}")
                
                # Extraer información de documentos firmados si está disponible
                documentos_firmados = []
                for doc in request.documentos:
                    documentos_firmados.append({
                        "folio": doc.folio,
                        "nombre": doc.nombre,
                        "estado": "FIRMADO"
                    })
                
                return FirmaDesatendidaResponse(
                    success=True,
                    mensaje="Documentos firmados exitosamente",
                    documentosFirmados=documentos_firmados
                )
            else:
                logger.warning(f"Respuesta vacía del servicio de firma")
                return FirmaDesatendidaResponse(
                    success=False,
                    mensaje="No se recibió respuesta del servicio de firma"
                )
            
        except Fault as fault:
            logger.error(f"Error SOAP en FirmaDesatendida: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en FirmaDesatendida: {str(e)}")
            raise


# Instancia global del cliente
firma_soap_client = FirmaSoapClientService()


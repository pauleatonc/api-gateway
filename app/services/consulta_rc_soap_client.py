"""
Cliente SOAP para el servicio de Consulta Registro Civil de SENCE
"""
from typing import Optional
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.settings import Settings
from requests import Session
from loguru import logger

from app.config.settings import settings
from app.models.consulta_rc import (
    RespuestaConsultaRunBe,
    RespuestaConsultaNroSerieNroDocBe,
    RespuestaConsultaCertNacimientoBe,
    RespuestaConsultaDiscapacidadBe,
    VerifyResponse,
    RespuestaBeOfRespuestaHuellaDactilarBe,
    ConsultaRunBe,
    DatosRespuestaNroSerieNroDocBe,
    ConsultaCertNacBe,
    ConsultaDiscapacidadBe,
    RespuestaHuellaDactilarBe,
    RespuestaProcesoBe,
    TipoEstado,
    TipoDocumento,
    HuellaDactilarBe,
    ErrorResponse
)


class ConsultaRcSoapClientService:
    """Cliente SOAP para el servicio de Consulta Registro Civil de SENCE"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.use_mocks = settings.use_soap_mocks
        
        # URL del WSDL de consulta registro civil
        self.wsdl_url = "https://wsdesa.sence.cl/WsMiddleware/WsConsulta_SRCeI.asmx?wsdl"
        
        if not self.use_mocks:
            self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente SOAP con configuración para XML grandes"""
        try:
            # Configurar sesión HTTP
            session = Session()
            session.verify = True
            
            # Configurar transporte
            transport = Transport(
                session=session,
                timeout=settings.soap_timeout,
                operation_timeout=settings.soap_timeout,
                cache=None
            )
            
            # Configurar settings de zeep
            zeep_settings = Settings(
                strict=False,
                xml_huge_tree=True,
                forbid_entities=False,
                forbid_external=False,
                forbid_dtd=False
            )
            
            # Crear cliente SOAP
            self.client = Client(
                wsdl=self.wsdl_url,
                transport=transport,
                settings=zeep_settings
            )
            
            logger.info(f"Cliente SOAP de consulta RC inicializado correctamente para: {self.wsdl_url}")
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente SOAP de consulta RC: {str(e)}")
            raise
    
    def _get_mock_consulta_run(self, rut: int, dv: Optional[str] = None) -> RespuestaConsultaRunBe:
        """Mock para ConsultaRun"""
        if rut == 11111111:
            # Simular error
            return RespuestaConsultaRunBe(
                cabecera=RespuestaProcesoBe(
                    estadoProceso=TipoEstado.ERROR,
                    respuestaProceso="RUT no encontrado",
                    codigoProceso=404
                ),
                respuesta=None,
                xmlRespuesta="<error>RUT no encontrado</error>"
            )
        
        return RespuestaConsultaRunBe(
            cabecera=RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                respuestaProceso="Consulta exitosa (MOCK)",
                codigoProceso=200
            ),
            respuesta=ConsultaRunBe(
                rut=rut,
                dv=dv or "9",
                nombres="Juan Carlos",
                apellidoPaterno="Pérez",
                apellidoMaterno="González",
                fechaNacimiento="1990-05-15T00:00:00Z",
                fechaDefuncion=None,
                sexo="M",
                nacionalidad="CHILENA",
                estadoCivil="SOLTERO",
                cantidadHijos=0,
                fechaNacTruncada="1990-05-15",
                fechaDefTruncada=None
            ),
            xmlRespuesta="<ConsultaRun><rut>12345678</rut><nombres>Juan Carlos</nombres></ConsultaRun>"
        )
    
    def _get_mock_consulta_nro_serie(self, rut: int, dv: Optional[str] = None) -> RespuestaConsultaNroSerieNroDocBe:
        """Mock para ConsultaNroSerieNroDocumento"""
        if rut == 11111111:
            return RespuestaConsultaNroSerieNroDocBe(
                cabecera=RespuestaProcesoBe(
                    estadoProceso=TipoEstado.ERROR,
                    respuestaProceso="Error en consulta",
                    codigoProceso=500
                ),
                respuesta=None,
                xmlRespuesta="<error>Error en consulta</error>"
            )
        
        return RespuestaConsultaNroSerieNroDocBe(
            cabecera=RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                respuestaProceso="Consulta exitosa (MOCK)",
                codigoProceso=200
            ),
            respuesta=DatosRespuestaNroSerieNroDocBe(
                EstadoRespuesta="Correcto",
                Rut=rut,
                Dv=dv or "9",
                CodigoTipoDocumento="C",
                CodigoClaseDocumento="CedulaIdentidadParaChileno",
                NumeroDocumento="123456789",
                NumeroSerie="A123456789",
                IndicadorVigencia="S",
                FechaVencimiento="2030-12-31T23:59:59Z",
                IndicadorBloqueo="NO_BLOQUEADO"
            ),
            xmlRespuesta="<ConsultaNroSerie><rut>12345678</rut><vigente>S</vigente></ConsultaNroSerie>"
        )
    
    def _get_mock_consulta_cert_nacimiento(self, rut: int, dv: Optional[str] = None) -> RespuestaConsultaCertNacimientoBe:
        """Mock para ConsultaCertificadoNacimiento"""
        if rut == 11111111:
            return RespuestaConsultaCertNacimientoBe(
                Cabecera=RespuestaProcesoBe(
                    estadoProceso=TipoEstado.ERROR,
                    respuestaProceso="Certificado no encontrado",
                    codigoProceso=404
                ),
                Respuesta=None,
                XmlRespuesta="<error>Certificado no encontrado</error>"
            )
        
        return RespuestaConsultaCertNacimientoBe(
            Cabecera=RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                respuestaProceso="Consulta exitosa (MOCK)",
                codigoProceso=200
            ),
            Respuesta=ConsultaCertNacBe(
                rut=rut,
                dv=dv or "9",
                circunscripcion="SANTIAGO",
                numeroInscripcionNacimiento="12345",
                registroInscripcionNacimiento="CIVIL",
                anioInscripcionNacimiento="1990",
                nombreCompleto="Juan Carlos Pérez González",
                fechaNacimiento="1990-05-15T00:00:00Z",
                sexo="M",
                lugarNacimiento="SANTIAGO",
                nacionalidadNacimiento="CHILENA",
                nombrePadre="Pedro Pérez",
                runPadre="11111111-1",
                nombreMadre="María González",
                runMadre="22222222-2",
                subInscripcionNacimiento="001"
            ),
            XmlRespuesta="<CertificadoNacimiento><rut>12345678</rut><nombre>Juan Carlos</nombre></CertificadoNacimiento>"
        )
    
    def _get_mock_consulta_discapacidad(self, run: int, dv: Optional[str] = None) -> RespuestaConsultaDiscapacidadBe:
        """Mock para ConsultaDiscapacidad"""
        if run == 11111111:
            return RespuestaConsultaDiscapacidadBe(
                Cabecera=RespuestaProcesoBe(
                    estadoProceso=TipoEstado.ERROR,
                    respuestaProceso="Error en consulta",
                    codigoProceso=500
                ),
                Respuesta=None,
                XmlRespuesta="<error>Error en consulta</error>"
            )
        
        return RespuestaConsultaDiscapacidadBe(
            Cabecera=RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                respuestaProceso="Consulta exitosa (MOCK)",
                codigoProceso=200
            ),
            Respuesta=ConsultaDiscapacidadBe(
                Run=run,
                Dv=dv or "9",
                ApareceEnRND="N",
                Discapacidad=None,
                DiscapacidadRn=None
            ),
            XmlRespuesta="<ConsultaDiscapacidad><run>12345678</run><aparece>N</aparece></ConsultaDiscapacidad>"
        )
    
    def _get_mock_verify(self, xml_param: Optional[str] = None) -> VerifyResponse:
        """Mock para Verify"""
        if xml_param and "error" in xml_param.lower():
            return VerifyResponse(
                VerifyResult=0,
                xmlparamout="<error>Error en verificación</error>"
            )
        
        return VerifyResponse(
            VerifyResult=1,
            xmlparamout="<resultado><verificado>true</verificado><puntaje>85</puntaje></resultado>"
        )
    
    def _get_mock_verificar_huella(self, datos: HuellaDactilarBe) -> RespuestaBeOfRespuestaHuellaDactilarBe:
        """Mock para VerificarHuellaDactilar"""
        if datos.RutPersona == 11111111:
                    return RespuestaBeOfRespuestaHuellaDactilarBe(
            decision=False,
            mensaje="Error en verificación",
            mensajeDetalle="RUT no válido para verificación",
            estructuraDatos=None,
            TipoRespuesta="ErrorReglaNegocio"
        )
        
        return RespuestaBeOfRespuestaHuellaDactilarBe(
            decision=True,
            mensaje="Verificación exitosa (MOCK)",
            mensajeDetalle="Huella dactilar verificada correctamente",
            estructuraDatos=RespuestaHuellaDactilarBe(
                Puntaje=85,
                RespuestaAFIS="Hit"
            ),
            TipoRespuesta="CorrectoNegocio"
        )
    
    async def consulta_run(self, id_sistema: int, rut: int, dv: Optional[str] = None) -> RespuestaConsultaRunBe:
        """Consulta información de un RUN"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaRun con RUT: {rut}")
            return self._get_mock_consulta_run(rut, dv)
        
        try:
            logger.info(f"Llamando a ConsultaRun SOAP para RUT: {rut}")
            
            result = self.client.service.ConsultaRun(
                idSistema=id_sistema,
                rut=rut,
                dv=dv
            )
            
            return RespuestaConsultaRunBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaRun: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaRun: {str(e)}")
            raise
    
    async def consulta_nro_serie_nro_documento(self, id_sistema: int, rut: int, dv: Optional[str] = None, 
                                              nro_serie_doc: Optional[str] = None, 
                                              tipo_documento: TipoDocumento = TipoDocumento.C) -> RespuestaConsultaNroSerieNroDocBe:
        """Consulta número de serie o documento"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaNroSerieNroDocumento con RUT: {rut}")
            return self._get_mock_consulta_nro_serie(rut, dv)
        
        try:
            logger.info(f"Llamando a ConsultaNroSerieNroDocumento SOAP para RUT: {rut}")
            
            result = self.client.service.ConsultaNroSerieNroDocumento(
                idSistema=id_sistema,
                rut=rut,
                dv=dv,
                nroSerieDoc=nro_serie_doc,
                tipoDocumento=tipo_documento.value
            )
            
            return RespuestaConsultaNroSerieNroDocBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaNroSerieNroDocumento: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaNroSerieNroDocumento: {str(e)}")
            raise
    
    async def consulta_certificado_nacimiento(self, id_sistema: int, rut: int, dv: Optional[str] = None) -> RespuestaConsultaCertNacimientoBe:
        """Consulta certificado de nacimiento"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaCertificadoNacimiento con RUT: {rut}")
            return self._get_mock_consulta_cert_nacimiento(rut, dv)
        
        try:
            logger.info(f"Llamando a ConsultaCertificadoNacimiento SOAP para RUT: {rut}")
            
            result = self.client.service.ConsultaCertificadoNacimiento(
                idSistema=id_sistema,
                rut=rut,
                dv=dv
            )
            
            return RespuestaConsultaCertNacimientoBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaCertificadoNacimiento: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaCertificadoNacimiento: {str(e)}")
            raise
    
    async def consulta_discapacidad(self, id_sistema: int, run: int, dv: Optional[str] = None) -> RespuestaConsultaDiscapacidadBe:
        """Consulta información de discapacidad"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaDiscapacidad con RUN: {run}")
            return self._get_mock_consulta_discapacidad(run, dv)
        
        try:
            logger.info(f"Llamando a ConsultaDiscapacidad SOAP para RUN: {run}")
            
            result = self.client.service.ConsultaDiscapacidad(
                idSistema=id_sistema,
                run=run,
                dv=dv
            )
            
            return RespuestaConsultaDiscapacidadBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaDiscapacidad: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaDiscapacidad: {str(e)}")
            raise
    
    async def verify(self, xml_param_in: Optional[str] = None) -> VerifyResponse:
        """Verifica huella dactilar mediante proceso BATCH"""
        if self.use_mocks:
            logger.info(f"Usando mock para Verify")
            return self._get_mock_verify(xml_param_in)
        
        try:
            logger.info(f"Llamando a Verify SOAP")
            
            result = self.client.service.Verify(xmlparamin=xml_param_in)
            
            return VerifyResponse.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en Verify: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en Verify: {str(e)}")
            raise
    
    async def verificar_huella_dactilar(self, id_sistema: int, datos: HuellaDactilarBe) -> RespuestaBeOfRespuestaHuellaDactilarBe:
        """Verifica huella dactilar"""
        if self.use_mocks:
            logger.info(f"Usando mock para VerificarHuellaDactilar con RUT: {datos.RutPersona}")
            return self._get_mock_verificar_huella(datos)
        
        try:
            logger.info(f"Llamando a VerificarHuellaDactilar SOAP para RUT: {datos.RutPersona}")
            
            result = self.client.service.VerificarHuellaDactilar(
                IdSistema=id_sistema,
                Datos=datos.model_dump()
            )
            
            return RespuestaBeOfRespuestaHuellaDactilarBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en VerificarHuellaDactilar: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en VerificarHuellaDactilar: {str(e)}")
            raise


# Instancia global del cliente SOAP de consulta RC
consulta_rc_soap_client = ConsultaRcSoapClientService() 
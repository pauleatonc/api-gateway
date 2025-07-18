"""
Cliente SOAP para el servicio de Registro de SENCE (WsRegistroCUS)
"""
from typing import Optional
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.settings import Settings
from requests import Session
from loguru import logger

from app.config.settings import settings
from app.models.registro import (
    RespuestaProcesoBe,
    TipoEstado,
    TipoEmpresa,
    DatosPersona,
    DatosPersonaCrm,
    DatosPersonaSiacOirs,
    DatosEmpresa,
    DatosEmpresaRudo,
    DatosEmpresaOracle,
    ErrorResponse
)


class RegistroSoapClientService:
    """Cliente SOAP para el servicio de Registro de SENCE"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.use_mocks = settings.use_soap_mocks
        
        # URL del WSDL de registro
        self.wsdl_url = "http://srv-ws-ora:8090/WsRegistroCUS/Autenticacion.asmx?wsdl"
        
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
            
            logger.info(f"Cliente SOAP de registro inicializado correctamente para: {self.wsdl_url}")
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente SOAP de registro: {str(e)}")
            raise
    
    def _get_mock_response(self, operation_name: str, success: bool = True) -> RespuestaProcesoBe:
        """Genera una respuesta mock para cualquier operación"""
        if success:
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                codigoProceso=200,
                respuestaProceso=f"Operación {operation_name} exitosa (MOCK)"
            )
        else:
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=500,
                respuestaProceso=f"Error en operación {operation_name} (MOCK)"
            )
    
    async def registro_persona(self, id_sistema: int, datos_persona: DatosPersona) -> RespuestaProcesoBe:
        """Registra una persona en el sistema"""
        if self.use_mocks:
            logger.info(f"Usando mock para RegistroPersona con RUT: {datos_persona.Rut}")
            # Mock: simular error si RUT es 11111111
            success = datos_persona.Rut != 11111111
            return self._get_mock_response("RegistroPersona", success)
        
        try:
            logger.info(f"Llamando a RegistroPersona SOAP para RUT: {datos_persona.Rut}")
            
            result = self.client.service.RegistroPersona(
                idSistema=id_sistema,
                datosPersona=datos_persona.model_dump()
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en RegistroPersona: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en RegistroPersona: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def registro_persona_crm(self, id_sistema: int, datos_persona: DatosPersonaCrm) -> RespuestaProcesoBe:
        """Registra una persona en CRM"""
        if self.use_mocks:
            logger.info(f"Usando mock para RegistroPersonaCrm con RUT: {datos_persona.Rut}")
            success = datos_persona.Rut != 11111111
            return self._get_mock_response("RegistroPersonaCrm", success)
        
        try:
            logger.info(f"Llamando a RegistroPersonaCrm SOAP para RUT: {datos_persona.Rut}")
            
            result = self.client.service.RegistroPersonaCrm(
                idSistema=id_sistema,
                datosPersona=datos_persona.model_dump()
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en RegistroPersonaCrm: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en RegistroPersonaCrm: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def registrar_persona_siac_oirs(self, id_sistema: int, datos_persona: DatosPersonaSiacOirs) -> RespuestaProcesoBe:
        """Registra una persona en SIAC-OIRS"""
        if self.use_mocks:
            logger.info(f"Usando mock para RegistrarPersonaSiacOirs con RUT: {datos_persona.Rut}")
            success = datos_persona.Rut != 11111111
            return self._get_mock_response("RegistrarPersonaSiacOirs", success)
        
        try:
            logger.info(f"Llamando a RegistrarPersonaSiacOirs SOAP para RUT: {datos_persona.Rut}")
            
            result = self.client.service.RegistrarPersonaSiacOirs(
                idSistema=id_sistema,
                datosPersona=datos_persona.model_dump()
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en RegistrarPersonaSiacOirs: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en RegistrarPersonaSiacOirs: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def registro_empresa(self, id_sistema: int, datos_empresa: DatosEmpresa) -> RespuestaProcesoBe:
        """Registra una empresa"""
        if self.use_mocks:
            logger.info(f"Usando mock para RegistroEmpresa con RUT: {datos_empresa.RutEmpresa}")
            success = datos_empresa.RutEmpresa != 11111111
            return self._get_mock_response("RegistroEmpresa", success)
        
        try:
            logger.info(f"Llamando a RegistroEmpresa SOAP para RUT: {datos_empresa.RutEmpresa}")
            
            result = self.client.service.RegistroEmpresa(
                idSistema=id_sistema,
                datosEmpresa=datos_empresa.model_dump()
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en RegistroEmpresa: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en RegistroEmpresa: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def actualizar_empresa(self, id_sistema: int, datos_empresa: DatosEmpresaRudo) -> RespuestaProcesoBe:
        """Actualiza una empresa"""
        if self.use_mocks:
            logger.info(f"Usando mock para ActualizarEmpresa con RUT: {datos_empresa.RutEmpresa}")
            success = datos_empresa.RutEmpresa != 11111111
            return self._get_mock_response("ActualizarEmpresa", success)
        
        try:
            logger.info(f"Llamando a ActualizarEmpresa SOAP para RUT: {datos_empresa.RutEmpresa}")
            
            result = self.client.service.ActualizarEmpresa(
                idSistema=id_sistema,
                datosEmpresa=datos_empresa.model_dump()
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en ActualizarEmpresa: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en ActualizarEmpresa: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def actualizar_razon_social(self, id_sistema: int, rut_empresa: int, dv_empresa: Optional[str] = None) -> RespuestaProcesoBe:
        """Actualiza la razón social de una empresa"""
        if self.use_mocks:
            logger.info(f"Usando mock para ActualizarRazonSocial con RUT: {rut_empresa}")
            success = rut_empresa != 11111111
            return self._get_mock_response("ActualizarRazonSocial", success)
        
        try:
            logger.info(f"Llamando a ActualizarRazonSocial SOAP para RUT: {rut_empresa}")
            
            result = self.client.service.ActualizarRazonSocial(
                idSistema=id_sistema,
                rutEmpresa=rut_empresa,
                dvEmpresa=dv_empresa
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en ActualizarRazonSocial: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en ActualizarRazonSocial: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def actualizar_rep_legales(self, id_sistema: int, rut_empresa: int, dv_empresa: Optional[str] = None) -> RespuestaProcesoBe:
        """Actualiza los representantes legales de una empresa"""
        if self.use_mocks:
            logger.info(f"Usando mock para ActualizarRepLegales con RUT: {rut_empresa}")
            success = rut_empresa != 11111111
            return self._get_mock_response("ActualizarRepLegales", success)
        
        try:
            logger.info(f"Llamando a ActualizarRepLegales SOAP para RUT: {rut_empresa}")
            
            result = self.client.service.ActualizarRepLegales(
                idSistema=id_sistema,
                rutEmpresa=rut_empresa,
                dvEmpresa=dv_empresa
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en ActualizarRepLegales: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en ActualizarRepLegales: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def actualizar_tipo_entidad(self, id_sistema: int, rut_empresa: int, dv_empresa: Optional[str], tipo_entidad: TipoEmpresa) -> RespuestaProcesoBe:
        """Actualiza el tipo de entidad de una empresa"""
        if self.use_mocks:
            logger.info(f"Usando mock para ActualizarTipoEntidad con RUT: {rut_empresa}")
            success = rut_empresa != 11111111
            return self._get_mock_response("ActualizarTipoEntidad", success)
        
        try:
            logger.info(f"Llamando a ActualizarTipoEntidad SOAP para RUT: {rut_empresa}")
            
            result = self.client.service.ActualizarTipoEntidad(
                idSistema=id_sistema,
                rutEmpresa=rut_empresa,
                dvEmpresa=dv_empresa,
                tipoEntidad=tipo_entidad.value
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en ActualizarTipoEntidad: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en ActualizarTipoEntidad: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def registro_empresa_con_cus(self, id_sistema: int, datos_empresa: DatosEmpresa) -> RespuestaProcesoBe:
        """Registra una empresa con CUS"""
        if self.use_mocks:
            logger.info(f"Usando mock para RegistroEmpresaConCus con RUT: {datos_empresa.RutEmpresa}")
            success = datos_empresa.RutEmpresa != 11111111
            return self._get_mock_response("RegistroEmpresaConCus", success)
        
        try:
            logger.info(f"Llamando a RegistroEmpresaConCus SOAP para RUT: {datos_empresa.RutEmpresa}")
            
            result = self.client.service.RegistroEmpresaConCus(
                idSistema=id_sistema,
                datosEmpresa=datos_empresa.model_dump()
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en RegistroEmpresaConCus: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en RegistroEmpresaConCus: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def cambio_cus_empresa(self, id_sistema: int, rut_empresa: int, dv_rut_empresa: Optional[str], cus_actual: Optional[str], nueva_cus: Optional[str]) -> RespuestaProcesoBe:
        """Cambia el CUS de una empresa"""
        if self.use_mocks:
            logger.info(f"Usando mock para CambioCusEmpresa con RUT: {rut_empresa}")
            success = rut_empresa != 11111111
            return self._get_mock_response("CambioCusEmpresa", success)
        
        try:
            logger.info(f"Llamando a CambioCusEmpresa SOAP para RUT: {rut_empresa}")
            
            result = self.client.service.CambioCusEmpresa(
                idSistema=id_sistema,
                rutEmpresa=rut_empresa,
                dvRutEmpresa=dv_rut_empresa,
                cusActual=cus_actual,
                nuevaCus=nueva_cus
            )
            
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado(result.estadoProceso),
                codigoProceso=result.codigoProceso,
                respuestaProceso=result.respuestaProceso
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en CambioCusEmpresa: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en CambioCusEmpresa: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )
    
    async def registro_empresa_oracle(self, id_sistema: int, datos_empresa: DatosEmpresaOracle) -> RespuestaProcesoBe:
        """Registra una empresa en Oracle"""
        if self.use_mocks:
            logger.info(f"Usando mock para RegistroEmpresaOracle")
            # Mock simplificado para Oracle
            return self._get_mock_response("RegistroEmpresaOracle", True)
        
        try:
            logger.info(f"Llamando a RegistroEmpresaOracle SOAP")
            
            result = self.client.service.RegistroEmpresaOracle(
                idSistema=id_sistema,
                datosEmpresa=datos_empresa.model_dump()
            )
            
            # Note: Oracle response might be different, adjust as needed
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                codigoProceso=200,
                respuestaProceso="Registro Oracle exitoso"
            )
            
        except Fault as fault:
            logger.error(f"Error SOAP en RegistroEmpresaOracle: {fault}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.ERROR,
                codigoProceso=502,
                respuestaProceso=f"Error SOAP: {str(fault)}"
            )
        except Exception as e:
            logger.error(f"Error general en RegistroEmpresaOracle: {str(e)}")
            return RespuestaProcesoBe(
                estadoProceso=TipoEstado.EXCEPCION,
                codigoProceso=500,
                respuestaProceso=f"Error de conexión: {str(e)}"
            )


# Instancia global del cliente SOAP de registro
registro_soap_client = RegistroSoapClientService() 
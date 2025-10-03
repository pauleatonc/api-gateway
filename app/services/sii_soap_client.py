"""
Cliente SOAP para el servicio SII (Servicio de Impuestos Internos)
"""
from typing import Optional
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.settings import Settings
from requests import Session
from loguru import logger
from datetime import datetime

from app.config.settings import settings
from app.models.sii import *


class SiiSoapClientService:
    """Servicio cliente SOAP para SII"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.use_mocks = settings.use_soap_mocks
        self.wsdl_url = "https://wsdesa.sence.cl/WsMiddleware/WsConsulta_SII.asmx?wsdl"
        
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
            
            logger.info(f"Cliente SOAP SII inicializado exitosamente")
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente SOAP SII: {str(e)}")
            raise
    
    def _get_mock_respuesta_proceso(self, operacion: str) -> RespuestaProcesoBe:
        """Genera respuesta proceso mock"""
        return RespuestaProcesoBe(
            estadoProceso=ETipoEstado.CORRECTO,
            respuestaProceso=f"Mock: {operacion} procesado correctamente",
            codigoProceso=200
        )
    
    def _get_mock_datos_glosa(self) -> RespuestaSiiDatosGlosa:
        """Genera datos glosa mock"""
        return RespuestaSiiDatosGlosa(
            fechaInicioActividad=datetime.now(),
            glosa="Mock: Glosa de ejemplo",
            estado="ACTIVO"
        )
    
    # Métodos para cada operación SOAP
    
    async def consulta_representante_legal(self, request: ConsultaRepresentanteLegalRequest) -> RespuestaSiiRepresentanteLegalBe:
        """Consulta representante legal"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaRepresentanteLegal - RUT: {request.rut}")
            return RespuestaSiiRepresentanteLegalBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaRepresentanteLegal"),
                respuesta=RepresentanteLegalSiiBe(
                    representantes=[
                        RepresentanteLegalSii(
                            rut=87654321,
                            dv="0",
                            fechaInicio="2023-01-01"
                        )
                    ],
                    datosGenerales=self._get_mock_datos_glosa()
                ),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaRepresentanteLegal(
                idSistema=request.idSistema,
                rut=request.rut,
                dv=request.dv
            )
            
            logger.info(f"ConsultaRepresentanteLegal ejecutada exitosamente para RUT: {request.rut}")
            return RespuestaSiiRepresentanteLegalBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaRepresentanteLegal: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaRepresentanteLegal: {str(e)}")
            raise
    
    async def consulta_relacion_contribuyente_empresa(self, request: ConsultaRelacionContribuyenteEmpresaRequest) -> RespuestaSiiConsIvaBe:
        """Consulta relación contribuyente empresa"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaRelacionContribuyenteEmpresa")
            return RespuestaSiiConsIvaBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaRelacionContribuyenteEmpresa"),
                respuesta=self._get_mock_datos_glosa(),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaRelacionContribuyenteEmpresa(
                idSistema=request.idSistema,
                rutEmp=request.rutEmp,
                dvEmp=request.dvEmp,
                rutSoc=request.rutSoc,
                dvSoc=request.dvSoc
            )
            
            logger.info(f"ConsultaRelacionContribuyenteEmpresa ejecutada exitosamente")
            return RespuestaSiiConsIvaBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaRelacionContribuyenteEmpresa: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaRelacionContribuyenteEmpresa: {str(e)}")
            raise
    
    async def consulta_movimiento_contribuyente(self, request: ConsultaMovimientoContribuyenteRequest) -> RespuestaSiiConsIvaBe:
        """Consulta movimiento contribuyente"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaMovimientoContribuyente")
            return RespuestaSiiConsIvaBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaMovimientoContribuyente"),
                respuesta=self._get_mock_datos_glosa(),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaMovimientoContribuyente(
                idSistema=request.idSistema,
                rutCont=request.rutCont,
                dvCont=request.dvCont,
                periodoTrib=request.periodoTrib
            )
            
            logger.info(f"ConsultaMovimientoContribuyente ejecutada exitosamente")
            return RespuestaSiiConsIvaBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaMovimientoContribuyente: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaMovimientoContribuyente: {str(e)}")
            raise
    
    async def consulta_numero_empleados(self, request: ConsultaNumeroEmpleadosRequest) -> RespuestaSiiNumeroEmpleadosBe:
        """Consulta número de empleados"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaNumeroEmpleados")
            return RespuestaSiiNumeroEmpleadosBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaNumeroEmpleados"),
                respuesta=ConsultaSiiNumeroEmpleadosBe(
                    fechaInicioActividad=datetime.now(),
                    glosa="Mock: Empresa con empleados",
                    estado="ACTIVO",
                    numeroEmpleados="50"
                ),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaNumeroEmpleados(
                idSistema=request.idSistema,
                rut=request.rut,
                dv=request.dv,
                periodo=request.periodo
            )
            
            logger.info(f"ConsultaNumeroEmpleados ejecutada exitosamente")
            return RespuestaSiiNumeroEmpleadosBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaNumeroEmpleados: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaNumeroEmpleados: {str(e)}")
            raise
    
    async def consulta_categoria_empresa(self, request: ConsultaCategoriaEmpresaRequest) -> RespuestaSiiCatEmpBe:
        """Consulta categoría empresa"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaCategoriaEmpresa")
            return RespuestaSiiCatEmpBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaCategoriaEmpresa"),
                respuesta=ConsultaSiiCatEmpBe(
                    fechaInicioActividad=datetime.now(),
                    glosa="Mock: Empresa mediana",
                    estado="ACTIVO",
                    tipo="MEDIANA",
                    glosaTipo="Empresa mediana según ventas",
                    cantPeriodo="12"
                ),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaCategoriaEmpresa(
                idSistema=request.idSistema,
                rut=request.rut,
                dv=request.dv,
                fecha=request.fecha,
                tipoConsulta=request.tipoConsulta
            )
            
            logger.info(f"ConsultaCategoriaEmpresa ejecutada exitosamente")
            return RespuestaSiiCatEmpBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaCategoriaEmpresa: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaCategoriaEmpresa: {str(e)}")
            raise
    
    async def consulta_datos_contribuyente(self, request: ConsultaDatosContribuyenteRequest) -> RespuestaSiiDatosContribuyenteBe:
        """Consulta datos contribuyente"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaDatosContribuyente")
            return RespuestaSiiDatosContribuyenteBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaDatosContribuyente"),
                respuesta=RespuestaSiiDatosGenerales(
                    estado="ACTIVO",
                    glosa="Mock: Contribuyente activo",
                    razonSocial="Empresa Mock S.A.",
                    nombre="Juan",
                    apPaterno="Pérez",
                    apMaterno="González",
                    xml="<mock>XML de datos</mock>"
                ),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaDatosContribuyente(
                idSistema=request.idSistema,
                rut=request.rut,
                dv=request.dv
            )
            
            logger.info(f"ConsultaDatosContribuyente ejecutada exitosamente")
            return RespuestaSiiDatosContribuyenteBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaDatosContribuyente: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaDatosContribuyente: {str(e)}")
            raise
    
    async def consulta_actividad_economica(self, request: ConsultaActividadEconomicaRequest) -> RespuestaSiiActividadEconomicaBe:
        """Consulta actividad económica"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaActividadEconomica")
            return RespuestaSiiActividadEconomicaBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaActividadEconomica"),
                respuesta=RespuestaSiiActEconomicaBe(
                    fechaInicioActividad=datetime.now(),
                    glosa="Mock: Actividades económicas",
                    estado="ACTIVO",
                    actividadEconomica=[
                        ActEconomicaBe(
                            actividad=620900,
                            categoria=1,
                            descripcion="Otras actividades de informática",
                            fechaInic=datetime.now()
                        )
                    ]
                ),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaActividadEconomica(
                idSistema=request.idSistema,
                rut=request.rut,
                dv=request.dv
            )
            
            logger.info(f"ConsultaActividadEconomica ejecutada exitosamente")
            return RespuestaSiiActividadEconomicaBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaActividadEconomica: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaActividadEconomica: {str(e)}")
            raise
    
    async def consulta_estado_giro(self, request: ConsultaEstadoGiroRequest) -> RespuestaSiiEstadoGiroBe:
        """Consulta estado giro"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaEstadoGiro")
            return RespuestaSiiEstadoGiroBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaEstadoGiro"),
                respuesta=self._get_mock_datos_glosa(),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaEstadoGiro(
                idSistema=request.idSistema,
                rut=request.rut,
                dv=request.dv
            )
            
            logger.info(f"ConsultaEstadoGiro ejecutada exitosamente")
            return RespuestaSiiEstadoGiroBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaEstadoGiro: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaEstadoGiro: {str(e)}")
            raise
    
    async def consulta_fecha_inicio_actividad(self, request: ConsultaFechaInicioActividadRequest) -> RespuestaSiiFecIniActBe:
        """Consulta fecha inicio actividad"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaFechaInicioActividad")
            return RespuestaSiiFecIniActBe(
                cabecera=self._get_mock_respuesta_proceso("ConsultaFechaInicioActividad"),
                respuesta=self._get_mock_datos_glosa(),
                xmlRespuesta="<mock>XML de respuesta</mock>"
            )
        
        try:
            result = self.client.service.ConsultaFechaInicioActividad(
                idSistema=request.idSistema,
                rut=request.rut,
                dv=request.dv
            )
            
            logger.info(f"ConsultaFechaInicioActividad ejecutada exitosamente")
            return RespuestaSiiFecIniActBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaFechaInicioActividad: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaFechaInicioActividad: {str(e)}")
            raise


# Instancia global del cliente
sii_soap_client = SiiSoapClientService()

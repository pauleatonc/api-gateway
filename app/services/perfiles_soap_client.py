"""
Cliente SOAP para el servicio de Perfiles de SENCE
"""
from typing import Optional, List
from zeep import Client
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.settings import Settings
from requests import Session
from loguru import logger

from app.config.settings import settings
from app.models.perfiles import (
    RespuestaPerfilesBe, AutorizacionBe, UsuarioBe, PerfilBe, FuncionBe,
    UsuarioEmpresaBe, PerfilSistemaBe, EstadoAcceso, ETipoPersona, EEstado,
    ETipoPerfil, ERegion, SolicitarPerfilUsuarioRequest, BloquearPerfilRequest,
    AsignarPerfilRequest
)


class PerfilesSoapClientService:
    """Servicio cliente SOAP para Perfiles de SENCE"""
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.use_mocks = settings.use_soap_mocks
        self.wsdl_url = "https://wsdesa.sence.cl/WSComponentes/WsPerfiles.asmx?wsdl"
        
        if not self.use_mocks:
            self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa el cliente SOAP con zeep"""
        try:
            # Configurar transport con timeout
            session = Session()
            session.timeout = settings.soap_timeout
            transport = Transport(session=session)
            
            # Configurar settings para manejo de XML grandes
            soap_settings = Settings(
                strict=False,
                xml_huge_tree=True
            )
            
            # Inicializar cliente
            self.client = Client(
                wsdl=self.wsdl_url,
                transport=transport,
                settings=soap_settings
            )
            
            logger.info(f"Cliente SOAP Perfiles inicializado exitosamente con WSDL: {self.wsdl_url}")
            
        except Exception as e:
            logger.error(f"Error al inicializar cliente SOAP Perfiles: {str(e)}")
            raise
    
    def _get_mock_response(self, operation_name: str, include_users: bool = True) -> RespuestaPerfilesBe:
        """Genera respuesta mock para desarrollo"""
        mock_autorizacion = AutorizacionBe(
            acceso=EstadoAcceso.AUTORIZADO.value,
            codigo=200,
            descripcion="Acceso autorizado"
        )
        
        mock_usuarios = []
        if include_users:
            mock_usuarios = [
                UsuarioBe(
                    idUsuario=1,
                    nombre="Juan Carlos",
                    apellidoPaterno="Pérez",
                    apellidoMaterno="González",
                    tipoPersona=ETipoPersona.PERSONA_NATURAL.value
                ),
                UsuarioBe(
                    idUsuario=2,
                    nombre="María Elena",
                    apellidoPaterno="Rodríguez",
                    apellidoMaterno="López",
                    tipoPersona=ETipoPersona.PERSONA_NATURAL.value
                )
            ]
        
        mock_funciones = [
            FuncionBe(
                idFuncion=1,
                nombreFuncion="Consultar datos",
                obligatorio=True,
                denegado=False,
                estado=EEstado.ACTIVO.value
            ),
            FuncionBe(
                idFuncion=2,
                nombreFuncion="Modificar datos",
                obligatorio=False,
                denegado=False,
                estado=EEstado.ACTIVO.value
            )
        ]
        
        mock_perfiles = [
            PerfilBe(
                idPerfil=1,
                nombrePerfil="Administrador",
                estado=EEstado.ACTIVO.value,
                tipoPerfil=ETipoPerfil.ADMINISTRADOR.value,
                region=ERegion.REGION_METROPOLITANA_DE_SANTIAGO.value,
                funcion=mock_funciones
            )
        ]
        
        mock_perfil_sistema = PerfilSistemaBe(
            idSistema=1,
            nombreSistema="Sistema de Pruebas",
            perfil=mock_perfiles
        )
        
        mock_empresas = [
            UsuarioEmpresaBe(
                idUsuarioEmpresa=1,
                razonSocial="Empresa de Pruebas S.A.",
                tipoEmpresa="Sociedad Anónima",
                tipoPersona=ETipoPersona.PERSONA_JURIDICA.value
            )
        ]
        
        return RespuestaPerfilesBe(
            autorizacion=mock_autorizacion,
            usuario=mock_usuarios,
            perfil=mock_perfil_sistema,
            funcion=mock_funciones,
            usuarioEmpresa=mock_empresas
        )
    
    async def consulta_usuarios_por_perfil_sistema(self, id_sistema: int, id_perfil: int) -> RespuestaPerfilesBe:
        """Consulta usuarios por perfil y sistema"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaUsuariosPorPerfilSistema - Sistema: {id_sistema}, Perfil: {id_perfil}")
            return self._get_mock_response("ConsultaUsuariosPorPerfilSistema")
        
        try:
            result = self.client.service.ConsultaUsuariosPorPerfilSistema(
                idSistema=id_sistema,
                idPerfil=id_perfil
            )
            
            logger.info(f"Respuesta exitosa de ConsultaUsuariosPorPerfilSistema")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaUsuariosPorPerfilSistema: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaUsuariosPorPerfilSistema: {str(e)}")
            raise
    
    async def consulta_perfil_usuario_sistema_por_rut(self, rut_persona: int, id_sistema: int, tipo_persona: str) -> RespuestaPerfilesBe:
        """Consulta perfil de usuario por RUT"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaPerfilUsuarioSistemaPorRut - RUT: {rut_persona}")
            return self._get_mock_response("ConsultaPerfilUsuarioSistemaPorRut")
        
        try:
            result = self.client.service.ConsultaPerfilUsuarioSistemaPorRut(
                rutPersona=rut_persona,
                idSistema=id_sistema,
                tipoPersona=tipo_persona
            )
            
            logger.info(f"Respuesta exitosa de ConsultaPerfilUsuarioSistemaPorRut")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaPerfilUsuarioSistemaPorRut: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaPerfilUsuarioSistemaPorRut: {str(e)}")
            raise
    
    async def consulta_perfil_por_sistema(self, id_sistema: int) -> RespuestaPerfilesBe:
        """Consulta perfiles por sistema"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaPerfilPorSistema - Sistema: {id_sistema}")
            return self._get_mock_response("ConsultaPerfilPorSistema", include_users=False)
        
        try:
            result = self.client.service.ConsultaPerfilPorSistema(idSistema=id_sistema)
            
            logger.info(f"Respuesta exitosa de ConsultaPerfilPorSistema")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaPerfilPorSistema: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaPerfilPorSistema: {str(e)}")
            raise
    
    async def consulta_funciones_por_sistema(self, id_sistema: int) -> RespuestaPerfilesBe:
        """Consulta funciones por sistema"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaFuncionesPorSistema - Sistema: {id_sistema}")
            return self._get_mock_response("ConsultaFuncionesPorSistema", include_users=False)
        
        try:
            result = self.client.service.ConsultaFuncionesPorSistema(idSistema=id_sistema)
            
            logger.info(f"Respuesta exitosa de ConsultaFuncionesPorSistema")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaFuncionesPorSistema: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaFuncionesPorSistema: {str(e)}")
            raise
    
    async def consulta_funciones_por_perfil_sistema(self, id_perfil: int, id_sistema: int) -> RespuestaPerfilesBe:
        """Consulta funciones por perfil y sistema"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaFuncionesPorPerfilSistema - Perfil: {id_perfil}, Sistema: {id_sistema}")
            return self._get_mock_response("ConsultaFuncionesPorPerfilSistema", include_users=False)
        
        try:
            result = self.client.service.ConsultaFuncionesPorPerfilSistema(
                idPerfil=id_perfil,
                idSistema=id_sistema
            )
            
            logger.info(f"Respuesta exitosa de ConsultaFuncionesPorPerfilSistema")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaFuncionesPorPerfilSistema: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaFuncionesPorPerfilSistema: {str(e)}")
            raise
    
    async def consulta_empresas_por_perfil_sistema(self, id_sistema: int, id_perfil: int) -> RespuestaPerfilesBe:
        """Consulta empresas por perfil y sistema"""
        if self.use_mocks:
            logger.info(f"Usando mock para ConsultaEmpresasPorPerfilSistema - Sistema: {id_sistema}, Perfil: {id_perfil}")
            return self._get_mock_response("ConsultaEmpresasPorPerfilSistema", include_users=False)
        
        try:
            result = self.client.service.ConsultaEmpresasPorPerfilSistema(
                idSistema=id_sistema,
                idPerfil=id_perfil
            )
            
            logger.info(f"Respuesta exitosa de ConsultaEmpresasPorPerfilSistema")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en ConsultaEmpresasPorPerfilSistema: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en ConsultaEmpresasPorPerfilSistema: {str(e)}")
            raise
    
    async def solicitar_perfil_usuario(self, request: SolicitarPerfilUsuarioRequest) -> RespuestaPerfilesBe:
        """Solicita perfil para usuario"""
        if self.use_mocks:
            logger.info(f"Usando mock para SolicitarPerfilUsuario - Usuario: {request.rutUsuario}")
            return self._get_mock_response("SolicitarPerfilUsuario", include_users=False)
        
        try:
            result = self.client.service.SolicitarPerfilUsuario(
                idSistema=request.idSistema,
                idPerfil=request.idPerfil,
                rutUsuario=request.rutUsuario,
                motivoSolicitud=request.motivoSolicitud,
                idRegion=request.idRegion,
                tipoPersona=request.tipoPersona,
                rutUsrUpdate=request.rutUsrUpdate
            )
            
            logger.info(f"Respuesta exitosa de SolicitarPerfilUsuario")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en SolicitarPerfilUsuario: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en SolicitarPerfilUsuario: {str(e)}")
            raise
    
    async def bloquear_perfil_sistema_usuario_por_rut(self, request: BloquearPerfilRequest) -> RespuestaPerfilesBe:
        """Bloquea perfil de usuario"""
        if self.use_mocks:
            logger.info(f"Usando mock para BloquearPerfilSistemaUsuarioPorRut - Usuario: {request.rutUsuario}")
            return self._get_mock_response("BloquearPerfilSistemaUsuarioPorRut", include_users=False)
        
        try:
            result = self.client.service.BloquearPerfilSistemaUsuarioPorRut(
                idSistema=request.idSistema,
                idPerfil=request.idPerfil,
                rutUsuario=request.rutUsuario,
                tipoPersona=request.tipoPersona,
                rutUsrUpdate=request.rutUsrUpdate
            )
            
            logger.info(f"Respuesta exitosa de BloquearPerfilSistemaUsuarioPorRut")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en BloquearPerfilSistemaUsuarioPorRut: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en BloquearPerfilSistemaUsuarioPorRut: {str(e)}")
            raise
    
    async def asignar_perfil_sistema_usuario_por_rut(self, request: AsignarPerfilRequest) -> RespuestaPerfilesBe:
        """Asigna perfil a usuario"""
        if self.use_mocks:
            logger.info(f"Usando mock para AsignarPerfilSistemaUsuarioPorRut - Usuario: {request.rutUsuario}")
            return self._get_mock_response("AsignarPerfilSistemaUsuarioPorRut", include_users=False)
        
        try:
            result = self.client.service.AsignarPerfilSistemaUsuarioPorRut(
                idSistema=request.idSistema,
                idPerfil=request.idPerfil,
                region=request.region,
                rutUsuario=request.rutUsuario,
                tipoPersona=request.tipoPersona,
                rutUsrUpdate=request.rutUsrUpdate
            )
            
            logger.info(f"Respuesta exitosa de AsignarPerfilSistemaUsuarioPorRut")
            return RespuestaPerfilesBe.model_validate(result)
            
        except Fault as fault:
            logger.error(f"Error SOAP en AsignarPerfilSistemaUsuarioPorRut: {fault}")
            raise
        except Exception as e:
            logger.error(f"Error general en AsignarPerfilSistemaUsuarioPorRut: {str(e)}")
            raise


# Instancia global del cliente
perfiles_soap_client = PerfilesSoapClientService() 
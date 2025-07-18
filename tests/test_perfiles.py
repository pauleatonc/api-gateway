"""
Tests unitarios para el módulo de Perfiles de SENCE
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from fastapi import status
from zeep.exceptions import Fault

from app.main import app
from app.models.perfiles import (
    RespuestaPerfilesBe, AutorizacionBe, UsuarioBe, PerfilBe, FuncionBe,
    UsuarioEmpresaBe, PerfilSistemaBe, ErrorResponse, EstadoAcceso,
    ETipoPersona, EEstado, ETipoPerfil, ERegion, SolicitarPerfilUsuarioRequest,
    BloquearPerfilRequest, AsignarPerfilRequest
)
from app.services.perfiles_soap_client import PerfilesSoapClientService

client = TestClient(app)


@pytest.fixture
def mock_perfiles_soap_client():
    """Fixture para mockear el cliente SOAP de perfiles"""
    return Mock(spec=PerfilesSoapClientService)


@pytest.fixture
def mock_perfiles_soap_client_dependency(mock_perfiles_soap_client):
    """Fixture para inyectar el mock como dependencia"""
    def get_mock_perfiles_soap_client():
        return mock_perfiles_soap_client
    
    from app.api.v1.perfiles import get_perfiles_soap_client
    app.dependency_overrides[get_perfiles_soap_client] = get_mock_perfiles_soap_client
    
    yield mock_perfiles_soap_client
    
    # Limpiar overrides después del test
    app.dependency_overrides.clear()


@pytest.fixture
def sample_respuesta_perfiles():
    """Fixture con datos de ejemplo para RespuestaPerfilesBe"""
    return RespuestaPerfilesBe(
        autorizacion=AutorizacionBe(
            acceso=EstadoAcceso.AUTORIZADO.value,
            codigo=200,
            descripcion="Acceso autorizado"
        ),
        usuario=[
            UsuarioBe(
                idUsuario=1,
                nombre="Juan Carlos",
                apellidoPaterno="Pérez",
                apellidoMaterno="González",
                tipoPersona=ETipoPersona.PERSONA_NATURAL.value
            )
        ],
        perfil=PerfilSistemaBe(
            idSistema=1,
            nombreSistema="Sistema de Pruebas",
            perfil=[
                PerfilBe(
                    idPerfil=1,
                    nombrePerfil="Administrador",
                    estado=EEstado.ACTIVO.value,
                    tipoPerfil=ETipoPerfil.ADMINISTRADOR.value,
                    region=ERegion.REGION_METROPOLITANA_DE_SANTIAGO.value
                )
            ]
        ),
        funcion=[
            FuncionBe(
                idFuncion=1,
                nombreFuncion="Consultar datos",
                obligatorio=True,
                denegado=False,
                estado=EEstado.ACTIVO.value
            )
        ],
        usuarioEmpresa=[
            UsuarioEmpresaBe(
                idUsuarioEmpresa=1,
                razonSocial="Empresa de Pruebas S.A.",
                tipoEmpresa="Sociedad Anónima",
                tipoPersona=ETipoPersona.PERSONA_JURIDICA.value
            )
        ]
    )


@pytest.fixture
def sample_solicitar_perfil_request():
    """Fixture con datos de ejemplo para SolicitarPerfilUsuarioRequest"""
    return {
        "idSistema": 1,
        "idPerfil": 1,
        "rutUsuario": 12345678,
        "motivoSolicitud": "Solicitud de acceso",
        "idRegion": 13,
        "tipoPersona": "PersonaNatural",
        "rutUsrUpdate": 87654321
    }


@pytest.fixture
def sample_bloquear_perfil_request():
    """Fixture con datos de ejemplo para BloquearPerfilRequest"""
    return {
        "idSistema": 1,
        "idPerfil": 1,
        "rutUsuario": 12345678,
        "tipoPersona": "PersonaNatural",
        "rutUsrUpdate": 87654321
    }


@pytest.fixture
def sample_asignar_perfil_request():
    """Fixture con datos de ejemplo para AsignarPerfilRequest"""
    return {
        "idSistema": 1,
        "idPerfil": 1,
        "region": "Region_Metropolitana_de_Santiago",
        "rutUsuario": 12345678,
        "tipoPersona": "PersonaNatural",
        "rutUsrUpdate": 87654321
    }


class TestConsultaUsuariosPorPerfilSistema:
    """Tests para consulta de usuarios por perfil y sistema"""
    
    def test_consulta_usuarios_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles):
        """Test exitoso de consulta de usuarios por perfil y sistema"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.consulta_usuarios_por_perfil_sistema = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/usuarios",
            params={"id_sistema": 1, "id_perfil": 1}
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert "usuario" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
        assert len(data["usuario"]) == 1
    
    def test_consulta_usuarios_error_soap(self, mock_perfiles_soap_client_dependency):
        """Test error SOAP en consulta de usuarios"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.consulta_usuarios_por_perfil_sistema = AsyncMock(
            side_effect=Fault("Sistema no encontrado")
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/usuarios",
            params={"id_sistema": 1, "id_perfil": 1}
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]
    
    def test_consulta_usuarios_parametros_requeridos(self):
        """Test validación de parámetros requeridos"""
        # Request sin parámetros
        response = client.get("/api/v1/perfiles/usuarios")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Request con un parámetro faltante
        response = client.get("/api/v1/perfiles/usuarios", params={"id_sistema": 1})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestConsultaPerfilUsuarioSistemaPorRut:
    """Tests para consulta de perfil de usuario por RUT"""
    
    def test_consulta_perfil_usuario_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles):
        """Test exitoso de consulta de perfil de usuario por RUT"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.consulta_perfil_usuario_sistema_por_rut = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/usuarios/12345678",
            params={"id_sistema": 1, "tipo_persona": "PersonaNatural"}
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert "perfil" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
    
    def test_consulta_perfil_usuario_error_soap(self, mock_perfiles_soap_client_dependency):
        """Test error SOAP en consulta de perfil de usuario"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.consulta_perfil_usuario_sistema_por_rut = AsyncMock(
            side_effect=Fault("Usuario no encontrado")
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/usuarios/12345678",
            params={"id_sistema": 1, "tipo_persona": "PersonaNatural"}
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]


class TestConsultaPerfilPorSistema:
    """Tests para consulta de perfiles por sistema"""
    
    def test_consulta_perfil_por_sistema_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles):
        """Test exitoso de consulta de perfiles por sistema"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.consulta_perfil_por_sistema = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/perfiles",
            params={"id_sistema": 1}
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert "perfil" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
    
    def test_consulta_perfil_por_sistema_error_soap(self, mock_perfiles_soap_client_dependency):
        """Test error SOAP en consulta de perfiles por sistema"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.consulta_perfil_por_sistema = AsyncMock(
            side_effect=Fault("Sistema no encontrado")
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/perfiles",
            params={"id_sistema": 1}
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]


class TestConsultaFuncionesPorSistema:
    """Tests para consulta de funciones por sistema"""
    
    def test_consulta_funciones_por_sistema_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles):
        """Test exitoso de consulta de funciones por sistema"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.consulta_funciones_por_sistema = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/funciones",
            params={"id_sistema": 1}
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert "funcion" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
    
    def test_consulta_funciones_por_sistema_error_soap(self, mock_perfiles_soap_client_dependency):
        """Test error SOAP en consulta de funciones por sistema"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.consulta_funciones_por_sistema = AsyncMock(
            side_effect=Fault("Sistema no encontrado")
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/funciones",
            params={"id_sistema": 1}
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]


class TestConsultaFuncionesPorPerfilSistema:
    """Tests para consulta de funciones por perfil y sistema"""
    
    def test_consulta_funciones_por_perfil_sistema_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles):
        """Test exitoso de consulta de funciones por perfil y sistema"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.consulta_funciones_por_perfil_sistema = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/funciones/por-perfil",
            params={"id_perfil": 1, "id_sistema": 1}
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert "funcion" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
    
    def test_consulta_funciones_por_perfil_sistema_error_soap(self, mock_perfiles_soap_client_dependency):
        """Test error SOAP en consulta de funciones por perfil y sistema"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.consulta_funciones_por_perfil_sistema = AsyncMock(
            side_effect=Fault("Perfil no encontrado")
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/funciones/por-perfil",
            params={"id_perfil": 1, "id_sistema": 1}
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]


class TestConsultaEmpresasPorPerfilSistema:
    """Tests para consulta de empresas por perfil y sistema"""
    
    def test_consulta_empresas_por_perfil_sistema_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles):
        """Test exitoso de consulta de empresas por perfil y sistema"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.consulta_empresas_por_perfil_sistema = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/empresas",
            params={"id_sistema": 1, "id_perfil": 1}
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert "usuarioEmpresa" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
    
    def test_consulta_empresas_por_perfil_sistema_error_soap(self, mock_perfiles_soap_client_dependency):
        """Test error SOAP en consulta de empresas por perfil y sistema"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.consulta_empresas_por_perfil_sistema = AsyncMock(
            side_effect=Fault("Sistema no encontrado")
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/empresas",
            params={"id_sistema": 1, "id_perfil": 1}
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]


class TestSolicitarPerfilUsuario:
    """Tests para solicitar perfil de usuario"""
    
    def test_solicitar_perfil_usuario_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles, sample_solicitar_perfil_request):
        """Test exitoso de solicitud de perfil de usuario"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.solicitar_perfil_usuario = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.post(
            "/api/v1/perfiles/solicitar",
            json=sample_solicitar_perfil_request
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
    
    def test_solicitar_perfil_usuario_error_soap(self, mock_perfiles_soap_client_dependency, sample_solicitar_perfil_request):
        """Test error SOAP en solicitud de perfil de usuario"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.solicitar_perfil_usuario = AsyncMock(
            side_effect=Fault("Usuario no encontrado")
        )
        
        # Hacer request
        response = client.post(
            "/api/v1/perfiles/solicitar",
            json=sample_solicitar_perfil_request
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]
    
    def test_solicitar_perfil_usuario_datos_invalidos(self):
        """Test validación de datos inválidos en solicitud de perfil"""
        # Request con datos faltantes
        response = client.post(
            "/api/v1/perfiles/solicitar",
            json={"idSistema": 1}  # Faltan campos requeridos
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestBloquearPerfilUsuario:
    """Tests para bloquear perfil de usuario"""
    
    def test_bloquear_perfil_usuario_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles, sample_bloquear_perfil_request):
        """Test exitoso de bloqueo de perfil de usuario"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.bloquear_perfil_sistema_usuario_por_rut = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.post(
            "/api/v1/perfiles/bloquear",
            json=sample_bloquear_perfil_request
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
    
    def test_bloquear_perfil_usuario_error_soap(self, mock_perfiles_soap_client_dependency, sample_bloquear_perfil_request):
        """Test error SOAP en bloqueo de perfil de usuario"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.bloquear_perfil_sistema_usuario_por_rut = AsyncMock(
            side_effect=Fault("Usuario no encontrado")
        )
        
        # Hacer request
        response = client.post(
            "/api/v1/perfiles/bloquear",
            json=sample_bloquear_perfil_request
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]


class TestAsignarPerfilUsuario:
    """Tests para asignar perfil de usuario"""
    
    def test_asignar_perfil_usuario_exitoso(self, mock_perfiles_soap_client_dependency, sample_respuesta_perfiles, sample_asignar_perfil_request):
        """Test exitoso de asignación de perfil de usuario"""
        # Configurar mock
        mock_perfiles_soap_client_dependency.asignar_perfil_sistema_usuario_por_rut = AsyncMock(
            return_value=sample_respuesta_perfiles
        )
        
        # Hacer request
        response = client.post(
            "/api/v1/perfiles/asignar",
            json=sample_asignar_perfil_request
        )
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "autorizacion" in data
        assert data["autorizacion"]["acceso"] == "Autorizado"
    
    def test_asignar_perfil_usuario_error_soap(self, mock_perfiles_soap_client_dependency, sample_asignar_perfil_request):
        """Test error SOAP en asignación de perfil de usuario"""
        # Configurar mock para lanzar Fault
        mock_perfiles_soap_client_dependency.asignar_perfil_sistema_usuario_por_rut = AsyncMock(
            side_effect=Fault("Usuario no encontrado")
        )
        
        # Hacer request
        response = client.post(
            "/api/v1/perfiles/asignar",
            json=sample_asignar_perfil_request
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]
    
    def test_asignar_perfil_usuario_datos_invalidos(self):
        """Test validación de datos inválidos en asignación de perfil"""
        # Request con datos faltantes
        response = client.post(
            "/api/v1/perfiles/asignar",
            json={"idSistema": 1}  # Faltan campos requeridos
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestErrorHandling:
    """Tests para manejo de errores generales"""
    
    def test_error_interno_servidor(self, mock_perfiles_soap_client_dependency):
        """Test manejo de errores internos del servidor"""
        # Configurar mock para lanzar excepción general
        mock_perfiles_soap_client_dependency.consulta_usuarios_por_perfil_sistema = AsyncMock(
            side_effect=Exception("Error interno")
        )
        
        # Hacer request
        response = client.get(
            "/api/v1/perfiles/usuarios",
            params={"id_sistema": 1, "id_perfil": 1}
        )
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "INTERNAL_ERROR" in data["codigo_error"] 
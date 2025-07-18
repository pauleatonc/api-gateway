"""
Tests para el módulo de identificación de SENCE
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, AsyncMock
from fastapi import status

from app.main import app
from app.models.identificacion import (
    IniciarSesionResponse,
    IniciarSesionPorGuidResponse,
    IniciarSesionTokenResponse,
    ObtenerListadoURLporRutResponse,
    UrlSistema,
    ErrorResponse
)
from app.services.soap_client import SoapClientService


# Crear cliente de prueba
client = TestClient(app)


@pytest.fixture
def mock_soap_client():
    """Fixture para crear un mock del cliente SOAP"""
    return Mock(spec=SoapClientService)


@pytest.fixture
def mock_soap_client_dependency(mock_soap_client):
    """Fixture para sobrescribir la dependencia del cliente SOAP"""
    def get_mock_soap_client():
        return mock_soap_client
    
    from app.api.v1.identificacion import get_soap_client
    app.dependency_overrides[get_soap_client] = get_mock_soap_client
    
    yield mock_soap_client
    
    # Limpiar después del test
    app.dependency_overrides.clear()


class TestIniciarSesion:
    """Tests para el endpoint de iniciar sesión"""
    
    def test_iniciar_sesion_exitoso(self, mock_soap_client_dependency):
        """Test de inicio de sesión exitoso"""
        # Configurar mock
        mock_soap_client_dependency.iniciar_sesion = AsyncMock(return_value=IniciarSesionResponse(
            success=True,
            token="test_token_123",
            guid="550e8400-e29b-41d4-a716-446655440000",
            mensaje="Sesión iniciada correctamente",
            codigo_error=None
        ))
        
        # Realizar petición
        response = client.post("/api/v1/auth/login", json={
            "usuario": "test_user",
            "clave": "test_pass"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["token"] == "test_token_123"
        assert data["guid"] == "550e8400-e29b-41d4-a716-446655440000"
        assert data["mensaje"] == "Sesión iniciada correctamente"
        assert data["codigo_error"] is None
        
        # Verificar que se llamó al método correcto
        mock_soap_client_dependency.iniciar_sesion.assert_called_once_with(
            usuario="test_user",
            clave="test_pass"
        )
    
    def test_iniciar_sesion_credenciales_invalidas(self, mock_soap_client_dependency):
        """Test de inicio de sesión con credenciales inválidas"""
        # Configurar mock
        mock_soap_client_dependency.iniciar_sesion = AsyncMock(return_value=IniciarSesionResponse(
            success=False,
            token=None,
            guid=None,
            mensaje="Credenciales inválidas",
            codigo_error="AUTH_ERROR"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/auth/login", json={
            "usuario": "invalid_user",
            "clave": "invalid_pass"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert data["token"] is None
        assert data["guid"] is None
        assert data["mensaje"] == "Credenciales inválidas"
        assert data["codigo_error"] == "AUTH_ERROR"
    
    def test_iniciar_sesion_error_soap(self, mock_soap_client_dependency):
        """Test de inicio de sesión con error SOAP"""
        # Configurar mock
        mock_soap_client_dependency.iniciar_sesion = AsyncMock(return_value=IniciarSesionResponse(
            success=False,
            token=None,
            guid=None,
            mensaje="Error de conexión SOAP",
            codigo_error="SOAP_FAULT"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/auth/login", json={
            "usuario": "test_user",
            "clave": "test_pass"
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["mensaje"] == "Error de conexión SOAP"
        assert data["codigo_error"] == "SOAP_FAULT"
    
    def test_iniciar_sesion_datos_invalidos(self, mock_soap_client_dependency):
        """Test de inicio de sesión con datos inválidos"""
        # Realizar petición sin clave
        response = client.post("/api/v1/auth/login", json={
            "usuario": "test_user"
        })
        
        # Verificar respuesta (debe devolver 422)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_iniciar_sesion_excepcion_inesperada(self, mock_soap_client_dependency):
        """Test de inicio de sesión con excepción inesperada"""
        # Configurar mock para lanzar excepción
        mock_soap_client_dependency.iniciar_sesion = AsyncMock(side_effect=Exception("Error inesperado"))
        
        # Realizar petición
        response = client.post("/api/v1/auth/login", json={
            "usuario": "test_user",
            "clave": "test_pass"
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "INTERNAL_ERROR"


class TestIniciarSesionPorGuid:
    """Tests para el endpoint de iniciar sesión por GUID"""
    
    def test_iniciar_sesion_por_guid_exitoso(self, mock_soap_client_dependency):
        """Test de inicio de sesión por GUID exitoso"""
        # Configurar mock
        mock_soap_client_dependency.iniciar_sesion_por_guid = AsyncMock(return_value=IniciarSesionPorGuidResponse(
            success=True,
            token="test_token_from_guid",
            mensaje="Sesión iniciada correctamente por GUID",
            codigo_error=None
        ))
        
        # Realizar petición
        response = client.post("/api/v1/auth/login/guid", json={
            "guid": "550e8400-e29b-41d4-a716-446655440000"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["token"] == "test_token_from_guid"
        assert data["mensaje"] == "Sesión iniciada correctamente por GUID"
        assert data["codigo_error"] is None
    
    def test_iniciar_sesion_por_guid_invalido(self, mock_soap_client_dependency):
        """Test de inicio de sesión por GUID inválido"""
        # Configurar mock
        mock_soap_client_dependency.iniciar_sesion_por_guid = AsyncMock(return_value=IniciarSesionPorGuidResponse(
            success=False,
            token=None,
            mensaje="GUID inválido",
            codigo_error="GUID_ERROR"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/auth/login/guid", json={
            "guid": "invalid-guid"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert data["token"] is None
        assert data["mensaje"] == "GUID inválido"
        assert data["codigo_error"] == "GUID_ERROR"


class TestIniciarSesionToken:
    """Tests para el endpoint de validar token"""
    
    def test_iniciar_sesion_token_exitoso(self, mock_soap_client_dependency):
        """Test de validación de token exitoso"""
        # Configurar mock
        mock_soap_client_dependency.iniciar_sesion_token = AsyncMock(return_value=IniciarSesionTokenResponse(
            success=True,
            usuario="test_user",
            mensaje="Token válido",
            codigo_error=None
        ))
        
        # Realizar petición
        response = client.post("/api/v1/auth/login/token", json={
            "token": "valid_token_123"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert data["usuario"] == "test_user"
        assert data["mensaje"] == "Token válido"
        assert data["codigo_error"] is None
    
    def test_iniciar_sesion_token_invalido(self, mock_soap_client_dependency):
        """Test de validación de token inválido"""
        # Configurar mock
        mock_soap_client_dependency.iniciar_sesion_token = AsyncMock(return_value=IniciarSesionTokenResponse(
            success=False,
            usuario=None,
            mensaje="Token inválido",
            codigo_error="TOKEN_ERROR"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/auth/login/token", json={
            "token": "invalid_token"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert data["usuario"] is None
        assert data["mensaje"] == "Token inválido"
        assert data["codigo_error"] == "TOKEN_ERROR"


class TestObtenerListadoURLporRut:
    """Tests para el endpoint de obtener listado de URLs por RUT"""
    
    def test_obtener_listado_url_por_rut_exitoso(self, mock_soap_client_dependency):
        """Test de obtener listado de URLs exitoso"""
        # Configurar mock
        mock_soap_client_dependency.obtener_listado_url_por_rut = AsyncMock(return_value=ObtenerListadoURLporRutResponse(
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
            mensaje="Listado obtenido correctamente",
            codigo_error=None
        ))
        
        # Realizar petición
        response = client.get("/api/v1/auth/systems/12345678-9")
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert len(data["sistemas"]) == 2
        assert data["sistemas"][0]["nombre"] == "Sistema de Capacitación"
        assert data["sistemas"][0]["url"] == "https://capacitacion.sence.cl"
        assert data["sistemas"][1]["nombre"] == "Sistema de Reportes"
        assert data["mensaje"] == "Listado obtenido correctamente"
        assert data["codigo_error"] is None
    
    def test_obtener_listado_url_por_rut_no_encontrado(self, mock_soap_client_dependency):
        """Test de obtener listado de URLs para RUT no encontrado"""
        # Configurar mock
        mock_soap_client_dependency.obtener_listado_url_por_rut = AsyncMock(return_value=ObtenerListadoURLporRutResponse(
            success=False,
            sistemas=[],
            mensaje="RUT no encontrado",
            codigo_error="RUT_NOT_FOUND"
        ))
        
        # Realizar petición
        response = client.get("/api/v1/auth/systems/99999999-9")
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is False
        assert len(data["sistemas"]) == 0
        assert data["mensaje"] == "RUT no encontrado"
        assert data["codigo_error"] == "RUT_NOT_FOUND"
    
    def test_obtener_listado_url_por_rut_invalido(self, mock_soap_client_dependency):
        """Test de obtener listado de URLs con RUT inválido"""
        # Realizar petición con RUT muy corto
        response = client.get("/api/v1/auth/systems/123")
        
        # Verificar respuesta (debe devolver 422)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_obtener_listado_url_por_rut_error_conexion(self, mock_soap_client_dependency):
        """Test de obtener listado de URLs con error de conexión"""
        # Configurar mock
        mock_soap_client_dependency.obtener_listado_url_por_rut = AsyncMock(return_value=ObtenerListadoURLporRutResponse(
            success=False,
            sistemas=[],
            mensaje="Error de conexión",
            codigo_error="CONNECTION_ERROR"
        ))
        
        # Realizar petición
        response = client.get("/api/v1/auth/systems/12345678-9")
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "CONNECTION_ERROR"


class TestIntegracionCompleta:
    """Tests de integración completa con mocks habilitados"""
    
    def test_flujo_completo_con_mocks(self):
        """Test del flujo completo usando mocks del sistema"""
        # Configurar variables de entorno para usar mocks
        with patch.dict('os.environ', {'USE_SOAP_MOCKS': 'true'}):
            # 1. Iniciar sesión
            response = client.post("/api/v1/auth/login", json={
                "usuario": "test_user",
                "clave": "test_pass"
            })
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "token" in data
            assert "guid" in data
            
            # 2. Usar el GUID para iniciar sesión
            guid = data["guid"]
            response = client.post("/api/v1/auth/login/guid", json={
                "guid": guid
            })
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert "token" in data
            
            # 3. Validar el token
            token = data["token"]
            response = client.post("/api/v1/auth/login/token", json={
                "token": token
            })
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert data["usuario"] == "test_user"
            
            # 4. Obtener sistemas para un RUT válido
            response = client.get("/api/v1/auth/systems/12345678-9")
            assert response.status_code == status.HTTP_200_OK
            data = response.json()
            assert data["success"] is True
            assert len(data["sistemas"]) > 0
    
    def test_endpoints_con_datos_invalidos(self):
        """Test de todos los endpoints con datos inválidos"""
        # Test con datos faltantes
        response = client.post("/api/v1/auth/login", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        response = client.post("/api/v1/auth/login/guid", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        response = client.post("/api/v1/auth/login/token", json={})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test con RUT muy corto
        response = client.get("/api/v1/auth/systems/123")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        # Test con RUT muy largo
        response = client.get("/api/v1/auth/systems/123456789012345")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
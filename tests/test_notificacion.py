"""
Tests unitarios para el módulo de Notificación de SENCE
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from fastapi import status
from zeep.exceptions import Fault
import base64

from app.main import app
from app.models.notificacion import (
    EnvioExitosoResponse, RespuestaMailBe, RespuestaProcesoBe, ETipoEstado,
    ErrorResponse, EnviarSMSRequest, EnviarCorreoPublicoRequest,
    EnviarListaCorreoPublicoRequest, EnviarCorreoPublicoRmRequest
)
from app.services.notificacion_soap_client import NotificacionSoapClientService

client = TestClient(app)


@pytest.fixture
def mock_notificacion_soap_client():
    """Fixture para mockear el cliente SOAP de notificación"""
    return Mock(spec=NotificacionSoapClientService)


@pytest.fixture
def mock_notificacion_soap_client_dependency(mock_notificacion_soap_client):
    """Fixture para inyectar el mock como dependencia"""
    def get_mock_notificacion_soap_client():
        return mock_notificacion_soap_client
    
    from app.api.v1.notificacion import get_notificacion_soap_client
    app.dependency_overrides[get_notificacion_soap_client] = get_mock_notificacion_soap_client
    
    yield mock_notificacion_soap_client
    
    # Limpiar overrides después del test
    app.dependency_overrides.clear()


@pytest.fixture
def sample_envio_exitoso_response():
    """Fixture con datos de ejemplo para EnvioExitosoResponse"""
    return EnvioExitosoResponse(
        success=True,
        mensaje="Operación realizada correctamente"
    )


@pytest.fixture
def sample_respuesta_mail_be():
    """Fixture con datos de ejemplo para RespuestaMailBe"""
    return RespuestaMailBe(
        estado=RespuestaProcesoBe(
            estadoProceso=ETipoEstado.CORRECTO,
            respuestaProceso="Correo enviado correctamente"
        ),
        mailsNoInsertados=[]
    )


class TestEnviarSMS:
    """Tests para envío de SMS"""
    
    def test_enviar_sms_exitoso(self, mock_notificacion_soap_client_dependency, sample_envio_exitoso_response):
        """Test exitoso de envío de SMS"""
        # Configurar mock
        mock_notificacion_soap_client_dependency.enviar_sms = AsyncMock(
            return_value=sample_envio_exitoso_response
        )
        
        # Datos del request
        sms_data = {
            "idSistema": 1,
            "ambiente": "desarrollo",
            "celular": 987654321,
            "mensaje": "Mensaje de prueba SMS"
        }
        
        # Hacer request
        response = client.post("/api/v1/notificacion/sms", json=sms_data)
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "correctamente" in data["mensaje"]
    
    def test_enviar_sms_error_soap(self, mock_notificacion_soap_client_dependency):
        """Test error SOAP en envío de SMS"""
        # Configurar mock para lanzar Fault
        mock_notificacion_soap_client_dependency.enviar_sms = AsyncMock(
            side_effect=Fault("Error en servicio SMS")
        )
        
        # Datos del request
        sms_data = {
            "idSistema": 1,
            "ambiente": "desarrollo",
            "celular": 987654321,
            "mensaje": "Mensaje de prueba SMS"
        }
        
        # Hacer request
        response = client.post("/api/v1/notificacion/sms", json=sms_data)
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]
    
    def test_enviar_sms_datos_invalidos(self):
        """Test validación de datos inválidos en SMS"""
        # Request con número de celular inválido
        sms_data = {
            "idSistema": 1,
            "celular": 123,  # Número muy corto
            "mensaje": "Mensaje de prueba"
        }
        
        response = client.post("/api/v1/notificacion/sms", json=sms_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestEnviarCorreoPublico:
    """Tests para envío de correos públicos"""
    
    def test_enviar_correo_publico_exitoso(self, mock_notificacion_soap_client_dependency, sample_envio_exitoso_response):
        """Test exitoso de envío de correo público"""
        # Configurar mock
        mock_notificacion_soap_client_dependency.enviar_correo_publico = AsyncMock(
            return_value=sample_envio_exitoso_response
        )
        
        # Datos del request
        correo_data = {
            "idSistema": 1,
            "ambiente": "desarrollo",
            "mail": "usuario@ejemplo.com",
            "asunto": "Asunto de prueba",
            "mensaje": "Contenido del correo de prueba"
        }
        
        # Hacer request
        response = client.post("/api/v1/notificacion/correo/publico", json=correo_data)
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "correctamente" in data["mensaje"]
    
    def test_enviar_correo_publico_error_soap(self, mock_notificacion_soap_client_dependency):
        """Test error SOAP en envío de correo público"""
        # Configurar mock para lanzar Fault
        mock_notificacion_soap_client_dependency.enviar_correo_publico = AsyncMock(
            side_effect=Fault("Error en servicio de correo")
        )
        
        # Datos del request
        correo_data = {
            "idSistema": 1,
            "ambiente": "desarrollo",
            "mail": "usuario@ejemplo.com",
            "asunto": "Asunto de prueba",
            "mensaje": "Contenido del correo de prueba"
        }
        
        # Hacer request
        response = client.post("/api/v1/notificacion/correo/publico", json=correo_data)
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]


class TestEnviarCorreoPublicoRm:
    """Tests para envío de correos públicos con respuesta"""
    
    def test_enviar_correo_publico_rm_exitoso(self, mock_notificacion_soap_client_dependency, sample_respuesta_mail_be):
        """Test exitoso de envío de correo público con respuesta"""
        # Configurar mock
        mock_notificacion_soap_client_dependency.enviar_correo_publico_rm = AsyncMock(
            return_value=sample_respuesta_mail_be
        )
        
        # Datos del request
        correo_data = {
            "idSistema": 1,
            "ambiente": "desarrollo",
            "mail": "usuario@ejemplo.com",
            "asunto": "Asunto de prueba RM",
            "mensaje": "Contenido del correo RM"
        }
        
        # Hacer request
        response = client.post("/api/v1/notificacion/correo/publico/rm", json=correo_data)
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "estado" in data
        assert data["estado"]["estadoProceso"] == "CORRECTO"
    
    def test_enviar_correo_publico_rm_error_soap(self, mock_notificacion_soap_client_dependency):
        """Test error SOAP en envío de correo público RM"""
        # Configurar mock para lanzar Fault
        mock_notificacion_soap_client_dependency.enviar_correo_publico_rm = AsyncMock(
            side_effect=Fault("Error en servicio de correo RM")
        )
        
        # Datos del request
        correo_data = {
            "idSistema": 1,
            "mail": "usuario@ejemplo.com",
            "asunto": "Asunto de prueba RM",
            "mensaje": "Contenido del correo RM"
        }
        
        # Hacer request
        response = client.post("/api/v1/notificacion/correo/publico/rm", json=correo_data)
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert "SOAP_FAULT" in data["codigo_error"]

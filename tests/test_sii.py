"""
Tests unitarios para el módulo SII (Servicio de Impuestos Internos)
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from fastapi import status
from zeep.exceptions import Fault
from datetime import datetime

from app.main import app
from app.models.sii import *
from app.services.sii_soap_client import SiiSoapClientService

client = TestClient(app)


@pytest.fixture
def mock_sii_soap_client():
    """Fixture para mockear el cliente SOAP de SII"""
    return Mock(spec=SiiSoapClientService)


@pytest.fixture
def mock_sii_soap_client_dependency(mock_sii_soap_client):
    """Fixture para inyectar el mock como dependencia"""
    def get_mock_sii_soap_client():
        return mock_sii_soap_client
    
    from app.api.v1.sii import get_sii_soap_client
    app.dependency_overrides[get_sii_soap_client] = get_mock_sii_soap_client
    
    yield mock_sii_soap_client
    
    # Limpiar overrides después del test
    app.dependency_overrides.clear()


@pytest.fixture
def sample_respuesta_proceso():
    """Fixture con datos de ejemplo para RespuestaProcesoBe"""
    return RespuestaProcesoBe(
        estadoProceso=ETipoEstado.CORRECTO,
        respuestaProceso="Consulta exitosa",
        codigoProceso=200
    )


@pytest.fixture
def sample_datos_glosa():
    """Fixture con datos de ejemplo para RespuestaSiiDatosGlosa"""
    return RespuestaSiiDatosGlosa(
        fechaInicioActividad=datetime.now(),
        glosa="Glosa de ejemplo",
        estado="ACTIVO"
    )


class TestConsultaRepresentanteLegal:
    """Tests para consulta de representante legal"""
    
    def test_consulta_representante_legal_exitoso(self, mock_sii_soap_client_dependency, sample_respuesta_proceso, sample_datos_glosa):
        """Test exitoso de consulta de representante legal"""
        # Configurar mock
        mock_response = RespuestaSiiRepresentanteLegalBe(
            cabecera=sample_respuesta_proceso,
            respuesta=RepresentanteLegalSiiBe(
                representantes=[
                    RepresentanteLegalSii(
                        rut=87654321,
                        dv="0",
                        fechaInicio="2023-01-01"
                    )
                ],
                datosGenerales=sample_datos_glosa
            ),
            xmlRespuesta="<mock>XML de respuesta</mock>"
        )
        
        mock_sii_soap_client_dependency.consulta_representante_legal = AsyncMock(
            return_value=mock_response
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rut": "12345678",
            "dv": "9"
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/representante-legal", json=request_data)
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cabecera"]["estadoProceso"] == "CORRECTO"
        assert "representantes" in data["respuesta"]
    
    def test_consulta_representante_legal_error_soap(self, mock_sii_soap_client_dependency):
        """Test error SOAP en consulta de representante legal"""
        # Configurar mock para lanzar Fault
        mock_sii_soap_client_dependency.consulta_representante_legal = AsyncMock(
            side_effect=Fault("Error en servicio SII")
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rut": "12345678",
            "dv": "9"
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/representante-legal", json=request_data)
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        assert "Error en servicio SII" in response.json()["detail"]
    
    def test_consulta_representante_legal_datos_invalidos(self):
        """Test validación de datos inválidos"""
        # Request con RUT inválido
        request_data = {
            "idSistema": 1,
            "rut": "abc123",  # RUT con letras
            "dv": "9"
        }
        
        response = client.post("/api/v1/sii/representante-legal", json=request_data)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestConsultaRelacionContribuyenteEmpresa:
    """Tests para consulta relación contribuyente-empresa"""
    
    def test_consulta_relacion_exitoso(self, mock_sii_soap_client_dependency, sample_respuesta_proceso, sample_datos_glosa):
        """Test exitoso de consulta de relación"""
        # Configurar mock
        mock_response = RespuestaSiiConsIvaBe(
            cabecera=sample_respuesta_proceso,
            respuesta=sample_datos_glosa,
            xmlRespuesta="<mock>XML de respuesta</mock>"
        )
        
        mock_sii_soap_client_dependency.consulta_relacion_contribuyente_empresa = AsyncMock(
            return_value=mock_response
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rutEmp": 12345678,
            "dvEmp": "9",
            "rutSoc": 87654321,
            "dvSoc": "0"
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/relacion-empresa", json=request_data)
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cabecera"]["estadoProceso"] == "CORRECTO"
    
    def test_consulta_relacion_error_soap(self, mock_sii_soap_client_dependency):
        """Test error SOAP en consulta de relación"""
        # Configurar mock para lanzar Fault
        mock_sii_soap_client_dependency.consulta_relacion_contribuyente_empresa = AsyncMock(
            side_effect=Fault("Error en servicio SII")
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rutEmp": 12345678,
            "dvEmp": "9",
            "rutSoc": 87654321,
            "dvSoc": "0"
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/relacion-empresa", json=request_data)
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        assert "Error en servicio SII" in response.json()["detail"]


class TestConsultaNumeroEmpleados:
    """Tests para consulta número de empleados"""
    
    def test_consulta_numero_empleados_exitoso(self, mock_sii_soap_client_dependency, sample_respuesta_proceso):
        """Test exitoso de consulta número de empleados"""
        # Configurar mock
        mock_response = RespuestaSiiNumeroEmpleadosBe(
            cabecera=sample_respuesta_proceso,
            respuesta=ConsultaSiiNumeroEmpleadosBe(
                fechaInicioActividad=datetime.now(),
                glosa="Empresa con empleados",
                estado="ACTIVO",
                numeroEmpleados="50"
            ),
            xmlRespuesta="<mock>XML de respuesta</mock>"
        )
        
        mock_sii_soap_client_dependency.consulta_numero_empleados = AsyncMock(
            return_value=mock_response
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rut": 12345678,
            "dv": "9",
            "periodo": 202312
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/numero-empleados", json=request_data)
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cabecera"]["estadoProceso"] == "CORRECTO"
        assert data["respuesta"]["numeroEmpleados"] == "50"
    
    def test_consulta_numero_empleados_error_soap(self, mock_sii_soap_client_dependency):
        """Test error SOAP en consulta número de empleados"""
        # Configurar mock para lanzar Fault
        mock_sii_soap_client_dependency.consulta_numero_empleados = AsyncMock(
            side_effect=Fault("Error en servicio SII")
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rut": 12345678,
            "dv": "9",
            "periodo": 202312
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/numero-empleados", json=request_data)
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        assert "Error en servicio SII" in response.json()["detail"]


class TestConsultaDatosContribuyente:
    """Tests para consulta datos contribuyente"""
    
    def test_consulta_datos_exitoso(self, mock_sii_soap_client_dependency, sample_respuesta_proceso):
        """Test exitoso de consulta datos contribuyente"""
        # Configurar mock
        mock_response = RespuestaSiiDatosContribuyenteBe(
            cabecera=sample_respuesta_proceso,
            respuesta=RespuestaSiiDatosGenerales(
                estado="ACTIVO",
                glosa="Contribuyente activo",
                razonSocial="Empresa Mock S.A.",
                nombre="Juan",
                apPaterno="Pérez",
                apMaterno="González",
                xml="<mock>XML de datos</mock>"
            ),
            xmlRespuesta="<mock>XML de respuesta</mock>"
        )
        
        mock_sii_soap_client_dependency.consulta_datos_contribuyente = AsyncMock(
            return_value=mock_response
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rut": 12345678,
            "dv": "9"
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/datos-contribuyente", json=request_data)
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cabecera"]["estadoProceso"] == "CORRECTO"
        assert data["respuesta"]["razonSocial"] == "Empresa Mock S.A."


class TestConsultaActividadEconomica:
    """Tests para consulta actividad económica"""
    
    def test_consulta_actividad_exitoso(self, mock_sii_soap_client_dependency, sample_respuesta_proceso):
        """Test exitoso de consulta actividad económica"""
        # Configurar mock
        mock_response = RespuestaSiiActividadEconomicaBe(
            cabecera=sample_respuesta_proceso,
            respuesta=RespuestaSiiActEconomicaBe(
                fechaInicioActividad=datetime.now(),
                glosa="Actividades económicas",
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
        
        mock_sii_soap_client_dependency.consulta_actividad_economica = AsyncMock(
            return_value=mock_response
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rut": 12345678,
            "dv": "9"
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/actividad-economica", json=request_data)
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cabecera"]["estadoProceso"] == "CORRECTO"
        assert len(data["respuesta"]["actividadEconomica"]) == 1
        assert data["respuesta"]["actividadEconomica"][0]["actividad"] == 620900


class TestValidacionesGenerales:
    """Tests para validaciones generales"""
    
    def test_endpoint_con_datos_faltantes(self):
        """Test validación de datos faltantes"""
        # Request sin idSistema requerido
        response = client.post("/api/v1/sii/representante-legal", json={
            "rut": "12345678",
            "dv": "9"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_endpoint_con_rut_invalido(self):
        """Test validación de RUT inválido"""
        # Request con RUT fuera del rango válido
        response = client.post("/api/v1/sii/datos-contribuyente", json={
            "idSistema": 1,
            "rut": 123,  # RUT muy corto
            "dv": "9"
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_endpoint_con_tipo_consulta_invalido(self):
        """Test validación de tipo de consulta inválido"""
        # Request con tipo de consulta inválido
        response = client.post("/api/v1/sii/categoria-empresa", json={
            "idSistema": 1,
            "rut": 12345678,
            "dv": "9",
            "fecha": "2023-12-01T00:00:00",
            "tipoConsulta": 5  # Tipo inválido
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_endpoint_con_periodo_invalido(self):
        """Test validación de período inválido"""
        # Request con período inválido
        response = client.post("/api/v1/sii/numero-empleados", json={
            "idSistema": 1,
            "rut": 12345678,
            "dv": "9",
            "periodo": 123  # Período inválido
        })
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_endpoint_inexistente(self):
        """Test endpoint inexistente"""
        response = client.post("/api/v1/sii/inexistente", json={})
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestManejadorExcepciones:
    """Tests para manejo de excepciones"""
    
    def test_excepcion_inesperada(self, mock_sii_soap_client_dependency):
        """Test manejo de excepciones inesperadas"""
        # Configurar mock para lanzar excepción general
        mock_sii_soap_client_dependency.consulta_representante_legal = AsyncMock(
            side_effect=Exception("Error interno del servicio")
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rut": "12345678",
            "dv": "9"
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/representante-legal", json=request_data)
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        assert "Error interno del servidor" in response.json()["detail"]
    
    def test_timeout_conexion(self, mock_sii_soap_client_dependency):
        """Test manejo de timeout de conexión"""
        # Configurar mock para simular timeout
        mock_sii_soap_client_dependency.consulta_datos_contribuyente = AsyncMock(
            side_effect=Exception("Connection timeout")
        )
        
        # Datos del request
        request_data = {
            "idSistema": 1,
            "rut": 12345678,
            "dv": "9"
        }
        
        # Hacer request
        response = client.post("/api/v1/sii/datos-contribuyente", json=request_data)
        
        # Verificar respuesta de error
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        assert "Error interno del servidor" in response.json()["detail"]

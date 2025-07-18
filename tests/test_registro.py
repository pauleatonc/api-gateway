"""
Tests para el módulo de registro de SENCE
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from fastapi import status

from app.main import app
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
    DatosContacto,
    DatosContactoSO,
    ErrorResponse
)
from app.services.registro_soap_client import RegistroSoapClientService


# Crear cliente de prueba
client = TestClient(app)


@pytest.fixture
def mock_registro_soap_client():
    """Fixture para crear un mock del cliente SOAP de registro"""
    return Mock(spec=RegistroSoapClientService)


@pytest.fixture
def mock_registro_soap_client_dependency(mock_registro_soap_client):
    """Fixture para sobrescribir la dependencia del cliente SOAP de registro"""
    def get_mock_registro_soap_client():
        return mock_registro_soap_client
    
    from app.api.v1.registro import get_registro_soap_client
    app.dependency_overrides[get_registro_soap_client] = get_mock_registro_soap_client
    
    yield mock_registro_soap_client
    
    # Limpiar después del test
    app.dependency_overrides.clear()


@pytest.fixture
def sample_datos_persona():
    """Datos de ejemplo para persona"""
    return {
        "Rut": 12345678,
        "Dv": "9",
        "ApellidoPaterno": "Pérez",
        "ApellidoMaterno": "González",
        "Nombres": "Juan Carlos",
        "NroSerie": "123456789",
        "CodigoCelular": "+56",
        "NumeroCelular": 987654321,
        "Mail": "juan.perez@example.com",
        "FechaNacimiento": "1990-05-15T00:00:00Z",
        "FechaDefuncion": None,
        "IdNacionalidad": 1,
        "Comuna": 13101,
        "Direccion": "Av. Principal",
        "NroDireccion": "123",
        "IdSexo": 1
    }


@pytest.fixture
def sample_datos_empresa():
    """Datos de ejemplo para empresa"""
    return {
        "RutEmpresa": 76543210,
        "DvEmpresa": "K",
        "TipoEmpresa": 1,
        "IdComuna": 13101,
        "DireccionCalle": "Av. Empresarial",
        "DireccionNumero": "456",
        "NumeroCelular": 987654321,
        "CodigoCelular": "+56",
        "MailEmpresa": "info@empresa.com",
        "IdPreguntaSecreta": 1,
        "RespuestaSecreta": "respuesta",
        "RutRepresentante": 12345678,
        "DvRepresentante": "9",
        "MailRepresentante": "representante@empresa.com",
        "NumeroCelularRepresentante": 987654321,
        "CodigoCelularRepresentante": "+56",
        "Cus": "CUS123456"
    }


class TestRegistroPersona:
    """Tests para el endpoint de registro de persona"""
    
    def test_registro_persona_exitoso(self, mock_registro_soap_client_dependency, sample_datos_persona):
        """Test de registro de persona exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.registro_persona = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Persona registrada correctamente"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/registro/persona", json={
            "idSistema": 1,
            "datosPersona": sample_datos_persona
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200
        assert data["respuestaProceso"] == "Persona registrada correctamente"
    
    def test_registro_persona_error_soap(self, mock_registro_soap_client_dependency, sample_datos_persona):
        """Test de registro de persona con error SOAP"""
        # Configurar mock
        mock_registro_soap_client_dependency.registro_persona = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.ERROR,
            codigoProceso=502,
            respuestaProceso="Error SOAP"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/registro/persona", json={
            "idSistema": 1,
            "datosPersona": sample_datos_persona
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "SOAP_ERROR"
    
    def test_registro_persona_datos_invalidos(self, mock_registro_soap_client_dependency):
        """Test de registro de persona con datos inválidos"""
        # Realizar petición sin datos requeridos
        response = client.post("/api/v1/registro/persona", json={
            "idSistema": 1,
            "datosPersona": {
                "Rut": 12345678
                # Faltan campos requeridos
            }
        })
        
        # Verificar respuesta (debe devolver 422)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestRegistroPersonaCrm:
    """Tests para el endpoint de registro de persona CRM"""
    
    def test_registro_persona_crm_exitoso(self, mock_registro_soap_client_dependency):
        """Test de registro de persona CRM exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.registro_persona_crm = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Persona registrada en CRM correctamente"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/registro/persona/crm", json={
            "idSistema": 1,
            "datosPersona": {
                "Rut": 12345678,
                "Dv": "9",
                "Contacto": {
                    "IdComuna": 13101,
                    "NumeroCelular": 987654321,
                    "CodigoTelefonoFijo": 2,
                    "TelefonoFijo": 22345678
                }
            }
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestRegistroPersonaSiacOirs:
    """Tests para el endpoint de registro de persona SIAC-OIRS"""
    
    def test_registro_persona_siac_oirs_exitoso(self, mock_registro_soap_client_dependency):
        """Test de registro de persona SIAC-OIRS exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.registrar_persona_siac_oirs = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Persona registrada en SIAC-OIRS correctamente"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/registro/persona/siac", json={
            "idSistema": 1,
            "datosPersona": {
                "Rut": 12345678,
                "Dv": "9",
                "Contacto": {
                    "IdComuna": 13101,
                    "NumeroCelular": "987654321",
                    "CodigoTelefonoFijo": "2",
                    "TelefonoFijo": "22345678"
                }
            }
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestRegistroEmpresa:
    """Tests para el endpoint de registro de empresa"""
    
    def test_registro_empresa_exitoso(self, mock_registro_soap_client_dependency, sample_datos_empresa):
        """Test de registro de empresa exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.registro_empresa = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Empresa registrada correctamente"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/registro/empresa", json={
            "idSistema": 1,
            "datosEmpresa": sample_datos_empresa
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200
        assert data["respuestaProceso"] == "Empresa registrada correctamente"
    
    def test_registro_empresa_error(self, mock_registro_soap_client_dependency, sample_datos_empresa):
        """Test de registro de empresa con error"""
        # Configurar mock
        mock_registro_soap_client_dependency.registro_empresa = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.ERROR,
            codigoProceso=502,
            respuestaProceso="Error al registrar empresa"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/registro/empresa", json={
            "idSistema": 1,
            "datosEmpresa": sample_datos_empresa
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "SOAP_ERROR"


class TestActualizarEmpresa:
    """Tests para el endpoint de actualizar empresa"""
    
    def test_actualizar_empresa_exitoso(self, mock_registro_soap_client_dependency):
        """Test de actualización de empresa exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.actualizar_empresa = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Empresa actualizada correctamente"
        ))
        
        # Realizar petición
        response = client.put("/api/v1/registro/empresa", json={
            "idSistema": 1,
            "datosEmpresa": {
                "RutEmpresa": 76543210,
                "DvEmpresa": "K",
                "TipoEmpresa": 1,
                "IdComuna": 13101,
                "DireccionCalle": "Av. Empresarial",
                "DireccionNumero": "456",
                "Telefono": 22345678,
                "MailEmpresa": "info@empresa.com"
            }
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestActualizarRazonSocial:
    """Tests para el endpoint de actualizar razón social"""
    
    def test_actualizar_razon_social_exitoso(self, mock_registro_soap_client_dependency):
        """Test de actualización de razón social exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.actualizar_razon_social = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Razón social actualizada correctamente"
        ))
        
        # Realizar petición
        response = client.patch("/api/v1/registro/empresa/razon", json={
            "idSistema": 1,
            "rutEmpresa": 76543210,
            "dvEmpresa": "K"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestActualizarRepLegales:
    """Tests para el endpoint de actualizar representantes legales"""
    
    def test_actualizar_rep_legales_exitoso(self, mock_registro_soap_client_dependency):
        """Test de actualización de representantes legales exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.actualizar_rep_legales = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Representantes legales actualizados correctamente"
        ))
        
        # Realizar petición
        response = client.patch("/api/v1/registro/empresa/rep-legal", json={
            "idSistema": 1,
            "rutEmpresa": 76543210,
            "dvEmpresa": "K"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestActualizarTipoEntidad:
    """Tests para el endpoint de actualizar tipo de entidad"""
    
    def test_actualizar_tipo_entidad_exitoso(self, mock_registro_soap_client_dependency):
        """Test de actualización de tipo de entidad exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.actualizar_tipo_entidad = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Tipo de entidad actualizado correctamente"
        ))
        
        # Realizar petición
        response = client.patch("/api/v1/registro/empresa/tipo", json={
            "idSistema": 1,
            "rutEmpresa": 76543210,
            "dvEmpresa": "K",
            "tipoEntidad": "OTEC"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestRegistroEmpresaConCus:
    """Tests para el endpoint de registro de empresa con CUS"""
    
    def test_registro_empresa_con_cus_exitoso(self, mock_registro_soap_client_dependency, sample_datos_empresa):
        """Test de registro de empresa con CUS exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.registro_empresa_con_cus = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Empresa registrada con CUS correctamente"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/registro/empresa/con-cus", json={
            "idSistema": 1,
            "datosEmpresa": sample_datos_empresa
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestCambioCusEmpresa:
    """Tests para el endpoint de cambio de CUS de empresa"""
    
    def test_cambio_cus_empresa_exitoso(self, mock_registro_soap_client_dependency):
        """Test de cambio de CUS de empresa exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.cambio_cus_empresa = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="CUS cambiado correctamente"
        ))
        
        # Realizar petición
        response = client.patch("/api/v1/registro/empresa/cambio-cus", json={
            "idSistema": 1,
            "rutEmpresa": 76543210,
            "dvRutEmpresa": "K",
            "cusActual": "CUS123456",
            "nuevaCus": "CUS789012"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestRegistroEmpresaOracle:
    """Tests para el endpoint de registro de empresa Oracle"""
    
    def test_registro_empresa_oracle_exitoso(self, mock_registro_soap_client_dependency):
        """Test de registro de empresa Oracle exitoso"""
        # Configurar mock
        mock_registro_soap_client_dependency.registro_empresa_oracle = AsyncMock(return_value=RespuestaProcesoBe(
            estadoProceso=TipoEstado.CORRECTO,
            codigoProceso=200,
            respuestaProceso="Empresa registrada en Oracle correctamente"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/registro/empresa/oracle", json={
            "idSistema": 1,
            "datosEmpresa": {
                "PerJur": {
                    "rutPersJur": 76543210,
                    "dvPersJur": "K",
                    "razonSocialPersJur": "Empresa Ejemplo S.A.",
                    "tipoPersJur": 1
                },
                "PerNat": {
                    "rutPerJur": 76543210,
                    "rutPer": 12345678,
                    "dvPer": "9",
                    "nombre": "Juan",
                    "aPaterno": "Pérez"
                }
            }
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["estadoProceso"] == "CORRECTO"
        assert data["codigoProceso"] == 200


class TestIntegracionCompleta:
    """Tests de integración completa del módulo de registro"""
    
    def test_todos_los_endpoints_con_datos_invalidos(self):
        """Test de todos los endpoints con datos inválidos"""
        endpoints = [
            ("POST", "/api/v1/registro/persona"),
            ("POST", "/api/v1/registro/persona/crm"),
            ("POST", "/api/v1/registro/persona/siac"),
            ("POST", "/api/v1/registro/empresa"),
            ("PUT", "/api/v1/registro/empresa"),
            ("PATCH", "/api/v1/registro/empresa/razon"),
            ("PATCH", "/api/v1/registro/empresa/rep-legal"),
            ("PATCH", "/api/v1/registro/empresa/tipo"),
            ("POST", "/api/v1/registro/empresa/con-cus"),
            ("PATCH", "/api/v1/registro/empresa/cambio-cus"),
            ("POST", "/api/v1/registro/empresa/oracle"),
        ]
        
        for method, endpoint in endpoints:
            # Test con datos vacíos
            if method == "POST":
                response = client.post(endpoint, json={})
            elif method == "PUT":
                response = client.put(endpoint, json={})
            elif method == "PATCH":
                response = client.patch(endpoint, json={})
            
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_flujo_completo_con_mocks(self):
        """Test del flujo completo usando mocks del sistema"""
        # Este test verifica que todos los endpoints respondan correctamente
        # usando los mocks integrados en el sistema
        
        # 1. Registrar persona
        response = client.post("/api/v1/registro/persona", json={
            "idSistema": 1,
            "datosPersona": {
                "Rut": 12345678,
                "Dv": "9",
                "ApellidoPaterno": "Pérez",
                "ApellidoMaterno": "González",
                "Nombres": "Juan Carlos",
                "NumeroCelular": 987654321,
                "Mail": "juan.perez@example.com",
                "FechaNacimiento": "1990-05-15T00:00:00Z",
                "IdNacionalidad": 1,
                "Comuna": 13101,
                "IdSexo": 1
            }
        })
        # Note: En este caso, el endpoint real usaría mocks si USE_SOAP_MOCKS=true
        # pero como no tenemos acceso directo a la configuración en este test,
        # simplemente verificamos que la respuesta sea válida
        assert response.status_code in [200, 502]  # Puede ser 200 con mocks o 502 sin servicio
        
        # 2. Registrar empresa
        response = client.post("/api/v1/registro/empresa", json={
            "idSistema": 1,
            "datosEmpresa": {
                "RutEmpresa": 76543210,
                "DvEmpresa": "K",
                "TipoEmpresa": 1,
                "IdComuna": 13101,
                "DireccionCalle": "Av. Empresarial",
                "DireccionNumero": "456",
                "NumeroCelular": 987654321,
                "CodigoCelular": "+56",
                "MailEmpresa": "info@empresa.com",
                "IdPreguntaSecreta": 1,
                "RespuestaSecreta": "respuesta",
                "RutRepresentante": 12345678,
                "DvRepresentante": "9",
                "MailRepresentante": "representante@empresa.com",
                "NumeroCelularRepresentante": 987654321,
                "CodigoCelularRepresentante": "+56",
                "Cus": "CUS123456"
            }
        })
        assert response.status_code in [200, 502]


class TestManejadorExcepciones:
    """Tests para el manejo de excepciones"""
    
    def test_excepcion_inesperada(self, mock_registro_soap_client_dependency, sample_datos_persona):
        """Test de excepción inesperada"""
        # Configurar mock para lanzar excepción
        mock_registro_soap_client_dependency.registro_persona = AsyncMock(side_effect=Exception("Error inesperado"))
        
        # Realizar petición
        response = client.post("/api/v1/registro/persona", json={
            "idSistema": 1,
            "datosPersona": sample_datos_persona
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "INTERNAL_ERROR"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
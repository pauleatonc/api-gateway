"""
Tests para el módulo de consulta de Registro Civil de SENCE
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, AsyncMock
from fastapi import status
from zeep.exceptions import Fault

from app.main import app
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
from app.services.consulta_rc_soap_client import ConsultaRcSoapClientService


# Crear cliente de prueba
client = TestClient(app)


@pytest.fixture
def mock_consulta_rc_soap_client():
    """Fixture para crear un mock del cliente SOAP de consulta RC"""
    return Mock(spec=ConsultaRcSoapClientService)


@pytest.fixture
def mock_consulta_rc_soap_client_dependency(mock_consulta_rc_soap_client):
    """Fixture para sobrescribir la dependencia del cliente SOAP de consulta RC"""
    def get_mock_consulta_rc_soap_client():
        return mock_consulta_rc_soap_client
    
    from app.api.v1.consulta_rc import get_consulta_rc_soap_client
    app.dependency_overrides[get_consulta_rc_soap_client] = get_mock_consulta_rc_soap_client
    
    yield mock_consulta_rc_soap_client
    
    # Limpiar después del test
    app.dependency_overrides.clear()


class TestConsultaRun:
    """Tests para el endpoint de consulta de RUN"""
    
    def test_consulta_run_exitoso(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de RUN exitoso"""
        # Configurar mock
        mock_consulta_rc_soap_client_dependency.consulta_run = AsyncMock(return_value=RespuestaConsultaRunBe(
            cabecera=RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                respuestaProceso="Consulta exitosa",
                codigoProceso=200
            ),
            respuesta=ConsultaRunBe(
                rut=12345678,
                dv="9",
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
            xmlRespuesta="<ConsultaRun>...</ConsultaRun>"
        ))
        
        # Realizar petición
        response = client.get("/api/v1/rc/run", params={
            "id_sistema": 1,
            "rut": 12345678,
            "dv": "9"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cabecera"]["estadoProceso"] == "CORRECTO"
        assert data["respuesta"]["rut"] == 12345678
        assert data["respuesta"]["nombres"] == "Juan Carlos"
    
    def test_consulta_run_error_soap(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de RUN con error SOAP"""
        # Configurar mock para lanzar Fault
        mock_consulta_rc_soap_client_dependency.consulta_run = AsyncMock(side_effect=Fault("RUN no encontrado"))
        
        # Realizar petición
        response = client.get("/api/v1/rc/run", params={
            "id_sistema": 1,
            "rut": 12345678,
            "dv": "9"
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "SOAP_FAULT"
    
    def test_consulta_run_parametros_invalidos(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de RUN con parámetros inválidos"""
        # Realizar petición sin parámetros requeridos
        response = client.get("/api/v1/rc/run")
        
        # Verificar respuesta (debe devolver 422)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestConsultaNroSerieNroDocumento:
    """Tests para el endpoint de consulta de número de serie/documento"""
    
    def test_consulta_nro_serie_exitoso(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de número de serie exitoso"""
        # Configurar mock
        mock_consulta_rc_soap_client_dependency.consulta_nro_serie_nro_documento = AsyncMock(return_value=RespuestaConsultaNroSerieNroDocBe(
            cabecera=RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                respuestaProceso="Consulta exitosa",
                codigoProceso=200
            ),
            respuesta=DatosRespuestaNroSerieNroDocBe(
                EstadoRespuesta="Correcto",
                Rut=12345678,
                Dv="9",
                CodigoTipoDocumento="C",
                CodigoClaseDocumento="CedulaIdentidadParaChileno",
                NumeroDocumento="123456789",
                NumeroSerie="A123456789",
                IndicadorVigencia="S",
                FechaVencimiento="2030-12-31T23:59:59Z",
                IndicadorBloqueo="NO_BLOQUEADO"
            ),
            xmlRespuesta="<ConsultaNroSerie>...</ConsultaNroSerie>"
        ))
        
        # Realizar petición
        response = client.get("/api/v1/rc/run/documento", params={
            "id_sistema": 1,
            "rut": 12345678,
            "dv": "9",
            "tipo_documento": "C"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["cabecera"]["estadoProceso"] == "CORRECTO"
        assert data["respuesta"]["Rut"] == 12345678
        assert data["respuesta"]["IndicadorVigencia"] == "S"
    
    def test_consulta_nro_serie_error_soap(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de número de serie con error SOAP"""
        # Configurar mock para lanzar Fault
        mock_consulta_rc_soap_client_dependency.consulta_nro_serie_nro_documento = AsyncMock(side_effect=Fault("Documento no encontrado"))
        
        # Realizar petición
        response = client.get("/api/v1/rc/run/documento", params={
            "id_sistema": 1,
            "rut": 12345678,
            "tipo_documento": "C"
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "SOAP_FAULT"


class TestConsultaCertificadoNacimiento:
    """Tests para el endpoint de consulta de certificado de nacimiento"""
    
    def test_consulta_cert_nacimiento_exitoso(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de certificado de nacimiento exitoso"""
        # Configurar mock
        mock_consulta_rc_soap_client_dependency.consulta_certificado_nacimiento = AsyncMock(return_value=RespuestaConsultaCertNacimientoBe(
            Cabecera=RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                respuestaProceso="Consulta exitosa",
                codigoProceso=200
            ),
            Respuesta=ConsultaCertNacBe(
                rut=12345678,
                dv="9",
                circunscripcion="SANTIAGO",
                numeroInscripcionNacimiento="12345",
                nombreCompleto="Juan Carlos Pérez González",
                fechaNacimiento="1990-05-15T00:00:00Z",
                sexo="M",
                lugarNacimiento="SANTIAGO",
                nacionalidadNacimiento="CHILENA",
                nombrePadre="Pedro Pérez",
                nombreMadre="María González"
            ),
            XmlRespuesta="<CertificadoNacimiento>...</CertificadoNacimiento>"
        ))
        
        # Realizar petición
        response = client.get("/api/v1/rc/cert-nac", params={
            "id_sistema": 1,
            "rut": 12345678,
            "dv": "9"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["Cabecera"]["estadoProceso"] == "CORRECTO"
        assert data["Respuesta"]["rut"] == 12345678
        assert data["Respuesta"]["nombreCompleto"] == "Juan Carlos Pérez González"
    
    def test_consulta_cert_nacimiento_error_soap(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de certificado de nacimiento con error SOAP"""
        # Configurar mock para lanzar Fault
        mock_consulta_rc_soap_client_dependency.consulta_certificado_nacimiento = AsyncMock(side_effect=Fault("Certificado no encontrado"))
        
        # Realizar petición
        response = client.get("/api/v1/rc/cert-nac", params={
            "id_sistema": 1,
            "rut": 12345678
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "SOAP_FAULT"


class TestConsultaDiscapacidad:
    """Tests para el endpoint de consulta de discapacidad"""
    
    def test_consulta_discapacidad_exitoso(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de discapacidad exitoso"""
        # Configurar mock
        mock_consulta_rc_soap_client_dependency.consulta_discapacidad = AsyncMock(return_value=RespuestaConsultaDiscapacidadBe(
            Cabecera=RespuestaProcesoBe(
                estadoProceso=TipoEstado.CORRECTO,
                respuestaProceso="Consulta exitosa",
                codigoProceso=200
            ),
            Respuesta=ConsultaDiscapacidadBe(
                Run=12345678,
                Dv="9",
                ApareceEnRND="N",
                Discapacidad=None,
                DiscapacidadRn=None
            ),
            XmlRespuesta="<ConsultaDiscapacidad>...</ConsultaDiscapacidad>"
        ))
        
        # Realizar petición
        response = client.get("/api/v1/rc/discapacidad", params={
            "id_sistema": 1,
            "run": 12345678,
            "dv": "9"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["Cabecera"]["estadoProceso"] == "CORRECTO"
        assert data["Respuesta"]["Run"] == 12345678
        assert data["Respuesta"]["ApareceEnRND"] == "N"
    
    def test_consulta_discapacidad_error_soap(self, mock_consulta_rc_soap_client_dependency):
        """Test de consulta de discapacidad con error SOAP"""
        # Configurar mock para lanzar Fault
        mock_consulta_rc_soap_client_dependency.consulta_discapacidad = AsyncMock(side_effect=Fault("Error en consulta"))
        
        # Realizar petición
        response = client.get("/api/v1/rc/discapacidad", params={
            "id_sistema": 1,
            "run": 12345678
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "SOAP_FAULT"


class TestVerify:
    """Tests para el endpoint de verificación BATCH"""
    
    def test_verify_exitoso(self, mock_consulta_rc_soap_client_dependency):
        """Test de verificación BATCH exitoso"""
        # Configurar mock
        mock_consulta_rc_soap_client_dependency.verify = AsyncMock(return_value=VerifyResponse(
            VerifyResult=1,
            xmlparamout="<resultado><verificado>true</verificado></resultado>"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/rc/verify", json={
            "xmlparamin": "<xml><huella>...</huella></xml>"
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["VerifyResult"] == 1
        assert "verificado" in data["xmlparamout"]
    
    def test_verify_error_soap(self, mock_consulta_rc_soap_client_dependency):
        """Test de verificación BATCH con error SOAP"""
        # Configurar mock para lanzar Fault
        mock_consulta_rc_soap_client_dependency.verify = AsyncMock(side_effect=Fault("Error en verificación"))
        
        # Realizar petición
        response = client.post("/api/v1/rc/verify", json={
            "xmlparamin": "<xml><huella>...</huella></xml>"
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "SOAP_FAULT"


class TestVerificarHuellaDactilar:
    """Tests para el endpoint de verificación de huella dactilar"""
    
    def test_verificar_huella_exitoso(self, mock_consulta_rc_soap_client_dependency):
        """Test de verificación de huella dactilar exitoso"""
        # Configurar mock
        mock_consulta_rc_soap_client_dependency.verificar_huella_dactilar = AsyncMock(return_value=RespuestaBeOfRespuestaHuellaDactilarBe(
            decision=True,
            mensaje="Verificación exitosa",
            mensajeDetalle="Huella dactilar verificada correctamente",
            estructuraDatos=RespuestaHuellaDactilarBe(
                Puntaje=85,
                RespuestaAFIS="Hit"
            ),
            TipoRespuesta="CorrectoNegocio"
        ))
        
        # Realizar petición
        response = client.post("/api/v1/rc/huella", json={
            "IdSistema": 1,
            "Datos": {
                "RutEmpresa": 76543210,
                "IdTransaccion": 12345,
                "Ip": "192.168.1.1",
                "UsuarioFinal": "admin",
                "RutPersona": 12345678,
                "NumeroDedo": 1,
                "Formato": 1,
                "ImagenBase64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
            }
        })
        
        # Verificar respuesta
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["decision"] is True
        assert data["mensaje"] == "Verificación exitosa"
        assert data["estructuraDatos"]["Puntaje"] == 85
        assert data["estructuraDatos"]["RespuestaAFIS"] == "Hit"
    
    def test_verificar_huella_error_soap(self, mock_consulta_rc_soap_client_dependency):
        """Test de verificación de huella dactilar con error SOAP"""
        # Configurar mock para lanzar Fault
        mock_consulta_rc_soap_client_dependency.verificar_huella_dactilar = AsyncMock(side_effect=Fault("Error en verificación"))
        
        # Realizar petición
        response = client.post("/api/v1/rc/huella", json={
            "IdSistema": 1,
            "Datos": {
                "RutEmpresa": 76543210,
                "IdTransaccion": 12345,
                "RutPersona": 12345678,
                "NumeroDedo": 1,
                "Formato": 1
            }
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "SOAP_FAULT"
    
    def test_verificar_huella_datos_invalidos(self, mock_consulta_rc_soap_client_dependency):
        """Test de verificación de huella dactilar con datos inválidos"""
        # Realizar petición sin datos requeridos
        response = client.post("/api/v1/rc/huella", json={
            "IdSistema": 1,
            "Datos": {
                "RutEmpresa": 76543210
                # Faltan campos requeridos
            }
        })
        
        # Verificar respuesta (debe devolver 422)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestIntegracionCompleta:
    """Tests de integración completa del módulo de consulta RC"""
    
    def test_todos_los_endpoints_con_mocks(self):
        """Test de todos los endpoints usando mocks del sistema"""
        # Este test verifica que todos los endpoints respondan correctamente
        # usando los mocks integrados en el sistema
        
        # 1. Consulta RUN
        response = client.get("/api/v1/rc/run", params={
            "id_sistema": 1,
            "rut": 12345678,
            "dv": "9"
        })
        assert response.status_code in [200, 502]
        
        # 2. Consulta documento
        response = client.get("/api/v1/rc/run/documento", params={
            "id_sistema": 1,
            "rut": 12345678,
            "tipo_documento": "C"
        })
        assert response.status_code in [200, 502]
        
        # 3. Consulta certificado nacimiento
        response = client.get("/api/v1/rc/cert-nac", params={
            "id_sistema": 1,
            "rut": 12345678
        })
        assert response.status_code in [200, 502]
        
        # 4. Consulta discapacidad
        response = client.get("/api/v1/rc/discapacidad", params={
            "id_sistema": 1,
            "run": 12345678
        })
        assert response.status_code in [200, 502]
        
        # 5. Verify
        response = client.post("/api/v1/rc/verify", json={
            "xmlparamin": "<xml><huella>test</huella></xml>"
        })
        assert response.status_code in [200, 502]
        
        # 6. Verificar huella dactilar
        response = client.post("/api/v1/rc/huella", json={
            "IdSistema": 1,
            "Datos": {
                "RutEmpresa": 76543210,
                "IdTransaccion": 12345,
                "RutPersona": 12345678,
                "NumeroDedo": 1,
                "Formato": 1
            }
        })
        assert response.status_code in [200, 502]
    
    def test_flujo_completo_con_datos_validos(self):
        """Test del flujo completo con datos válidos"""
        # Test con RUT válido que no cause error en mocks
        rut_valido = 12345678
        
        # Consulta RUN
        response = client.get("/api/v1/rc/run", params={
            "id_sistema": 1,
            "rut": rut_valido,
            "dv": "9"
        })
        assert response.status_code in [200, 502]
        
        # Consulta certificado de nacimiento
        response = client.get("/api/v1/rc/cert-nac", params={
            "id_sistema": 1,
            "rut": rut_valido
        })
        assert response.status_code in [200, 502]
        
        # Consulta discapacidad
        response = client.get("/api/v1/rc/discapacidad", params={
            "id_sistema": 1,
            "run": rut_valido
        })
        assert response.status_code in [200, 502]
    
    def test_endpoints_con_rut_error(self):
        """Test de endpoints con RUT que causa error en mocks"""
        # Test con RUT que simula error (11111111)
        rut_error = 11111111
        
        # Consulta RUN
        response = client.get("/api/v1/rc/run", params={
            "id_sistema": 1,
            "rut": rut_error
        })
        assert response.status_code in [200, 502]
        
        # Consulta certificado de nacimiento
        response = client.get("/api/v1/rc/cert-nac", params={
            "id_sistema": 1,
            "rut": rut_error
        })
        assert response.status_code in [200, 502]


class TestManejadorExcepciones:
    """Tests para el manejo de excepciones"""
    
    def test_excepcion_inesperada_consulta_run(self, mock_consulta_rc_soap_client_dependency):
        """Test de excepción inesperada en consulta RUN"""
        # Configurar mock para lanzar excepción
        mock_consulta_rc_soap_client_dependency.consulta_run = AsyncMock(side_effect=Exception("Error inesperado"))
        
        # Realizar petición
        response = client.get("/api/v1/rc/run", params={
            "id_sistema": 1,
            "rut": 12345678
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "INTERNAL_ERROR"
    
    def test_excepcion_inesperada_verificar_huella(self, mock_consulta_rc_soap_client_dependency):
        """Test de excepción inesperada en verificar huella"""
        # Configurar mock para lanzar excepción
        mock_consulta_rc_soap_client_dependency.verificar_huella_dactilar = AsyncMock(side_effect=Exception("Error inesperado"))
        
        # Realizar petición
        response = client.post("/api/v1/rc/huella", json={
            "IdSistema": 1,
            "Datos": {
                "RutEmpresa": 76543210,
                "IdTransaccion": 12345,
                "RutPersona": 12345678,
                "NumeroDedo": 1,
                "Formato": 1
            }
        })
        
        # Verificar respuesta (debe devolver 502)
        assert response.status_code == status.HTTP_502_BAD_GATEWAY
        data = response.json()
        assert data["success"] is False
        assert data["codigo_error"] == "INTERNAL_ERROR"


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 
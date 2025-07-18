"""
Configuración global de tests con pytest
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """
    Fixture para crear cliente de pruebas de FastAPI
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_request_data():
    """
    Fixture con datos de ejemplo para requests
    """
    return {
        "test_field": "test_value",
        "number_field": 123,
        "boolean_field": True
    }


@pytest.fixture
def sample_response_data():
    """
    Fixture con datos de ejemplo para responses
    """
    return {
        "status": "success",
        "data": {
            "id": "123",
            "name": "Test Item"
        }
    }


@pytest.fixture(scope="session")
def test_settings():
    """
    Fixture para configuración de tests
    """
    return {
        "app_name": "FastAPI SOAP Service Test",
        "app_version": "1.0.0-test",
        "debug": True,
        "log_level": "DEBUG"
    } 
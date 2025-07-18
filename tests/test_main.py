"""
Tests para la aplicación principal
"""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_root_endpoint(client: TestClient):
    """
    Test del endpoint raíz
    """
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
    assert "health" in data


@pytest.mark.unit
def test_info_endpoint(client: TestClient):
    """
    Test del endpoint de información
    """
    response = client.get("/info")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "app_name" in data
    assert "version" in data
    assert "debug" in data
    assert "environment" in data
    assert "python_version" in data


@pytest.mark.unit
def test_openapi_json(client: TestClient):
    """
    Test del endpoint OpenAPI JSON
    """
    response = client.get("/openapi.json")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert "paths" in data
    assert data["info"]["title"] == "FastAPI SOAP Service"


@pytest.mark.unit
def test_docs_endpoint(client: TestClient):
    """
    Test del endpoint de documentación Swagger UI
    """
    response = client.get("/docs")
    
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]


@pytest.mark.unit
def test_redoc_endpoint(client: TestClient):
    """
    Test del endpoint de documentación ReDoc
    """
    response = client.get("/redoc")
    
    assert response.status_code == status.HTTP_200_OK
    assert "text/html" in response.headers["content-type"]


@pytest.mark.unit
def test_cors_headers(client: TestClient):
    """
    Test de headers CORS
    """
    response = client.get("/", headers={"Origin": "https://example.com"})
    
    # Verificar que los headers CORS están presentes
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"
    assert "access-control-allow-credentials" in response.headers


@pytest.mark.unit
def test_404_endpoint(client: TestClient):
    """
    Test de endpoint que no existe
    """
    response = client.get("/nonexistent-endpoint")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.integration
def test_application_startup(client: TestClient):
    """
    Test de que la aplicación se inicia correctamente
    """
    # Verificar que la aplicación responde correctamente
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    
    # Verificar que los endpoints principales están disponibles
    endpoints_to_test = [
        "/",
        "/info",
        "/api/v1/health/",
        "/docs",
        "/redoc",
        "/openapi.json"
    ]
    
    for endpoint in endpoints_to_test:
        response = client.get(endpoint)
        assert response.status_code == status.HTTP_200_OK, f"Endpoint {endpoint} falló" 
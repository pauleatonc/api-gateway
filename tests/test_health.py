"""
Tests para los endpoints de salud
"""
import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_health_check(client: TestClient):
    """
    Test del endpoint de health check
    """
    response = client.get("/api/v1/health/")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "version" in data
    assert "uptime" in data


@pytest.mark.unit
def test_readiness_check(client: TestClient):
    """
    Test del endpoint de readiness check
    """
    response = client.get("/api/v1/health/ready")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["status"] == "ready"
    assert "timestamp" in data
    assert "checks" in data
    assert isinstance(data["checks"], dict)


@pytest.mark.unit
def test_liveness_check(client: TestClient):
    """
    Test del endpoint de liveness check
    """
    response = client.get("/api/v1/health/live")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


@pytest.mark.integration
def test_health_endpoints_response_time(client: TestClient):
    """
    Test de tiempo de respuesta de los endpoints de salud
    """
    import time
    
    # Test health check
    start_time = time.time()
    response = client.get("/api/v1/health/")
    end_time = time.time()
    
    assert response.status_code == status.HTTP_200_OK
    assert (end_time - start_time) < 1.0  # Debe responder en menos de 1 segundo
    
    # Test readiness check
    start_time = time.time()
    response = client.get("/api/v1/health/ready")
    end_time = time.time()
    
    assert response.status_code == status.HTTP_200_OK
    assert (end_time - start_time) < 1.0  # Debe responder en menos de 1 segundo
    
    # Test liveness check
    start_time = time.time()
    response = client.get("/api/v1/health/live")
    end_time = time.time()
    
    assert response.status_code == status.HTTP_200_OK
    assert (end_time - start_time) < 1.0  # Debe responder en menos de 1 segundo 
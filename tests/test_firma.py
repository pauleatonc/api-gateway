"""
Tests para el servicio de Firma Desatendida
"""
import pytest
from fastapi.testclient import TestClient
import base64
import hashlib


def test_firma_desatendida_success(client: TestClient):
    """Test exitoso de firma desatendida"""
    # Crear un documento de prueba
    contenido = b"Este es un documento de prueba en formato PDF"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "mensaje" in data
    assert "documentosFirmados" in data
    assert len(data["documentosFirmados"]) == 1
    assert data["documentosFirmados"][0]["folio"] == 1000


def test_firma_desatendida_multiples_documentos(client: TestClient):
    """Test de firma desatendida con múltiples documentos"""
    documentos = []
    for i in range(1, 4):
        contenido = f"Documento de prueba {i}".encode('utf-8')
        checksum = hashlib.sha256(contenido).hexdigest()
        base64_content = base64.b64encode(contenido).decode('utf-8')
        
        documentos.append({
            "base64": base64_content,
            "checksum": checksum,
            "descripcion": f"Documento de prueba {i}",
            "folio": 1000 + i,
            "formato": "PDF",
            "nombre": f"prueba_{i}.pdf",
            "region": 100000,
            "tipoDocumento": "RESOLUCION_EXENTA"
        })
    
    payload = {
        "documentos": documentos,
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["documentosFirmados"]) == 3


def test_firma_desatendida_sin_guion_run(client: TestClient):
    """Test de firma con RUN sin guión"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "123456789"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_firma_desatendida_con_puntos_run(client: TestClient):
    """Test de firma con RUN con puntos y guión"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "12.345.678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_firma_desatendida_proposito_visar(client: TestClient):
    """Test de firma con propósito Visar"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Visar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_firma_desatendida_proposito_aprobar(client: TestClient):
    """Test de firma con propósito Aprobar"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "CERTIFICADO"
            }
        ],
        "proposito": "Aprobar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_firma_desatendida_tipo_contrato(client: TestClient):
    """Test de firma con tipo de documento CONTRATO"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Contrato de servicios",
                "folio": 2000,
                "formato": "PDF",
                "nombre": "contrato.pdf",
                "region": 80000,
                "tipoDocumento": "CONTRATO"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_firma_desatendida_formato_docx(client: TestClient):
    """Test de firma con formato DOCX"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento Word",
                "folio": 3000,
                "formato": "DOCX",
                "nombre": "documento.docx",
                "region": 100000,
                "tipoDocumento": "OTRO"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_firma_desatendida_checksum_invalido(client: TestClient):
    """Test con checksum inválido (longitud incorrecta)"""
    contenido = b"Documento de prueba"
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": "abc123",  # Checksum muy corto
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 422


def test_firma_desatendida_sin_documentos(client: TestClient):
    """Test sin documentos"""
    payload = {
        "documentos": [],
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 422


def test_firma_desatendida_run_invalido(client: TestClient):
    """Test con RUN inválido"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "ABCD"  # RUN inválido
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 422


def test_firma_desatendida_base64_vacio(client: TestClient):
    """Test con contenido Base64 vacío"""
    payload = {
        "documentos": [
            {
                "base64": "",
                "checksum": "0" * 64,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 422


def test_firma_desatendida_campos_requeridos(client: TestClient):
    """Test verificando campos requeridos"""
    payload = {
        "runFirmante": "12345678-9"
        # Falta el campo documentos
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 422


def test_firma_desatendida_formato_invalido(client: TestClient):
    """Test con formato de documento inválido"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "TXT",  # Formato no válido
                "nombre": "prueba.txt",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 422


def test_firma_desatendida_tipo_documento_invalido(client: TestClient):
    """Test con tipo de documento inválido"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "TIPO_INVALIDO"
            }
        ],
        "proposito": "Firmar",
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 422


def test_firma_desatendida_proposito_invalido(client: TestClient):
    """Test con propósito inválido"""
    contenido = b"Documento de prueba"
    checksum = hashlib.sha256(contenido).hexdigest()
    base64_content = base64.b64encode(contenido).decode('utf-8')
    
    payload = {
        "documentos": [
            {
                "base64": base64_content,
                "checksum": checksum,
                "descripcion": "Documento de prueba",
                "folio": 1000,
                "formato": "PDF",
                "nombre": "prueba.pdf",
                "region": 100000,
                "tipoDocumento": "RESOLUCION_EXENTA"
            }
        ],
        "proposito": "Destruir",  # Propósito inválido
        "runFirmante": "12345678-9"
    }
    
    response = client.post("/api/v1/firma/desatendida", json=payload)
    
    assert response.status_code == 422


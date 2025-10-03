"""
Modelos Pydantic para el servicio de Firma Desatendida de SENCE
"""
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum


class TipoDocumento(str, Enum):
    """Enumeración para tipos de documento"""
    RESOLUCION_EXENTA = "RESOLUCION_EXENTA"
    CONTRATO = "CONTRATO"
    CONVENIO = "CONVENIO"
    CERTIFICADO = "CERTIFICADO"
    OTRO = "OTRO"


class FormatoDocumento(str, Enum):
    """Enumeración para formatos de documento"""
    PDF = "PDF"
    DOC = "DOC"
    DOCX = "DOCX"
    XML = "XML"


class Proposito(str, Enum):
    """Enumeración para propósito de firma"""
    FIRMAR = "Firmar"
    VISAR = "Visar"
    APROBAR = "Aprobar"


class DocumentoFirma(BaseModel):
    """Modelo para documento a firmar"""
    base64: str = Field(..., description="Contenido del documento en Base64", example="JVBERi0xLjQKJe...")
    checksum: str = Field(..., description="Checksum SHA256 del documento", example="259672a6fe8696b6dba05c97844f4ce04779bf61568c5a0e43d247f59e4e4eca")
    descripcion: str = Field(..., description="Descripción del documento", example="Resolución Concesión Subsidio")
    folio: int = Field(..., description="Folio del documento", example=1619)
    formato: FormatoDocumento = Field(..., description="Formato del documento", example="PDF")
    nombre: str = Field(..., description="Nombre del archivo", example="resolucion.pdf")
    region: int = Field(..., description="Código de región", example=100000)
    tipoDocumento: TipoDocumento = Field(..., description="Tipo de documento", example="RESOLUCION_EXENTA")

    @validator('checksum')
    def validate_checksum(cls, v):
        if len(v) != 64:
            raise ValueError('El checksum debe tener 64 caracteres (SHA256)')
        return v.lower()

    @validator('base64')
    def validate_base64(cls, v):
        if not v or len(v) < 10:
            raise ValueError('El contenido Base64 no puede estar vacío')
        return v


class FirmaDesatendidaRequest(BaseModel):
    """Modelo para request de Firma Desatendida"""
    documentos: List[DocumentoFirma] = Field(..., description="Lista de documentos a firmar", min_items=1)
    proposito: Proposito = Field(default=Proposito.FIRMAR, description="Propósito de la firma")
    runFirmante: str = Field(..., description="RUN del firmante (sin puntos, con guión)", example="12644163-5")

    @validator('runFirmante')
    def validate_run(cls, v):
        # Eliminar puntos y guiones para validar
        run_limpio = v.replace('.', '').replace('-', '')
        if not run_limpio[:-1].isdigit():
            raise ValueError('El RUN debe contener solo números antes del dígito verificador')
        if len(run_limpio) < 2:
            raise ValueError('El RUN debe tener al menos un número y un dígito verificador')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "documentos": [
                    {
                        "base64": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL...",
                        "checksum": "259672a6fe8696b6dba05c97844f4ce04779bf61568c5a0e43d247f59e4e4eca",
                        "descripcion": "Resolución Concesión Subsidio",
                        "folio": 1619,
                        "formato": "PDF",
                        "nombre": "resolucion.pdf",
                        "region": 100000,
                        "tipoDocumento": "RESOLUCION_EXENTA"
                    }
                ],
                "proposito": "Firmar",
                "runFirmante": "12644163-5"
            }
        }


class FirmaDesatendidaResponse(BaseModel):
    """Modelo para respuesta de Firma Desatendida"""
    success: bool = Field(..., description="Indica si la firma fue exitosa")
    mensaje: str = Field(..., description="Mensaje de respuesta")
    documentosFirmados: Optional[List[dict]] = Field(None, description="Lista de documentos firmados con su información")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "mensaje": "Documentos firmados exitosamente",
                "documentosFirmados": [
                    {
                        "folio": 1619,
                        "nombre": "resolucion.pdf",
                        "estado": "FIRMADO"
                    }
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Modelo para respuestas de error"""
    success: bool = Field(default=False, description="Indica si la operación falló")
    mensaje: str = Field(..., description="Mensaje de error")
    codigo_error: Optional[str] = Field(None, description="Código de error específico")
    detalle: Optional[str] = Field(None, description="Detalle adicional del error")


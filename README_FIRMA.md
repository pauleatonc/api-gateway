# Servicio de Firma Desatendida SENCE

API REST para el servicio de Firma Desatendida de SENCE, que permite firmar documentos de forma automática sin intervención del usuario.

## Descripción

Este servicio actúa como una capa intermedia entre aplicaciones REST y el servicio SOAP de Firma Desatendida de SENCE, facilitando la integración mediante endpoints REST modernos.

## Endpoints Disponibles

### POST `/api/v1/firma/desatendida`

Realiza la firma desatendida de uno o más documentos.

#### Request Body

```json
{
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
```

#### Parámetros

- **documentos** (array, requerido): Lista de documentos a firmar
  - **base64** (string, requerido): Contenido del documento codificado en Base64
  - **checksum** (string, requerido): Hash SHA256 del documento (64 caracteres)
  - **descripcion** (string, requerido): Descripción del documento
  - **folio** (integer, requerido): Número de folio del documento
  - **formato** (string, requerido): Formato del documento (PDF, DOC, DOCX, XML)
  - **nombre** (string, requerido): Nombre del archivo
  - **region** (integer, requerido): Código de región (ej: 100000)
  - **tipoDocumento** (string, requerido): Tipo de documento (RESOLUCION_EXENTA, CONTRATO, CONVENIO, CERTIFICADO, OTRO)
- **proposito** (string, opcional): Propósito de la firma (Firmar, Visar, Aprobar). Default: "Firmar"
- **runFirmante** (string, requerido): RUN del firmante autorizado (puede incluir puntos y guión)

#### Response 200 OK

```json
{
  "success": true,
  "mensaje": "Documentos firmados exitosamente",
  "documentosFirmados": [
    {
      "folio": 1619,
      "nombre": "resolucion.pdf",
      "estado": "FIRMADO"
    }
  ]
}
```

#### Response 400 Bad Request

```json
{
  "success": false,
  "mensaje": "Error de validación",
  "codigo_error": "VALIDATION_ERROR",
  "detalle": "El checksum debe tener 64 caracteres"
}
```

#### Response 502 Bad Gateway

```json
{
  "success": false,
  "mensaje": "Error en el servicio SOAP",
  "codigo_error": "SOAP_FAULT",
  "detalle": "Error de comunicación con el servicio"
}
```

## Tipos de Documento

- `RESOLUCION_EXENTA`: Resolución exenta
- `CONTRATO`: Contrato
- `CONVENIO`: Convenio
- `CERTIFICADO`: Certificado
- `OTRO`: Otro tipo de documento

## Formatos de Documento Soportados

- `PDF`: Documento PDF
- `DOC`: Documento Microsoft Word (.doc)
- `DOCX`: Documento Microsoft Word (.docx)
- `XML`: Documento XML

## Propósitos de Firma

- `Firmar`: Firma electrónica del documento (default)
- `Visar`: Visación del documento
- `Aprobar`: Aprobación del documento

## Cálculo del Checksum

El checksum debe calcularse usando SHA256 sobre el contenido **original** del archivo (antes de codificar en Base64):

### Ejemplo en Python

```python
import hashlib
import base64

# Leer el archivo
with open('documento.pdf', 'rb') as f:
    contenido = f.read()

# Calcular checksum SHA256
checksum = hashlib.sha256(contenido).hexdigest()

# Codificar en Base64
base64_content = base64.b64encode(contenido).decode('utf-8')

print(f"Checksum: {checksum}")
print(f"Base64: {base64_content[:50]}...")
```

### Ejemplo en JavaScript/Node.js

```javascript
const crypto = require('crypto');
const fs = require('fs');

// Leer el archivo
const contenido = fs.readFileSync('documento.pdf');

// Calcular checksum SHA256
const checksum = crypto.createHash('sha256').update(contenido).digest('hex');

// Codificar en Base64
const base64Content = contenido.toString('base64');

console.log(`Checksum: ${checksum}`);
console.log(`Base64: ${base64Content.substring(0, 50)}...`);
```

## Códigos de Región

El código de región debe ser un valor numérico. Ejemplos comunes:

- `100000`: Región Metropolitana
- `80000`: Región del Biobío
- `130000`: Región de Los Lagos

(Consultar con SENCE para el listado completo de códigos de región)

## Ejemplo de Uso

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/firma/desatendida" \
  -H "Content-Type: application/json" \
  -d '{
    "documentos": [
      {
        "base64": "JVBERi0xLjQKJeLjz9MK...",
        "checksum": "259672a6fe8696b6dba05c97844f4ce04779bf61568c5a0e43d247f59e4e4eca",
        "descripcion": "Resolución de prueba",
        "folio": 1000,
        "formato": "PDF",
        "nombre": "resolucion_prueba.pdf",
        "region": 100000,
        "tipoDocumento": "RESOLUCION_EXENTA"
      }
    ],
    "proposito": "Firmar",
    "runFirmante": "12345678-9"
  }'
```

### Python con requests

```python
import requests
import base64
import hashlib

# Leer y preparar el documento
with open('documento.pdf', 'rb') as f:
    contenido = f.read()

checksum = hashlib.sha256(contenido).hexdigest()
base64_content = base64.b64encode(contenido).decode('utf-8')

# Preparar request
payload = {
    "documentos": [
        {
            "base64": base64_content,
            "checksum": checksum,
            "descripcion": "Resolución de prueba",
            "folio": 1000,
            "formato": "PDF",
            "nombre": "documento.pdf",
            "region": 100000,
            "tipoDocumento": "RESOLUCION_EXENTA"
        }
    ],
    "proposito": "Firmar",
    "runFirmante": "12345678-9"
}

# Realizar request
response = requests.post(
    "http://localhost:8000/api/v1/firma/desatendida",
    json=payload
)

print(response.json())
```

### JavaScript con fetch

```javascript
const fs = require('fs').promises;
const crypto = require('crypto');

async function firmarDocumento() {
  // Leer y preparar el documento
  const contenido = await fs.readFile('documento.pdf');
  const checksum = crypto.createHash('sha256').update(contenido).digest('hex');
  const base64Content = contenido.toString('base64');
  
  // Preparar request
  const payload = {
    documentos: [
      {
        base64: base64Content,
        checksum: checksum,
        descripcion: "Resolución de prueba",
        folio: 1000,
        formato: "PDF",
        nombre: "documento.pdf",
        region: 100000,
        tipoDocumento: "RESOLUCION_EXENTA"
      }
    ],
    proposito: "Firmar",
    runFirmante: "12345678-9"
  };
  
  // Realizar request
  const response = await fetch('http://localhost:8000/api/v1/firma/desatendida', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });
  
  const result = await response.json();
  console.log(result);
}

firmarDocumento();
```

## Consideraciones Importantes

1. **Tamaño de Documentos**: Los documentos grandes pueden exceder límites de payload HTTP. Considere dividir o comprimir documentos muy grandes.

2. **Tiempo de Respuesta**: La firma de múltiples documentos puede tomar tiempo. Configure timeouts apropiados en su cliente HTTP.

3. **Seguridad**: 
   - Nunca exponga directamente este servicio sin autenticación
   - Use HTTPS en producción
   - Valide los RUN de firmantes contra una lista autorizada
   - Registre todas las operaciones de firma para auditoría

4. **Manejo de Errores**: Implemente reintentos con backoff exponencial para errores temporales del servicio SOAP.

5. **Validación de Checksum**: Siempre valide que el checksum coincida con el contenido del documento antes de enviarlo.

## Variables de Entorno

Asegúrese de configurar las siguientes variables en su archivo `.env`:

```env
# Configuración del servicio SOAP de Firma
USE_SOAP_MOCKS=false
SOAP_TIMEOUT=60
```

## Testing

Para ejecutar los tests de este servicio:

```bash
pytest tests/test_firma.py -v
```

## Troubleshooting

### Error: "El checksum debe tener 64 caracteres"

**Solución**: El checksum debe ser un hash SHA256 en formato hexadecimal, que siempre tiene 64 caracteres. Verifique que está usando SHA256 y no otro algoritmo.

### Error: "SOAP_FAULT"

**Solución**: Verifique:
- La conectividad con el servicio SOAP
- Que el RUN del firmante esté autorizado
- Que el formato y contenido del documento sean correctos
- Los logs del servidor para más detalles

### Error: "Error de validación del RUN"

**Solución**: El RUN debe tener formato válido (números y dígito verificador). Puede incluir puntos y guión (12.345.678-9) o solo números (123456789).

## Soporte

Para más información sobre el servicio SOAP subyacente, consulte la documentación oficial de SENCE.

## Changelog

- **v1.0.0**: Implementación inicial del servicio de Firma Desatendida


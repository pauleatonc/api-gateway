# Módulo de Consulta Registro Civil SENCE

Este módulo implementa la integración con el servicio SOAP de Consulta Registro Civil de SENCE, proporcionando endpoints REST para consultar información del registro civil chileno.

## Características

- ✅ Integración completa con el WSDL de Consulta Registro Civil
- ✅ 6 endpoints REST con documentación automática
- ✅ Manejo de errores con códigos HTTP apropiados
- ✅ Soporte para mocks de desarrollo
- ✅ Tests completos con pytest (19 tests)
- ✅ Configuración optimizada para XML grandes
- ✅ Inyección de dependencias
- ✅ Logging estructurado

## Endpoints Disponibles

### 🔍 Consulta de Personas

#### 1. Consultar RUN
```
GET /api/v1/rc/run
```
Verifica el RUN de una persona en el Registro Civil.

**Parámetros de consulta:**
- `id_sistema` (int): ID del sistema que realiza la consulta
- `rut` (int): RUT de la persona a consultar
- `dv` (string, opcional): Dígito verificador del RUT

**Ejemplo de uso:**
```bash
curl -X GET "http://localhost:8000/api/v1/rc/run?id_sistema=1&rut=12345678&dv=9"
```

**Respuesta exitosa:**
```json
{
  "cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "respuesta": {
    "rut": 12345678,
    "dv": "9",
    "nombres": "Juan Carlos",
    "apellidoPaterno": "Pérez",
    "apellidoMaterno": "González",
    "fechaNacimiento": "1990-05-15T00:00:00Z",
    "sexo": "M",
    "nacionalidad": "CHILENA",
    "estadoCivil": "SOLTERO",
    "cantidadHijos": 0
  },
  "xmlRespuesta": "<ConsultaRun>...</ConsultaRun>"
}
```

#### 2. Consultar Número de Serie/Documento
```
GET /api/v1/rc/run/documento
```
Verifica el número de serie o número de documento del RUN.

**Parámetros de consulta:**
- `id_sistema` (int): ID del sistema que realiza la consulta
- `rut` (int): RUT de la persona
- `dv` (string, opcional): Dígito verificador del RUT
- `nro_serie_doc` (string, opcional): Número de serie del documento
- `tipo_documento` (enum): Tipo de documento (C, P, S, T, D)

**Tipos de documento:**
- `C`: Cédula de identidad
- `P`: Pasaporte
- `S`: Salvoconducto
- `T`: Título de viaje
- `D`: Documento de viaje

**Ejemplo de uso:**
```bash
curl -X GET "http://localhost:8000/api/v1/rc/run/documento?id_sistema=1&rut=12345678&tipo_documento=C"
```

#### 3. Consultar Certificado de Nacimiento
```
GET /api/v1/rc/cert-nac
```
Obtiene información del certificado de nacimiento.

**Parámetros de consulta:**
- `id_sistema` (int): ID del sistema que realiza la consulta
- `rut` (int): RUT de la persona
- `dv` (string, opcional): Dígito verificador del RUT

**Ejemplo de uso:**
```bash
curl -X GET "http://localhost:8000/api/v1/rc/cert-nac?id_sistema=1&rut=12345678"
```

**Respuesta exitosa:**
```json
{
  "Cabecera": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Consulta exitosa",
    "codigoProceso": 200
  },
  "Respuesta": {
    "rut": 12345678,
    "dv": "9",
    "circunscripcion": "SANTIAGO",
    "nombreCompleto": "Juan Carlos Pérez González",
    "fechaNacimiento": "1990-05-15T00:00:00Z",
    "sexo": "M",
    "lugarNacimiento": "SANTIAGO",
    "nacionalidadNacimiento": "CHILENA",
    "nombrePadre": "Pedro Pérez",
    "nombreMadre": "María González"
  },
  "XmlRespuesta": "<CertificadoNacimiento>...</CertificadoNacimiento>"
}
```

#### 4. Consultar Discapacidad
```
GET /api/v1/rc/discapacidad
```
Consulta si una persona tiene alguna discapacidad registrada.

**Parámetros de consulta:**
- `id_sistema` (int): ID del sistema que realiza la consulta
- `run` (int): RUN de la persona
- `dv` (string, opcional): Dígito verificador del RUN

**Ejemplo de uso:**
```bash
curl -X GET "http://localhost:8000/api/v1/rc/discapacidad?id_sistema=1&run=12345678"
```

### 🔒 Verificación de Huellas Dactilares

#### 5. Verificar Huella Dactilar (BATCH)
```
POST /api/v1/rc/verify
```
Verifica la huella dactilar mediante proceso BATCH de BioPortal.

**Cuerpo de la petición:**
```json
{
  "xmlparamin": "<xml><huella>...</huella></xml>"
}
```

**Ejemplo de uso:**
```bash
curl -X POST "http://localhost:8000/api/v1/rc/verify" \
     -H "Content-Type: application/json" \
     -d '{"xmlparamin": "<xml><huella>test</huella></xml>"}'
```

#### 6. Verificar Huella Dactilar
```
POST /api/v1/rc/huella
```
Verifica la huella dactilar de una persona.

**Cuerpo de la petición:**
```json
{
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
}
```

**Respuesta exitosa:**
```json
{
  "decision": true,
  "mensaje": "Verificación exitosa",
  "mensajeDetalle": "Huella dactilar verificada correctamente",
  "estructuraDatos": {
    "Puntaje": 85,
    "RespuestaAFIS": "Hit"
  },
  "TipoRespuesta": "CorrectoNegocio"
}
```

## Respuestas Estándar

### Estados de Proceso
- `NULO`: Estado nulo
- `CORRECTO`: Operación exitosa
- `INCORRECTO`: Operación incorrecta
- `PROCESAR`: En proceso
- `ERROR`: Error en la operación
- `EXCEPCION`: Excepción en la operación

### Respuesta de Error (502)
```json
{
  "success": false,
  "mensaje": "Error al conectar con el servicio SOAP",
  "codigo_error": "SOAP_FAULT",
  "detalle": "Error al comunicarse con el servicio SOAP"
}
```

## Configuración

### Variables de Entorno

```bash
# Configuración SOAP
USE_SOAP_MOCKS=true
SOAP_TIMEOUT=30
SOAP_RETRY_ATTEMPTS=3
```

### Modo de Desarrollo (Mocks)

Por defecto, el sistema usa mocks para facilitar el desarrollo:

```bash
USE_SOAP_MOCKS=true
```

#### Datos de Prueba para Mocks

- **RUT válido**: Cualquier RUT excepto `11111111`
- **RUT de error**: `11111111` (simula error)
- **Tipo de documento**: `C` (Cédula), `P` (Pasaporte), etc.
- **Número de dedo**: 1-10 (para verificación de huella)
- **Formato de huella**: 1 (formato estándar)

### Modo de Producción

Para usar el servicio SOAP real:

```bash
USE_SOAP_MOCKS=false
```

## Instalación y Ejecución

### 1. Activar el entorno virtual
```bash
source venv/bin/activate
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

### 4. Ejecutar la aplicación
```bash
uvicorn app.main:app --reload
```

### 5. Ejecutar con Docker
```bash
docker build -t fastapi-soap-service .
docker run -p 8000:8000 --env-file .env fastapi-soap-service
```

## Tests

### Ejecutar tests del módulo de consulta RC
```bash
pytest tests/test_consulta_rc.py -v
```

### Ejecutar todos los tests
```bash
pytest tests/ -v
```

### Tests con coverage
```bash
pytest tests/test_consulta_rc.py --cov=app --cov-report=html
```

### Estructura de Tests

Los tests incluyen:
- ✅ **19 tests** para el módulo de consulta RC
- ✅ Tests de éxito para todos los endpoints
- ✅ Tests de error (SOAP faults, conexión, etc.)
- ✅ Tests de validación de datos
- ✅ Tests de integración completa
- ✅ Tests de manejo de excepciones

## Documentación de la API

Una vez que la aplicación esté ejecutándose:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Arquitectura del Módulo

### Estructura de Archivos

```
app/
├── models/
│   └── consulta_rc.py                 # Modelos Pydantic
├── services/
│   └── consulta_rc_soap_client.py     # Cliente SOAP
├── api/v1/
│   └── consulta_rc.py                 # Endpoints REST
└── main.py                           # Configuración principal
```

### Componentes Principales

1. **Modelos Pydantic**: Validación automática de datos
2. **Cliente SOAP**: Integración con zeep y manejo de errores
3. **Endpoints REST**: Mapeo de SOAP a REST con documentación
4. **Inyección de Dependencias**: Cliente SOAP como dependencia
5. **Mocks**: Datos de prueba para desarrollo

## Manejo de Errores

### Tipos de Errores

1. **Errores de Validación (422)**: Parámetros de entrada inválidos
2. **Errores de Servicio SOAP (502)**: 
   - `SOAP_FAULT`: Error del servicio SOAP
   - `INTERNAL_ERROR`: Error interno del servidor

### Logging

El sistema incluye logging estructurado:

```python
logger.info(f"Consultando RUN: {rut}")
logger.error(f"Error SOAP: {fault}")
```

## Optimizaciones SOAP

El cliente SOAP está configurado para:

- **XML grandes**: `xml_huge_tree = True`
- **Parsing flexible**: `strict = False`
- **Sin cache**: `cache = None`
- **Timeouts configurables**

## Ejemplos de Uso

### Usando Python

```python
import requests

# Consultar RUN
response = requests.get(
    "http://localhost:8000/api/v1/rc/run",
    params={
        "id_sistema": 1,
        "rut": 12345678,
        "dv": "9"
    }
)

print(response.json())

# Verificar huella dactilar
response = requests.post(
    "http://localhost:8000/api/v1/rc/huella",
    json={
        "IdSistema": 1,
        "Datos": {
            "RutEmpresa": 76543210,
            "IdTransaccion": 12345,
            "RutPersona": 12345678,
            "NumeroDedo": 1,
            "Formato": 1
        }
    }
)

print(response.json())
```

### Usando JavaScript

```javascript
// Consultar certificado de nacimiento
const response = await fetch('/api/v1/rc/cert-nac?id_sistema=1&rut=12345678');
const data = await response.json();
console.log(data);

// Verificar huella dactilar
const huellaResponse = await fetch('/api/v1/rc/huella', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    IdSistema: 1,
    Datos: {
      RutEmpresa: 76543210,
      IdTransaccion: 12345,
      RutPersona: 12345678,
      NumeroDedo: 1,
      Formato: 1
    }
  })
});

const huellaData = await huellaResponse.json();
console.log(huellaData);
```

## Contribución

Para agregar nuevos endpoints:

1. Definir modelos en `app/models/consulta_rc.py`
2. Implementar método en `app/services/consulta_rc_soap_client.py`
3. Crear endpoint en `app/api/v1/consulta_rc.py`
4. Agregar tests en `tests/test_consulta_rc.py`

## Estado del Proyecto

✅ **Módulo completamente funcional**:
- 6 endpoints REST implementados ✅
- Modelos Pydantic simplificados ✅
- Cliente SOAP con mocks ✅
- 19 tests (100% pasando) ✅
- Documentación automática ✅
- Configuración por variables de entorno ✅
- Manejo robusto de errores ✅
- Documentación completa ✅

## Seguridad

- Validación de entrada con Pydantic
- Manejo seguro de errores sin exposición de detalles internos
- Timeouts configurables para evitar ataques DoS
- Logging de operaciones para auditoría

## Licencia

MIT License 
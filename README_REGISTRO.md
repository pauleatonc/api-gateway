# Módulo de Registro SENCE

Este módulo implementa la integración con el servicio SOAP de Registro de SENCE (WsRegistroCUS), proporcionando endpoints REST para todas las operaciones del WSDL.

## Características

- ✅ Integración completa con el WSDL de Registro de SENCE
- ✅ 11 endpoints REST con documentación automática
- ✅ Manejo de errores con códigos HTTP apropiados
- ✅ Soporte para mocks de desarrollo
- ✅ Tests completos con pytest (17 tests)
- ✅ Configuración optimizada para XML grandes
- ✅ Inyección de dependencias
- ✅ Logging estructurado

## Endpoints Disponibles

### 👤 Registro de Personas

#### 1. Registrar Persona
```
POST /api/v1/registro/persona
```
Registra una persona en el sistema SENCE.

**Cuerpo de la petición:**
```json
{
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
}
```

#### 2. Registrar Persona en CRM
```
POST /api/v1/registro/persona/crm
```
Registra una persona en el sistema CRM de SENCE.

**Cuerpo de la petición:**
```json
{
  "idSistema": 1,
  "datosPersona": {
    "Rut": 12345678,
    "Dv": "9",
    "Contacto": {
      "IdComuna": 13101,
      "Email": "contacto@example.com",
      "NumeroCelular": 987654321,
      "CodigoTelefonoFijo": 2,
      "TelefonoFijo": 22345678
    }
  }
}
```

#### 3. Registrar Persona en SIAC-OIRS
```
POST /api/v1/registro/persona/siac
```
Registra una persona en el sistema SIAC-OIRS de SENCE.

### 🏢 Registro de Empresas

#### 4. Registrar Empresa
```
POST /api/v1/registro/empresa
```
Registra una empresa en el sistema SENCE.

**Cuerpo de la petición:**
```json
{
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
}
```

#### 5. Actualizar Empresa
```
PUT /api/v1/registro/empresa
```
Actualiza los datos de una empresa existente.

#### 6. Actualizar Razón Social
```
PATCH /api/v1/registro/empresa/razon
```
Actualiza la razón social de una empresa.

**Cuerpo de la petición:**
```json
{
  "idSistema": 1,
  "rutEmpresa": 76543210,
  "dvEmpresa": "K"
}
```

#### 7. Actualizar Representantes Legales
```
PATCH /api/v1/registro/empresa/rep-legal
```
Actualiza los representantes legales de una empresa.

#### 8. Actualizar Tipo de Entidad
```
PATCH /api/v1/registro/empresa/tipo
```
Actualiza el tipo de entidad de una empresa.

**Cuerpo de la petición:**
```json
{
  "idSistema": 1,
  "rutEmpresa": 76543210,
  "dvEmpresa": "K",
  "tipoEntidad": "OTEC"
}
```

**Tipos de entidad disponibles:**
- `EMPRESA`
- `OTEC`
- `OTIC`

#### 9. Registrar Empresa con CUS
```
POST /api/v1/registro/empresa/con-cus
```
Registra una empresa con código CUS.

#### 10. Cambiar CUS de Empresa
```
PATCH /api/v1/registro/empresa/cambio-cus
```
Cambia el código CUS de una empresa.

**Cuerpo de la petición:**
```json
{
  "idSistema": 1,
  "rutEmpresa": 76543210,
  "dvRutEmpresa": "K",
  "cusActual": "CUS123456",
  "nuevaCus": "CUS789012"
}
```

#### 11. Registrar Empresa en Oracle
```
POST /api/v1/registro/empresa/oracle
```
Registra una empresa en el sistema Oracle de SENCE.

**Cuerpo de la petición:**
```json
{
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
}
```

## Respuestas Estándar

Todos los endpoints retornan una respuesta estándar basada en `RespuestaProcesoBe`:

### Respuesta Exitosa
```json
{
  "estadoProceso": "CORRECTO",
  "codigoProceso": 200,
  "respuestaProceso": "Operación exitosa"
}
```

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
  "codigo_error": "SOAP_ERROR",
  "detalle": "Error al comunicarse con el servicio SOAP de registro"
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
- **Tipo de empresa**: `1` (empresa), `2` (OTEC), `3` (OTIC)
- **ID Comuna**: `13101` (Las Condes)
- **ID Sexo**: `1` (Masculino), `2` (Femenino)
- **ID Nacionalidad**: `1` (Chilena)

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

### Ejecutar tests del módulo de registro
```bash
pytest tests/test_registro.py -v
```

### Ejecutar todos los tests
```bash
pytest tests/ -v
```

### Tests con coverage
```bash
pytest tests/test_registro.py --cov=app --cov-report=html
```

### Estructura de Tests

Los tests incluyen:
- ✅ **17 tests** para el módulo de registro
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
│   └── registro.py                    # Modelos Pydantic
├── services/
│   └── registro_soap_client.py        # Cliente SOAP
├── api/v1/
│   └── registro.py                    # Endpoints REST
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

1. **Errores de Validación (422)**: Datos de entrada inválidos
2. **Errores de Servicio SOAP (502)**: 
   - `SOAP_FAULT`: Error del servicio SOAP
   - `CONNECTION_ERROR`: Error de conexión
   - `INTERNAL_ERROR`: Error interno del servidor

### Logging

El sistema incluye logging estructurado:

```python
logger.info(f"Registrando persona con RUT: {rut}")
logger.error(f"Error SOAP: {fault}")
```

## Optimizaciones SOAP

El cliente SOAP está configurado para:

- **XML grandes**: `xml_huge_tree = True`
- **Parsing flexible**: `strict = False`
- **Sin cache**: `cache = None`
- **Timeouts configurables**

## Ejemplos de Uso

### Usando cURL

```bash
# Registrar persona
curl -X POST "http://localhost:8000/api/v1/registro/persona" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'

# Registrar empresa
curl -X POST "http://localhost:8000/api/v1/registro/empresa" \
     -H "Content-Type: application/json" \
     -d '{
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
     }'
```

### Usando Python

```python
import requests

# Registrar persona
response = requests.post(
    "http://localhost:8000/api/v1/registro/persona",
    json={
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
    }
)

print(response.json())
```

## Contribución

Para agregar nuevos endpoints:

1. Definir modelos en `app/models/registro.py`
2. Implementar método en `app/services/registro_soap_client.py`
3. Crear endpoint en `app/api/v1/registro.py`
4. Agregar tests en `tests/test_registro.py`

## Estado del Proyecto

✅ **Módulo completamente funcional**:
- 11 endpoints REST implementados
- Modelos Pydantic completos
- Cliente SOAP con mocks
- 17 tests (100% pasando)
- Documentación automática
- Configuración por variables de entorno
- Manejo robusto de errores

## Licencia

MIT License 
# Módulo de Identificación SENCE

Este módulo implementa la integración con el servicio SOAP de Identificación de SENCE, proporcionando endpoints REST para facilitar el acceso a las funcionalidades del WSDL.

## Características

- ✅ Integración completa con el WSDL de SENCE
- ✅ Endpoints REST con documentación automática
- ✅ Manejo de errores con códigos HTTP apropiados
- ✅ Soporte para mocks de desarrollo
- ✅ Tests completos con pytest
- ✅ Configuración optimizada para XML grandes
- ✅ Inyección de dependencias
- ✅ Logging estructurado

## Endpoints Disponibles

### 1. Iniciar Sesión
```
POST /api/v1/auth/login
```
Inicia sesión con usuario y contraseña.

**Cuerpo de la petición:**
```json
{
  "usuario": "mi_usuario",
  "clave": "mi_clave"
}
```

**Respuesta exitosa:**
```json
{
  "success": true,
  "token": "abc123token",
  "guid": "550e8400-e29b-41d4-a716-446655440000",
  "mensaje": "Sesión iniciada correctamente",
  "codigo_error": null
}
```

### 2. Iniciar Sesión por GUID
```
POST /api/v1/auth/login/guid
```
Inicia sesión usando un GUID de sesión.

**Cuerpo de la petición:**
```json
{
  "guid": "550e8400-e29b-41d4-a716-446655440000"
}
```

### 3. Validar Token
```
POST /api/v1/auth/login/token
```
Valida un token de sesión existente.

**Cuerpo de la petición:**
```json
{
  "token": "abc123token"
}
```

### 4. Obtener Sistemas por RUT
```
GET /api/v1/auth/systems/{rut}
```
Obtiene la lista de sistemas disponibles para un RUT específico.

**Parámetros:**
- `rut`: RUT del usuario (formato: 12345678-9)

**Respuesta exitosa:**
```json
{
  "success": true,
  "sistemas": [
    {
      "nombre": "Sistema de Capacitación",
      "url": "https://capacitacion.sence.cl",
      "descripcion": "Sistema para gestión de capacitaciones"
    }
  ],
  "mensaje": "Listado obtenido correctamente",
  "codigo_error": null
}
```

## Configuración

### Variables de Entorno

Copia el archivo `env.example` a `.env` y configura las siguientes variables:

```bash
# Configuración SENCE
SENCE_WSDL_URL=https://wsdesa.sence.cl/WsComponentes/WsIdentificacion.asmx?wsdl
USE_SOAP_MOCKS=true

# Configuración SOAP
SOAP_TIMEOUT=30
SOAP_RETRY_ATTEMPTS=3
```

### Modo de Desarrollo (Mocks)

Por defecto, el sistema usa mocks para facilitar el desarrollo. Para usar mocks:

```bash
USE_SOAP_MOCKS=true
```

#### Datos de Prueba para Mocks

- **Usuario válido**: `test_user` / `test_pass`
- **GUID válido**: `550e8400-e29b-41d4-a716-446655440000`
- **Token válido**: `mock_token_123` o `mock_token_from_guid_123`
- **RUT válido**: `12345678-9`

### Modo de Producción

Para usar el servicio SOAP real:

```bash
USE_SOAP_MOCKS=false
```

## Instalación y Ejecución

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

### 3. Ejecutar la aplicación
```bash
# Modo desarrollo
python -m app.main

# O con uvicorn
uvicorn app.main:app --reload
```

### 4. Ejecutar con Docker
```bash
# Construir imagen
docker build -t fastapi-soap-service .

# Ejecutar contenedor
docker run -p 8000:8000 --env-file .env fastapi-soap-service
```

## Tests

### Ejecutar todos los tests
```bash
pytest tests/test_identificacion.py -v
```

### Ejecutar tests con coverage
```bash
pytest tests/test_identificacion.py --cov=app --cov-report=html
```

### Estructura de Tests

Los tests incluyen:
- ✅ Tests de éxito para todos los endpoints
- ✅ Tests de error (credenciales inválidas, SOAP faults, etc.)
- ✅ Tests de validación de datos
- ✅ Tests de integración completa
- ✅ Tests con mocks y sin mocks

## Documentación de la API

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Manejo de Errores

El sistema maneja los siguientes tipos de errores:

### Errores de Validación (400)
Datos de entrada inválidos o faltantes.

### Errores de Servicio SOAP (502)
- **SOAP_FAULT**: Error devuelto por el servicio SOAP
- **CONNECTION_ERROR**: Error de conexión con el servicio
- **INTERNAL_ERROR**: Error interno del servidor

### Respuesta de Error Típica
```json
{
  "success": false,
  "mensaje": "Error al conectar con el servicio SOAP",
  "codigo_error": "SOAP_FAULT",
  "detalle": "Timeout al conectar con el servidor"
}
```

## Arquitectura

### Estructura del Módulo

```
app/
├── models/
│   └── identificacion.py          # Modelos Pydantic
├── services/
│   └── soap_client.py             # Cliente SOAP
├── api/v1/
│   └── identificacion.py          # Endpoints REST
└── config/
    └── settings.py                # Configuración
```

### Componentes Principales

1. **Modelos Pydantic**: Validación automática de datos
2. **Cliente SOAP**: Integración con zeep y manejo de errores
3. **Endpoints REST**: Mapeo de SOAP a REST con documentación
4. **Inyección de Dependencias**: Cliente SOAP como dependencia
5. **Configuración**: Settings centralizados con pydantic-settings

## Optimizaciones para XML Grandes

El cliente SOAP está configurado para manejar documentos XML grandes:

- `xml_huge_tree = True`: Soporte para árboles XML grandes
- `strict = False`: Parsing menos estricto
- `cache = None`: Sin cache para XML grandes
- Timeouts configurables

## Logging

El sistema incluye logging estructurado:

```python
logger.info(f"Iniciando sesión para usuario: {usuario}")
logger.error(f"Error SOAP: {fault}")
```

Los logs se almacenan en el directorio `logs/` y se rotan automáticamente.

## Contribución

Para agregar nuevos endpoints:

1. Añadir modelos en `models/identificacion.py`
2. Implementar método en `services/soap_client.py`
3. Crear endpoint en `api/v1/identificacion.py`
4. Agregar tests en `tests/test_identificacion.py`

## Licencia

MIT License 
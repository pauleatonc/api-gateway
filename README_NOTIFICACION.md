# Módulo de Notificación SENCE

Este módulo implementa la integración con el servicio SOAP de Notificación de SENCE para envío de SMS, correos electrónicos públicos, internos y mixtos.

## Características

- **4 endpoints REST** básicos que mapean a operaciones SOAP
- **Envío de SMS** a números de celular
- **Correos públicos** (Gmail, Hotmail, etc.)
- **Correos con respuesta** detallada
- **Modo mock** para desarrollo
- **Validación de datos** con Pydantic
- **Tests unitarios** completos

## Endpoints Disponibles

### 1. Enviar SMS
```
POST /api/v1/notificacion/sms
```

**Request:**
```json
{
  "idSistema": 1,
  "ambiente": "desarrollo",
  "celular": 987654321,
  "mensaje": "Hola desde SENCE"
}
```

**Response:**
```json
{
  "success": true,
  "mensaje": "SMS enviado correctamente"
}
```

### 2. Enviar Correo Público
```
POST /api/v1/notificacion/correo/publico
```

**Request:**
```json
{
  "idSistema": 1,
  "ambiente": "desarrollo",
  "mail": "usuario@ejemplo.com",
  "asunto": "Notificación SENCE",
  "mensaje": "Contenido del correo"
}
```

### 3. Enviar Lista de Correos
```
POST /api/v1/notificacion/correo/publico/lista
```

**Request:**
```json
{
  "idSistema": 1,
  "ambiente": "desarrollo",
  "lstMails": ["usuario1@ejemplo.com", "usuario2@ejemplo.com"],
  "asunto": "Notificación masiva",
  "mensaje": "Contenido del correo masivo"
}
```

### 4. Enviar Correo con Respuesta
```
POST /api/v1/notificacion/correo/publico/rm
```

**Response:**
```json
{
  "estado": {
    "estadoProceso": "CORRECTO",
    "respuestaProceso": "Correo enviado correctamente"
  },
  "mailsNoInsertados": []
}
```

## Configuración

### Variables de Entorno

```bash
# Modo mock para desarrollo
USE_SOAP_MOCKS=true

# Configuración SOAP
SOAP_TIMEOUT=30
SOAP_RETRY_ATTEMPTS=3
```

### WSDL URL

```
https://wsdesa.sence.cl/wscomponentes/wsnotificacion.asmx?wsdl
```

## Validaciones

- **Números de celular:** Deben tener 9 dígitos (100000000 - 999999999)
- **Emails:** Deben contener el símbolo `@`
- **Archivos:** Deben estar en formato base64 válido

## Uso

```bash
# Enviar SMS
curl -X POST "http://localhost:8000/api/v1/notificacion/sms" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "ambiente": "desarrollo",
    "celular": 987654321,
    "mensaje": "Hola desde la API"
  }'

# Enviar correo
curl -X POST "http://localhost:8000/api/v1/notificacion/correo/publico" \
  -H "Content-Type: application/json" \
  -d '{
    "idSistema": 1,
    "ambiente": "desarrollo",
    "mail": "usuario@ejemplo.com",
    "asunto": "Notificación",
    "mensaje": "Contenido del correo"
  }'
```

## Tests

```bash
# Ejecutar tests del módulo
python -m pytest tests/test_notificacion.py -v

# Ejecutar todos los tests
python -m pytest tests/ -v
```

## Arquitectura

```
app/
├── models/notificacion.py          # Esquemas Pydantic
├── services/notificacion_soap_client.py   # Cliente SOAP
├── api/v1/notificacion.py          # Router REST
└── tests/test_notificacion.py      # Tests unitarios
```

## Estados del Proceso

- `CORRECTO`: Operación exitosa
- `INCORRECTO`: Operación incorrecta
- `ERROR`: Error en la operación
- `EXCEPCION`: Excepción en el proceso

## Documentación

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

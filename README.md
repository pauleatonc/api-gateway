# FastAPI SOAP Service

API REST que sirve como capa intermedia para servicios SOAP, construida con FastAPI.

## 🚀 Características

- **FastAPI**: Framework moderno para crear APIs REST de alto rendimiento
- **Documentación automática**: OpenAPI/Swagger UI disponible en `/docs`
- **Logging estructurado**: Configurado con Loguru para mejor observabilidad
- **Manejo de errores**: Middleware global para respuestas uniformes
- **Configuración flexible**: Variables de entorno con pydantic-settings
- **Contenedores Docker**: Imagen optimizada para producción
- **Tests incluidos**: Suite de tests con pytest
- **Preparado para SOAP**: Arquitectura lista para integrar servicios SOAP

## 📁 Estructura del Proyecto

```
fastapi-soap-service/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── health.py       # Endpoints de salud
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py         # Configuración con pydantic-settings
│   │   └── logging.py          # Configuración de logging
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── error_handler.py    # Middleware para manejo de errores
│   ├── models/
│   │   ├── __init__.py
│   │   └── responses.py        # Modelos de respuesta
│   └── utils/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Configuración de tests
│   ├── test_main.py            # Tests principales
│   └── test_health.py          # Tests de salud
├── logs/                       # Directorio de logs (generado automáticamente)
├── requirements.txt            # Dependencias de Python
├── env.example                 # Ejemplo de variables de entorno
├── Dockerfile                  # Imagen Docker optimizada
├── docker-compose.yml          # Orquestación con Docker Compose
├── pytest.ini                 # Configuración de pytest
└── README.md                   # Este archivo
```

## 🔧 Instalación y Configuración

### Prerrequisitos

- Python 3.12+
- pip

### Instalación Local

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd fastapi-soap-service
   ```

2. **Crear y activar entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   cp env.example .env
   # Editar .env con tus configuraciones
   ```

5. **Ejecutar la aplicación**
   ```bash
   python -m app.main
   # O usando uvicorn directamente:
   uvicorn app.main:app --reload
   ```

### Instalación con Docker

1. **Construir la imagen**
   ```bash
   docker build -t fastapi-soap-service .
   ```

2. **Ejecutar el contenedor**
   ```bash
   docker run -p 8000:8000 fastapi-soap-service
   ```

3. **Usar Docker Compose (recomendado)**
   ```bash
   docker-compose up -d
   ```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` basado en `env.example`:

```env
# Configuración de la aplicación
APP_NAME=FastAPI SOAP Service
APP_VERSION=1.0.0
DEBUG=false

# Configuración del servidor
HOST=0.0.0.0
PORT=8000

# Configuración de logging
LOG_LEVEL=INFO

# Configuración de CORS
ALLOW_ORIGINS=["*"]
ALLOW_METHODS=["*"]
ALLOW_HEADERS=["*"]

# Configuración para servicios SOAP
SOAP_TIMEOUT=30
SOAP_RETRY_ATTEMPTS=3

# Configuración de entorno
ENVIRONMENT=production
```

### Configuración de Logging

Los logs se configuran automáticamente con Loguru y se guardan en:
- `logs/app.log`: Logs de la aplicación
- `logs/access.log`: Logs de acceso
- Salida estándar (stdout) con colores

## 📊 Endpoints

### Endpoints de Salud

- **GET /api/v1/health/**: Health check principal
- **GET /api/v1/health/ready**: Readiness check
- **GET /api/v1/health/live**: Liveness check

### Endpoints de Información

- **GET /**: Información básica de la API
- **GET /info**: Información detallada de la aplicación

### Documentación

- **GET /docs**: Swagger UI
- **GET /redoc**: ReDoc
- **GET /openapi.json**: Esquema OpenAPI

## 🧪 Tests

### Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con coverage
pytest --cov=app

# Ejecutar solo tests unitarios
pytest -m unit

# Ejecutar solo tests de integración
pytest -m integration

# Ejecutar tests en modo verbose
pytest -v
```

### Tipos de Tests

- **Unit Tests**: Tests unitarios para funciones individuales
- **Integration Tests**: Tests de integración para endpoints completos
- **Slow Tests**: Tests marcados como lentos (pueden omitirse)

## 🐳 Docker

### Dockerfile

La imagen Docker está optimizada para producción:
- Base: Python 3.12 slim
- Usuario no privilegiado
- Capas cacheables
- Health check incluido
- Logs persistentes

### Docker Compose

El archivo `docker-compose.yml` incluye:
- Servicio principal de la API
- Configuración de red
- Volúmenes para logs
- Health checks
- Servicios comentados para PostgreSQL y Redis (uso futuro)

## 🚦 Desarrollo

### Agregar Nuevos Endpoints

1. Crear el router en `app/api/v1/`
2. Definir modelos en `app/models/`
3. Incluir el router en `app/main.py`
4. Agregar tests en `tests/`

### Estructura de Archivos

```python
# app/api/v1/nuevo_endpoint.py
from fastapi import APIRouter
from app.models.responses import SuccessResponse

router = APIRouter(prefix="/nuevo", tags=["Nuevo"])

@router.get("/", response_model=SuccessResponse)
async def nuevo_endpoint():
    return SuccessResponse(message="Nuevo endpoint")
```

### Integración con Servicios SOAP

Para integrar servicios SOAP:

1. Instalar cliente SOAP (ej: `zeep`)
2. Crear servicio en `app/services/`
3. Configurar endpoints en `app/config/settings.py`
4. Implementar endpoints REST que llamen a SOAP

## 🔍 Monitoring y Observabilidad

### Logs

- Logs estructurados con Loguru
- Rotación automática de archivos
- Diferentes niveles de log por componente
- Logs de request/response automáticos

### Health Checks

- **Health**: Estado general de la aplicación
- **Readiness**: Verificación de dependencias
- **Liveness**: Verificación de vida del proceso

### Métricas

Para agregar métricas (futuro):
- Prometheus metrics
- Tiempo de respuesta
- Contadores de errores
- Métricas de negocio

## 🛠️ Mantenimiento

### Actualización de Dependencias

```bash
# Actualizar requirements.txt
pip freeze > requirements.txt

# Verificar vulnerabilidades
pip audit

# Actualizar imagen Docker
docker build -t fastapi-soap-service:latest .
```

### Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f api

# Ver logs específicos
tail -f logs/app.log
```

## 📝 Próximos Pasos

1. **Integración SOAP**: Agregar clientes para servicios SOAP específicos
2. **Base de Datos**: Configurar PostgreSQL para persistencia
3. **Autenticación**: Implementar JWT o OAuth2
4. **Cache**: Agregar Redis para cache de respuestas
5. **Monitoring**: Implementar Prometheus y Grafana
6. **CI/CD**: Configurar pipelines de integración continua

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-feature`)
3. Commit tus cambios (`git commit -am 'Agregar nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

Para más información, consulta la documentación automática en `/docs` cuando la aplicación esté ejecutándose. 
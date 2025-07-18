"""
Middleware para manejo global de errores
"""
import traceback
from typing import Any, Dict
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware para manejo global de errores"""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return await self.handle_error(request, exc)
    
    async def handle_error(self, request: Request, exc: Exception) -> JSONResponse:
        """Manejar errores y devolver respuesta JSON uniforme"""
        
        # Log del error
        logger.error(
            f"Error en {request.method} {request.url.path}: {str(exc)}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        
        # Determinar el tipo de error y respuesta
        error_response = self._create_error_response(exc)
        
        return JSONResponse(
            status_code=error_response["status_code"],
            content=error_response["content"]
        )
    
    def _create_error_response(self, exc: Exception) -> Dict[str, Any]:
        """Crear respuesta de error basada en el tipo de excepción"""
        
        # Errores específicos
        if isinstance(exc, ValueError):
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "content": {
                    "error": "Bad Request",
                    "message": str(exc),
                    "code": "VALIDATION_ERROR"
                }
            }
        
        elif isinstance(exc, FileNotFoundError):
            return {
                "status_code": status.HTTP_404_NOT_FOUND,
                "content": {
                    "error": "Not Found",
                    "message": "El recurso solicitado no fue encontrado",
                    "code": "RESOURCE_NOT_FOUND"
                }
            }
        
        elif isinstance(exc, PermissionError):
            return {
                "status_code": status.HTTP_403_FORBIDDEN,
                "content": {
                    "error": "Forbidden",
                    "message": "No tiene permisos para acceder a este recurso",
                    "code": "PERMISSION_DENIED"
                }
            }
        
        elif isinstance(exc, TimeoutError):
            return {
                "status_code": status.HTTP_504_GATEWAY_TIMEOUT,
                "content": {
                    "error": "Gateway Timeout",
                    "message": "El servicio no respondió en el tiempo esperado",
                    "code": "TIMEOUT_ERROR"
                }
            }
        
        # Error genérico
        else:
            return {
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "content": {
                    "error": "Internal Server Error",
                    "message": "Ha ocurrido un error interno del servidor",
                    "code": "INTERNAL_ERROR"
                }
            } 
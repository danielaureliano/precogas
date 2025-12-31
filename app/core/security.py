from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adiciona headers de segurança HTTP para reforçar a proteção do cliente (browser).
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # HSTS (HTTP Strict Transport Security) - Força HTTPS por 1 ano
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Previne que o site seja carregado em iframes (Clickjacking)
        response.headers["X-Frame-Options"] = "DENY"
        
        # Previne sniffing de MIME type
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        return response
"""
Metrics Module

Provides Prometheus-based metrics collection for microservices.
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

http_requests_in_progress = Gauge(
    'http_requests_in_progress',
    'Number of HTTP requests in progress',
    ['method', 'endpoint']
)

business_operations_total = Counter(
    'business_operations_total',
    'Total business operations',
    ['operation', 'status']
)

business_operation_duration_seconds = Histogram(
    'business_operation_duration_seconds',
    'Business operation duration in seconds',
    ['operation']
)


class MetricsCollector:
    """
    Metrics collector for business operations
    """
    
    @staticmethod
    def record_operation(operation: str, status: str = "success"):
        """Record a business operation"""
        business_operations_total.labels(operation=operation, status=status).inc()
    
    @staticmethod
    def time_operation(operation: str):
        """Context manager to time a business operation"""
        return business_operation_duration_seconds.labels(operation=operation).time()
    
    @staticmethod
    def increment_counter(name: str, labels: dict = None):
        """Increment a custom counter"""
        if labels:
            counter = Counter(name, f'Custom counter: {name}', list(labels.keys()))
            counter.labels(**labels).inc()
        else:
            counter = Counter(name, f'Custom counter: {name}')
            counter.inc()


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for automatic metrics collection
    
    Collects RED metrics (Rate, Errors, Duration) for all HTTP requests.
    """
    
    async def dispatch(self, request: Request, call_next):
        method = request.method
        endpoint = request.url.path
        
        # Track requests in progress
        http_requests_in_progress.labels(method=method, endpoint=endpoint).inc()
        
        # Time the request
        start_time = time.time()
        
        try:
            response = await call_next(request)
            status = response.status_code
        except Exception as e:
            status = 500
            logger.error(f"Error processing request: {e}")
            raise
        finally:
            # Record metrics
            duration = time.time() - start_time
            
            http_requests_total.labels(
                method=method,
                endpoint=endpoint,
                status=status
            ).inc()
            
            http_request_duration_seconds.labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
            
            http_requests_in_progress.labels(method=method, endpoint=endpoint).dec()
        
        return response


def get_metrics():
    """Get MetricsCollector instance"""
    return MetricsCollector()


def metrics_endpoint():
    """
    Endpoint to expose Prometheus metrics
    
    Usage:
        @app.get("/metrics")
        async def metrics():
            return metrics_endpoint()
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

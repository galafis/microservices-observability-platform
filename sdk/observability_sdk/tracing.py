"""
Distributed Tracing Module

Provides OpenTelemetry-based distributed tracing for microservices.
"""

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    HAS_INSTRUMENTATION = True
except ImportError:
    HAS_INSTRUMENTATION = False
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


def setup_tracing(service_name: str, jaeger_host: str = "localhost", jaeger_port: int = 6831):
    """
    Setup distributed tracing with Jaeger
    
    Args:
        service_name: Name of the service
        jaeger_host: Jaeger agent host
        jaeger_port: Jaeger agent port
    """
    resource = Resource(attributes={
        SERVICE_NAME: service_name
    })
    
    tracer_provider = TracerProvider(resource=resource)
    
    jaeger_exporter = JaegerExporter(
        agent_host_name=jaeger_host,
        agent_port=jaeger_port,
    )
    
    span_processor = BatchSpanProcessor(jaeger_exporter)
    tracer_provider.add_span_processor(span_processor)
    
    trace.set_tracer_provider(tracer_provider)
    
    # Auto-instrument common libraries if available
    if HAS_INSTRUMENTATION:
        try:
            RequestsInstrumentor().instrument()
            logger.info("Requests instrumentation enabled")
        except Exception as e:
            logger.warning(f"Could not instrument requests: {e}")
    
    logger.info(f"Tracing initialized for service: {service_name}")


def get_tracer(name: str = __name__):
    """Get a tracer instance"""
    return trace.get_tracer(name)


class TracingMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for distributed tracing
    
    Automatically creates spans for incoming requests and propagates trace context.
    """
    
    async def dispatch(self, request: Request, call_next):
        tracer = get_tracer(__name__)
        
        with tracer.start_as_current_span(
            f"{request.method} {request.url.path}",
            kind=trace.SpanKind.SERVER
        ) as span:
            # Add request attributes to span
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.url", str(request.url))
            span.set_attribute("http.route", request.url.path)
            
            # Add custom attributes
            if request.client:
                span.set_attribute("http.client_ip", request.client.host)
            
            # Process request
            response = await call_next(request)
            
            # Add response attributes
            span.set_attribute("http.status_code", response.status_code)
            
            return response

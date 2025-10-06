"""
Observability SDK for Microservices

A comprehensive SDK for instrumenting microservices with distributed tracing,
metrics, and structured logging.
"""

from .tracing import TracingMiddleware, get_tracer, setup_tracing
from .metrics import MetricsMiddleware, get_metrics, metrics_endpoint
from .logging import setup_logging, get_logger

__version__ = "0.1.0"
__author__ = "Gabriel Demetrios Lafis"

__all__ = [
    "TracingMiddleware",
    "MetricsMiddleware",
    "setup_logging",
    "setup_tracing",
    "get_tracer",
    "get_metrics",
    "get_logger",
    "metrics_endpoint",
]

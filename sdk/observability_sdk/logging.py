"""
Structured Logging Module

Provides JSON structured logging with correlation IDs and trace context.
"""

import logging
import json
import sys
from datetime import datetime
from typing import Optional
from contextvars import ContextVar
from opentelemetry import trace

# Context variable for correlation ID
correlation_id_var: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


class StructuredFormatter(logging.Formatter):
    """
    JSON formatter for structured logging
    """
    
    def format(self, record: logging.LogRecord) -> str:
        # Get trace context
        span = trace.get_current_span()
        trace_id = None
        span_id = None
        
        if span.get_span_context().is_valid:
            trace_id = format(span.get_span_context().trace_id, '032x')
            span_id = format(span.get_span_context().span_id, '016x')
        
        # Build structured log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add trace context
        if trace_id:
            log_entry["trace_id"] = trace_id
            log_entry["span_id"] = span_id
        
        # Add correlation ID
        correlation_id = correlation_id_var.get()
        if correlation_id:
            log_entry["correlation_id"] = correlation_id
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
        
        return json.dumps(log_entry)


class StructuredLogger(logging.LoggerAdapter):
    """
    Logger adapter for adding structured fields
    """
    
    def process(self, msg, kwargs):
        # Extract extra fields
        extra = kwargs.get('extra', {})
        
        # Add correlation ID
        correlation_id = correlation_id_var.get()
        if correlation_id:
            extra['correlation_id'] = correlation_id
        
        kwargs['extra'] = {'extra_fields': extra}
        return msg, kwargs


def setup_logging(
    service_name: str,
    level: str = "INFO",
    json_format: bool = True
) -> None:
    """
    Setup structured logging
    
    Args:
        service_name: Name of the service
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        json_format: Use JSON format for logs
    """
    log_level = getattr(logging, level.upper())
    
    # Create handler
    handler = logging.StreamHandler(sys.stdout)
    
    if json_format:
        formatter = StructuredFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    
    # Add service name to all logs
    logging.info(f"Logging initialized for service: {service_name}")


def get_logger(name: str) -> StructuredLogger:
    """
    Get a structured logger instance
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        StructuredLogger instance
    """
    logger = logging.getLogger(name)
    return StructuredLogger(logger, {})


def set_correlation_id(correlation_id: str) -> None:
    """Set correlation ID for current context"""
    correlation_id_var.set(correlation_id)


def get_correlation_id() -> Optional[str]:
    """Get correlation ID from current context"""
    return correlation_id_var.get()

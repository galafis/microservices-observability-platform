# 🔭 Microservices Observability Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

[English](#english) | [Português](#português)

---

<a name="english"></a>

## 📖 Overview

A **comprehensive observability platform** for microservices architectures with distributed tracing, metrics collection, and structured logging. This project provides production-ready observability infrastructure and SDK for instrumenting Python microservices.

### Key Features

- **🔍 Distributed Tracing**: OpenTelemetry + Jaeger for end-to-end request tracing
- **📊 Metrics Collection**: Prometheus for RED metrics (Rate, Errors, Duration)
- **📝 Structured Logging**: JSON logs with correlation IDs and trace context
- **📈 Visualization**: Grafana dashboards for real-time monitoring
- **🛠️ Observability SDK**: Easy-to-use Python SDK for service instrumentation
- **🐳 Docker Compose**: Complete stack ready to run
- **🎯 Production-Ready**: Best practices for observability in microservices

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Observability Platform                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │  API Gateway │   │ User Service │   │Order Service │        │
│  │   :8000      │   │    :8001     │   │    :8002     │        │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘        │
│         │                  │                   │                 │
│         └──────────────────┼───────────────────┘                 │
│                            │                                     │
│         ┌──────────────────┼───────────────────┐                │
│         │                  │                   │                 │
│         ▼                  ▼                   ▼                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   Jaeger    │    │ Prometheus  │    │   Grafana   │         │
│  │   :16686    │    │    :9090    │    │    :3000    │         │
│  │  (Tracing)  │    │  (Metrics)  │    │ (Dashboard) │         │
│  └─────────────┘    └─────────────┘    └─────────────┘         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker** and **Docker Compose**
- **Python 3.11+** (for local development)

### Running the Complete Stack

```bash
# Clone the repository
git clone https://github.com/galafis/microservices-observability-platform.git
cd microservices-observability-platform

# Start all services
docker-compose up -d

# Check service health
curl http://localhost:8000/  # API Gateway
curl http://localhost:8001/  # User Service
```

### Access Observability Tools

- **Jaeger UI**: http://localhost:16686 (Distributed Tracing)
- **Prometheus**: http://localhost:9090 (Metrics)
- **Grafana**: http://localhost:3000 (Dashboards)
  - Username: `admin`
  - Password: `admin`

---

## 💻 Observability SDK Usage

### 1. Install SDK

```bash
pip install -r requirements.txt
```

### 2. Instrument Your Service

```python
from fastapi import FastAPI
from observability_sdk import (
    TracingMiddleware,
    MetricsMiddleware,
    setup_logging,
    setup_tracing,
    get_logger,
    get_metrics,
    metrics_endpoint
)

# Initialize observability
setup_logging("my-service", level="INFO", json_format=True)
setup_tracing("my-service", jaeger_host="localhost")

logger = get_logger(__name__)
metrics = get_metrics()

# Create FastAPI app
app = FastAPI(title="My Service")

# Add observability middleware
app.add_middleware(TracingMiddleware)
app.add_middleware(MetricsMiddleware)

# Add metrics endpoint
@app.get("/metrics")
async def metrics_route():
    return metrics_endpoint()

# Your business logic
@app.get("/users")
async def list_users():
    logger.info("Listing users")
    
    with metrics.time_operation("list_users"):
        # Your code here
        metrics.record_operation("list_users", "success")
        return {"users": []}
```

### 3. Structured Logging

```python
from observability_sdk import get_logger

logger = get_logger(__name__)

# Log with structured fields
logger.info("User created", extra={
    "user_id": 123,
    "username": "john_doe",
    "action": "create"
})

# Output (JSON):
# {
#   "timestamp": "2025-10-06T12:00:00Z",
#   "level": "INFO",
#   "message": "User created",
#   "trace_id": "abc123...",
#   "span_id": "def456...",
#   "user_id": 123,
#   "username": "john_doe",
#   "action": "create"
# }
```

### 4. Custom Metrics

```python
from observability_sdk import get_metrics

metrics = get_metrics()

# Record business operations
metrics.record_operation("payment_processed", "success")
metrics.record_operation("payment_processed", "failed")

# Time operations
with metrics.time_operation("database_query"):
    # Your code here
    pass
```

---

## 📊 Observability Features

### Distributed Tracing

**OpenTelemetry + Jaeger** provides:
- End-to-end request tracing across services
- Automatic span creation for HTTP requests
- Trace context propagation
- Latency analysis per span
- Service dependency mapping

**Example Trace**:
```
API Gateway → User Service → Database
   100ms         50ms          30ms
```

### Metrics Collection

**Prometheus** collects RED metrics:
- **Rate**: Requests per second
- **Errors**: Error rate
- **Duration**: Request latency (p50, p95, p99)

**Available Metrics**:
- `http_requests_total` - Total HTTP requests
- `http_request_duration_seconds` - Request duration histogram
- `http_requests_in_progress` - Current requests in progress
- `business_operations_total` - Business operation counter
- `business_operation_duration_seconds` - Business operation duration

### Structured Logging

**JSON logs** with:
- Timestamp (ISO 8601)
- Log level
- Message
- Trace ID and Span ID (for correlation)
- Correlation ID
- Custom fields
- Exception stack traces

---

## 🐳 Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| api-gateway | 8000 | API Gateway |
| user-service | 8001 | User management service |
| order-service | 8002 | Order management service |
| payment-service | 8003 | Payment processing service |
| jaeger | 16686 | Jaeger UI (tracing) |
| prometheus | 9090 | Prometheus (metrics) |
| grafana | 3000 | Grafana (dashboards) |
| redis | 6379 | Redis (caching) |

---

## 📁 Project Structure

```
microservices-observability-platform/
├── sdk/
│   └── observability_sdk/
│       ├── __init__.py
│       ├── tracing.py          # Distributed tracing
│       ├── metrics.py          # Prometheus metrics
│       └── logging.py          # Structured logging
├── services/
│   ├── api-gateway/            # API Gateway
│   ├── user-service/           # User service example
│   ├── order-service/          # Order service example
│   └── payment-service/        # Payment service example
├── infrastructure/
│   ├── prometheus/
│   │   └── prometheus.yml      # Prometheus config
│   └── grafana/
│       ├── provisioning/       # Grafana provisioning
│       └── dashboards/         # Pre-built dashboards
├── docker-compose.yml          # Complete stack
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| Web Framework | FastAPI |
| Tracing | OpenTelemetry + Jaeger |
| Metrics | Prometheus |
| Visualization | Grafana |
| Logging | Structured JSON |
| Containerization | Docker + Docker Compose |
| Caching | Redis |

---

## 📈 Grafana Dashboards

Pre-configured dashboards for:
1. **System Overview**: All services health and performance
2. **Service Details**: Per-service metrics and traces
3. **RED Metrics**: Rate, Errors, Duration
4. **SLIs/SLOs**: Service Level Indicators and Objectives

---

## 🧪 Testing

### Run Unit Tests

```bash
pytest tests/ -v
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load/locustfile.py --host=http://localhost:8000
```

### Test Observability

```bash
# Generate some traffic
for i in {1..100}; do
  curl http://localhost:8001/users
  sleep 0.1
done

# Check Jaeger for traces
open http://localhost:16686

# Check Prometheus for metrics
open http://localhost:9090
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Service configuration
PORT=8001
SERVICE_NAME=user-service

# Jaeger configuration
JAEGER_HOST=localhost
JAEGER_PORT=6831

# Log level
LOG_LEVEL=INFO
```

### Prometheus Scrape Configuration

Edit `infrastructure/prometheus/prometheus.yml` to add new services:

```yaml
scrape_configs:
  - job_name: 'my-new-service'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['my-new-service:8004']
```

---

## 📊 Best Practices

### Tracing
- Create spans for significant operations
- Add relevant attributes to spans
- Propagate trace context across services
- Use meaningful span names

### Metrics
- Follow RED metrics pattern (Rate, Errors, Duration)
- Use histograms for latency measurements
- Add labels for dimensionality (but not too many)
- Expose `/metrics` endpoint on all services

### Logging
- Use structured (JSON) logging
- Include correlation IDs
- Log at appropriate levels
- Avoid logging sensitive data
- Include context in log messages

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-lafis)

---

<a name="português"></a>

## 📖 Visão Geral

Uma **plataforma abrangente de observabilidade** para arquiteturas de microsserviços com distributed tracing, coleta de métricas e logging estruturado. Este projeto fornece infraestrutura de observabilidade pronta para produção e SDK para instrumentar microsserviços Python.

### Principais Recursos

- **🔍 Distributed Tracing**: OpenTelemetry + Jaeger para rastreamento end-to-end
- **📊 Coleta de Métricas**: Prometheus para métricas RED (Rate, Errors, Duration)
- **📝 Logging Estruturado**: Logs JSON com correlation IDs e trace context
- **📈 Visualização**: Dashboards Grafana para monitoramento em tempo real
- **🛠️ SDK de Observabilidade**: SDK Python fácil de usar
- **🐳 Docker Compose**: Stack completo pronto para executar
- **🎯 Pronto para Produção**: Best practices de observabilidade

---

## 🚀 Início Rápido

### Pré-requisitos

- **Docker** e **Docker Compose**
- **Python 3.11+** (para desenvolvimento local)

### Executando a Stack Completa

```bash
# Clone o repositório
git clone https://github.com/galafis/microservices-observability-platform.git
cd microservices-observability-platform

# Inicie todos os serviços
docker-compose up -d

# Verifique a saúde dos serviços
curl http://localhost:8000/  # API Gateway
curl http://localhost:8001/  # User Service
```

### Acessar Ferramentas de Observabilidade

- **Jaeger UI**: http://localhost:16686 (Distributed Tracing)
- **Prometheus**: http://localhost:9090 (Métricas)
- **Grafana**: http://localhost:3000 (Dashboards)
  - Usuário: `admin`
  - Senha: `admin`

---

## 💻 Uso do SDK de Observabilidade

### 1. Instalar SDK

```bash
pip install -r requirements.txt
```

### 2. Instrumentar Seu Serviço

```python
from fastapi import FastAPI
from observability_sdk import (
    TracingMiddleware,
    MetricsMiddleware,
    setup_logging,
    setup_tracing,
    get_logger,
    get_metrics,
    metrics_endpoint
)

# Inicializar observabilidade
setup_logging("meu-servico", level="INFO", json_format=True)
setup_tracing("meu-servico", jaeger_host="localhost")

logger = get_logger(__name__)
metrics = get_metrics()

# Criar app FastAPI
app = FastAPI(title="Meu Serviço")

# Adicionar middleware de observabilidade
app.add_middleware(TracingMiddleware)
app.add_middleware(MetricsMiddleware)

# Adicionar endpoint de métricas
@app.get("/metrics")
async def metrics_route():
    return metrics_endpoint()

# Sua lógica de negócio
@app.get("/usuarios")
async def listar_usuarios():
    logger.info("Listando usuários")
    
    with metrics.time_operation("listar_usuarios"):
        # Seu código aqui
        metrics.record_operation("listar_usuarios", "success")
        return {"usuarios": []}
```

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 👤 Autor

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-lafis)

---

## ⭐ Mostre seu apoio

Se este projeto foi útil para você, considere dar uma ⭐️!

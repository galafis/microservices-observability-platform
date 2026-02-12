# 🚀 Microservices Observability Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)](https://fastapi.tiangolo.com/)
[![Prometheus](https://img.shields.io/badge/Prometheus-2.48-E6522C.svg)](https://prometheus.io/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D.svg)](https://redis.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](#english) | [Português](#português)

---

## English

### 🎯 Overview

**Microservices Observability Platform** — Professional Python project

Total source lines: **546** across **5** files in **1** language.

### ✨ Key Features

- **Production-Ready Architecture**: Modular, well-documented, and following best practices
- **Comprehensive Implementation**: Complete solution with all core functionality
- **Clean Code**: Type-safe, well-tested, and maintainable codebase
- **Easy Deployment**: Docker support for quick setup and deployment

### 🚀 Quick Start

#### Prerequisites
- Python 3.12+
- Docker and Docker Compose (optional)

#### Installation

1. **Clone the repository**
```bash
git clone https://github.com/galafis/microservices-observability-platform.git
cd microservices-observability-platform
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Running

```bash
python services/user-service/main.py
```

## 🐳 Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```




### 📁 Project Structure

```
microservices-observability-platform/
├── docs/
│   ├── FAQ.md
│   ├── USE_CASES.md
│   └── observability.md
├── infrastructure/
│   └── prometheus/
│       └── prometheus.yml
├── sdk/
│   └── observability_sdk/
│       ├── __init__.py
│       ├── logging.py
│       ├── metrics.py
│       └── tracing.py
├── services/
│   └── user-service/
│       └── main.py
├── CHANGELOG.md
├── README.md
├── docker-compose.yml
└── requirements.txt
```

### 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python | 5 files |

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👤 Author

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

---

## Português

### 🎯 Visão Geral

**Microservices Observability Platform** — Professional Python project

Total de linhas de código: **546** em **5** arquivos em **1** linguagem.

### ✨ Funcionalidades Principais

- **Arquitetura Pronta para Produção**: Modular, bem documentada e seguindo boas práticas
- **Implementação Completa**: Solução completa com todas as funcionalidades principais
- **Código Limpo**: Type-safe, bem testado e manutenível
- **Fácil Implantação**: Suporte Docker para configuração e implantação rápidas

### 🚀 Início Rápido

#### Pré-requisitos
- Python 3.12+
- Docker e Docker Compose (opcional)

#### Instalação

1. **Clone the repository**
```bash
git clone https://github.com/galafis/microservices-observability-platform.git
cd microservices-observability-platform
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

#### Execução

```bash
python services/user-service/main.py
```




### 📁 Estrutura do Projeto

```
microservices-observability-platform/
├── docs/
│   ├── FAQ.md
│   ├── USE_CASES.md
│   └── observability.md
├── infrastructure/
│   └── prometheus/
│       └── prometheus.yml
├── sdk/
│   └── observability_sdk/
│       ├── __init__.py
│       ├── logging.py
│       ├── metrics.py
│       └── tracing.py
├── services/
│   └── user-service/
│       └── main.py
├── CHANGELOG.md
├── README.md
├── docker-compose.yml
└── requirements.txt
```

### 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|------------|-----|
| Python | 5 files |

### 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

### 👤 Autor

**Gabriel Demetrios Lafis**

- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

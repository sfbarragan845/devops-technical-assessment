# DevOps Microservice - Technical Assessment

![CI/CD](https://github.com/sfbarragan845/devops-technical-assessment/workflows/CI%2FCD%20Pipeline/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Azure](https://img.shields.io/badge/azure-AKS-0078D4.svg)

Microservicio REST API desarrollado en Python con Flask, containerizado con Docker, orquestado con Kubernetes y con pipeline CI/CD automatizado.

## 📋 Tabla de Contenidos

- [Requisitos](#requisitos)
- [Características](#características)
- [Instalación](#instalación)
- [Uso](#uso)
- [Testing](#testing)
- [Deployment](#deployment)
- [Arquitectura](#arquitectura)
- [API Documentation](#api-documentation)

## 🎯 Requisitos Cumplidos

✅ **Microservicio REST** con endpoint `/DevOps` (POST)  
✅ **Autenticación**: API Key + JWT único por transacción  
✅ **Containerización**: Docker con multi-stage build  
✅ **Load Balancer**: Kubernetes Ingress + mínimo 2 nodos  
✅ **IaC**: Terraform + Kubernetes manifests versionados  
✅ **CI/CD Pipeline**: GitHub Actions con múltiples stages  
✅ **Testing**: Pytest con coverage > 80%  
✅ **Static Analysis**: Pylint, Flake8, Black, MyPy  
✅ **Dynamic Scaling**: Horizontal Pod Autoscaler  
✅ **API Manager**: Generación y validación de JWT  

## 🚀 Características

- **Clean Code**: Código limpio siguiendo PEP 8
- **TDD**: Desarrollo guiado por tests
- **Security**: API Key + JWT authentication
- **High Availability**: Múltiples replicas con auto-scaling
- **Monitoring**: Health checks y readiness probes
- **Observability**: Logs estructurados y métricas

## 📦 Instalación

### Prerrequisitos

- Python 3.11+
- Docker 24+
- Kubernetes 1.28+
- Terraform 1.0+
- kubectl
- Git

### Setup Local

```powershell
# Clonar repositorio
git clone https://github.com/sfbarragan845/devops-technical-assessment.git
cd devops-technical-assessment

# Instalar dependencias (usando Make)
make install

# Ejecutar tests con coverage
make test

# Ver todos los comandos disponibles
make help

# Ejecutar localmente
make run
```

## 🔧 Uso

### 1. Generar JWT Token

```bash
curl -X POST http://localhost:5000/generate-jwt \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "Content-Type: application/json"
```

Respuesta:
```json
{
  "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

### 2. Llamar al Endpoint /DevOps

```bash
curl -X POST https://your-domain.com/DevOps \
  -H "X-Parse-REST-API-Key: 2f5ae96c-b558-4c7b-a590-a501ae1c3f6c" \
  -H "X-JWT-KWY: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "message": "This is a test",
    "to": "Juan Perez",
    "from": "Rita Asturia",
    "timeToLifeSec": 45
  }'
```

Respuesta:
```json
{
  "message": "Hello Juan Perez your message will be send"
}
```

### 3. Health Checks

```bash
# Health check
curl http://localhost:5000/health

# Readiness check
curl http://localhost:5000/ready
```

## 🧪 Testing

```powershell
# Ejecutar todos los tests
make test

# Tests con coverage detallado
make test-coverage

# Ver reporte HTML de coverage
Start-Process htmlcov/index.html

# Lint del código
make lint

# Formatear código
make format
```

### Coverage y Quality

- **Test Coverage**: > 80% (objetivo cumplido)
- **Linters**: Pylint, Flake8, Black, MyPy
- **Framework**: Pytest + pytest-cov + pytest-flask

## 🐳 Docker

### Build y Run Local

```powershell
# Build (usando Make)
make docker-build

# Run container
make docker-run

# Docker Compose (con load balancer y 2 instancias)
make docker-compose-up

# Ver logs
make docker-logs

# Detener stack
make docker-compose-down
```

### Multi-stage Build

El Dockerfile usa multi-stage build para:
- Reducir tamaño de imagen (de ~1GB a ~150MB)
- Separar dependencias de build y runtime
- Mejorar seguridad (usuario no-root)

## ☸️ Kubernetes Deployment

### Prerequisitos

```powershell
# Configurar kubectl para Azure AKS
az aks get-credentials --resource-group your-rg --name your-cluster
```

### Deploy a Development

```powershell
# Deploy completo
make k8s-deploy-dev

# Ver status
make k8s-status-dev

# Ver logs
make k8s-logs-dev

# Port forward para testing local
make k8s-port-forward-dev
```

### Deploy a Production

```powershell
# Deploy completo
make k8s-deploy-prod

# Ver status
make k8s-status-prod

# Ver logs
make k8s-logs-prod

# Reiniciar deployment
make k8s-restart-prod
```

### Configuración del Cluster

- **Replicas**: 3 (mínimo 2 requerido)
- **Resources**:
  - Request: 100m CPU, 128Mi RAM
  - Limit: 500m CPU, 256Mi RAM
- **HPA**: Auto-scaling de 2 a 10 pods
- **Load Balancer**: Nginx Ingress

## 🏗️ Infrastructure as Code (Terraform)

```powershell
cd terraform/

# Inicializar
terraform init

# Plan
terraform plan

# Aplicar
terraform apply -auto-approve

# Destruir (cuidado!)
terraform destroy
```

### Recursos Creados en Azure

- **Azure Container Registry (ACR)**: Repositorio de imágenes Docker
- **Azure Kubernetes Service (AKS)**: Cluster Kubernetes administrado
- **Virtual Network**: Red virtual con subnets
- **Resource Group**: Grupo de recursos
- **Managed Identity**: Identidad para AKS
- **Log Analytics Workspace**: Monitoreo y logs

## 🔄 CI/CD Pipeline

El pipeline se ejecuta automáticamente en:
- Push a `main`, `master`, `develop`
- Pull Requests
- Manual dispatch

### Stages

1. **Lint**: Pylint, Flake8, Black, MyPy
2. **Test**: Pytest con coverage
3. **Build**: Docker image + vulnerability scan
4. **Deploy Dev**: Auto-deploy a development
5. **Deploy Prod**: Auto-deploy a production (solo main/master)

### Configuración

Variables necesarias en GitHub Secrets:
- `AZURE_REGISTRY_NAME`: devopstechnicalassessment.azurecr.io
- `AZURE_REGISTRY_USERNAME`: Usuario de ACR
- `AZURE_REGISTRY_PASSWORD`: Password de ACR
- `KUBE_CONFIG_DEV`: Kubeconfig para development
- `KUBE_CONFIG_PROD`: Kubeconfig para production
- `API_KEY`: Api key para ejecutar http request
- `JWT_SECRET`: JWT Secret para generar JWT para production
- `API_KEY_TEST`: Api key para ejecutar http request para development
- `JWT_SECRET_TEST`: JWT Secret para generar JWT para development

## 📊 Arquitectura

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│   Load Balancer     │ (Ingress)
│    (Nginx)          │
└──────┬──────────────┘
       │
       ├────────┬────────┬────────┐
       ▼        ▼        ▼        ▼
    ┌────┐   ┌────┐   ┌────┐   ┌────┐
    │Pod1│   │Pod2│   │Pod3│   │PodN│
    └────┘   └────┘   └────┘   └────┘
       │        │        │        │
       └────────┴────────┴────────┘
                │
                ▼
         ┌─────────────┐
         │  Secrets    │
         │  ConfigMap  │
         └─────────────┘
```

## 📚 API Documentation

### Endpoints

#### POST /DevOps
Endpoint principal del microservicio.

**Headers**:
- `X-Parse-REST-API-Key`: API Key (obligatorio)
- `X-JWT-KWY`: JWT Token (obligatorio)
- `Content-Type`: application/json

**Body**:
```json
{
  "message": "string",
  "to": "string",
  "from": "string",
  "timeToLifeSec": integer
}
```

**Response 200**:
```json
{
  "message": "Hello {to} your message will be send"
}
```

**Errores**:
- `401`: Missing API Key or JWT
- `403`: Invalid API Key or JWT
- `400`: Invalid payload
- `405`: Method not allowed

#### GET /health
Health check endpoint.

#### GET /ready
Readiness check endpoint.

#### POST /generate-jwt
Genera un nuevo JWT token.

## 🔐 Seguridad

- API Key validation en headers
- JWT único por transacción
- Secrets manejados con Kubernetes Secrets
- Container ejecuta como usuario no-root
- Vulnerability scanning con Trivy
- Network policies en Kubernetes

## 📈 Monitoring y Observability

- **Health Checks**: Endpoints `/health` y `/ready`
- **Probes**: Liveness y Readiness probes configurados
- **Logs**: Azure Log Analytics + Container Insights
- **Métricas**: Azure Monitor + Kubernetes metrics
- **Auto-scaling**: HPA basado en CPU (80%) y memoria
- **Alertas**: Configurables en Azure Monitor

## 🤝 Contribuciones

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

## 🛠️ Comandos Útiles del Makefile

El proyecto incluye un Makefile completo con todos los comandos necesarios:

```powershell
make help                 # Ver todos los comandos disponibles

# Desarrollo
make install              # Instalar dependencias
make test                 # Ejecutar tests
make test-coverage        # Tests con coverage HTML
make lint                 # Linters (pylint + flake8 + black)
make format               # Formatear código con black
make run                  # Ejecutar localmente

# Docker
make docker-build         # Build imagen Docker
make docker-run           # Run container
make docker-push          # Push a Azure ACR
make docker-compose-up    # Levantar stack completo
make docker-compose-down  # Detener stack
make docker-logs          # Ver logs

# Kubernetes Development
make k8s-deploy-dev       # Deploy a development
make k8s-status-dev       # Ver status
make k8s-logs-dev         # Ver logs
make k8s-delete-dev       # Eliminar recursos

# Kubernetes Production
make k8s-deploy-prod      # Deploy a production
make k8s-status-prod      # Ver status
make k8s-logs-prod        # Ver logs
make k8s-restart-prod     # Reiniciar deployment

# Azure
make acr-login            # Login a Azure Container Registry
make acr-list-images      # Listar imágenes en ACR

# Limpieza
make clean                # Limpiar archivos temporales
make docker-clean         # Limpiar imágenes Docker
```

## 📝 Notas Importantes

- **JWT único por transacción**: Cada request debe usar un JWT diferente
- **API Key fijo**: Proporcionado por el evaluador
- **Métodos no POST**: Retornan "ERROR" con código 405
- **Coverage mínimo**: 80%
- **Clean Code**: Siguiendo principios SOLID

## 📞 Contacto

- **GitHub**: [@sfbarragan845](https://github.com/sfbarragan845)
- **Repositorio**: [devops-technical-assessment](https://github.com/sfbarragan845/devops-technical-assessment)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

**Fecha**: Noviembre 2025  
**Stack**: Python 3.11, Flask, Docker, Kubernetes (AKS), Azure Container Registry, Terraform, GitHub Actions  
**Cloud Provider**: Microsoft Azure
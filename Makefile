# Makefile - Comandos útiles del proyecto
.PHONY: help install test lint run docker-build docker-run clean k8s-*

# Variables
IMAGE_NAME := devopstechnicalassessment.azurecr.io/devops-technical-assessment
IMAGE_TAG := latest
REGISTRY := devopstechnicalassessment.azurecr.io
NAMESPACE_DEV := development
NAMESPACE_PROD := production

help:
	@echo "======================================"
	@echo "  DevOps Microservice - Comandos"
	@echo "======================================"
	@echo ""
	@echo "📦 Desarrollo Local:"
	@echo "  make install              - Instalar dependencias"
	@echo "  make test                 - Ejecutar tests"
	@echo "  make test-coverage        - Ejecutar tests con coverage"
	@echo "  make lint                 - Ejecutar linters"
	@echo "  make format               - Formatear código con black"
	@echo "  make run                  - Ejecutar localmente"
	@echo ""
	@echo "🐳 Docker Local:"
	@echo "  make docker-build         - Construir imagen Docker"
	@echo "  make docker-run           - Ejecutar container Docker"
	@echo "  make docker-push          - Push imagen a ACR"
	@echo "  make docker-compose-up    - Levantar stack completo"
	@echo "  make docker-compose-down  - Bajar stack completo"
	@echo "  make docker-logs          - Ver logs de containers"
	@echo ""
	@echo "☸️  Kubernetes - Development:"
	@echo "  make k8s-deploy-dev       - Deploy a development namespace"
	@echo "  make k8s-delete-dev       - Delete de development"
	@echo "  make k8s-status-dev       - Ver status de development"
	@echo "  make k8s-logs-dev         - Ver logs de development"
	@echo "  make k8s-describe-dev     - Describe pods de development"
	@echo ""
	@echo "☸️  Kubernetes - Production:"
	@echo "  make k8s-deploy-prod      - Deploy a production namespace"
	@echo "  make k8s-delete-prod      - Delete de production"
	@echo "  make k8s-status-prod      - Ver status de production"
	@echo "  make k8s-logs-prod        - Ver logs de production"
	@echo "  make k8s-describe-prod    - Describe pods de production"
	@echo ""
	@echo "🔧 Azure Container Registry:"
	@echo "  make acr-login            - Login a ACR"
	@echo "  make acr-list-images      - Listar imágenes en ACR"
	@echo ""
	@echo "🧹 Limpieza:"
	@echo "  make clean                - Limpiar archivos temporales"
	@echo "  make docker-clean         - Limpiar imágenes Docker locales"
	@echo ""

# ==========================================
# Desarrollo Local
# ==========================================

install:
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=app --cov-report=term-missing

test-coverage:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=xml
	@echo "✅ Coverage report: htmlcov/index.html"

lint:
	pylint app/
	flake8 app/
	black --check app/

format:
	black app/ tests/

run:
	python -m flask --app app.main run

# ==========================================
# Docker Local
# ==========================================

docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .
	@echo "✅ Imagen construida: $(IMAGE_NAME):$(IMAGE_TAG)"

docker-run:
	docker run -p 5000:5000 \
		-e PORT=5000 \
		-e API_KEY=2f5ae96c-b558-4c7b-a590-a501ae1c3f6c \
		-e JWT_SECRET=your-secret-key-change-in-production \
		-e JWT_EXPIRATION_HOURS=1 \
		$(IMAGE_NAME):$(IMAGE_TAG)

docker-push: docker-build acr-login
	docker push $(IMAGE_NAME):$(IMAGE_TAG)
	@echo "✅ Imagen pusheada a ACR: $(IMAGE_NAME):$(IMAGE_TAG)"

docker-compose-up:
	docker-compose up -d
	@echo "✅ Stack levantado en http://localhost:8080"

docker-compose-down:
	docker-compose down
	@echo "✅ Stack detenido"

docker-logs:
	docker-compose logs -f

docker-clean:
	docker system prune -af
	@echo "✅ Imágenes Docker locales limpiadas"

# ==========================================
# Azure Container Registry
# ==========================================

acr-login:
	az acr login --name devopstechnicalassessment
	@echo "✅ Logged in to ACR"

acr-list-images:
	az acr repository list --name devopstechnicalassessment --output table
	@echo ""
	az acr repository show-tags --name devopstechnicalassessment \
		--repository devops-technical-assessment --output table

# ==========================================
# Kubernetes - Development
# ==========================================

k8s-create-namespace-dev:
	kubectl create namespace $(NAMESPACE_DEV) --dry-run=client -o yaml | kubectl apply -f -
	@echo "✅ Namespace $(NAMESPACE_DEV) creado/verificado"

k8s-deploy-dev: k8s-create-namespace-dev
	kubectl apply -f k8s/configmap.yaml -n $(NAMESPACE_DEV)
	kubectl apply -f k8s/secret.yaml -n $(NAMESPACE_DEV)
	kubectl apply -f k8s/deployment.yaml -n $(NAMESPACE_DEV)
	kubectl apply -f k8s/service.yaml -n $(NAMESPACE_DEV)
	kubectl apply -f k8s/hpa.yaml -n $(NAMESPACE_DEV)
	@echo "✅ Deployment a $(NAMESPACE_DEV) completado"

k8s-delete-dev:
	kubectl delete -f k8s/ -n $(NAMESPACE_DEV) --ignore-not-found=true
	@echo "✅ Resources eliminados de $(NAMESPACE_DEV)"

k8s-status-dev:
	@echo "=== Pods ==="
	kubectl get pods -n $(NAMESPACE_DEV) -l app=devops-microservice
	@echo ""
	@echo "=== Services ==="
	kubectl get svc -n $(NAMESPACE_DEV)
	@echo ""
	@echo "=== Deployments ==="
	kubectl get deployments -n $(NAMESPACE_DEV)
	@echo ""
	@echo "=== HPA ==="
	kubectl get hpa -n $(NAMESPACE_DEV)

k8s-logs-dev:
	kubectl logs -f -n $(NAMESPACE_DEV) -l app=devops-microservice --tail=100

k8s-describe-dev:
	kubectl describe pods -n $(NAMESPACE_DEV) -l app=devops-microservice

k8s-restart-dev:
	kubectl rollout restart deployment/devops-microservice -n $(NAMESPACE_DEV)
	@echo "✅ Deployment reiniciado en $(NAMESPACE_DEV)"

# ==========================================
# Kubernetes - Production
# ==========================================

k8s-create-namespace-prod:
	kubectl create namespace $(NAMESPACE_PROD) --dry-run=client -o yaml | kubectl apply -f -
	@echo "✅ Namespace $(NAMESPACE_PROD) creado/verificado"

k8s-deploy-prod: k8s-create-namespace-prod
	kubectl apply -f k8s/configmap.yaml -n $(NAMESPACE_PROD)
	kubectl apply -f k8s/secret.yaml -n $(NAMESPACE_PROD)
	kubectl apply -f k8s/deployment.yaml -n $(NAMESPACE_PROD)
	kubectl apply -f k8s/service.yaml -n $(NAMESPACE_PROD)
	kubectl apply -f k8s/ingress.yaml -n $(NAMESPACE_PROD)
	kubectl apply -f k8s/hpa.yaml -n $(NAMESPACE_PROD)
	@echo "✅ Deployment a $(NAMESPACE_PROD) completado"

k8s-delete-prod:
	kubectl delete -f k8s/ -n $(NAMESPACE_PROD) --ignore-not-found=true
	@echo "✅ Resources eliminados de $(NAMESPACE_PROD)"

k8s-status-prod:
	@echo "=== Pods ==="
	kubectl get pods -n $(NAMESPACE_PROD) -l app=devops-microservice
	@echo ""
	@echo "=== Services ==="
	kubectl get svc -n $(NAMESPACE_PROD)
	@echo ""
	@echo "=== Deployments ==="
	kubectl get deployments -n $(NAMESPACE_PROD)
	@echo ""
	@echo "=== Ingress ==="
	kubectl get ingress -n $(NAMESPACE_PROD)
	@echo ""
	@echo "=== HPA ==="
	kubectl get hpa -n $(NAMESPACE_PROD)

k8s-logs-prod:
	kubectl logs -f -n $(NAMESPACE_PROD) -l app=devops-microservice --tail=100

k8s-describe-prod:
	kubectl describe pods -n $(NAMESPACE_PROD) -l app=devops-microservice

k8s-restart-prod:
	kubectl rollout restart deployment/devops-microservice -n $(NAMESPACE_PROD)
	@echo "✅ Deployment reiniciado en $(NAMESPACE_PROD)"

# ==========================================
# Kubernetes - Utilities
# ==========================================

k8s-port-forward-dev:
	kubectl port-forward -n $(NAMESPACE_DEV) svc/devops-microservice 5000:80
	@echo "Service available at http://localhost:5000"

k8s-port-forward-prod:
	kubectl port-forward -n $(NAMESPACE_PROD) svc/devops-microservice 5000:80
	@echo "Service available at http://localhost:5000"

k8s-shell-dev:
	kubectl exec -it -n $(NAMESPACE_DEV) $(kubectl get pod -n $(NAMESPACE_DEV) -l app=devops-microservice -o jsonpath='{.items[0].metadata.name}') -- /bin/sh

k8s-shell-prod:
	kubectl exec -it -n $(NAMESPACE_PROD) $(kubectl get pod -n $(NAMESPACE_PROD) -l app=devops-microservice -o jsonpath='{.items[0].metadata.name}') -- /bin/sh

# ==========================================
# Limpieza
# ==========================================

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf dist build *.egg-info
	@echo "✅ Archivos temporales limpiados"

---
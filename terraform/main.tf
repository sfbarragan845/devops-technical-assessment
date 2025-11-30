# ==============================
# Datos existentes de Azure
# ==============================
data "azurerm_resource_group" "rg" {
  name = var.resource_group_name
}

data "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = data.azurerm_resource_group.rg.name
}

# ==============================
# Crear AKS Cluster
# ==============================
resource "azurerm_kubernetes_cluster" "aks" {
  name                = var.aks_name
  location            = data.azurerm_resource_group.rg.location
  resource_group_name = data.azurerm_resource_group.rg.name
  dns_prefix          = "flask-aks"

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
  }
}

# ==============================
# Permisos AKS para ACR
# ==============================
resource "azurerm_role_assignment" "acr_pull" {
  principal_id         = azurerm_kubernetes_cluster.aks.kubelet_identity[0].object_id
  role_definition_name = "AcrPull"
  scope                = data.azurerm_container_registry.acr.id
}

# ==============================
# Kubernetes Provider
# ==============================
provider "kubernetes" {
  host                   = azurerm_kubernetes_cluster.aks.kube_config[0].host
  client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config[0].client_certificate)
  client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config[0].client_key)
  cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config[0].cluster_ca_certificate)
}

# ==============================
# Namespaces
# ==============================
resource "kubernetes_namespace" "production" {
  metadata {
    name = "production"
    labels = {
      name        = "production"
      environment = "production"
    }
  }
}

resource "kubernetes_namespace" "development" {
  metadata {
    name = "development"
    labels = {
      name        = "development"
      environment = "development"
    }
  }
}

# ==============================
# Deployment de Flask en Production
# ==============================
resource "kubernetes_deployment" "flask_production" {
  metadata {
    name      = "devops-microservice"
    namespace = kubernetes_namespace.production.metadata[0].name
    labels = {
      app = "devops-microservice"
    }
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "devops-microservice"
      }
    }

    template {
      metadata {
        labels = {
          app = "devops-microservice"
        }
      }

      spec {
        container {
          name  = "devops-microservice"
          image = var.docker_image

          ports {
            container_port = 5000
          }
        }
      }
    }
  }
}

# Service LoadBalancer para Production
resource "kubernetes_service" "flask_production" {
  metadata {
    name      = "devops-microservice"
    namespace = kubernetes_namespace.production.metadata[0].name
  }

  spec {
    selector = {
      app = kubernetes_deployment.flask_production.spec[0].template[0].metadata[0].labels["app"]
    }

    port {
      port        = 80
      target_port = 5000
    }

    type = "LoadBalancer"
  }
}

# ==============================
# Deployment de Flask en Development
# ==============================
resource "kubernetes_deployment" "flask_development" {
  metadata {
    name      = "devops-microservice-dev"
    namespace = kubernetes_namespace.development.metadata[0].name
    labels = {
      app = "devops-microservice-dev"
    }
  }

  spec {
    replicas = 2

    selector {
      match_labels = {
        app = "devops-microservice-dev"
      }
    }

    template {
      metadata {
        labels = {
          app = "devops-microservice-dev"
        }
      }

      spec {
        container {
          name  = "devops-microservice"
          image = var.docker_image_dev

          port {
            container_port = 5000
          }
        }
      }
    }
  }
}

# Service LoadBalancer para Development
resource "kubernetes_service" "flask_development" {
  metadata {
    name      = "devops-microservice-dev"
    namespace = kubernetes_namespace.development.metadata[0].name
  }

  spec {
    selector = {
      app = kubernetes_deployment.flask_development.spec[0].template[0].metadata[0].labels["app"]
    }

    port {
      port        = 80
      target_port = 5000
    }

    type = "LoadBalancer"
  }
}

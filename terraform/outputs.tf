output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "flask_service_ip" {
  value = kubernetes_service.flask_production.status[0].load_balancer[0].ingress[0].ip
  description = "Public IP of the Flask production service"
}

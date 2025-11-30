variable "resource_group_name" {
  type    = string
  default = "rg-devops-aks"
}

variable "location" {
  type    = string
  default = "East US"
}

variable "aks_name" {
  type    = string
  default = "aks-devops"
}

variable "acr_name" {
  type    = string
  default = "devopstechnicalassessment"
}

variable "docker_image" {
  type    = string
  default = "devopstechnicalassessment.azurecr.io/devops-technical-assessment:latest"
}

variable "docker_image_dev" {
  type    = string
  default = "devopstechnicalassessment.azurecr.io/devops-technical-assessment:latest"
}

variable "node_count" {
  type    = number
  default = 1
}

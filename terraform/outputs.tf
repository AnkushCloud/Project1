# GKE Cluster Information
output "cluster_name" {
  description = "GKE Cluster Name"
  value       = google_container_cluster.primary.name
}

output "cluster_region" {
  description = "GKE Cluster Region"
  value       = var.region
}

output "cluster_endpoint" {
  description = "GKE Cluster Endpoint"
  value       = google_container_cluster.primary.endpoint
  sensitive   = true
}

# Node Pool Information
output "node_pool_name" {
  description = "GKE Node Pool Name"
  value       = google_container_node_pool.primary_nodes.name
}

output "node_count" {
  description = "Number of nodes in the cluster"
  value       = google_container_node_pool.primary_nodes.node_count
}

output "machine_type" {
  description = "Machine type of nodes"
  value       = var.machine_type
}

# Network Information
output "vpc_name" {
  description = "VPC Name"
  value       = google_compute_network.vpc.name
}

output "subnet_name" {
  description = "Subnet Name"
  value       = google_compute_subnetwork.subnet.name
}

# Kubernetes Configuration
output "kubeconfig_command" {
  description = "Command to configure kubectl"
  value       = "gcloud container clusters get-credentials ${google_container_cluster.primary.name} --region ${var.region} --project ${var.project_id}"
}

# Application Access Information
output "application_url" {
  description = "URL to access the application"
  value       = "http://${data.kubernetes_service.web_app_service.status.0.load_balancer.0.ingress.0.ip}"
}

# Helm Release Information
output "helm_release_name" {
  description = "Name of the Helm release"
  value       = helm_release.web_app.name
}

output "helm_release_status" {
  description = "Status of the Helm release"
  value       = helm_release.web_app.status
}

# HPA Information
output "hpa_configuration" {
  description = "HPA configuration details"
  value = {
    min_replicas = 1
    max_replicas = 3
    target_cpu   = 50
  }
}

# Data source to get the LoadBalancer IP
data "kubernetes_service" "web_app_service" {
  metadata {
    name      = "web-app-service"
    namespace = "default"
  }

  depends_on = [helm_release.web_app]
}

output "load_balancer_ip" {
  description = "External IP address of the LoadBalancer"
  value       = data.kubernetes_service.web_app_service.status.0.load_balancer.0.ingress.0.ip
}

# Project Information
output "project_id" {
  description = "Google Cloud Project ID"
  value       = var.project_id
}

# Useful Commands
output "useful_commands" {
  description = "Useful commands for managing the deployment"
  value = {
    get_pods         = "kubectl get pods -w"
    get_services     = "kubectl get services"
    get_hpa          = "kubectl get hpa -w"
    get_nodes        = "kubectl get nodes"
    view_logs        = "kubectl logs -l app=web-app --tail=50"
    load_test        = "python3 ../app/stress-test.py http://${data.kubernetes_service.web_app_service.status.0.load_balancer.0.ingress.0.ip} 60"
    cluster_info     = "gcloud container clusters describe ${google_container_cluster.primary.name} --region ${var.region}"
  }
}
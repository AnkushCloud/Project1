terraform {
  required_version = ">= 1.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.80"
    }

    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.80"
    }

    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.11"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }

    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }

  # Optional: Backend configuration for state storage
  # backend "gcs" {
  #   bucket = "your-tf-state-bucket"
  #   prefix = "gke-web-app/terraform.state"
  # }
}
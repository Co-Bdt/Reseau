terraform {
  required_version = "1.9.1"
  backend "gcs" {
    bucket = "tf-state-prod-reseau-devperso"
    prefix = "terraform/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.36.0"
    }
  }
}

provider "google" {
  project      = var.project_id
  region       = var.region
  zone         = var.zone
  # access_token = var.auth_token
}

##### Resources #####

# GKE cluster
resource "google_container_cluster" "cluster" {
  name     = "${var.project_name}-auto-cluster"
  location = var.region

  # Enabling Autopilot for this cluster
  enable_autopilot = true

  network    = "default"
  subnetwork = "default"

  deletion_protection = false

  dns_config { # to avoid cluster replacement every time a state is applied
    cluster_dns        = "CLOUD_DNS"
    cluster_dns_domain = "cluster.local"
    cluster_dns_scope  = "CLUSTER_SCOPE"
  }
}

resource "google_compute_global_address" "global-static-ip" {
  name = "${var.project_name}-global-static-ip"
}
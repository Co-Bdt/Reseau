terraform {
  required_version = "1.9.2"

  backend "gcs" {
    bucket = "tf-state-prod-reseau-devperso"
    prefix = "terraform/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.38.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "5.58.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
}

provider "aws" {
  region = var.aws_region
}

##### Resources #####

# GKE cluster
resource "google_container_cluster" "cluster" {
  name     = "${var.project_name}-auto-cluster"
  location = var.gcp_region

  # Enabling Autopilot for this cluster
  enable_autopilot = true

  network    = "default"
  subnetwork = "default"

  deletion_protection = false

  # to avoid cluster replacement every time a state is applied
  dns_config {
    cluster_dns        = "CLOUD_DNS"
    cluster_dns_domain = "cluster.local"
    cluster_dns_scope  = "CLUSTER_SCOPE"
  }
}

# GCP Global static IP for the web application
resource "google_compute_global_address" "global_static_ip" {
  name = "${var.project_name}-global-static-ip"
}

# AWS RDS instance
resource "aws_db_instance" "db_instance" {
  identifier = "${var.project_name}-db-instance"
  # db_name               = "${var.project_name}-db-instance"
  engine = "postgres"
  # engine_version        = "16.3"
  instance_class            = "db.t4g.micro"
  username                  = "postgres"
  password                  = var.aws_rds_password
  allocated_storage         = 20
  max_allocated_storage     = 1000
  # snapshot_identifier       = var.aws_rds_snapshot_identifier
  skip_final_snapshot       = false
  publicly_accessible       = true
  final_snapshot_identifier = "${var.project_name}-db-instance-final-snapshot"
  # restore_to_point_in_time {
  #   source_dbi_resource_id = "${var.project_name}-db-instance2"
  #   use_latest_restorable_time    = true
  # }
  storage_encrypted = true # to avoid replacement every time a state is applied
}

# Amazon Machine Image (AMI)
data "aws_ami" "linux-2023-ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
}

# AWS EC2 instance
resource "aws_instance" "vm" {
  ami           = data.aws_ami.linux-2023-ami.id
  instance_type = "t2.micro"
  tags = {
    Name = "${var.project_name}-compute-instance"
  }
}
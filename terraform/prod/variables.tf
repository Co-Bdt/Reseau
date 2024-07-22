variable "gcp_region" {
  description = "Region in which GCP ressources are located"
}

variable "aws_region" {
  description = "Region in which AWS ressources are located"
}

variable "gcp_zone" {
  description = "One of the gcp_zone used by GKE and the compute engine gcp_zone"
}

variable "project_id" {
  description = "GCP project id"
  sensitive   = true
}

variable "project_name" {
  description = "GCP project name"
}

variable "aws_rds_password" {
  description = "Password for the RDS instance"
  sensitive   = true
}

# variable "aws_rds_snapshot_identifier" {
#   description = "Snapshot identifier to load for the RDS instance creation"
# }
variable "region" {
  description = "region in which GCP ressources are located"
}

variable "zone" {
  description = "one of the zone used by GKE and the compute engine zone"
}

variable "project_id" {
  description = "GCP project id"
  sensitive = true
}

variable "project_name" {
  description = "GCP project name"
}

variable "user" {
  description = "the user on GCP"
  sensitive = true
}

# variable "auth_token" {
#   type        = string
#   description = "auth token allowing Terraform to access GCP"
# }
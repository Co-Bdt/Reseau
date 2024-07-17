output "static ip address" {
  value = google_compute_global_address.global_static_ip.address
}
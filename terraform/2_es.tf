resource "aiven_elasticsearch" "es-svc" {
  project = var.project
  cloud_name = "google-europe-west1"
  plan = "business-8"
  service_name = var.es_svc
  maintenance_window_dow = "monday"
  maintenance_window_time = "10:00:00"

  elasticsearch_user_config {
    elasticsearch_version = "7"
  }
}

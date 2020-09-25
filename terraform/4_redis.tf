resource "aiven_redis" "redis-svc" {
  project = var.project
  service_name = var.redis_svc
  cloud_name = "google-europe-west2"
  plan = "startup-4"
  maintenance_window_dow = "monday"
  maintenance_window_time = "10:00:00"
}



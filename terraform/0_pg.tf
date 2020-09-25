resource "aiven_service" "avn-pg" {
  project      = var.project
  cloud_name   = "aws-eu-west-2" # London
  plan         = "business-8"    # Primary + read replica
  service_name = var.pg_svc
  service_type = "pg"
  pg_user_config {
	pg_version = 12
	pg {
	  log_min_duration_statement = -1
	  jit = "true"
	}
  }
}

# PostgreSQL user
resource "aiven_service_user" "pg_user" {
	project = var.project
	service_name = var.pg_svc
	username = var.pg_user
	depends_on = [aiven_service.avn-pg]
}

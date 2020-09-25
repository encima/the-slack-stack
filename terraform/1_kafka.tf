resource "aiven_kafka" "kafka-svc" {
  project = var.project
  cloud_name = "google-europe-west1"
  plan = "business-4"
  service_name = var.kafka_svc
  maintenance_window_dow = "monday"
  maintenance_window_time = "10:00:00"

  kafka_user_config {
	// Enables Kafka Connectors
	kafka_connect = true
	kafka_version = "2.6"
	kafka {
	  group_max_session_timeout_ms = 70000
	  log_retention_bytes = 1000000000
	}
  }
}

# Kafka topic
resource "aiven_kafka_topic" "kafka-topic" {
  project = var.project
  service_name = var.kafka_svc
  topic_name = var.kafka_topic
  partitions = 3
  replication = 2
	depends_on = [aiven_kafka.kafka-svc]
}

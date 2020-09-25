resource "aiven_kafka_connector" "kafka-es-con" {
  project = var.project
  service_name = var.kafka_svc
  connector_name = var.kafka_es_conn
  depends_on = [aiven_elasticsearch.es-svc, aiven_kafka.kafka-svc]

  config = {
    "topics" = aiven_kafka_topic.kafka-topic.topic_name
    "connector.class" : "io.aiven.connect.elasticsearch.ElasticsearchSinkConnector"
    "type.name" = "es-connector"
    "name" = var.kafka_es_conn
    "connection.url" = aiven_elasticsearch.es-svc.service_uri
  }
}

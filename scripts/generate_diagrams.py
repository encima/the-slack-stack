import contextvars

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL, Cassandra, InfluxDB
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.alibabacloud.analytics import OpenSearch

from diagrams.programming.framework import Flutter


outdir="../presentation/slack_stack.assets/"
files = ["{}{}".format(outdir, f'step_{x}') for x in range(1, 6)]
steps = ["Step 1 - Webapp and Database", "Step 2 - Scaling Messages", "Step 3 - Searching Messages", "Step 4 -Client-side Caching", "Step 5 - Logging and Metrics"]



with Diagram(show=False) as d:
    
        
    # Step 1    
    with d, Diagram(show=True, filename=files[0]):
        with Cluster("Web"):
            web_clients = [Flutter("Client 1"), Flutter("Client 2")]
        with Cluster("Database"):
            with Cluster("Aiven"):
                pg = PostgreSQL("DB")
        web_clients << Edge(color="green") << pg
    
    # Step 2
    with Diagram(show=True, filename=files[1]):
        with Cluster("Web"):
            web_clients = [Flutter("Client 1"), Flutter("Client 2")]
        with Cluster("Database"):
            with Cluster("Aiven"):
                pg = PostgreSQL("DB")
        web_clients << Edge(color="green") << pg
        
        with Cluster("Aiven"):
            kfk = Kafka("Kafka")
        web_clients << Edge(color="red", label="Produce/Consume") >> kfk
        kfk >> Edge(color="red", label="Postgres Sink Connector") >> pg
     
    # Step 3   
    with Diagram(show=True, filename=files[2]):
        with Cluster("Web"):
            web_clients = [Flutter("Client 1"), Flutter("Client 2")]
        with Cluster("Database"):
            with Cluster("Aiven"):
                pg = PostgreSQL("DB")
        web_clients << Edge(color="green")  << pg
        
        with Cluster("Aiven"):
            kfk = Kafka("Kafka")
        web_clients << Edge(color="red", label="Produce/Consume") >> kfk
        kfk >> Edge(color="red", label="Postgres Sink Connector") >> pg
        
        with Cluster("Message Search"):
            es = OpenSearch("OpenSearch")
        kfk >> Edge(color="blue", label="OpenSearch Sink Connector") >> es
        es << Edge(color="blue",label="Search") >> web_clients
      
    # Step 4  
    with Diagram(show=True, filename=files[3]):
        with Cluster("Web"):
            web_clients = [Flutter("Client 1"), Flutter("Client 2")]
        with Cluster("Database"):
            with Cluster("Aiven"):
                pg = PostgreSQL("DB")
        web_clients << Edge(color="green")  << pg
        
        with Cluster("Aiven"):
            kfk = Kafka("Kafka")
        web_clients << Edge(color="red", label="Produce/Consume") >> kfk
        kfk >> Edge(color="red", label="Postgres Sink Connector") >> pg
        
        with Cluster("Message Search"):
            es = OpenSearch("OpenSearch")
        kfk >> Edge(color="blue", label="OpenSearch Sink Connector") >> es
        es << Edge(color="blue",label="Search") >> web_clients
        
        with Cluster("Caching"):
            with Cluster("Aiven"):
                rds = Redis("Redis")
        web_clients << Edge(color="yellow", label="Response") << rds
        
    # Step 5
    with Diagram(show=True, filename=files[4]):
        with Cluster("Metrics"):
            metrics = InfluxDB("InfluxDB / M3")
            graf = Grafana("Dashboards")

        with Cluster("Web"):
            web_clients = [Flutter("Client 1"), Flutter("Client 2")]
        with Cluster("Database"):
            with Cluster("Aiven"):
                with Cluster("Database HA"):
                    pg = PostgreSQL("DB")
                    pg - Edge(color="brown", style="dotted") - PostgreSQL("secondary") << Edge(label="collect") << metrics
                    web_clients << Edge(color="green") << pg
        web_clients << Edge(color="green")  << pg
        
        with Cluster("Aiven"):
            kfk = Kafka("Kafka")
        web_clients << Edge(color="red", label="Produce/Consume") >> kfk
        kfk >> Edge(color="red", label="Postgres Sink Connector") >> pg
        
        with Cluster("Message Search"):
            es = OpenSearch("OpenSearch")
        kfk >> Edge(color="blue", label="OpenSearch Sink Connector") >> es
        es << Edge(color="blue",label="Search") >> web_clients
        
        with Cluster("Caching"):
            with Cluster("Aiven"):
                rds = Redis("Redis")
                rds - Edge(color="brown", style="dashed") - Redis("replica") << Edge(label="collect") << metrics
        web_clients << Edge(color="yellow", label="Response") << rds 
        
        kfk >> Edge(color="purple", style="dotted", label="collect") >> metrics
        pg >> Edge(color="purple",  style="dotted", label="collect") >> metrics
        
        metrics >> Edge(style="dotted", label="visualise") >> graf
        
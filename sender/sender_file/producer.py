import json
import pika

ROUTING_KEY = 'report.save.key'
EXCHANGE = 'report_exchange'
THREADS = 5

class ProducerReportSave:
    def __init__(self) -> None:        
        # hearbeat = 600 indicates that after 600 seconds 
        # the peer TCP connection should be considered unreachable 
        #  by RabbitMQ and client libraries
        #
        #blocked_connection_timeout=300 means after 300 seconds 
        # the peer TCP connection is interrupted and dropped.
        credentials = pika.PlainCredentials("root", "12345")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost',port=49103, heartbeat=600, blocked_connection_timeout=300, credentials=credentials)
            )
        self.channel = self.connection.channel()

    # This method will be called inside view for sending RabbitMQ message
    # method here is same as properties.content_type in listener callback
    def publish(self,method, body):
        print('Inside UserService: Sending to RabbitMQ: ')
        properties = pika.BasicProperties(method)
        self.channel.basic_publish(
            exchange=EXCHANGE, routing_key=ROUTING_KEY, body=json.dumps(body), 
            properties=properties)
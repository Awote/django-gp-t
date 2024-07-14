import json
import pika

ROUTING_KEY = 'report.save.key'
EXCHANGE = 'report_exchange'
THREADS = 5

class ProducerReportSave:
    def __init__(self) -> None:        
        credentials = pika.PlainCredentials("root", "12345")
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost',port=49103, heartbeat=600, blocked_connection_timeout=300, credentials=credentials)
            )
        self.channel = self.connection.channel()


    def publish(self,method, body):
        print('Inside UserService: Sending to RabbitMQ: ')
        properties = pika.BasicProperties(method)
        self.channel.basic_publish(
            exchange=EXCHANGE, routing_key=ROUTING_KEY, body=json.dumps(body), 
            properties=properties)
import json

import pika


credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/',
                                   credentials=credentials)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)

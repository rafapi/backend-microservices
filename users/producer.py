import json

import pika


credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='10.0.0.214', port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)

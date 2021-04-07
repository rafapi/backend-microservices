import json

import pika

from pika.exchange_type import ExchangeType


credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/',
                                   credentials=credentials)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.exchange_declare(exchange='main', exchange_type=ExchangeType.direct)


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='test_exchange', routing_key='main', body=json.dumps(body), properties=properties)

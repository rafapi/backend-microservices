import json

import pika

from pika.exchange_type import ExchangeType


credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/',
                                   credentials=credentials)


def get_ch():
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    return connection, channel


conn, ch = get_ch()


def publish(method, body):
    global conn, ch
    properties = pika.BasicProperties(method)

    if not conn or conn.is_closed:
        conn, ch = get_ch()

    ch.basic_publish(exchange='', routing_key='main',
                     body=json.dumps(body), properties=properties)

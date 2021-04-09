import json

import pika

from pika.exceptions import StreamLostError


credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='products',
                                   credentials=credentials)


def get_ch():
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='main', auto_delete=True)

    return connection, channel


conn, ch = get_ch()


def publish(method, body):
    global conn, ch
    properties = pika.BasicProperties(method)

    try:
        ch.basic_publish(exchange='products', routing_key='main',
                         body=json.dumps(body), properties=properties)

    except StreamLostError:
        conn, ch = get_ch()

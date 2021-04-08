import json

import pika

from pika.exceptions import StreamLostError


credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='products',
                                   credentials=credentials, heartbeat=1800)


def get_ch():
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='admin', durable=True, auto_delete=False)

    return connection, channel


conn, ch = get_ch()


def publish(method, body):
    global conn, ch
    properties = pika.BasicProperties(method)

    try:
        ch.basic_publish(exchange='', routing_key='admin',
                         body=json.dumps(body), properties=properties)

    except StreamLostError:
        conn, ch = get_ch()

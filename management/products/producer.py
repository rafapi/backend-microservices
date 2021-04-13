import json

import pika


credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='products',
                                   credentials=credentials)


def publish(method, body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='main', auto_delete=True)
    properties = pika.BasicProperties(method)

    try:
        channel.basic_publish(exchange='products', routing_key='main',
                              body=json.dumps(body), properties=properties)

    except Exception as e:
        print(e)

    finally:
        connection.close()

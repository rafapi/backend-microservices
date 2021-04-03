import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672,
                                                               virtual_host='/', credentials=credentials))
channel = connection.channel()


def publish():
    channel.basic_publish(exchange='', routing_key='admin', body='hello')

import os
import json

import pika
import django

from pika.exchange_type import ExchangeType

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/',
                                   credentials=credentials)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.exchange_declare(exchange='test_exchange', exchange_type=ExchangeType.direct, passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue='admin', auto_delete=True)
channel.queue_bind(queue='admin', exchange='test_exchange', routing_key='admin')


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print('Product likes increased.')
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='admin', on_message_callback=callback)


print('Started Consuming')

channel.start_consuming()

channel.close()

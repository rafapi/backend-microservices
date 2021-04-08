import os
import json

import pika
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

from products.models import Product

credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='products',
                                   credentials=credentials, heartbeat=1800)
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.basic_qos(prefetch_count=1)

channel.queue_declare(queue='admin', durable=True, auto_delete=False)


def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body)
    print(id)
    product = Product.objects.get(id=id)
    product.likes += 1
    product.save()
    print('Product likes increased.')
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("MANAG: Acknowledged message! Timeout NOT triggered.")


channel.basic_consume(queue='admin', on_message_callback=callback)


print('Started Consuming')

channel.start_consuming()

channel.close()

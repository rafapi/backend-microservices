import json
from main import Product, db_u
import pika

from pika.exchange_type import ExchangeType


credentials = pika.PlainCredentials('guest', 'guest')
params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.exchange_declare(exchange='test_exchange', exchange_type=ExchangeType.direct,
                         passive=False, durable=True, auto_delete=False)
channel.queue_declare(queue='main', auto_delete=True)
channel.queue_bind(queue='main', exchange='test_exchange', routing_key='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db_u.session.add(product)
        db_u.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db_u.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db_u.session.delete(product)
        db_u.session.commit()
        print('Product Deleted')

    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='main', on_message_callback=callback)


print('Started Consuming')

channel.start_consuming()

channel.close()

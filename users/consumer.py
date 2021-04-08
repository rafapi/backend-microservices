import json
import pika

from main import Product, db_u


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
    print("USER: Acknowledged message! Timeout NOT triggered.")


while True:
    try:
        print("Connecting...")
        credentials = pika.PlainCredentials('guest', 'guest')
        params = pika.ConnectionParameters(host='rabbitmq', port=5672, virtual_host='products',
                                           credentials=credentials, heartbeat=1800)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.queue_declare('main', durable=True, auto_delete=False)
        channel.basic_consume('main', on_message_callback=callback)
        try:
            print('Started Consuming')
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
            break
    except pika.exceptions.ConnectionClosedByBroker:
        continue
    # Do not recover on channel errors
    except pika.exceptions.AMQPChannelError as err:
        print("Caught a channel error: {}, stopping...".format(err))
        break
    # Recover on all other connection errors
    except pika.exceptions.AMQPConnectionError:
        print("Connection was closed, retrying...")
        continue

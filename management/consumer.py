import pika

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', port=5672,
                                                               virtual_host='/', credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='admin')


def callback(ch, method, properties, body):
    print('Received in admiin')
    print(body)


channel.basic_consume(queue='admin', on_message_callback=callback)


print('Started Consuming')

channel.start_consuming()

channel.close()

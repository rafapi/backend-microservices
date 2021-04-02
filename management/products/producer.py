import pika


params = pika.ConnectionParameters('amqp://rafa:rafa@localhost:5672/')

connection = pika.BlockingConnection(params)

# channel = connection.channel()


# def publish():
#     channel.basic_publish(exchange='', routing_key='admin', body='hello')

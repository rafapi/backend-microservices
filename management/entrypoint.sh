#!/usr/bin/env sh

echo "Waiting for RabbitMQ..."

while ! nc -z rabbitmq 5672; do
  sleep 0.1
done

echo "RabbitMQ started"

echo "Waiting for MySQL..."

while ! nc -z db 3306; do
  sleep 0.1
done

echo "MySQL started"

exec "$@"

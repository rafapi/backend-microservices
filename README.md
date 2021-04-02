# Microservices

### RabbitMQ
* Pull and run the instance - note that we are mapping the management port (8080) so that the web interface is available right away:

  `docker run -d --rm --net rabbits -p 8080:15672 --hostname rabbit-1 --name rabbit-1 rabbitmq:3`
  
* Check the logs to verify everithing is running correctly: `docker logs rabbit-1`
* Open a console on the container to enable the management_pluggin: `docker exec -it rabbit-1 bash`
  * Check the status of all the pluggins: `rabbitmq-plugins list`
  * Enable the management_pluggin if it's not yet running: `rabbitmq-plugins enable rabbitmq_management`

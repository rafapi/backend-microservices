# Microservices backend

### It provides two microservices accessible via two independent REST APIs.
* Admin operations: port `8000`
* User operations: port `8001`


### RabbitMQ
```bash
# Pull and run the instance - note that we are mapping the management port (8080) so that the web interface is available right away
$ docker run -d --rm --net rabbits -p 8080:15672 --hostname rabbit-1 --name rabbit-1 rabbitmq:3.8-management
```  
```bash
# Check the logs to verify everithing is running correctly
$ docker logs rabbit-1
```
```bash
# In case you need to enable the management_pluggin
# Open a console on the container
$ docker exec -it rabbit-1 bash
  
  # Check the status of all the pluggins
  $ rabbitmq-plugins list

  # Enable the management_pluggin
  $ rabbitmq-plugins enable rabbitmq_management
```

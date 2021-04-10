# Microservices backend

#### It provides two microservices accessible via two independent REST APIs.
* Admin operations: port `8000`
* User operations: port `8001`

#### Tech stack
* `django` for the `admin` API
* `flask` for the `users` API
* `RabbitMQ` for message distribution
* Each of the previous services runs on a `docker` container

### Setup
* Each service is initiated from a dedicated `docker-compose` file

### Notes
#### Run RabbitMQ base image and enable plugins on demand
```bash
# Pull and run the instance - note that we are mapping the management port (8080) so that the web interface is available right away
$ docker run -d --rm --net rabbits -p 8080:15672 -p 5672:5672 --hostname rabbit-1 --name rabbit-1 rabbitmq:3.8
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
#### Django and Flask migrations
```bash
# Django
* Create the django application 
* Crea the db models module
$ python manage.py makemigrations
$ python manage.py migrate
```
```bash
# Flask
* Create a migrations module (see [manager.py](https://github.com/rafapi/backend-microservices/blob/main/users/manager.py)
* Create the db models - make sure flask-sqlalchemy is installed
# Initialise and run migrations
$ python manager.py db_u init
$ python manager.py db_u migrate
$ python manager.py db_u upgrade
```

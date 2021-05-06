# Microservices backend
<p align="left">
     <img src="https://img.shields.io/github/license/rafapi/backend-microservices">
     <img src="https://img.shields.io/github/last-commit/rafapi/backend-microservices">
</p>

#### It provides two microservices accessible via two independent REST APIs.
* Admin operations: port `8000`
* User operations: port `8001`
* Independent arquitecture
* Independent deployment

#### Tech stack
*  User-facing API
   * `FastAPI`
   * `PostgreSQL`
   * `SQLAlchemy 1.4.7` Async
   * `aio-pika` for async communication with RabbitMQ
*  Admin API
    * `Django`
    * `MySQL`
    * `SQLAlchemy 1.3`
    * `pika`
* `RabbitMQ` for message distribution
* `Docker` for instance isolation and separation of concerns

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
# Django (admiin site)
* Create the django application 
* Crea the db models module
$ python manage.py makemigrations
$ python manage.py migrate
```
```bash
# FastAPI/Flask (client site)
* Create a migrations module (see */users/manager.py*)
* Create the db models - make sure flask-sqlalchemy is installed
# Initialise and run migrations
$ python manager.py db_u init
$ python manager.py db_u migrate
$ python manager.py db_u upgrade
```

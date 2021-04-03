FROM python:3.9

RUN apt-get update \
  && apt-get install -y --no-install-recommends netcat \
  && apt-get clean

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

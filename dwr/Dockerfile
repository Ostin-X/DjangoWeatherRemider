FROM python:3.11-slim
#
## Install PostgreSQL development package
#RUN apt-get update && \
#    apt-get install -y build-essential libpq-dev python3-dev && \
#    rm -rf /var/lib/apt/lists/*

RUN mkdir code
WORKDIR code

ADD . /code/
ADD .env.docker /code/.env

ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

RUN #python setup.py build_ext --pg-config "c:\Program Files\PostgreSQL\14\bin\pg_config.exe" build

CMD gunicorn dwr.wsgi:application -b 0.0.0.0:8000
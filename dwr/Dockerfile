FROM python:3.11-slim

# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1
#ENV USE_DOCKER=true

# setting work directory
WORKDIR /code

RUN pip install --upgrade pip

# install psycopg dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN mkdir /code/static && mkdir /code/media

# install dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt


COPY . .



FROM python:3.11-slim


# setting work directory
WORKDIR /code


# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1


# install psycopg dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# install dependencies
ADD requirements.txt .
RUN pip install -r requirements.txt


COPY . .



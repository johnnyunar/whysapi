FROM python:3.11.1-slim-buster

COPY . /usr/src/app
WORKDIR /usr/src/app

RUN apt update && \
    pip install --upgrade pip && \
    apt-get install -y git libpq-dev g++ --no-install-recommends && \
    apt-get clean -y

RUN pip install -r requirements.txt

WORKDIR /usr/src/app

CMD ["./startup.sh"]

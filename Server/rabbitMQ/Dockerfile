FROM python:3.10

WORKDIR /rabbitMQ

COPY requirements.txt /rabbitMQ

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY transmitter.py /rabbitMQ

CMD [ "python", "./transmitter.py" ]



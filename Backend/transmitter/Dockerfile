FROM python:3.10-alpine


WORKDIR /usr/src/app/transmitter

# install pika to access rabbitmq
RUN pip install --upgrade pip && pip install pika && pip install requests

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1

# declare the source directory

# copy the file
COPY transmitter.py .

# start command
CMD [ "python", "transmitter.py" ]


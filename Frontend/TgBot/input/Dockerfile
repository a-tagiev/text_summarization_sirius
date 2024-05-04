FROM python:3.10-alpine

WORKDIR /input

COPY requirements.txt /input

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . /input

CMD [ "python", "tg_bot_input.py" ]
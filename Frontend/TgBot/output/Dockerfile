FROM python:3.10-alpine

WORKDIR /output

COPY requirements.txt /output

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . /output

CMD [ "python", "tg_bot_output.py" ]
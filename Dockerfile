
FROM python:3.9

COPY *.py /app/
COPY requirements.txt /app/

WORKDIR /app/

RUN pip install -r requirements.txt


EXPOSE 80

CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

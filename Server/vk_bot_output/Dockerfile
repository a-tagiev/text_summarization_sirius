FROM python:3.10

WORKDIR /vk_bot_output

COPY requirements.txt /vk_bot_output

RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY token_bot.py /vk_bot_output
COPY vk_bot.py /vk_bot_output

CMD [ "python", "./vk_bot.py" ]

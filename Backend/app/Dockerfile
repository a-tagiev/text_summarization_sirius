FROM python:3.10


WORKDIR /app

COPY requirements.txt /app


#RUN pip install --upgrade pip
##RUN pip3 install torch --index-url https://download.pytorch.org/whl/cu118
#RUN pip install -r requirements.txt

RUN pip3 install --no-cache-dir -U pip setuptools  wheel
RUN pip3 install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip install datasets transformers[sentencepiece]
RUN pip install sentencepiece



COPY . /app


FROM python:3.10.7-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY data2019.csv /usr/src/app/
COPY data2020.csv /usr/src/app/
COPY main.py Dockerfile /usr/src/app/

CMD ["python", "main.py"]

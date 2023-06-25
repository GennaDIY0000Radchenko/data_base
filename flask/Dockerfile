FROM python:3.10.7-slim-buster

WORKDIR /usr/src/flask

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/flask/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/flask

CMD ["python", "app.py"]
CMD ["flask", "run", "--host", "0.0.0.0"]

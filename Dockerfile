FROM python:3.6.8

EXPOSE 5000

WORKDIR /lostandfound

COPY . /lostandfound

RUN pip3 install -r requirements.txt

RUN python3 app.py
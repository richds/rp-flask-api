FROM python:3.9.6-alpine

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

RUN python3 build_database.py

EXPOSE 8000

ENTRYPOINT python3 app.py
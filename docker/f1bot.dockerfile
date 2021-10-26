FROM python:3.9.7-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1

COPY docker/requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /app
COPY / /app

LABEL Project=f1bot
 

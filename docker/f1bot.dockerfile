FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE=1

COPY docker/requirements.txt .

RUN apk add --no-cache gcc musl-dev
RUN pip install --upgrade pip \
	&& pip install --upgrade pip setuptools wheel \
	&& pip install -r requirements.txt

WORKDIR /app
COPY / /app

LABEL Project=f1bot
 

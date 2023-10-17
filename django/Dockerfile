FROM python:3.11.4-slim-buster

WORKDIR /opt/app/django

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY empty

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python3 manage.py collectstatic --no-input


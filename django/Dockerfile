FROM python:3.11.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/opt/app
ENV APP_HOME=/opt/app
ENV SECRET_KEY = empty

RUN mkdir -p $APP_HOME
RUN mkdir -p $APP_HOME/static
RUN mkdir -p $APP_HOME/media
RUN mkdir -p $APP_HOME/bundles

WORKDIR $APP_HOME
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./django .

RUN python3 manage.py collectstatic --no-input

EXPOSE 8000

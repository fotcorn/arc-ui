FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
COPY requirements-prod.txt /app/
RUN pip install -r requirements-prod.txt

COPY ./app /app/app/
COPY ./arcui /app/arcui/
COPY ./manage.py /app/

RUN SECRET_KEY=1234 python manage.py collectstatic --noinput

FROM python:3-alpine

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT gunicorn -w 5 -b 0.0.0.0:8000 header_validation:app

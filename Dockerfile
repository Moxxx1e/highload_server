FROM python:3.8-slim-buster

COPY . .

EXPOSE 80

CMD python3 main.py
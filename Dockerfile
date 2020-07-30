FROM python:3.8.5-alpine3.11

COPY . /app

RUN pip install requests
RUN pip install trello

CMD python /app/app.py



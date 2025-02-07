
FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY run.sh run.sh
COPY server.py server.py

EXPOSE 5000

CMD [ "sh", "./run.sh" ]


FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY client.py client.py

EXPOSE 5000

CMD ["sh", "-c", "while true; do sleep 30; done"]

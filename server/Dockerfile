FROM python:3.10-slim

WORKDIR /app

COPY server.py /app/

RUN pip install websockets redis

CMD ["python", "server.py"]

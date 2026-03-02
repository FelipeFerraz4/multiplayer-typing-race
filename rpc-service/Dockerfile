FROM python:3.11-slim

WORKDIR /app

COPY room.py .

RUN pip install rpyc psycopg2-binary

EXPOSE 18861

CMD ["python", "room.py"]
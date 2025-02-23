FROM python:3.11-slim AS builder

WORKDIR /code

COPY ./requirements.txt .

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN ollama pull nomic-embed-text
RUN ollama pull granite3.1-dense:2b

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]

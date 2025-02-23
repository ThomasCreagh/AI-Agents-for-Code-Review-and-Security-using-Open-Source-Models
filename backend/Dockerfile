# FROM ollama/ollama
#
#
# # RUN ollama serve
#
# RUN ollama serve & sleep 5 && ollama pull nomic-embed-text && ollama pull granite3.1-dense:2b

FROM python:3.11-slim AS builder

WORKDIR /code

RUN apt-get update && apt-get install -y curl bash libc6 && rm -rf /var/lib/apt/lists/*
# RUN curl -fsSL https://ollama.com/install.sh | bash

# ENV PATH="/root/.ollama/bin:$PATH"
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# RUN ollama pull nomic-embed-text && ollama pull granite3.1-dense:2b

COPY . .

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]

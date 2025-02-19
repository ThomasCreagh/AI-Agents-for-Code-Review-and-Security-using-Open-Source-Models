FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /uvx /bin/

ENV PATH="/code/.venv/bin:$PATH"

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

ENV PYTHONPATH=/code

# Ref: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY . .

RUN pip install --upgrade pip
# RUN pip install --upgrade uv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync
# RUN pip install --no-cache-dir -r requirements.txt

RUN python3 app/ai/llm_rag_database/db.py


EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
# CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]
# , "--workers", "4"
# CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
# CMD ["unicorn", "run"]
# CMD ["fastapi", "run", "app/main.py"]

# BUILDER
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app/src ./src/
COPY app/alembic.ini ./alembic.ini
COPY app/migrations ./migrations/
COPY app/seed ./seed

# TEST
FROM builder AS test

ENV PYTHONPATH=/app

RUN pip install pytest pytest-flask

COPY app/tests ./tests

RUN pytest tests -v

# FINAL
FROM python:3.12-slim AS final

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/src ./src/
COPY --from=builder /app/migrations ./migrations/
COPY --from=builder /app/alembic.ini ./alembic.ini
COPY --from=builder /app/seed ./seed

ENV PYTHONPATH=/app
ENV FLASK_APP=src
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]

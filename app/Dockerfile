# BUILDER
FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --prefix=/install -r requirements.txt

COPY src/ ./src/

# TEST
FROM builder AS test

ENV PYTHONPATH=/app/src

RUN pip install pytest
RUN pytest src/tests/

# FINAL
FROM python:3.12-slim AS final

WORKDIR /app

COPY --from=builder /install /usr/local

COPY src/ ./src/

ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["flask", "run"]

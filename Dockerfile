FROM python:3.12-slim as builder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM builder as assets
WORKDIR /build
COPY . .

ENV SECRET_KEY="temporary-build-key-123456789" \
    CORS_ORIGIN_WHITELIST="http://localhost:8000,http://localhost:3000" \
    PG_DB="forum" \
    PG_USER="postgres" \
    PG_PASSWORD="postgres" \
    DB_HOST="localhost" \
    DB_PORT="5432" \
    EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend" \
    EMAIL_HOST="dummy" \
    EMAIL_PORT="587" \
    EMAIL_USE_TLS="1" \
    EMAIL_HOST_USER="dummy" \
    EMAIL_HOST_PASSWORD="dummy"

RUN python manage.py collectstatic --noinput --clear

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash app

WORKDIR /app

RUN mkdir -p /app/staticfiles /app/media && \
    chown -R app:app /app && \
    chmod -R 755 /app

COPY --from=builder /opt/venv /opt/venv

COPY --from=assets --chown=app:app /build/staticfiles /app/staticfiles

COPY --chown=app:app . .

USER app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "forum-sandbox.wsgi:application"]
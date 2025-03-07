# Stage 1: Builder stage
FROM python:3.12-slim as builder

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==$POETRY_VERSION

# Create a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
WORKDIR /build
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-ansi --no-interaction && \
    poetry show && \
    poetry run python -c "import django; print(django.__version__)"

# Stage 2: Assets stage (for collecting static files)
FROM builder as assets

# Set environment variables for Django
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

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code
WORKDIR /build
COPY . .

# Collect static files
RUN mkdir -p /build/staticfiles && \
    poetry run python manage.py collectstatic --noinput --clear

# Stage 3: Final stage
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -s /bin/bash app

# Set up the working directory
WORKDIR /app

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R app:app /app && \
    chmod -R 755 /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy static files from the assets stage
COPY --from=assets --chown=app:app /build/staticfiles /app/staticfiles

# Copy the application code
COPY --chown=app:app . .

# Switch to the non-root user
USER app

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "forum_sandbox.wsgi:application"]
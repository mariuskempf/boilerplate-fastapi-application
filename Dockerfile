# ---------- Stage 1: Build ----------
FROM python:3.12.13-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/app/.venv

COPY --from=ghcr.io/astral-sh/uv:0.10.12 /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files only
COPY pyproject.toml uv.lock ./

# Install only the main dependencies (not dev)
RUN uv sync --frozen --no-dev --no-cache


# ---------- Stage 2: Runtime ----------
FROM python:3.12.13-slim AS runtime

WORKDIR /

# Make the virtualenv binaries accessible in PATH
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Add non-root user
RUN useradd --create-home appuser

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application codefederated-exp-mnist
COPY ./app ./app

# use non-root user
USER appuser

EXPOSE 8000

# Start FastAPI app with uvicorn using the venv
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]

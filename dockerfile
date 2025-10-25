# -------- STAGE 1: Build Stage --------
FROM python:3.11-alpine3.20 AS builder

LABEL maintainer="natanjesuss20@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VENV_PATH=/venv
ENV PATH="${VENV_PATH}/bin:$PATH"

# Install build dependencies
RUN apk add --no-cache \
  gcc \
  musl-dev \
  python3-dev \
  postgresql-dev \
  libffi-dev \
  bash

# Create virtual environment
RUN python -m venv ${VENV_PATH}

# Download uv installer (runs as root here)
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it (runs as root here, which is fine)
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the PATH (for root user in this stage)
ENV PATH="/root/.local/bin/:$PATH"

ADD . /app

WORKDIR /app

RUN uv sync --locked

# Copy full app code (used in collectstatic, etc.)
COPY ./ /app

# -------- STAGE 2: Final Stage --------
FROM python:3.11-alpine3.20

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VENV_PATH=/venv
ENV PATH="${VENV_PATH}/bin:/scripts:$PATH"

# Install only runtime dependencies
RUN apk add --no-cache \
  bash \
  postgresql-libs

# 1. Create necessary directories
RUN mkdir -p /app /data/web/static /data/web/media /venv

# 2. Create a non-root user and group 
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -s /bin/sh -D appuser

# 3. Download the installer script to the /tmp directory
ADD https://astral.sh/uv/install.sh /tmp/uv-installer.sh

# 4. Set ownership for the application directories
RUN chown -R appuser:appgroup /app /data /venv

# 5. Explicitly set ownership of the installer script in /tmp
RUN chown appuser:appgroup /tmp/uv-installer.sh

# 6. Switch to the non-root user
USER appuser



# 7. Run the installer as the new user from /tmp
# 'appuser' now owns the script and has permission to execute/delete it.
RUN sh /tmp/uv-installer.sh && rm /tmp/uv-installer.sh

# 8. Ensure the installed binary is on the PATH for the 'appuser'
ENV PATH="/home/appuser/.local/bin/:$PATH"

# Set working directory
WORKDIR /app

# 9. Copy app code with correct ownership
COPY --chown=appuser:appgroup ./ /app/

RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "manage.py","runserver", "0.0.0.0:8000"]
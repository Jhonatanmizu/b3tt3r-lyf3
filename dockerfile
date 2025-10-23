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

ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the PATH
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

# Create necessary directories
RUN mkdir -p /app /data/web/static /data/web/media  /venv



ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the PATH
ENV PATH="/root/.local/bin/:$PATH"

ADD . /app

# Set working directory
WORKDIR /app
# Copy app and scripts
COPY ./ /app/

RUN uv sync --locked


EXPOSE 8000

CMD ["uv", "run", "manage.py","runserver"]

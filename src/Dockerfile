# Use official Python slim image (Debian-based)
FROM python:3.12-slim

# Set work directory
WORKDIR /usr/src/app

# Set environment variables (optional)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        gcc \
        python3-dev \
    ; \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/app/requirements.txt \
    && rm -rf /root/.cache/pip

# Copy project files
COPY . /usr/src/app/
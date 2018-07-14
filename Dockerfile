FROM ubuntu:16.04
LABEL maintainer="Denis Krivak"

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app/

RUN mkdir -p \
        ./public/.well-known \
        ./public/media && \
    apt update -y && \
    apt install -y \
        curl \
        gcc \
        libjpeg-dev \
        libpq-dev \
        python3-dev \
        python3-pip \
        zlib1g-dev && \
    pip3 install gunicorn && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r ./requirements.txt

COPY project .
COPY configs/gunicorn.py .

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/healthz || exit 1

CMD [ "gunicorn", "--config", "/app/gunicorn.py", "core.wsgi:application" ]

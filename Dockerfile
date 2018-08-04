FROM python:3.7-alpine
LABEL maintainer="Denis Krivak"

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app/

RUN apk add --no-cache gcc postgresql-dev musl-dev && \
    pip3 install gunicorn

COPY requirements.txt .
RUN pip3 install -r ./requirements.txt

COPY project .
COPY configs/gunicorn.py .

CMD [ "gunicorn", "--config", "/app/gunicorn.py", "core.wsgi:application" ]

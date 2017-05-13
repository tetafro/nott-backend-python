FROM ubuntu:16.10
MAINTAINER Denis Ivanov

# Build:
# docker pull ubuntu:16.10
# docker build -t nott .
# Create container:
# docker create \
#     --name nott-app \
#     --net docknet \
#     --ip 172.20.0.10 \
#     --volume /home/tetafro/IT/projects/pet/nott:/srv \
#     --tty \
#     nott

# Quiet apt-get
ARG DEBIAN_FRONTEND=noninteractive

# Make locales
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Server mode
ENV SERVER_MODE=dev

# Install deps
RUN apt-get -y update && \
    apt-get -y install \
    gcc \
    libjpeg-dev \
    libpq-dev \
    python3-dev \
    python3-pip \
    zlib1g-dev
RUN pip3 install --upgrade pip
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Cleaning
RUN rm -f /tmp/requirements.txt
RUN apt-get -y autoremove
RUN apt-get -y clean

# Mount point
RUN mkdir -p /srv/
WORKDIR /srv/project/

ENTRYPOINT ["python3", "/srv/project/manage.py", "runserver", "0.0.0.0:80"]

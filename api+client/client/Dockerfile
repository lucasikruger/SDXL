# Dockerfile
FROM python:3.10.9-slim

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1 TZ=America/Argentina/Buenos_Aires

RUN apt-get update && \
  apt-get install -y fonts-dejavu-core git\
  ffmpeg build-essential && \
  apt-get autoclean

WORKDIR /app
RUN pip install --upgrade pip


# Install dependencies
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt 
# Setting up permissions
RUN echo "umask 002" >> /etc/profile
RUN chmod -R 777 /app

EXPOSE 8501
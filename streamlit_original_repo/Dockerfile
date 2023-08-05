# Dockerfile
FROM python:3.10.9-slim

ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1 NVIDIA_VISIBLE_DEVICES=all TZ=America/Argentina/Buenos_Aires

RUN apt-get update && \
  apt-get install -y fonts-dejavu-core git\
  ffmpeg build-essential && \
  apt-get autoclean

WORKDIR /repository

# INSTALLATION OF STABLEDIFFUSION

# Clone the repository
RUN git clone https://github.com/Stability-AI/stablediffusion.git

WORKDIR /repository/stablediffusion/generative-models

# Install dependencies
RUN pip install -r requirements/pt13.txt # Or pt2.txt for PyTorch 2.0

# Install sgm
RUN pip install .

# Install sdata for training
RUN pip install -e git+https://github.com/Stability-AI/datapipelines.git@main#egg=sdata

# Install hatch and build wheel
RUN pip install hatch
RUN hatch build -t wheel

# Downloading weights
RUN mkdir -p /repository/stablediffusion/checkpoints/
RUN wget -O /repository/stablediffusion/checkpoints/sd_xl_base_1.0.safetensors https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors
RUN wget -O /repository/stablediffusion/checkpoints/sd_xl_refiner_1.0.safetensors https://huggingface.co/stabilityai/stable-diffusion-xl-refiner-1.0/resolve/main/sd_xl_refiner_1.0.safetensors

# Setting up permissions
RUN echo "umask 002" >> /etc/profile
RUN chmod -R 777 /repository

WORKDIR /repository/stablediffusion

EXPOSE 8501
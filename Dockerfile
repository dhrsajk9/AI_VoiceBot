## Use official lightweight base image
FROM python:3.11-slim

## Copy application code there
COPY . /app/

## Set working directory
WORKDIR /app

## Install required dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libportaudio2 \
    portaudio19-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


## Expose the required port
EXPOSE 7860

## Start the code inside the docker container
CMD ["sh", "-c", "python gradio_app.py"]
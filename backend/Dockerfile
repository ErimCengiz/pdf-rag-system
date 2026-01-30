FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tzdata \
    python3 \
    python3-pip \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x /app/backend/entrypoint.sh

ENV HUGGINGFACE_HUB_TOKEN=your_token_is_here

EXPOSE 8000

ENTRYPOINT ["/app/backend/entrypoint.sh"]

# Base Python image
FROM python:3.10-slim

# Quiet + writable caches for HF on Spaces
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/tmp/hf \
    TRANSFORMERS_CACHE=/tmp/hf \
    TOKENIZERS_PARALLELISM=false

# Workdir
WORKDIR /app

# Upgrade pip and install deps first (better layer caching)
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy your LoRA export and app code
COPY medbot_model /app/medbot_model
COPY app.py inference.py ./
COPY templates ./templates

# Port used by Spaces
EXPOSE 8080

# Production server
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "app:app"]

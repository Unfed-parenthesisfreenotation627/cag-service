FROM python:3.12-slim

LABEL maintainer="cag-service contributors"
LABEL description="Cache-Augmented Generation as a Service"

WORKDIR /app

# Install deps first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY cag_service/ ./cag_service/

# Environment defaults (override at runtime)
ENV CAG_PROVIDER=ollama
ENV CAG_MODEL=llama3.3
ENV CAG_CORPUS=sops
ENV OLLAMA_HOST=http://ollama:11434

EXPOSE 8000

CMD ["uvicorn", "cag_service.api:app", "--host", "0.0.0.0", "--port", "8000"]

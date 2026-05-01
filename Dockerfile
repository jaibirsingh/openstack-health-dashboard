FROM python:3.11-slim

WORKDIR /app

# Install dependencies first (Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment defaults
ENV DEMO_MODE=true
ENV FLASK_APP=app.main
ENV FLASK_ENV=production

EXPOSE 5000

# Health check — Kubernetes will use this
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:5000/api/health')" \
    || exit 1

CMD ["python3", "-m", "app.main"]

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies like curl first
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN pip install aiomysql pymysql cryptography uvicorn fastapi requests typing

# Copy shared modules
COPY config.py /app/src/
COPY logger.py /app/src/
COPY db_api /app/src/

# Create necessary directories
RUN mkdir -p logs configs

ENV PYTHONPATH=/app

# Command sẽ được override bởi docker-compose
CMD ["uvicorn", "src.db_api.db_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


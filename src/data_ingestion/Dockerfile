FROM python:3.10-slim

WORKDIR /app

RUN pip install python-dotenv aiohttp APScheduler aiofiles loguru PyYAML yacs filelock pandas

# Copy shared modules
COPY config.py /app/src/
COPY logger.py /app/src/
COPY data_ingestion /app/src/data_ingestion/

# Create necessary directories
RUN mkdir -p logs configs

ENV PYTHONPATH=/app

# Command sẽ được override bởi docker-compose
CMD ["python", "-m", "src.data_ingestion.data_ingestion"]


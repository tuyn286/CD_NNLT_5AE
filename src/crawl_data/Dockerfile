FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install python-dotenv aiohttp APScheduler aiofiles loguru PyYAML yacs filelock fastapi uvicorn
# Copy shared modules
COPY config.py /app/src/
COPY logger.py /app/src/

# Copy service code
COPY crawl_data /app/src/crawl_data/

# Create necessary directories
RUN mkdir -p logs configs data

ENV PYTHONPATH=/app

# Command sẽ được override bởi docker-compose
CMD ["uvicorn", "src.crawl_data.pet_crawl:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
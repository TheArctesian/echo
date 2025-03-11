FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Create necessary directories
RUN mkdir -p /data/obsidian_vault
RUN mkdir -p /storage/vector_db

CMD ["python", "main.py"]
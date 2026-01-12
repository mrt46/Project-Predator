# PROJECT PREDATOR - Dockerfile
# Trading Operating System - Phase 2

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ ./backend/

# Set Python path
ENV PYTHONPATH=/app

# Expose health check port
EXPOSE 8000

# Run the platform
CMD ["python", "-m", "backend.main"]
